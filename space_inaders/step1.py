import tkinter as tk
from tkinter import *

import tkinter.messagebox as tkMessageBox
from tkinter import messagebox

class Alien(object):

    def __init__(self):
        self.id = None
        self.alive = True
        self.alien_img= PhotoImage(file='alien.gif')
        self.alien_width = self.alien_img.width()
        self.alien_height = self.alien_img.height()
        
    def install_in(self, canvas, x, y):
       #self.id=canvas.create_rectangle(x,y,x+self.alien_width,y+self.alien_height,fill="white")
       self.id=canvas.create_image(x,y,image=self.alien_img,tags="alien")
       return self 
    def get_width(self):
        return self.alien_width    
    def get_height(self):
        return self.alien_height
    def move_in(self, canvas, dx, dy):
        canvas.move(self.id, dx, dy)#va bouger en fonction de la direction donné par fleet
    def touched_by(self,canvas,projectile):
        print("completer plus tard")
    def animation_alien(self,canvas):
        if (self.alien_img.cget("file") == "alien.gif"): #si c'est la 1ere image
            self.alien_img = PhotoImage(file="alienw.gif") #on modifie la variable de l'image
            canvas.itemconfigure(self.id, image=self.alien_img)
        else:
            self.alien_img=PhotoImage(file="alien.gif")
            canvas.itemconfigure(self.id, image=self.alien_img)

class Fleet(object):
    def __init__(self):
        self.aliens_lines = 5
        self.aliens_columns =10
        self.aliens_inner_gap = 20
        self.alien_x_delta = 5
        self.alien_y_delta = 15
        fleet_size =self.aliens_lines * self.aliens_columns
        self.aliens_fleet = [None] * fleet_size
        self.occurence=0
    def install_in(self, canvas):
        x, y = 50 , 75   #coord du position initial
        pos = 0 #l'indice dans la liste
        for i in range(0,self.aliens_lines):
            for j in range(0,self.aliens_columns):
                alien = Alien()
                self.aliens_fleet[pos] = alien.install_in(canvas,x,y) 
                pos += 1
                x += self.aliens_inner_gap + alien.alien_width
            x = 50
            y += self.aliens_inner_gap + alien.alien_height
    def move_in(self, canvas):
        if len(self.aliens_fleet) != 0:
            x1 = canvas.bbox("alien")[0]
            x2 = canvas.bbox("alien")[2]
            if x2 >= int(canvas.cget("width")):
                self.alien_x_delta = -self.alien_x_delta
                dy = 0
            elif x1 <= 0: 
                self.alien_x_delta = -self.alien_x_delta
                dy = self.alien_y_delta
            else:
                dy = 0
            for i in range(0,len(self.aliens_fleet)):
                self.aliens_fleet[i].move_in(canvas,self.alien_x_delta,dy)
    def animation_fleet(self,canvas):
         self.occurence=self.occurence+1
         if self.occurence%5==0:
             for i in range(len(self.aliens_fleet)):
                 self.aliens_fleet[i].animation_alien(canvas)
class Defender(object):
    def __init__(self):
        self.width = 20
        self.height = 20
        self.move_delta = 20
        self.id = None
        self.max_fired_bullets = 8
        self.fired_bullets = []

    def install_in(self, canvas):
        mid_width=int(canvas.cget("width"))//2
        can_height=int(canvas.cget("height"))-10
        self.id=canvas.create_rectangle(mid_width,can_height,mid_width+self.width,can_height-self.height,fill="white")
    def move_in(self,canvas, dx):
        canvas.move(self.id, dx, 0)

    class Bullet(object):
        def __init__(self, shooter):
            self.radius = 5
            self.color = "red"
            self.speed = 8
            self.id = None
            self.shooter = shooter

        def install_in(self, canvas,dx,dy):
            self.canvas=canvas
            self.id=self.canvas.create_oval(dx-self.radius, dy-self.radius, dx+self.radius, dy+self.radius, fill=self.color )
             

class Example:
    def __init__(self):
        self.root = Tk()
        self.canvas_width = 1200
        self.canvas_height = 800
        self.canvas = Canvas(self.root, width=self.canvas_width, height=self.canvas_height, bg='black')
        self.canvas.pack()
        self.fleet = Fleet()
        self.defender= Defender()
    def install(self):
        self.fleet.install_in(self.canvas)
        self.defender.install_in(self.canvas)
    def start_animation(self):
        self.canvas.after(10, self.animation)

    def animation(self):
        self.fleet.move_in(self.canvas)
        self.fleet.animation_fleet(self.canvas)
        self.canvas.after(200, self.animation)
    def keypress(self,event):
        print("test")
        if event.keysym == 'Left':
            if (self.canvas.coords(self.defender.id)[0]>=self.defender.width):
                self.defender.move_in(self.canvas,-self.defender.move_delta)
        elif event.keysym == 'Right':
            if (self.canvas.coords(self.defender.id)[2]<=self.canvas_width-self.defender.width):
                self.defender.move_in(self.canvas,self.defender.move_delta).
        elif event.keysym == 'space':
            
    def start(self):
        self.install()
        self.start_animation()
        self.root.bind("<Key>", self.keypress)
        self.root.mainloop()

ex = Example()
ex.start()