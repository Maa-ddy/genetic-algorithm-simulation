import pygame


from simulation import Simulation
from display import Gui




class App():
	def __init__(self):
		self.simulation = Simulation()
		self._init_pygame_attributes(self.simulation)
		self.gui = Gui(self.canvas, self.simulation)
		self.running = True

	def _init_pygame_attributes(self, simulation):
		dimensions = simulation.get_dimensions()
		self.fps = 60
		self.canvas = pygame.display.set_mode(dimensions)
		self.clock = pygame.time.Clock()
	
	def _tick(self):
		self.simulation.update()
		self.clock.tick(self.fps)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
	
	def _render(self):
		self.gui.clear()
		self.gui.render()
	
	def run(self):
		while self.running:
			self._render()
			self._tick()
			
		pygame.quit()
		quit()	


if __name__ == '__main__':
	App().run()
