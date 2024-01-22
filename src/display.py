import pygame
from entities.cell import Cell
import numpy

class Gui():

    black = (0,0,0)
	
    def __init__(self, canvas, simulation):
        self.canvas = canvas
        self.simulation = simulation

    def _build_display_objs(self):
        cells = [DisplayCell(self.canvas, cell) for cell in self.simulation.population.values()]
        food = [DisplayFood(self.canvas).with_pos(food) for food in self.simulation.food]
        poison = [DisplayPoison(self.canvas).with_pos(poison) for poison in self.simulation.poison]
        return cells + food + poison
	
    def clear(self):
        self.canvas.fill(Gui.black)
	
    def render(self):
        self.clear()
        for display_obj in self._build_display_objs():
            display_obj.render()
        pygame.display.update()


class DisplayObj():

    cyan = (66, 244, 176)
    green = (90, 240, 40)
    orange = (240, 110, 40)
    blue = (7, 90, 180)
    red = (220, 10, 40)
    
    def __init__(self, canvas):
        self.canvas = canvas
    
    def with_id(self, display_obj_id):
        self.id = display_obj_id
        
    def with_pos(self, pos):
        self.pos = pos
        return self
    
    def render(self):
        print("can't render abstract display obj")

class DisplayCell(DisplayObj):

    def __init__(self, canvas, cell):
        self.cell = cell
        self.radius = cell.radius
        self.pos = cell.pos     
        self.color = DisplayObj.cyan
        super().__init__(canvas)

    def _get_color(self):
        r, g, b = self.color
        saturation = self.cell.health / Cell.max_health
        return tuple(map(int, (
            r * saturation, 
            g * saturation, 
            b * saturation
        )))

    def render(self):
        pygame.draw.circle(self.canvas, self._get_color(), self.cell.pos, self.radius)
        pygame.draw.circle(self.canvas, DisplayObj.green, self.cell.pos, self.cell.vision_for_food, 2)
        pygame.draw.circle(self.canvas, DisplayObj.orange, self.cell.pos, self.cell.vision_for_poison, 2)
        pygame.draw.line(self.canvas, DisplayObj.blue, self.cell.pos, self.cell.pos + self.cell.speed * self.cell.desire_for_food, 2)
        pygame.draw.line(self.canvas, DisplayObj.red, self.cell.pos, self.cell.pos + self.cell.speed * self.cell.desire_for_poison, 2)

class DisplayFood(DisplayObj):
    def __init__(self, canvas):
        self.radius = 5
        self.color = DisplayObj.green
        super().__init__(canvas)

    def render(self):
        pygame.draw.circle(self.canvas, self.color, self.pos, 5, 2)

class DisplayPoison(DisplayObj):
    def __init__(self, canvas):
        self.color = DisplayObj.orange
        self.radius = 5
        super().__init__(canvas)

    def render(self):
        pygame.draw.circle(self.canvas, self.color, self.pos, 5)