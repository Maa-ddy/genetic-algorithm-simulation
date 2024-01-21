
class DomainEventsQueue():

    singleton_instance = None

    def __init__(self):
        if DomainEventsQueue.singleton_instance is None:
            DomainEventsQueue.singleton_instance = __init_instance(self)
        return DomainEventsQueue.singleton_instance
    
    def __init_instance(self):
        self.queue = []
        self.subscribers = []
        return self

    def subscribe(self, sub):
        self.subscribers.append(sub)
    
    def unsubscribe(self, sub):
        self.subscribers.remove(sub)

    def push(self, event):
        for sub in self.subscribers:
            sub.notify(event)
        self.queue.append(event)
    
    def clear(self):
        self.queue = []
    
    def events_history(self):
        return self.queue[:]


class NewbornCellEvent():
    def __init__(self, cell):
        self.data = cell
    
class CellDeathEvent():
    def __init__(self, cell):
        self.data = cell