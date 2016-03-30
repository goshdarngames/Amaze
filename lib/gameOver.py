##############################################################################
# gameOver.py
##############################################################################
# Contains the GameOverScene class.
##############################################################################
# 03/12 GoshDarnGames
##############################################################################

import pygame
from abs.scene import Scene

class GameOverScene(Scene):
   
   def render(self):
      screen = self.gameEngine.screen
      
      #game over
      fontobj = pygame.font.Font(None,100)
      GOText = fontobj.render("YOU ARE THE WIN",1,(255,255,255))
      screen.blit(GOText,(self.__center(GOText),20))
      
      #Smaller font for next text
      fontobj = pygame.font.Font(None,32)
      
      #press any key
      keyTxt = fontobj.render("Press space to try again.",1,(255,255,255))
      screen.blit(keyTxt,(self.__center(keyTxt),250))
      
   def update(self):
      
      if pygame.key.get_pressed()[pygame.K_SPACE]:
         self.gameEngine.newGame()
         
   def __center(self,img):
      return (800-img.get_width())/2