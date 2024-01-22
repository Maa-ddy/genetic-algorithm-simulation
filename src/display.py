import pygame
from .entities.cell import Cell

class Gui():
	
    def __init__(self, simulation):
        self.simulation = simulation

    def _build_display_objs(self):
        cells = [DisplayCell(cell) for cell in self.simulation.population.values()]
        food = [DisplayFood(food) for food in self.simulation.food]
        poison = [DisplayPoison(poison) for poison in self.simulation.poison]
        return cells + food + poison
	
    def clear(self):
        canvas.fill(black)
	
    def render(self):
        self.clear()
        for display_obj in self._build_display_objs():
            display_obj.render()
        pygame.display.update()


class DisplayObj():

    black = (0,0,0)
    cyan = (66, 244, 176)
    green = (90, 240, 40)
    orange = (240, 110, 40)
    blue = (7, 90, 180)
    red = (220, 10, 40)
    
    def __init__(self):
        pass
    
    def with_id(self, display_obj_id):
        self.id = display_obj_id
        
    def with_pos(self, pos):
        self.pos = pos
        return self
    
    def render(self):
        print("can't render abstract display obj")

class DisplayCell(DisplayObj):

    def __init__(self, cell):
        self.cell = cell
        self.radius = cell.radius
        self.pos = cell.pos     
        return self

    def _get_color(self):
        r, g, b = self.cell.color
        saturation = self.cell.health / Cell.max_health
        return tuple(map(int, (
            r * saturation, 
            g * saturation, 
            b * saturation
        )))

    def render(self):
        pygame.draw.circle(canvas, self._get_color(), self.pos, self.radius)
        pygame.draw.circle(canvas, DisplayObj.green, self.pos, self.cell.vision_for_food, 2)
        pygame.draw.circle(canvas, DisplayObj.orange, self.pos, self.cell.vision_for_poison, 2)
        pygame.draw.line(canvas, DisplayObj.blue, self.pos, self.pos + self.cell.speed * self.cell.desire_for_food, 2)
        pygame.draw.line(canvas, DisplayObj.red, self.pos, self.pos + self.cell.speed * self.cell.desire_for_poison, 2)

class DisplayFood(DisplayObj):
    def __init__(self):
        self.radius = 5
        self.color = DisplayObj.green

    def render(self):
        pygame.draw.circle(canvas, self.color, self.pos, 5, 2)

class DisplayPoison(DisplayObj):
    def __init__(self):
        self.color = DisplayObj.orange
        self.radius = 5

    def render(self):
        pygame.draw.circle(canvas, self.color, self.pos, 5)