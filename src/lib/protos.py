from __future__ import annotations
from typing import Protocol, Callable
from enum import StrEnum

class COLOR(StrEnum):
    RED = "red" 
    ORANGE = "orange" 
    YELLOW = "yellow" 
    GREEN = "green" 
    BLUE = "blue" 
    PURPLE = "purple" 
    PINK = "pink"
    WHITE = "white" 
    BLACK = "black" 

class STYLE(StrEnum):
    CURSOR_ON = COLOR.YELLOW
    CURSOR_OFF = COLOR.GREEN


# Globals
DRAWINGS:list[PDrawable] = []
E_LIST:list[PEvent] = []
GROUP_MAP: dict[str, PEventGroup] ={}
WIDTH = 500
HEIGHT = 500
POINT2DB:dict[str, PPoint2] = {}
BOUNDS = [(0, WIDTH), (0, HEIGHT)]

# Protocols and definitions
class PEvent(Protocol):
    group:str
    def perform(self):
        ...
    
class PEventListener(Protocol):
    def react(self, event:PEvent):
        ...
class PEventGroup(Protocol):
    subscribers:list[PEventListener]
    
    def attach(self, listener:PEventListener):
        ...
    def detach(self, listener:PEventListener):
        ...
    def notify(self, event:PEvent):
        ...
    

class PDrawable(Protocol):
    def draw(self, canvas:PCanvas, **kwargs):
        ...

class PEntity(Protocol):
    def add_dialog(self, flag:str, event:PEvent)-> None:
        ...
    def notify(self, flag:str, state:str) -> None:
        ...
    def set_state(self, flag:str, state:str):
        ...
    def get_state(self, flag:str, state:str):
        ...
    def adjust(self, event:PEvent):
        ...


class PPoint2(Protocol):
    x:int
    y:int
    def draw(self, canvas:PCanvas, **kwargs):
        ...
    def move(self, dx:int, dy:int):
        ...

class PCircle(Protocol):
    origin: PPoint2
    radius: PPoint2

    def on_circle(self, x, y):
        ...
    def in_circle(self, x, y):
        ...
    def draw(self, canvas:PCanvas, **kwargs):
        ...
class PLine(Protocol):
    origin: PPoint2
    dest: PPoint2
    def draw(self, canvas:PCanvas, **kwargs):
        ...

class PRect(Protocol):
    origin:PPoint2
    corner:PPoint2
    def on_rectangle(self,x,y)->bool:
        """Determines if a point is on the rectangle edges included (True/False)"""
    def in_rectangle(self,x,y) -> bool:
        """Determine if point is in the rectangle or not (Return True/False)"""
    def draw(self, canvas:PCanvas, **kwargs):
        """Draw the Rectangle on the Canvas"""

class PJoint(Protocol):
    child_indices:list[int]
    dir:float
    len:int
    origin:PPoint2
    dest:PPoint2

    def snap(self):
        ...
    
    def rotate(self, delta:float):
        """Update the bone line"""
    def calculate_next(self):
        """Calculate Dest Position from attributes"""
    def add_child(self, c_index):
        """Add a child index to this specific node"""
 
           
class PSkeleton(Protocol):
    origin: PPoint2
    base_joint: PJoint
    joints: list[PJoint]
    def add_joint(self, p_index:int, _dir:int, _len:int, color:str, rotatable:bool, bwidth:int):
        ...
    def add_child(self, p_index:int, c_index:int):
        ...

class PCanvas(Protocol):
    def draw_circle(self, x:int, y:int, r:int, **kwargs)->PCircle:
        ...
    def create_line(self,x:int, y:int, dx:int, dy:int, fill:str):
        ...
    def delete(self, tag:str):
        ...
    def after_(self, time:int, _lambda:Callable):
        ...
        
class PComponent(Protocol):
    ...

    
# Exceptions
class FailedEvent(BaseException):
    ...

class EventGroupException(BaseException):
    ...

class OutOfBoundsPointException(BaseException):
    ...
class SpatialAdditionException(BaseException):
    ...
class SpatialAccessException(BaseException):
    ...