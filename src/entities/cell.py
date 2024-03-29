from .domain_events import DomainEventQueue, NewbornCellEvent, CellDeathEvent
from random import random, uniform
from math import sqrt
import numpy

default_noise = [0,0]
default_vision_for_food = 100
default_vision_for_poison = 50
default_desire_for_food = 5
default_desire_for_poison = -2
default_dna = [10, default_noise[:], default_vision_for_food, 30, default_desire_for_food, 0, 1]

def random_dna():
	return [
		int(random() * Cell.max_radius) + 4, 
		[uniform(-2, 2), uniform(-2, 2)], 
		int(random() * default_vision_for_food) + 5, 
		int(random() * default_vision_for_poison) + 5, 
		int(uniform(-default_desire_for_food, default_desire_for_food)) + 1, 
		int(uniform(-default_desire_for_poison, default_desire_for_poison)) - 1,
		1
	]

def sign(a):
	return 1 if a > 0 else -1

class Cell():

	max_health = 200
	max_radius = 40
	reproduction_rate = 0.001
	mutation_radius_range = 0.5
	mutation_vision_range = 2
	mutation_desire_range = 0.05

	INF = 1000
	
	def __init__(self, x, y, dna=default_dna):
		self.pos = numpy.array([x,y])
		self.target = numpy.array([0,0])
		self.escape = numpy.array([0,0])
		self.random_target = [random() * Cell.INF, random() * Cell.INF]
		self.health = Cell.max_health
		self.speed = numpy.array([0,0])
		self.dna = dna[:]
		self.radius, self.move_noise, self.vision_for_food, self.vision_for_poison, self.desire_for_food, self.desire_for_poison, self.age = dna
		
		DomainEventQueue.get_instance().push(NewbornCellEvent(self))
	
	def selection(self):
		if random() < Cell.reproduction_rate:
			self.dna[-1] = self.age
			child_dna = self.crossover()
			child_dna = self.mutation(child_dna)
			child_pos = self.pos - self.move_noise 
			return Cell(*child_pos, child_dna)


	def crossover(self):
		return self.dna[:]

	def mutation(self, propagated_dna):
		start = int(random()*6)
		end = int(random()*6)
		start, end = min(start, end) , max(start, end)
		dna = propagated_dna[:]
		for idx in range(start, end+1):
			if idx == 0:
				dna[0] = min(max(4, dna[0] + int(random() * Cell.mutation_radius_range)), Cell.max_radius)
			elif idx == 1:
				dna[1] = [dna[1][0]+uniform(-0.5,0.5), dna[1][1]*uniform(-0.5,0.5)]
			elif idx == 2:
				dna[2] = min(max(2, dna[2] + int(random() * Cell.mutation_vision_range)), default_vision_for_food * 2)
			elif idx == 3:
				dna[3] = min(max(2, dna[3] + int(random() * Cell.mutation_vision_range)), default_vision_for_poison * 2)
			elif idx == 4:
				dna[4] = min(
					max(
						-default_desire_for_food*2,
						dna[4] + int(uniform(-default_desire_for_food, default_desire_for_food) * Cell.mutation_desire_range)
					), 
					default_desire_for_food * 2
				)
			elif idx == 5:
				dna[5] = min(
					max(
						-default_desire_for_poison * 2,
						dna[5] + int(uniform(-default_desire_for_poison, default_desire_for_poison) * Cell.mutation_desire_range)
					), default_desire_for_poison * 2
				)
		return dna

	def dist(self, point):
		return sqrt(sum(e*e for e in self.pos - point))

	def seek_food(self, meals, poison):
		#target = numpy.array([max(width, height),max(width, height)])
		#escape = numpy.array([max(width, height),max(width, height)])
		target = numpy.array([Cell.INF, Cell.INF])
		escape = numpy.array([Cell.INF, Cell.INF])
		for meal in meals:
			if self.dist(meal) < self.radius + 5:
				meals.pop(meals.index(meal))
				self.health += 20
				self.health = min(self.health, Cell.max_health)
			elif self.dist(meal) < self.dist(target):
				target = meal
		for p in poison:
			if self.dist(p) < self.radius + 5:
				poison.pop(poison.index(p))
				self.health -= 80
				self.health = max(self.health, 0)
			elif self.dist(p) < self.dist(escape):
				escape = p
		if self.dist(target) > self.vision_for_food or self.dist(target) == self.dist(numpy.array([Cell.INF, Cell.INF])):
			self.target = None
		else:
			self.target = target
		if self.dist(escape) > self.vision_for_poison or self.dist(escape) == self.dist(numpy.array([Cell.INF, Cell.INF])):
			self.escape = None
		else:
			self.escape = escape



	def apply_force(self, intensity, pos):
		steering = pos - self.pos
		if abs(steering[0]) < abs(steering[1]) :
			steering = [
				intensity * (sign(steering[0]) * abs(steering[0]/steering[1])), 
				intensity*sign(steering[1])
			]
		else:
			steering = [
				intensity*sign(steering[0]) + self.move_noise[0], 
				intensity * sign(steering[1]) * abs(steering[1]/steering[0]) + self.move_noise[1]
			]
		steering = list(map(int,steering))
		self.speed = numpy.array(steering)

	def chase(self):
		if self.target is None:
			self.apply_force(self.desire_for_food, self.random_target)
			if self.dist(self.random_target) < 5:
				self.random_target = [10 + random()*(Cell.INF - 10), 10 + random() * (Cell.INF - 10)]
		else:
			self.random_target = [random() * Cell.INF, random() * Cell.INF]
			if self.dist(self.target) < self.radius and self.target in food:
				food.pop(food.index(self.target))
			self.apply_force(self.desire_for_food,self.target)
		self.pos += self.speed
		if self.escape is not None:
			self.apply_force(self.desire_for_poison, self.escape)

	def move(self):
		if (self.speed & numpy.array([0,0])).all():
			self.pos += self.move_noise
		self.pos += self.speed
	
	def live(self):
		self.age += 1
		self.health -= 1
		if self.health <= 0:
			self.die()
			
	def update(self, food, poison):
		self.seek_food(food, poison)
		self.chase()
		self.move()
		self.live()
		self.selection()
		if self.age > 10000:
			print("candidate :",self.dna)

	def die(self):
		DomainEventQueue.get_instance().push(CellDeathEvent(self))
