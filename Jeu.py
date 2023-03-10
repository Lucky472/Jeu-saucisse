#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 08:08:32 2023

@author: kchateau
"""
from tkinter import *

RADIUS = 5
XMIN = 20
YMIN = 20
DIST = 10
WIDTH = 2*XMIN + 8*DIST
HEIGHT = 2*YMIN + 6*DIST
WIDTHCANVAS = 800
HEIGHTCANVAS = 800
COLORCANVAS = "#000000"
COLORPOINT = "#FFFFFF"



class GameShow:
    def __init__(self,window):
        self.game_engine = GameEngine()
        #BIND LE CLIC 


        #Initialise l'interface graphique
        self.window = window
        self.plateau = Frame()
        self.menu = Frame()
        self.canvas = Canvas(self.plateau, width = WIDTHCANVAS,height=HEIGHTCANVAS,bg=COLORCANVAS)
        
        self.labelActivePlayer = Label(self.menu,textvariable= self.game_engine.activePlayer)
        #Pack l'interface graphique
        self.plateau.pack(expand=YES,side=LEFT)
        self.menu.pack(expand=YES,side=RIGHT)
        self.canvas.pack(expand=YES)
        self.labelActivePlayer.pack(expand=YES)

        self.draw_board()
        
    def draw_board(self):
        #parcours la liste et quand il y a un point il le dessine 
        for i in range(0,9):
            for j in range(0,7):
                if (i+j) %2 == 0:
                  self.game_engine.board[i][j].id = self.canvas.create_oval(XMIN+i*DIST-RADIUS,YMIN+j*DIST-RADIUS,XMIN+i*DIST+RADIUS,YMIN+j*DIST+RADIUS,fill = COLORPOINT)
                  print(self.game_engine.board[i][j].id)
    def on_click(self,evt):
        #gère si le click est sur un point et appelle les fonctions associées
        self.game_engine.on_click(evt)
        pass
    
    def draw_sausage(self,points):
        #dessine une saucisse étant donné un tuple de 3 points
        pass
    
    def highlight_points(self):
        #met en surbrillance les points accessibles depuis un point sélectionné
        pass
    
    
    


class GameEngine:
    def __init__(self):
        self.board = self.set_new_board()
        self.activePlayer = "UI"

    def on_click(self,evt):
        # Adrien l'a dans sa tête
        pass

    def set_new_board(self):
        #Créer le tableau 2D avec des points en i+j pair et crossing sinon, renvoie ce tabelau
        point = [[0 for j in range(7)] for i in range(9)]

        for i in range(0,9):
            for j in range(0,7):
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
        pass
    


    def check_coord_mouse(self,evt):
        #vérifie si la souris clique sur un point
        pass
    
    
class Point:
    def __init__(self):
        self.occupied = False
        self.degree = 0
        self.id = 0

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
