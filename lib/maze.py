##############################################################################
# maze.py
##############################################################################
# Classes used to represent the maze.
##############################################################################
# 03/12 GoshDarnGames
##############################################################################

import random

class Maze:
   
   def __init__(self,width,height):
      
      self.width = width
      self.height = height
      
      self.__createArrays()
      self.__generateMaze()
   
   #--------------------------------------------------------------------------
    
   """
   Creates and initializes the walls of the maze.
   """  
   def __createArrays(self):
      
      self.walls_ns = []
      
      for x in range(0,self.width):
         self.walls_ns.append([])
         for y in range(0,self.height):
            self.walls_ns[x].append(True)
            
      self.walls_we = []
      
      for x in range(0,self.width):
         self.walls_we.append([])
         for y in range(0,self.height):
            self.walls_we[x].append(True)
            
   #--------------------------------------------------------------------------
   
   """
   Generates the maze using a depth-first search.
   """
   def __generateMaze(self):
      
      cell_stack = []
      
      #create and initialize the array of visited cells
      visited_cells = []
      
      for x in range(0,self.width):
         visited_cells.append([])
         for y in range(0,self.height):
            visited_cells[x].append(False)
            
      #select a random cell as the starting point
      current_cell = (random.choice(range(0,self.width)),
                      random.choice(range(0,self.height)))
               
      #add cell to visited list
      visited_cells[current_cell[0]][current_cell[1]]=True
                      
      #tally of cells visited
      num_visited = 1
      
      #total number of cells to visit
      total_cells = self.width*self.height
      
      while num_visited<total_cells:
         neighbours = self.__findNeighbours(current_cell)
         
         #filter neighbours that have already been visited
         not_visited = lambda cell: visited_cells[cell[0]][cell[1]] is False
         neighbours = filter(not_visited,neighbours)         
               
         if len(neighbours) is not 0:
             
            #pick a random neighbour
            new_cell = random.choice(neighbours)
             
            #get the wall between new_cell and current_cell
            wall_between = self.wallBetween(current_cell,new_cell)
            array = wall_between[0]
            wall = wall_between[1]
            
            #remove the wall
            array[wall[0]][wall[1]] = False
                
            #add old cell to the cell stack
            cell_stack.append(current_cell)
            
            #make the new cell the current cell 
            current_cell = new_cell
             
            #record new cell as visited 
            num_visited += 1
            visited_cells[new_cell[0]][new_cell[1]] = True
               
               
         #all neighbours have been visited, so backtrack to find new cells
         #that haven't been visited yet      
         else:
            if len(cell_stack) is 0:
               break
               
            current_cell = cell_stack[len(cell_stack)-1]
            cell_stack.remove(current_cell)
         
   #--------------------------------------------------------------------------
   
   """
   Returns a list of all a cell's neighbours.
   """
   def __findNeighbours(self,cell):
      
      neighbours = []
      
      x=cell[0]
      y=cell[1]
      
      if x > 0:
         neighbours.append((x-1,y))
      if x < self.width-1:
         neighbours.append((x+1,y))
      
      if y > 0:
         neighbours.append((x,y-1))
      if y < self.height-1:
         neighbours.append((x,y+1))
         
      return neighbours
      
   #--------------------------------------------------------------------------
   
   """
   Returns the location of the wall between two adjacent cells.  Returns a
   tuple in the form (array,(x,y))
   
   Note: undefined result if cells are not adjacent!
   """
   def wallBetween(self,cell1, cell2):
      
      #will point to either walls_ns or walls_we
      array = None
      
      #will store the x,y of the wall
      wall = None
      
      #short-hand for the x and y coordinates
      x1 = cell1[0]
      y1 = cell1[1]
      x2 = cell2[0]
      y2 = cell2[1]
      
      #if cells are adjacent vertically
      if x1 == x2:
         
         #the wall is horizontal
         array = self.walls_we
      
         #if cell1 is above cell2
         if y1 < y2:
            wall = cell1
         else:
            wall = cell2
      
      #if cells are adjacent horizontally       
      elif y1 == y2:
      
         #the wall is vertical
         array = self.walls_ns
      
         if x1 < x2:
            wall = cell1
         else:
            wall = cell2
            
      return (array,wall)
   