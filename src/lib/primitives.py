from .protos import *
import math 
import tkinter as tk
import lib.events as E

class Drawing:
    def __init__(self, obj):
        global DRAWINGS
        DRAWINGS += [obj]

class Component:
    ...

class Draggable(E.EventListener):
    def __init__(self, p:PPoint2):
        self.point = p
        self.radius = 10
        self.dragged = False
        super().__init__("Draggable")
    def react(self, event:PEvent):
        if isinstance(event, E.MouseDragStart):
            if abs(math.dist([event.x, event.y], [self.point.x, self.point.y])) < self.radius:
                print("Dragging", self.point)
                self.dragged = True      
        elif isinstance(event, E.MouseDragMove):
            if self.dragged == True:
                self.point.move(event.x, event.y)
        elif isinstance(event, E.MouseDragEnd):
            if self.dragged == True:
                self.dragged = False
    
class Point2:
    def __init__(self, x:int, y:int, draggable:bool = True):
        self.x = x
        self.y = y
        self.point_size = 3
        if draggable:
            self.draggable = Draggable(self)
        self.drawing = Drawing(self)
        
    def move(self, dx:int, dy:int):
        self.x = dx
        self.y = dy
        # self.entity.set_state("Moved", "1")

    def draw(self, canvas:PCanvas, **kwargs):
        canvas.draw_circle(self.x, self.y, self.point_size, fill="White",**kwargs)

class Line:
    def __init__(self, _origin:PPoint2, _dest:PPoint2):
        self.origin =_origin
        self.dest =_dest
        self.drawing = Drawing(self)
    
    def move_origin(self, dx:int, dy:int):
        self.origin.move(dx, dy)
    
    def draw(self, canvas:PCanvas, **kwargs):
        canvas.create_line(self.origin.x, self.origin.y,
                           self.dest.x, self.dest.y, fill="white")

class Circle:
    def __init__(self, _origin:PPoint2, radius:int, fill:str):
        self.origin = _origin
        self.radius = radius
        self.fill = fill
        self.drawing = Drawing(self)
        
    def in_circle(self, x, y) -> bool:
        dist = math.dist([self.origin.x,self.origin.y],[x,y])
        return dist < self.radius
    
    def on_circle(self, x, y) -> bool:
        dist = math.dist([self.origin.x,self.origin.y],[x,y])
        return dist <= self.radius
    def move(self, dx:int, dy:int):
        self.origin.move(dx, dy)
    
    def draw(self, canvas:PCanvas):
        canvas.draw_circle(self.origin.x, self.origin.y, self.radius, fill = self.fill)
    

class Rectangle:
    def __init__(self, origin:PPoint2, corner:PPoint2):
        self.origin =  origin
        self.corner = corner
        self.drawing = Drawing(self)
    
    # def in_rect(self, x, y) -> bool:
    #     dist = math.dist([self.origin.x,self.origin.y],[x,y])
    #     return dist < self.radius
    # def on_rect(self, x, y) -> bool:
    #     dist = math.dist([self.origin.x,self.origin.y],[x,y])
    #     return dist <= self.radius
    
    def draw(self, canvas:tk.Canvas):
        canvas.create_rectangle(self.origin.x, self.origin.y, self.corner.x, self.corner.y, fill="white")
       
def check_bounds(*args):
    global BOUNDS
    if len(args) > len(BOUNDS):
        raise IndexError("Attempted to reach into a nonexistent dimension! Watch Yourself")
    elif len(args) < len(BOUNDS):
        raise Exception("Failed to specify enough dimensions")
    base = True
    for index, (bmin, bmax) in enumerate(BOUNDS):
        base = base and (args[index] >= bmin) and (args[index] <= bmax)
    return base


def index_coord(_x:int, _y:int) -> str:
    return f"{int(_x)}:{int(_y)}"

def coord_index(indx:str) -> tuple[int, int]:
    indices = indx.split(":")
    if len(indices) == 2:
        return (int(indices[0]) , int(indices[1]) )
    raise Exception("Failed to Coord Index Due to incorrect dimension count")

    
def add_point(_x:int, _y:int, draggable:bool=True) -> PPoint2:
    if not check_bounds(_x, _y):
        raise OutOfBoundsPointException("Point Location was out of bounds")
    
    if hit_point(_x, _y):
        raise SpatialAdditionException("Cannot add space to existing Space")
    
    new_point = Point2(_x,_y, draggable)
    set_point(_x, _y, new_point)
    return new_point

def set_point(_x:int, _y:int, _point:PPoint2):
    global POINT2DB
    index = index_coord(_x,_y)
    POINT2DB[index] = _point
   
def get_point(_x:int, _y:int) -> PPoint2:
    global POINT2DB
    if not hit_point(_x, _y):
        raise SpatialAccessException("Unable to Access Random point in space")
    return POINT2DB[index_coord(_x, _y)]

def hit_point(_x:int, _y:int):
    global POINT2DB
    index = index_coord(_x, _y)
    return index in POINT2DB
def hit_radius(_x:int, _y:int, _r):
    global POINT2DB
    
    return any([_r > math.dist(coord_index(indx),(_x,_y)) for indx in POINT2DB])

def delete_point(_x:int, _y:int):
    index = index_coord(_x, _y)
    del POINT2DB[index]

def move_point(_x:int, _y:int, _dx:int, _dy:int):
    original_point = get_point(_x, _y)
    if hit_point(_dx, _dy):
        raise SpatialAdditionException("Attempting to move point onto a point")
    original_point.move(_dx, _dy)
    set_point(_dx, _dy, original_point)
    delete_point(_x, _y)



def create_line(_x, _y, _dx, _dy):
    origin = add_point(_x, _y)
    dest = add_point(_dx,_dy)
    return Line(origin, dest)

def create_circle(_x, _y, _r, draggable:bool=True, fill:str="white"):
    origin = add_point(_x, _y, draggable)
    return Circle(origin, _r, fill)


def create_rectangle(_x,_y, _dx, _dy):
    origin = add_point(_x, _y)
    dest = add_point(_x+_dx,_y+_dy)
    return Rectangle(origin, dest)

