import tkinter as tk
from lib.protos import *
from lib.models import *
from lib.events import *
from typing import Callable


def draw(canvas:PCanvas):
    global DRAWINGS
    canvas.delete("all")
    for drawable in DRAWINGS:
        test = canvas
        drawable.draw(test)



def draw_call(call:Callable, canvas:PCanvas):
    call()
    draw(canvas)


def build_app(setup:Callable, update:Callable):
    root = tk.Tk()
    root.geometry("500x500")
    bind_events(root)
    
    canvas = myCanvas(root, background = "black", cursor="None")
    canvas.pack(expand=True, fill="both")
    draw_call(setup, canvas)
    
    Cursor(canvas)
    
    engine(update, canvas)
    root.mainloop()

def bind_events(root:tk.Tk):
    root.bind('<Motion>', lambda x: occur(MouseMove(x)))
    root.bind('<Button>', lambda x:occur(MouseClick(x)))
    root.bind("<ButtonPress>", lambda x: occur(MousePressed(x)))
    root.bind("<ButtonRelease>", lambda x: occur(MouseReleased(x)))
    
    add_register("Mouse")
    add_register("Draggable")

def engine(_update:Callable,canvas:myCanvas):
    draw_call(_update, canvas)
    canvas.after(10, lambda: engine(_update, canvas))


def hit(e):
    print(e)

def relax(e):
    print(e)