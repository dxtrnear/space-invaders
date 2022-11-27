import tkinter as tk
from tkinter import *
import json

import tkinter.messagebox as tkMessageBox
from tkinter import messagebox

class Alien(object):

    def __init__(self):
        self.id = None
        self.alive = True
        self.alien_img= PhotoImage(file='alien.gif')#récupere l'image
        self.alien_width = self.alien_img.width()#récupere la largeur de l'image
        self.alien_height = self.alien_img.height()#récupere la hauteur de l'image
        
    def install_in(self, canvas, x, y):
       self.id=canvas.create_image(x,y,image=self.alien_img,tags="alien")#dessine l'image
       return self 
    def get_width(self):
        return self.alien_width    
    def get_height(self):
        return self.alien_height
    def move_in(self, canvas, dx, dy):
        canvas.move(self.id, dx, dy)#va bouger en fonction de la direction donné par fleet
    def touched_by(self,canvas,bullet):#permet d'effacer la bullet et l'alien touché
        canvas.delete(bullet.id)  
        canvas.delete(self.id)    
        self.alive = False
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
        self.width=1200
        self.height=800
        self.occurence=0#cette variable permet de changer l'image d'animation et faire d'autres evenements

    def get_width(self):
        return self.width
    def get_height(self):
        return self.height
    def install_in(self, canvas):
        x, y = 50 , 75   #coord du position initial
        pos = 0 #l'indice dans la liste
        for i in range(0,self.aliens_lines):#permet de dessiner des aliens avec les espaces voulus entre eux
            for j in range(0,self.aliens_columns):
                alien = Alien()
                self.aliens_fleet[pos] = alien.install_in(canvas,x,y) 
                pos += 1
                x += self.aliens_inner_gap + alien.alien_width
            x = 50
            y += self.aliens_inner_gap + alien.alien_height
    def move_in(self, canvas):#permet à la fleet de bouger ainsi :droite gauche bas
        if len(self.aliens_fleet) != 0:
            x1,y1,x2,y2 = canvas.bbox("alien")
            if x2 >= int(canvas.cget("width")):
                self.alien_x_delta = -self.alien_x_delta #on change la direction de mouvement
                dy = 0
            elif x1 <= 0: 
                self.alien_x_delta = -self.alien_x_delta
                dy = self.alien_y_delta
            else:
                dy = 0
            for i in range(0,len(self.aliens_fleet)):
                self.aliens_fleet[i].move_in(canvas,self.alien_x_delta,dy)
    def animation_fleet(self,canvas):
         self.occurence=self.occurence+1#va changer d'image toute les 5 occurences
         if self.occurence%5==0:
             for i in range(len(self.aliens_fleet)):
                 self.aliens_fleet[i].animation_alien(canvas)

    def manage_touched_aliens_by(self,canvas,defender,score):
        condition = False #condition d'arret si on trouve l'overlapping
        for i in range(len(self.aliens_fleet)): 
            x1,y1,x2,y2 = canvas.bbox(self.aliens_fleet[i].id) #Position des aliens
            overlapped = canvas.find_overlapping(x1, y1, x2, y2)
            if len(overlapped) > 1 : #il y a plus d'un seul element
                for j in range(len(defender.fired_bullets)):
                    for z in range(len(overlapped)):
                        if defender.fired_bullets[j].id == overlapped[z]: #on teste toute les bullets pour trouver celle qui overlap(colision)
                            self.explosion(canvas,defender.fired_bullets[j]) #effet de collision
                            self.aliens_fleet[i].touched_by(canvas,defender.fired_bullets[j]) #suppression de l'image cd l'alien et de la bullet avec la fonction
                            del defender.fired_bullets[j]   #delete la bullet de liste pour pouvoir la réutiliser
                            del self.aliens_fleet[i]
                            score.score_calcul()
                            condition = True
                            break; #on a trouvé la bullets qui touche l'alien
                    if  condition: #sortir de la boucle de fired_bullets
                        break;
                if condition: #sortir de la boucle pour la fleet
                    break;
    def explosion(self,canvas,bullet):
        self.explosion_img = PhotoImage(file="explosion.gif")
        x1,y1,x2,y2 = canvas.bbox(bullet.id) 
        x,y = x1+(x2-x1)/2, y1+(y2-y1)/2#cree les coordonnées de l'explosion pour quelle soit aux millieux de l'alien
        explosion = canvas.create_image(x, y, image=self.explosion_img, tags="explosion")
        canvas.after(45,canvas.delete,explosion) 
