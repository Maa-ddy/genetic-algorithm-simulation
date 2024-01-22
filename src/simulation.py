from entities.domain_events import DomainEventQueue, CellDeathEvent, NewbornCellEvent
from entities.cell import Cell, random_dna
from random import random, uniform

class Simulation():
	max_food = 100
	poison_generation_rate = 0.1
	max_population = 20

	default_width = 1500
	default_height = 1200
	
	def __init__(self):
		self.width = Simulation.default_width
		self.height = Simulation.default_height
		self.food = []
		self.poison = []
		self.population = {}
		self.event_dispatcher = EventDispatcher(self)
		self.init_food(count=30)
		self.init_population(count=10)
	
	def get_dimensions(self):
		return (self.width, self.height)
	
	def init_food(self, count=30):
		for k in range(count):
			self.generate_food()

	def init_population(self, count=10):
		for k in range(count):
			x, y = list(map(int,[20 + random() * (self.width - 20) , 20 + random() * (self.height - 20)]))
			Cell(x,y)
	
	def generate_food(self):
		if len(self.food) <= Simulation.max_food:
			random_pos = tuple(map(int, (10 + random() * (self.width - 10), 10 + random() * (self.height - 10))))
			if random() < Simulation.poison_generation_rate:
				self.poison.append(random_pos)
			else:
				self.food.append(random_pos)
	
	def revive_population(self):
		if len(self.population) < 4 or random() < 0.001:
			random_pos = tuple(map(int, (10 + random() * (self.height - 10), 10 + random() * (self.width - 10))))
			Cell(*random_pos, random_dna())
			
	def update(self):
		population_copy = self.population.copy().items()
		for cell_id, cell in population_copy:
			cell.update(self.food, self.poison)
			if self.cell_is_out_of_map(cell):
				cell.die()
		self.generate_food()
		self.revive_population()
	
	def cell_is_out_of_map(self, cell):
		x, y = cell.pos
		return x < 0 or x > self.width or y < 0 or y > self.height
            
	def newborn(self, cell):
		if len(self.population) < Simulation.max_population:
			self.population[id(cell)] = cell
	
	def death(self, cell):
		self.population.pop(id(cell))

class EventDispatcher():

	def __init__(self, simulation):
		DomainEventQueue.get_instance().subscribe(self)
		self.simulation = simulation

	def notify(self, event):
		if type(event) is NewbornCellEvent:
			self.simulation.newborn(event.data)
		elif type(event) is CellDeathEvent:
			self.simulation.death(event.data)
			