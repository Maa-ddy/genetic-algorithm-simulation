from .entities.domain_events import DomainEventQueue, CellDeathEvent, NewbornCellEvent
from .entities.cell import Cell

class Simulation():
	max_food = 5000
	poison_generation_rate = 0.1
	max_population = 20
	
	def __init__(self):
		self.food = []
		self.poison = []
		self.population = {}
		self.init_food(count=30)
		self.init_population(count=10)
	
	def init_food(self, count=30):
		for k in range(count):
			self.generate_food()

	def init_population(self, count=10):
		for k in range(count):
			x, y = list(map(int,[20 + random() * (width - 20) , 20 + random() * (height - 20)]))
			Cell(x,y)
	
	def generate_food(self):
		if len(self.food) <= Simulation.max_food:
			random_pos = tuple(map(int, (10 + random() * (width - 10), 10 + random() * (height - 10))))
			if random() < Simulation.poison_generation_rate:
				self.poison.append(random_pos)
			else:
				self.food.append(random_pos)
	
	def revive_population(self):
		if len(self.population) < 4 or random() < 0.001:
			random_pos = tuple(map(int, (10 + random() * (height - 10), 10 + random() * (width - 10))))
			random_dna = [
				int(random() * Cell.max_radius) + 4, 
				[uniform(-2, 2), uniform(-2, 2)], 
				int(random() * default_vision_for_food) + 5, 
				int(random() * default_vision_for_poison) + 5, 
				int(uniform(-default_desire_for_food, default_desire_for_food)) + 1, 
				int(uniform(-default_desire_for_poison, default_desire_for_poison)) - 1,
				1
			]
			self.population.append(Cell(*random_pos, random_dna))
	def update(self):
		for cell_id, cell in self.population.items():
			cell.update()
            
	def newborn(self, cell):
		if len(self.population) < Simulation.max_population:
			self.population[id(cell)] = cell
	
	def death(self, cell):
		self.population.pop(id(cell))

class EventDispatcher():

	def __init__(self, simulation):
		DomainEventQueue().subscribe(self)
		self.simulation = simulation

	def notify(self, event):
		if type(event) is NewbornCellEvent:
			simulation.newborn(event.data)
		elif type(event) is CellDeathEvent:
			simulation.death(event.data)
			