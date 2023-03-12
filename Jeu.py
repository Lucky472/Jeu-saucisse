#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 08:08:32 2023

@author: kchateau
"""
from tkinter import *
from math import sqrt

RADIUS = 15
XMIN = 20
YMIN = 20
X_AXIS_LENGTH = 9
Y_AXIS_LENGTH = 7
DIST = 50
WIDTHCANVAS = 2*XMIN + 8*DIST
HEIGHTCANVAS = 2*YMIN + 6*DIST
HEIGHTMENU = WIDTHCANVAS//128
COLORCANVAS = "#EEEEEE"
COLORPOINT = "#416FEC"
SHINY = "#fafa21"
COLORPLAYER1 = "#008000"
COLORPLAYER2 = "#ed1111"

class GameShow:
    def __init__(self,window):


        #Initialise l'interface graphique
        self.window = window
        self.plateau = Frame(self.window,width=WIDTHCANVAS,height=HEIGHTCANVAS)
        self.menu = Frame(self.window,width=WIDTHCANVAS,height=HEIGHTMENU)
        self.canvas = Canvas(self.plateau, width = WIDTHCANVAS,height=HEIGHTCANVAS,bg=COLORCANVAS,highlightthickness=3,highlightbackground=COLORPOINT)
        self.game_engine = GameEngine(self.canvas)
        self.label_active_player = Label(self.menu,textvariable= self.game_engine.active_player)
        self.button_forfeit = Button(self.menu, text='Forfeit')
        self.canvas.bind("<Button-1>",self.on_click)
        
        #Pack l'interface graphique
        self.menu.pack(expand=YES,side=TOP)
        self.plateau.pack(expand=YES,side=BOTTOM)
        self.canvas.pack(expand=YES)
        self.button_forfeit.pack()
        self.label_active_player.pack(expand=YES,side=TOP)

        self.draw_board()
        
    def draw_board(self):
        #parcours la liste et quand il y a un point il le dessine 
        for i in range(0,X_AXIS_LENGTH):
            for j in range(0,Y_AXIS_LENGTH):
                if (i+j) %2 == 0:
                    self.game_engine.board[i][j].id = self.canvas.create_oval(XMIN+i*DIST-RADIUS,YMIN+j*DIST-RADIUS,XMIN+i*DIST+RADIUS,YMIN+j*DIST+RADIUS,fill = COLORPOINT)
    
    def on_click(self,evt):
        #gère si le click est sur un point et appelle les fonctions associées
        self.game_engine.on_click(evt)
        if len(self.game_engine.selected_dots) == 3 :
            self.draw_sausage(self.game_engine.selected_dots)
            self.game_engine.selected_dots = []
            #vérifie si la partie est finie
            self.game_engine.game_over_test()
            #il faut gérer ici le passage à l'autre joueur (ou appeller une founction de game_engine qui s'en charge)
            self.game_engine.change_active_player()
            #il faut aussi gérer la création de la saucisse côté cerveau
        pass
    
    def draw_sausage(self,points):
        #dessine une saucisse étant donné un tuple de 3 points
        pass
    
    def highlight_points(self,dot_x,dot_y):
        #met en surbrillance les points accessibles depuis un point sélectionné
        for dot in self.game_engine.accessible_neighbours(dot_x,dot_y):
            self.color_point(dot,SHINY)
    
    def color_point(self,point,color):
        #change la couleur d'un point par la couleur donnée.
        pass
    
    def change_color_point(self):
        for i in self.game_engine.selected_dots:
            if self.game_engine.active_player == self.game_engine.list_player[0]:
                self.color_point(i,COLORPLAYER1)
            if self.game_engine.active_player == self.game_engine.list_player[1]:
                self.color_point(i,COLORPLAYER2)            
    
    
    


class GameEngine:
    def __init__(self,canvas):
        self.canvas = canvas
        self.board = self.set_new_board()
        self.list_player = ["Joueur 1","Joueur 2"]
        self.active_player = self.list_player[0]
        self.selected_dots = []
        
    def on_click(self,evt):
        """
        si le point cliqué peut être sélectionné : sélectionne le point
        """
        dot = self.check_coord_mouse(evt)
        if dot != None and dot not in self.selected_dots :
            self.selected_dots.append(dot)
        self.update_dots_clickability()

    def update_dots_clickability(self):
        for dot_x in range(0,X_AXIS_LENGTH):
            for dot_y in range(0,Y_AXIS_LENGTH):
                if (dot_x+dot_y)%2 == 0:
                    self.update_dot_clickability(dot_x,dot_y)
    
    def update_dot_clickability(self,dot_x,dot_y):
        """
        teste si le point peut être séléctionné pour une saucisse et modifie l'atribut correctement
        """
        if len(self.selected_dots) == 0:
            self.board[dot_x][dot_y].can_be_clicked = self.dot_next_to_degree_2(dot_x,dot_y)
        else :
            self.board[dot_x][dot_y].can_be_clicked = self.are_connectable(self.selected_dots[-1],(dot_x,dot_y))
        pass

    def are_connectable(self,dot1_coords,dot2_coords):
        """
        renvoie un booléen
        True si les deux points sont adjacents et si (si elle existe) l'intersection entre eux n'est pas occupée
        False sinon
        """
        pass
    
    def dot_next_to_degree_2(self,dot_x,dot_y):
        #regarde les points adjacents et vérifie si au moins l'un d'eux est de degrès 2
        for dot in self.accessible_neighbours(dot_x,dot_y):
            if self.board[dot_x][dot_y].degree > 1 :
                return True
        return False
        
    def accessible_neighbours(self,dot_x,dot_y):
        """
        renvoie un tuple contenant les tuples de coordonnées des points accessibles depuis le point de coordonnées x,y
        (doit prendre en compte si le point est occupé ainsi que les intersections)
        renvoie tuple vide si pas de points accessibles
        """
        return ()
    
    def set_new_board(self):
        #Créer le tableau 2D avec des points en i+j pair et crossing sinon, renvoie ce tabelau
        point = [[0 for j in range(Y_AXIS_LENGTH)] for i in range(X_AXIS_LENGTH)]

        for i in range(0,X_AXIS_LENGTH):
            for j in range(0,Y_AXIS_LENGTH):
                if (i+j)%2 == 0:
                    point[i][j] = Point()
                else:
                    point[i][j] = Crossing()
        return point


    
    def game_over_test(self):
        #teste si des coups sont encore possibles sur le plateau
        pass
    
    def update_degree(self,point):
        #calcule le degré ( points libres atteignables) autour du point
        pass
    
    def update_all_degree(self):
        #update degree pour chaque point 
        for i in range(0,X_AXIS_LENGTH):
            for j in range(0,Y_AXIS_LENGTH):
                if (i+j)%2 == 0:
                    self.update_degree(self.board[i][j])
    


    def check_coord_mouse(self,evt):
        #vérifie si la souris clique sur un point et renvoie les coords du point si oui et None sinon
        x = evt.x
        y = evt.y
        for i in range(0,X_AXIS_LENGTH):
            for j in range(0,Y_AXIS_LENGTH):
                if (i+j)%2 ==0:
                    point_coord = self.canvas.coords(self.board[i][j].id)
                    if self.is_in_point(x,y,point_coord):
                        print(i,j)
                        return (i,j)
        return None


    
    def is_in_point(self,x,y,point_coord):
        center_x = (point_coord[2] + point_coord[0])/2
        center_y = (point_coord[3] + point_coord[1])/2
        dist = sqrt((abs(x-center_x))**2 +(abs(y-center_y))**2)
        if dist <= RADIUS:
            return True
        return False
    
    def change_active_player(self):
        if self.active_player == self.list_player[0]:
            self.active_player = self.list_player[1]
        else :
            self.active_player = self.list_player[0]


    
    
class Point:
    def __init__(self):
        self.occupied = False
        self.degree = 0
        self.id = 0
        self.can_be_clicked = True

        #ADRIEN A L'IDEE, TABLEAU COORDONNES DE POINTS A DOUBLE ENTREE JE SAIS PLUS QUOI 
        pass
    

class Crossing:
    def __init__(self):
        self.occupied = False





root = Tk()
root.title("SaucisseTheGame")
game = GameShow(root)

root.mainloop()





"""Jeu"""        #Etats : en cours, fini
        #self.activePlayer
        #textvariable "pseudo"

"""Plateau"""    #32 Points : 5 LIgnes --> 5 points ligne pair , 4 points ligne impair
        #Autour : Joueur qui doit jouer , Timer pour les deux en haut et en bas

"""Point"""      #Non selectionné, sélectionné, occupé, impossible
        #non selectionné --> sélectionné --> occupé
                    #clique              #3 pts cliqués

"""Joueur"""     #survoler --> brillance = True
        # relacher le clic --> occuper le point si possible
        
"""Saucisse"""   #Forme = Trait
        #2 couleurs , 1 pour chaque joueur
