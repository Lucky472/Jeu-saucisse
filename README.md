# Jeu-saucisse

COLORPLAYER1 = ' Green '
COLORPLAYER2 = ' red '
SURBRILLANCE = ' yellow ' 


def change_color_point(self):
     for i in self.game_engine.selected_dots:
   if active_player==list_player[0]:
          colorierSommets(i, COLORPLAYER1)
  if active_player==list_player[1]:
         colorierSommets(i, COLORPLAYER2) 

def highlight_points (self ):
    for dot in self.game_engine.accessible_neighbours(dot_x,dot_y):
colorierSommets(dot, SURBRILLANCE)
