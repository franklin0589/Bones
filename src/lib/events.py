from .protos import *
from abc import ABC, abstractmethod

#  Functional Event Queue
def occur(new_event:PEvent):
    global E_LIST
    global GROUP_MAP
    if not isinstance(new_event, Event):
        raise FailedEvent("Stating a non-event element occurred")
    if new_event.perform() ==  -1:
        raise FailedEvent("Failed to perform event. Exited ungracefully") 
    E_LIST += [new_event]
    GROUP_MAP[new_event.group].notify(new_event)

def subscribe(group_name:str, listener:PEventListener):
    global GROUP_MAP
    GROUP_MAP[group_name].attach(listener)

def add_register(group:str):
    global GROUP_MAP
    GROUP_MAP[group] = EventGroup()

def view_events() -> list[PEvent]:
    global E_LIST
    return list(reversed(E_LIST))

class EventGroup:
    def __init__(self, _subs:list[PEventListener] = []):
        self.subscribers = _subs
        
    def attach(self, listener:PEventListener):
        if not isinstance(listener, EventListener):
            raise EventGroupException("Attempting to attach non-event listener to Group")
        self.subscribers+=[listener]
    
    def detach(self, listener:PEventListener):
        if not listener in self.subscribers:
            raise EventGroupException("Attempting to detach an event that isn't present in group")
        self.subscribers.remove(listener)

    def notify(self, event:PEvent):
        for sub in self.subscribers:
            sub.react(event)                

class Event(ABC):
    def __init__(self, _group:str):
        self.group = _group
    @abstractmethod
    def perform(self):
        ...

class EventListener(ABC):
    def __init__(self, group:str):
        subscribe(group, self)

    @abstractmethod
    def react(self, event:PEvent):
        ...


    
class MouseMove(Event):
    def __init__(self, tk_event):
        self.tk_event = tk_event
        self.group = "Mouse"
    def perform(self):
        occur(MouseDragMove(self.tk_event.x, self.tk_event.y))
        ...


class MousePressed(Event):
    def __init__(self, tk_event):
        self.tk_event = tk_event
        self.group = "Mouse"
        
        
    def perform(self):
        occur(MouseDragStart(self.tk_event.x, self.tk_event.y))


class MouseReleased(Event):
    def __init__(self, tk_event):
        self.tk_event = tk_event
        self.group = "Mouse"
        
        
    def perform(self):
        occur(MouseDragEnd(self.tk_event.x, self.tk_event.y))


class MouseClick(Event):
    def __init__(self, tk_event):
        self.tk_event = tk_event
        self.group = "Mouse"

    def perform(self):
        ...

class MouseDragStart(Event):
    def __init__(self, x, y):
        self.group = "Draggable"
        self.x = x
        self.y = y
    def perform(self):
        ...


class MouseDragMove(Event):
    def __init__(self, x, y):
        self.group = "Draggable"
        self.x = x
        self.y = y
        
    def perform(self):
        ...

class MouseDragEnd(Event):
    def __init__(self, x, y):
        self.group = "Draggable"
        self.x = x
        self.y = y
    def perform(self):
        ...