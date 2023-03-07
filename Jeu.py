#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 08:08:32 2023

@author: kchateau
"""
from tkinter import *
from Point import *

widthCanvas = 800
heightCanvas = 800
colorCanvas = "#000000"



class GameEngine:
    def __init__(self):
        self.temp = "temp"

class GameShow:
    def __init__(self,window):
        #Initialise l'interface graphique
        self.window = window
        self.plateau = Frame()
        self.menu = Frame()
        self.canvas = Canvas(self.plateau, width = widthCanvas,height =heightCanvas,bg=colorCanvas)
        self.activePlayer = "UI"
        self.labelActivePlayer = Label(self.menu,textvariable= self.activePlayer)
        
        
        #Pack l'interface graphique
        self.plateau.pack(expand=YES,side=LEFT)
        self.menu.pack(expand=YES,side=RIGHT)
        self.canvas.pack(expand=YES)
        self.labelActivePlayer.pack(expand=YES)

        self.listPoint =  []
        self.test = "bit"
   
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


root = Tk()
root.title("SaucisseTheGame")
game = Game(root)

root.mainloop()