class Defender(object):
    def __init__(self):
        self.move_delta = 20
        self.defender_img = PhotoImage(file="defender.gif")
        self.width = self.defender_img.width()
        self.height = self.defender_img.height()#on reccuperere l'image + sa hauteur et largeur
        self.id = None
        self.max_fired_bullets = 8
        self.fired_bullets = []

    def install_in(self, canvas):
        mid_width=int(canvas.cget("width"))//2
        can_height=int(canvas.cget("height"))-10 #cree les coordonnées du millieux du canvas
        #self.id=canvas.create_rectangle(mid_width,can_height,mid_width+self.width,can_height-self.height,fill="white") 
        self.id = canvas.create_image(mid_width, can_height-self.height, image=self.defender_img)
    def move_in(self,canvas, dx):
        canvas.move(self.id, dx, 0)#permet de bouger selon la touche pressé
    def fire(self,canvas):
        coords=canvas.coords(self.id)
        dx=coords[0]
        dy=coords[1]
        if len(self.fired_bullets) < self.max_fired_bullets: #cree une bullet avec un max de 8 a chaque fois
            bullet = Bullet("defender")
            bullet = bullet.install_in(canvas,dx,dy)  
            self.fired_bullets.append(bullet)
    def movebullets(self,canvas):#permet a la bullet de bouger quand elle atteint le haut du canvas elle disparait
         for i in range(0,len(self.fired_bullets)):
            y= canvas.bbox(self.fired_bullets[i].id)[1]
            if y<0: 
                canvas.delete(self.fired_bullets[i].id) 
                del self.fired_bullets[i] 
                break
            else:
                self.fired_bullets[i].move_in(canvas) 

    
    
class Bullet(object):
    def __init__(self, shooter):
        self.radius = 5
        self.color = "red"
        self.speed = 8
        self.id = None
        self.shooter = shooter #permet de preciser si c'est un defender ou un alien qui tire

    def install_in(self, canvas,dx,dy):
        self.canvas=canvas
        self.id=self.canvas.create_oval(dx-self.radius, dy-self.radius, dx+self.radius, dy+self.radius, fill=self.color,tags="bullet" )#dessin du cercle
        return self 
    def move_in(self,canvas):
        canvas.move(self.id, 0, -self.speed)#la selectin de bullet et d'alien n'as pas encore été faite

class Score(object):
    def __init__(self):
        self.name=None
        self.game_state=False #permet de savoir la partie gagner
        self.points=0
        self.time=0
        self.optimal_time=10000 #delai ou les points rapportent le plus le temps est en ms

    #accessueurs pour le nb des points et lenom
    def get_points(self):
        return self.points
    def get_name(self):
        return self.name
    def __str__(self):
        return "Player name:"+str(self.name)+"\n"+"score: "+str(self.points)+"Time (ms)\n" +str(self.time)+"Game state : \n"+str(self.game_state)
    def score_calcul(self):
        if self.time<self.optimal_time:
            self.points+=50
        else:
            self.points+=10
    def toFile(self,fich):#permet d'ajouter les scores à un fichier
        f=open(fich,"a")#ajoute sans supprimer
        l=self
        json.dump(l.__dict__,f)
        f.close()



