from lib.protos import *

from lib.models import *

from time import sleep

# skully = Skeleton(200, 200)



        
        

        
def setup():
    skully = Skeleton(200, 200)

    # Chest = 1
    skully.add_joint(0, -90, 100, "red", True, 30)
    # RLeg = 2
    skully.add_joint(0, 135, 130, "orange", True, 15)
    # LLeg = 3
    skully.add_joint(0, 45, 120, "orange", True, 15)
    
    # RShin = 4
    skully.add_joint(2, 90, 100, "yellow", True, 10)
    # LShin = 5
    skully.add_joint(3, 90, 100, "yellow",True, 10)
    
    # Head = 6
    skully.add_joint(1,-90,50, "green",True,15)

    # RShoulder = 7
    skully.add_joint(1, 20, 50, "cyan",True, 10)
    # LShoulder = 8
    skully.add_joint(1, 160, 50, "cyan", True, 10)
    
    # RUArm = 9
    skully.add_joint(7, 45, 50, "blue", True, 7)
    # LUArm = 10 
    skully.add_joint(8, 135, 50, "blue", True, 7)
    # RLArm = 10 
    skully.add_joint(9, 45, 50, "purple", True, 7)
    # LLArm = 10 
    skully.add_joint(10, 135, 50, "purple", True, 7)

    


    # create_circle(20, 200, 10)  
    # # create_rectangle(20,20, 50, 50)
    # l1 = create_line(10, 10, 200, 200)  
    # p1 = add_point(50,50)
    # c1 = create_circle(40, 40, 20)


# timer = 0
def update():
    ...
