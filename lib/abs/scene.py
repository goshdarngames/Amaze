##############################################################################
# scene.py
##############################################################################
# Interface for scenes.  A game is composed of different scenes.  E.g. one
# for the main menu, one for gameplay and one for the game over screen.
##############################################################################
# 09/09 GoshDarnGames
##############################################################################

class Scene:

   def __init__(self,gameEngine):
      self.gameEngine = gameEngine

   def update(self):
      pass
   def render(self):
      pass
