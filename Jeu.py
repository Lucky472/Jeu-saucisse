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
SAUSAGEWIDTH = 10

class GameShow:
    def __init__(self,window):


        #Initialise l'interface graphique
        self.window = window
        self.plateau = Frame(self.window,width=WIDTHCANVAS,height=HEIGHTCANVAS)
        self.menu = Frame(self.window,width=WIDTHCANVAS,height=HEIGHTMENU)
        self.canvas = Canvas(self.plateau, width = WIDTHCANVAS,height=HEIGHTCANVAS,bg=COLORCANVAS,highlightthickness=3,highlightbackground=COLORPOINT)
        self.game_engine = GameEngine(self.canvas)
        self.active_player = StringVar()
        self.active_player.set(self.game_engine.active_player)
        self.label_active_player = Label(self.menu,textvariable = self.active_player)
        self.button_forfeit = Button(self.menu, text='Forfeit', command = self.forfeit_popup)
        self.canvas.bind("<Button-1>",self.on_click)
        
        #Pack l'interface graphique
        self.menu.pack(expand=YES,side=TOP)
        self.plateau.pack(expand=YES,side=BOTTOM)
        self.canvas.pack(expand=YES)
        self.button_forfeit.pack(side=LEFT)
        self.label_active_player.pack(expand=YES,side=RIGHT)

        self.draw_board()
        
    def forfeit_popup(self):
        #J'suis pas sûr que la fonction aille au bout, c'est marqué sur la doc que le messagebox renvoie soit Yes soit No mais la fenêtre de jeu se ferme pas
        #PS: c'est juste un test voir si la fonction marche, faudra faire une commande restart
        self.forfeit_popup = messagebox.askyesno(title='Forfeit', message='Do you really want to forfeit?')
        if self.forfeit_popup == 'Yes':
            self.window.destroy()
        if self.forfeit_popup == 'No':
            pass
        
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
            self.change_color_point()
            self.game_engine.selected_dots = []
            #vérifie si la partie est finie
            if self.game_engine.game_over_test():
                self.show_winner()
            #il faut gérer ici le passage à l'autre joueur (ou appeller une founction de game_engine qui s'en charge)
            self.game_engine.change_active_player()
            #il faut aussi gérer la création de la saucisse côté cerveau
        pass
    
    def draw_sausage(self,dots):
        #dessine une saucisse étant donné un tuple de 3 points
        point1 = self.game_engine.canvas.coords(self.game_engine.board[dots[0][0]][dots[0][1]].id)
        point2 = self.game_engine.canvas.coords(self.game_engine.board[dots[1][0]][dots[1][1]].id)
        point3 = self.game_engine.canvas.coords(self.game_engine.board[dots[2][0]][dots[2][1]].id)

        if self.game_engine.active_player == self.game_engine.list_player[0] : 
            alpha = COLORPLAYER1 
        else : 
            alpha = COLORPLAYER2 

        if len (self.game_engine.selected_dots) ==3: 
            center1 = ((point1[2] + point1[0])/2,(point1[3] + point1[1])/2)
            center2 = ((point2[2] + point2[0])/2,(point2[3] + point2[1])/2)
            center3 = ((point3[2] + point3[0])/2,(point3[3] + point3[1])/2)

            print(alpha)
            self.canvas.create_line(center1[0],center1[1],center2[0],center2[1], fill= alpha, width=SAUSAGEWIDTH )
            self.canvas.create_line(center2[0],center2[1],center3[0],center3[1], fill= alpha, width=SAUSAGEWIDTH )
    
    def highlight_points(self,dot_x,dot_y):
        #met en surbrillance les points accessibles depuis un point sélectionné
        for dot in self.game_engine.accessible_neighbours(dot_x,dot_y):
            point = self.game_engine.board[dot[0]][dot[1]]
            self.color_point(point,SHINY)
    
    def color_point(self,point,color):
        #change la couleur d'un point par la couleur donnée.
        self.canvas.itemconfig(point.id,fill = color)
    
    def change_color_point(self):
        for dot in self.game_engine.selected_dots:
            point = self.game_engine.board[dot[0]][dot[1]]
            if self.game_engine.active_player == self.game_engine.list_player[0]:
                self.color_point(point,COLORPLAYER1)
            if self.game_engine.active_player == self.game_engine.list_player[1]:
                self.color_point(point,COLORPLAYER2)            
    
    def reset_sausage(self):
        for dot in self.game_engine.selected_dots:
            self.color_point(self.game_engine.board[dot[0]][dot[1]],COLORPOINT)
            self.can_be_clicked = True
        self.game_engine.selected_dots = []

    def reset_game(self):
        self.game_engine.reset()
        self.canvas.delete("sausage")
        #lors de la création de la saucisse, ajouter l'attribut tag ="saucisse"
    
    def show_winner(self):
        self.canvas.create_text(WIDTHCANVAS//2,HEIGHTCANVAS//2,text="Victoire du "+str(self.active_player.get()),fill= "black",font=20)


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
            if self.board[dot[0]][dot[1]].can_be_clicked ==True:
                self.selected_dots.append(dot)
        #self.update_dots_clickability()

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
        le premier point peut être occupé
        si le second est occupé, renvoie false
        """
        dot1_x,dot1_y = dot1_coords
        dot2_x,dot2_y = dot2_coords
        dot2 = self.board[dot2_x][dot2_y]
        if abs(dot1_x - dot2_x) > 2 or abs(dot1_y - dot2_y) > 2 :
            return False
        if dot2.occupied :
            return False
        if dot1_coords[0] != dot2_coords[0] and dot1_coords[1] != dot2_coords[1]:
            return True
        if dot1_x == dot2_x :
            return self.board[dot1_x][(dot1_y+dot2_y)//2].occupied
        if dot1_y == dot2_y :
            return self.board[dot1_x][(dot1_y+dot2_y)//2].occupied
        return False

    def dot_next_to_degree_2(self,dot_x,dot_y):
        #regarde les points adjacents et vérifie si au moins l'un d'eux est de degrès 2
        for dot in self.accessible_neighbours(dot_x,dot_y):
            if self.board[dot_x][dot_y].degree > 1 :
                return True
        return False

    def neighbours(self,dot_x,dot_y):
        pass

    def accessible_neighbours(self,dot_x,dot_y):
        """
        renvoie un tuple contenant les tuples de coordonnées des points accessibles depuis le point de coordonnées x,y
        (doit prendre en compte si le point est occupé ainsi que les intersections)
        renvoie tuple vide si pas de points accessibles
        """
        accessible = []
        for other_dot in self.neighbours(dot_x,dot_y):
            if self.are_connectable((dot_x,dot_y),other_dot):
                accessible.append(other_dot)
        return tuple(accessible)

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

    def reset(self):

        self.active_player = self.list_player[0]
        self.selected_dots = []
        for i in range(0,X_AXIS_LENGTH):
            for j in range(0,Y_AXIS_LENGTH):
                self.board[i][j].reset()


class Point:
    def __init__(self):
        self.occupied = False
        self.degree = 0
        self.id = 0
        self.can_be_clicked = True

        #ADRIEN A L'IDEE, TABLEAU COORDONNES DE POINTS A DOUBLE ENTREE JE SAIS PLUS QUOI 
        def reset(self):
            self.occupied = False
            self.degree = 0
            self.can_be_clicked = True
    

class Crossing:
    def __init__(self):
        self.occupied = False
    
    def reset(self):
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