class Game(object):#cette classe permet de gerer les elements du jeu

    def __init__(self, frame):
        self.frame = frame
        self.score= Score()
        self.fleet = Fleet()
        self.defender = Defender()
        self.height =580
        self.width = 1100
        self.canvas = Canvas(self.frame, width=self.width, height=self.height, bg='black')
        self.canvas.pack()
    def install_in(self):#permet de regrouper toutes les fonctions install
        self.defender.install_in(self.canvas)
        self.fleet.install_in(self.canvas)
    
    def compteur(self):#permet de simuler un timer
        self.score.time=self.score.time+1
        self.canvas.after(1, self.compteur)
   
  
    def affiche_score(self):
        self.score_actuel = StringVar()  #score actuel
        score_label = Label(self.canvas, textvariable = self.score_actuel, bg="black", fg="white", font="Helvetica 13")
        self.score_actuel.set("Score : " + str(self.score.get_points())) # affiche le score
        self.canvas.create_window(1000, 25, window = score_label)
    def affiche_name(self):
        message_text = "Welcome : "+str(self.score.name) #text avec le nom
        message_label = Label(self.canvas, text=message_text, bg="black", fg="white", font="Helvetica 13")
        self.canvas.create_window(110,25, window=message_label)
    def start_animation(self):
        self.canvas.after(10, self.compteur)
        self.canvas.after(10, self.animation)
        self.canvas.after(10, self.move_bullets)
    
    def animation(self):
        if len(self.fleet.aliens_fleet)!=0:#verifie si il reste + d'un alien vivant
            if self.canvas.bbox("alien")[3]<=self.height-self.fleet.alien_y_delta*2:#verifie la position de la fleet si il n'est pas en bas
                self.affiche_score()#affiche le score en temps reel
                self.affiche_name()#affiche le nom
                self.fleet.move_in(self.canvas)
                self.fleet.animation_fleet(self.canvas)
                self.fleet.manage_touched_aliens_by(self.canvas,self.defender,self.score)
                self.canvas.after(100, self.animation)
            else:
                self.lost()#permet d'afficher game over
        else:
            self.win()#permet d'afficher que le joueur a gagner
    def move_bullets(self):#avoir deux fonctions permet d'avoir une vitesse de mouvement de bullets superieur a celle d'alien
        self.defender.movebullets(self.canvas)
        self.canvas.after(60, self.move_bullets)
    #def move_aliens_fleet(self) j'ai créé l'animation dans fleet directement
    def keypress(self,event):#peremt de gerer les differents evenements de keypress 
        if event.keysym == 'Left':
            if (self.canvas.coords(self.defender.id)[0]>=2*self.defender.width):#permet de ne pas sortir de l'écran
                self.defender.move_in(self.canvas,-self.defender.move_delta)
        elif event.keysym == 'Right':
            if (self.canvas.coords(self.defender.id)[0]<=self.width-2*self.defender.width):#permet de ne pas sortir de l'écran
                self.defender.move_in(self.canvas,self.defender.move_delta)
        elif event.keysym == 'space':#permet de tirer
            self.defender.fire(self.canvas)
    def lost(self):#affiche un ecran de fin en supprimant tout les autres elements
        x,y = int(self.canvas.cget("width"))//2 , int(self.canvas.cget("height"))//2
        self.canvas.delete("all")#supprime tout
        self.score.toFile("scores.json")#recopie les données aux fichiers
        self.canvas.create_text(x,y,text="GAME OVER", fill="red", font="Helvetica 30 bold")#affiche le texte voulu
    def win(self):#affiche un ecran de fin en supprimant tout les autres elements
        x,y = int(self.canvas.cget("width"))//2 , int(self.canvas.cget("height"))//2
        self.canvas.delete("all")#supprime tout
        self.score.game_state=True #permet de specifier qu'on a gagner
        self.score.toFile("scores.json")#recopie les données aux fichiers
        self.canvas.create_text(x,y,text="You won !", fill="green", font="Helvetica 30 bold")#affiche le texte voulu


class SpaceInvaders(object):
    def __init__(self):
        self.root = Tk()
        self.root.title("Space Invaders")
        self.frame = Frame(self.root)
        self.frame.pack()
        self.game = Game(self.frame)
        self.root.resizable(0, 0)#rend la taille de la fenetre fixe
    def close(self):
        self.root.quit()
    def menu(self):
        self.game.canvas.create_text(self.game.width/2,120,text="Space invader", fill="lime", font="Helvetica 50 bold")#titre du jeu
        self.player_name=Entry(self.game.canvas,bg="gray", bd=1)#zone de text où on saisit les nom du joueur
        self.player_name.place(x=self.game.width/2 - 50, y=220)
        
        self.game.canvas.create_text(self.game.width/2,300,text="Enter your name", fill="lime", font="Helvetica 30 ")
        self.game.canvas.create_text(self.game.width/2,340,text='"Press Enter to start"', fill="lime", font="Helvetica 12 ")
    def start(self,event):
        self.game.score.name=self.player_name.get()#reccuperele nom entrer par l'utilisateur
        self.game.canvas.delete("all") #supprime tout les texte
        self.player_name.destroy() #supprime la zone de text
        self.game.install_in()
        self.game.start_animation()
    def play(self):
        self.menu()
        self.root.bind("<Key>", self.game.keypress) 
        self.root.bind("<Return>",self.start)#permet de detecter la touche entrer pour lancer le jeu
        self.root.mainloop()

SpaceInvaders().play()

