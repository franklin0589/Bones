from lib.protos import *
from lib.primitives import *
import lib.events as E

class myCanvas(tk.Canvas):
    def draw_circle(self, x, y, r, **kwargs):
        return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
    def after_(self, time:int, _lambda:Callable):
        self.after(time, _lambda)

class Cursor(E.EventListener):
    def __init__(self, canvas:myCanvas):
        self.canvas = canvas
        self.circle = create_circle(0,0, 10, draggable=False, fill=STYLE.CURSOR_OFF)
        super().__init__("Mouse")        
        
    def react(self, event):
        if isinstance(event, E.MouseMove):
            self.circle.move(event.tk_event.x, event.tk_event.y)
        elif isinstance(event, E.MousePressed):
            self.circle.fill = STYLE.CURSOR_ON
        elif isinstance(event, E.MouseReleased):
            self.circle.fill = STYLE.CURSOR_OFF
    
    

class Rotatable(E.EventListener):
    def __init__(self, joint:PJoint):
        self.joint = joint
        self.rotating = False
        self.radius = 10
        super().__init__("Draggable")        
        

    def react(self, event:PEvent):
        if isinstance(event, E.MouseDragStart):
            if abs(math.dist([event.x, event.y], [self.joint.dest.x, self.joint.dest.y])) < self.radius:
                self.rotating = True      
        elif isinstance(event, E.MouseDragMove):
            if self.rotating == True:
                dx = event.x - self.joint.origin.x
                dy = event.y - self.joint.origin.y
                theta = math.atan2(dy,dx)/(2*math.pi)*360
                self.joint.rotate(theta)
    
        elif isinstance(event, E.MouseDragEnd):
            if self.rotating== True:
                self.rotating = False

def lerp(a,b,t):
    if t > 1:
        return b
    elif t < 0:
        return a
    return b * t + a * (1-t)

def angle_to(origin:PPoint2, dest:PPoint2):
    dx = dest.x - origin.x
    dy = dest.y - origin.y
    return math.atan2(dy,dx)/(2*math.pi)*360

class Bone:
    def __init__(self, origin:PPoint2, dest:PPoint2, width:int, color:str):
        self.origin = origin
        self.dest = dest 
        self.num_circles = 8
        self.width = width
        self.color = color
        Drawing(self)
    
    def draw(self, canvas:tk.Canvas):

        theta = angle_to(self.dest, self.origin)
        inv_theta = 90 - theta        
        
        point_list = [(self.origin.x, self.origin.y),]
        for i in range(self.num_circles + 1):
            x = lerp(self.origin.x, self.dest.x, i/self.num_circles)
            y = lerp(self.origin.y, self.dest.y, i/self.num_circles)     
            f_x = x + self.width * math.cos(inv_theta/360 * 2*math.pi)
            f_y = y -  self.width * math.sin(inv_theta/360 * 2 * math.pi)   
            point_list += [(f_x, f_y)]
        
        point_list += [(self.dest.x,self.dest.y)]
        for i in range(self.num_circles, -1, -1):
            x = lerp(self.origin.x, self.dest.x, i/self.num_circles)
            y = lerp(self.origin.y, self.dest.y, i/self.num_circles)     
            f_x = x - self.width * math.cos(inv_theta/360 * 2*math.pi)
            f_y = y +  self.width * math.sin(inv_theta/360 * 2 * math.pi)   
            point_list += [(f_x, f_y)]
        
        canvas.create_polygon(*point_list, fill=self.color)
           
class Joint:
    def __init__(self, origin:PPoint2, skeleton:PSkeleton, _direction:float, _length:int, rotatable:bool = False, width:int = 10, color:str = "white"):
        self.skeleton = skeleton
        self.child_indices:list[int] = []
        self.dir = _direction
        self.len = _length
        self.origin = origin
        nx, ny = self.calculate_next() 
        self.dest = add_point(nx, ny, draggable=False)
        self.bone = Bone(origin, self.dest, width, color)
        if rotatable:
            Rotatable(self)
        Drawing(self)
    
    def snap(self):
        dx, dy = self.calculate_next()
        move_point(self.dest.x, self.dest.y, dx, dy)
        for c_index in self.child_indices:
            self.skeleton.joints[c_index].snap()

    def rotate(self, delta:float):
        self.dir = delta
        self.snap()

            
    def calculate_next(self):
        next_x = self.origin.x + self.len*math.cos(self.dir/360 * (2*math.pi))    
        next_y = self.origin.y+ self.len*math.sin(self.dir/360 * (2*math.pi))    
        return next_x, next_y
    
    def add_child(self, c_index):
        self.child_indices +=[c_index]

    def draw(self, canvas:PCanvas):
            canvas.draw_circle(self.origin.x, self.origin.y, 10, fill='blue')

class Skeleton:
    def __init__(self, x , y):
        self.origin = add_point(x, y, draggable=False)
        self.base_joint = Joint(self.origin, self, 60, 5, width=1)
        self.joints = [self.base_joint]
    
    def add_joint(self, p_index:int, _dir:int, _len:int, color:str, rotatable:bool, bwidth:int):
        p_origin = self.joints[p_index].dest 
        self.add_child(p_index, len(self.joints))
        self.joints += [Joint(p_origin, self, _dir, _len, color=color, rotatable=rotatable, width=bwidth)]

    def add_child(self, p_index:int, c_index:int):
        self.joints[p_index].add_child(c_index)

