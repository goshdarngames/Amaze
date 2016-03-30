##############################################################################
# gameScene.py
##############################################################################
# Contains the classes used to render and explore the maze.
##############################################################################
# 03/12 GoshDarnGames
##############################################################################

import pygame

from abs.scene import Scene
from abs.gameObject import GameObject

from maze import Maze

##############################################################################
# GLOBAL VARIABLES
##############################################################################

TILE_WIDTH = 20
TILE_HEIGHT = TILE_WIDTH

GRID_WIDTH = 40
GRID_HEIGHT = 30

VISITED_COLOUR = (100,100,100)
WALL_COLOUR = (0,255,200)
MAN_COLOUR = (200,200,0)
GOAL_COLOUR = (0,255,0)

##############################################################################
# CLASSES
##############################################################################

##############################################################################
# Game Scene
##############################################################################

class GameScene(Scene):
   
   def __init__(self,gameEngine):
      Scene.__init__(self,gameEngine)
      
      self.man = Man(self,0,0)
      
      self.maze = Maze(GRID_WIDTH,GRID_HEIGHT)
      
      self.goal = Goal(self,TILE_WIDTH*(GRID_WIDTH-1),
                            TILE_HEIGHT*(GRID_HEIGHT-1))
      
      self.__initVisited()
      self.addVisited((0,0))
      
      
   #-------------------------------------------------------------------------- 
      
   def render(self):
   
      self.__renderVisited()      
   
      self.man.render()
      
      self.goal.render()
      
      self.__renderMaze()
      
   #--------------------------------------------------------------------------
      
   def update(self):
      self.man.update()
      self.__checkWin()
      
   #--------------------------------------------------------------------------
   
   def __checkWin(self):
      man_cell = (self.man.rect.left,self.man.rect.top)
      goal_cell = (self.goal.rect.left,self.goal.rect.top)
      
      if man_cell == goal_cell:
         self.gameEngine.gameOver()
      
   #--------------------------------------------------------------------------
   
   def __renderVisited(self):
      for x in range(0,GRID_WIDTH):
         for y in range(0,GRID_HEIGHT):
            if self.visited[x][y]:
              rect = pygame.Rect(x*TILE_WIDTH,y*TILE_HEIGHT,
                                 TILE_WIDTH,TILE_HEIGHT)
              pygame.draw.rect(self.gameEngine.screen,VISITED_COLOUR,rect)
      
   #--------------------------------------------------------------------------
   
   def __renderMaze(self):
      
      #Draw the north-south walls
      walls_ns = self.maze.walls_ns
      
      for x in range(0,len(walls_ns)):
         for y in range(0,len(walls_ns[x])):
         
            if walls_ns[x][y] is False:
               continue
         
            pygame.draw.line(self.gameEngine.screen,WALL_COLOUR,
                              (x*TILE_WIDTH+TILE_WIDTH,y*TILE_HEIGHT),
                              (x*TILE_WIDTH+TILE_WIDTH,
                              y*TILE_HEIGHT+TILE_HEIGHT),2)
       
      #Draw the west-east walls                       
      walls_we = self.maze.walls_we
      
      for x in range(0,len(walls_we)):
         for y in range(0,len(walls_we[x])):
         
            if walls_we[x][y] is False:
               continue
         
            pygame.draw.line(self.gameEngine.screen,WALL_COLOUR,
                              (x*TILE_WIDTH,y*TILE_HEIGHT+TILE_HEIGHT),
                              (x*TILE_WIDTH+TILE_WIDTH,
                              y*TILE_HEIGHT+TILE_HEIGHT),2)
                              
   #-------------------------------------------------------------------------
    
   def __initVisited(self):
      self.visited = []
      
      for x in range(0,GRID_WIDTH):
         self.visited.append([])
         
         for y in range(0,GRID_HEIGHT):
            self.visited[x].append(False)
            
   #--------------------------------------------------------------------------
   
   def addVisited(self,cell):
      self.visited[cell[0]][cell[1]] = True
   
##############################################################################
# Man
##############################################################################

class Man(GameObject):
   
   def __init__(self,scene,x,y):
      GameObject.__init__(self,scene,x,y,TILE_WIDTH,TILE_HEIGHT,MAN_COLOUR)
      
   def update(self):
      events = self.scene.gameEngine.events
      for event in events:
         if event.type == pygame.KEYUP:
         
            
            current_loc = (self.rect.left/TILE_WIDTH,
                           self.rect.top/TILE_HEIGHT)
                           
            dest = current_loc
         
            #change the destination according to arrow key pressed
            if event.key == pygame.K_DOWN:
               dest = (current_loc[0],current_loc[1]+1)    
            if event.key == pygame.K_UP:
               dest = (current_loc[0],current_loc[1]-1)               
            if event.key == pygame.K_RIGHT:
               dest = (current_loc[0]+1,current_loc[1])               
            if event.key == pygame.K_LEFT:
               dest = (current_loc[0]-1,current_loc[1])
            
            self.__move(current_loc,dest)               
            
   #--------------------------------------------------------------------------
            
   """
   Moves the man from cell1 to cell2.  Movement will not occur if there is
   a wall between the two locations.
   """            
   def __move(self,cell1,cell2):
      
      #cancel movement if destination is outside grid bounds
      if cell2[0] < 0 or cell2[0] > GRID_WIDTH-1  \
         or cell2[1] < 0 or cell2[1] > GRID_HEIGHT -1:
            return
            
      #check if there's a wall between current cell and dest cell
      wall_tuple = self.scene.maze.wallBetween(cell1,cell2)
      wall_array = wall_tuple[0]
      wall_loc = wall_tuple[1]
      
      if wall_array[wall_loc[0]][wall_loc[1]]:
         return
      
      #apply the movement
      self.rect.left = cell2[0]*TILE_WIDTH
      self.rect.top = cell2[1]*TILE_HEIGHT
      
      #record destination as visited
      self.scene.addVisited(cell2)
      
##############################################################################
# GOAL
##############################################################################

class Goal(GameObject):

   def __init__(self,scene,x,y):
      GameObject.__init__(self,scene,x,y,TILE_WIDTH,TILE_HEIGHT,GOAL_COLOUR)

   