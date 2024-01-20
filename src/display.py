


class Gui():
	queue = {}
	
	def __init__(self):
		pass

	def push(self, display_obj):
		self.queue.add(display_obj.id, display_obj)
	
	def clear(self):
		canvas.fill(black)
	
	def render(self):
		self.clear()
		for display_obj in self.queue:
			display_obj.render()
		self.queue = []
		pygame.display.update()


class DisplayObj():
    def __init__(self):
        pass
    
    def with_cell(self, cell):
        self.color = cell.color
        self.radius = cell.radius
        self.pos = cell.pos     
        return self
        
    def with_pos(self, pos):
        self.pos = pos
        return self
    
    def with_color(self, color):
        self.color = color
        return self
    
    def with_radius(self, radius):
        self.radius = radius
        return self

    def render(self):
        pygame.draw.circle(canvas, self.color, self.pos, self.radius, 0)