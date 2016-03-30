##############################################################################
# gameObject.py
##############################################################################
# Base class for objects that appear on a scene.
##############################################################################
# 09/09 GoshDarnGames
##############################################################################

import pygame

class GameObject:
   
   def __init__(self,scene,x,y,width,height,colour=(255,255,255)):
      self.scene = scene
      self.rect = pygame.Rect(x,y,width,height)
      self.colour = colour
      
   def render(self):
      
      pygame.draw.rect(self.scene.gameEngine.screen,self.colour,self.rect)
      
   def update(self):
      pass