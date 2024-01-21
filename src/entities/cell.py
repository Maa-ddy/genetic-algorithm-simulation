from .domain_events import DomainEventsQueue, NewbornCellEvent, CellDeathEvent

class Cell():

	max_health = 200
	
	def __init__(self, x, y, dna=default_dna):
		self.pos = numpy.array([x,y])
		self.color = cell_color
		self.target = numpy.array([0,0])
		self.escape = numpy.array([0,0])
		self.random_target = [random()*width, random()*height]
		self.health = max_health
		self.speed = [0,0]
		#dna here:
		self.dna = dna[:]
		self.radius, self.move_noise, self.vision_for_food, self.vision_for_poison, self.desire_for_food, self.desire_for_poison, self.age = dna
		
		DomainEventsQueue().push(NewbornCellEvent(self))
	
	def selection(self):
		if random() < reproduction_rate:
			self.dna[-1] = self.age
			dna = self.crossover()
			dna = self.mutation(dna)
			return Cell(*self.pos, dna)


	def crossover(self):
		return self.dna[:]

	def mutation(self, propagated_dna):
		start = int(random()*6)
		end = int(random()*6)
		start, end = min(start, end) , max(start, end)
		dna = propagated_dna[:]
		for idx in range(start, end+1):
			if idx == 0:
				dna[0] = min(max(4, dna[0] + int(random()*mutation_radius_range)), max_cell_radius)
			elif idx == 1:
				dna[1] = [dna[1][0]+uniform(-0.5,0.5), dna[1][1]*uniform(-0.5,0.5)]
			elif idx == 2:
				dna[2] = min(max(2, dna[2] + int(random()*mutation_vision_range)), default_vision_for_food*2 )
			elif idx == 3:
				dna[3] = min(max(2, dna[3] + int(random()*mutation_vision_range)), default_vision_for_poison*2)
			elif idx == 4:
				dna[4] = min( max(-default_desire_for_food*2 ,dna[4] + int(uniform(-default_desire_for_food, default_desire_for_food)*mutation_desire_range)), default_desire_for_food*2)
			elif idx == 5:
				dna[5] = min( max(-default_desire_for_poison*2 ,dna[5] + int(uniform(-default_desire_for_poison, default_desire_for_poison)*mutation_desire_range)), default_desire_for_poison*2)
		return dna

	def dist(self, point):
		return sqrt(sum(e*e for e in self.pos - point))

	def seek_food(self, meals):
		target = numpy.array([max(width, height),max(width, height)])
		escape = numpy.array([max(width, height),max(width, height)])
		for meal in meals:
			if self.dist(meal) < self.radius + 5:
				meals.pop(meals.index(meal))
				self.health += 20
				self.health = min(self.health, max_health)
			elif self.dist(meal) < self.dist(target):
				target = meal
		for p in poison:
			if self.dist(p) < self.radius + 5:
				poison.pop(poison.index(p))
				self.health -= 80
				self.health = max(self.health, 0)
			elif self.dist(p) < self.dist(escape):
				escape = p
		if self.dist(target) > self.vision_for_food or self.dist(target) == self.dist(numpy.array([max(width, height),max(width, height)])):
			self.target = None
		else:
			self.target = target
		if self.dist(escape) > self.vision_for_poison or self.dist(escape) == self.dist(numpy.array([max(width, height),max(width, height)])):
			self.escape = None
		else:
			self.escape = escape



	def apply_force(self, intensity, pos):
		steering = pos - self.pos
		if abs(steering[0]) < abs(steering[1]) :
			steering = [intensity*(sign(steering[0])*abs(steering[0]/steering[1])), intensity*sign(steering[1])]
		else:
			steering = [intensity*sign(steering[0]) + self.move_noise[0], intensity*sign(steering[1])*abs(steering[1]/steering[0]) + self.move_noise[1]]
		steering = list(map(int,steering))
		#print(steering)
		self.speed = numpy.array(steering)

	def chase(self):
		if self.target is None:
			self.apply_force(self.desire_for_food, self.random_target)
			if self.dist(self.random_target) < 5:
				self.random_target = [10 + random()*(width-10), 10+random()*(height-10)]
		else:
			self.random_target = [random()*width, random()*height]
			if self.dist(self.target) < self.radius and self.target in food:
				food.pop(food.index(self.target))
			self.apply_force(self.desire_for_food,self.target)
		self.pos += self.speed
		if self.escape is not None:
			self.apply_force(self.desire_for_poison, self.escape)

	def lerp(self):
		ratio = self.health/max_health
		self.color = tuple(map(int,(cell_color[0]*ratio, cell_color[1]*ratio, cell_color[2]*ratio)))

	def move(self):
		self.pos += self.speed
		self.lerp()
		self.health -= 1

	def update(self):
		self.seek_food(food)
		self.chase()
		self.move()
		self.examine()
		self.selection()
		self.age += 1
		if self.age > 10000:
			print("candidate :",self.dna)

	def die(self):
		DomainEventsQueue().push(CellDeathEvent(self))

	def examine(self):
		x,y = self.pos[0], self.pos[1]
		if x < 0 or x > width or y < 0 or y > height or self.health <= 0:
			self.die()