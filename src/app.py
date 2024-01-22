import pygame
from random import random, uniform
from math import sqrt
import numpy

from .simulation import Simulation
from .display import Gui




class App():
	def __init__(self):
		self._init_pygame_attributes()
		self.running = True
		self.simulation = Simulation()
		self.gui = Gui(self.simulation)

	def _init_pygame_attributes(self):
		self.width = 1000
		self.height = 800
		self.dimensions = (width, height)
		self.fps = 30
		self.canvas = pygame.display.set_mode(dimensions)
		self.clock = pygame.time.Clock()
	
	def _tick(self):
		self.simulation.update()
		clock.tick(fps)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
	
	def _render(self):
		self.gui.clear()
		self.gui.render()
	
	def run(self):
		while running:
			self._render()
			self._tick()
			
		pygame.quit()
		quit()	


if __name__ == '__main__':
	App().run()
