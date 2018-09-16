import matplotlib.pyplot as plt
import matplotlib
import random, time
import numpy as np
from IPython import display
import math

#%matplotlib inline
#matplotlib.rcParams['figure.figsize'] = (2,2)

class Snake:
    
    def __init__(self,initial_coords=(0,0),grid=None):
        self.grid = grid
        self.body = [initial_coords]
        self.grid.set_pixel(initial_coords,1)
        self.direction = 'R'
        
    def set_direction(self,new_direction):
        self.direction = new_direction
        
    def step(self):
        reward = 0
        if self.direction == 'L':
            self.body.insert(0,(self.body[0][0],self.body[0][1]-1))
            if self.body[0][1] > self.grid.food[1]: reward += 50
        elif self.direction == 'R':
            self.body.insert(0,(self.body[0][0],self.body[0][1]+1))
            if self.body[0][1] < self.grid.food[1]: reward += 50
        elif self.direction == 'U':
            self.body.insert(0,(self.body[0][0]-1,self.body[0][1]))
            if self.body[0][0] > self.grid.food[0]: reward += 50
        elif self.direction == 'D':
            self.body.insert(0,(self.body[0][0]+1,self.body[0][1]))
            if self.body[0][0] < self.grid.food[0]: reward += 50
        r = self.grid.check_pixel(self.body[0])
        if r==1:
            self.die()
            reward -= 200
            return reward
        self.grid.set_pixel(self.body[-1],0)
        if r==0 or r==2:
            self.grid.set_pixel(self.body[0],1)
            if r!=2: 
                self.body = self.body[:-1]
                reward += 50 * (1 - math.sqrt((self.body[0][0]-self.grid.food[0])**2 + (self.body[0][1]-self.grid.food[1])**2) / math.sqrt(2))
            else:
                self.grid.spawn_food()
                reward += 200
        self.grid.rewards = reward 
        self.grid.info = look(self.body)
        return reward
    
    def look(self,body):
        the_look = {}
        if self.direction   == 'L':
            the_look['FRONT'] = [body[0][0]][body[0][1]-1] # in front of the head
            the_look['LEFT'] = [body[0][0]+1][body[0][1]] # to the left of the head
            the_look['RIGHT'] = [body[0][0]-1][body[0][1]] # to the right of the head
        elif self.direction == 'R':
            the_look['FRONT'] = [body[0][0]][body[0][1]+1] # in front of the head
            the_look['LEFT'] = [body[0][0]-1][body[0][1]] # to the left of the head
            the_look['RIGHT'] = [body[0][0]+1][body[0][1]] # to the right of the head
        elif self.direction == 'U':
            the_look['FRONT'] = [body[0][0]-1][body[0][1]] # in front of the head
            the_look['LEFT'] = [body[0][0]][body[0][1]-1] # to the left of the head
            the_look['RIGHT'] = [body[0][0]][body[0][1]+1] # to the right of the head
        elif self.direction == 'D':
            the_look['FRONT'] = [body[0][0]+1][body[0][1]] # in front of the head
            the_look['LEFT'] = [body[0][0]][body[0][1]+1] # to the left of the head
            the_look['RIGHT'] = [body[0][0]][body[0][1]-1] # to the right of the head
        the_look['YPROJ'] = self.body[0][0]-self.grid.food[0][0]
        the_look['XPROJ'] = self.body[0][1]-self.grid.food[0][1]
        return the_look

    def die(self):
        for c in self.body[1:]:
            self.grid.set_pixel(c,0)
        self.grid.gameover()

class Grid:

    def __init__(self,width=10,height=10):
        row = [1 for i in range(width+2)]
        self.pixels = [row] + [[1] + [0 for j in range(width)] + [1] for i in range(height)] + [row]
        self.snake = Snake((5,5),self)
        self.rewards = []
        self.info = {}
        self.spawn_food()
        self.done = False
        
    def spawn_food(self):
        free_pixels = []
        for x in range(len(self.pixels)):
            for y in range(len(self.pixels[0])):
                if self.pixels[x][y] == 0:
                    free_pixels.append((x,y))
        self.food = random.choice(free_pixels)
        self.set_pixel(self.food,2)
    
    def turn(self):
        self.snake.step()
        return self.pixels, self.rewards, self.done, self.info
        
    def set_pixel(self,coord,c):
        self.pixels[coord[0]][coord[1]] = c
        
    def check_pixel(self,coord):
        return self.pixels[coord[0]][coord[1]]
    
    def show(self):
        fig = plt.imshow(self.pixels)
        fig.axes.get_xaxis().set_visible(False)
        fig.axes.get_yaxis().set_visible(False)
        return fig
    
    def gameover(self):
        self.done = True
        
class Controller:
    def __init__(self, controller_params=None):
        self.grid = Grid(30,30)
        
    def step(action):
        if self.grid.snake.direction ==   'L':
            if action == 0:
                self.grid.snake.direction = 'B'
            elif action == 1:
                self.grid.snake.direction = 'U'
            return self.grid.turn()
        elif self.grid.snake.direction == 'U':
            if action == 0:
                self.grid.snake.direction = 'L'
            elif action == 1:
                self.grid.snake.direction = 'R'
            return self.grid.turn()
        elif self.grid.snake.direction == 'R':
            if action == 0:
                self.grid.snake.direction = 'U'
            elif action == 1:
                self.grid.snake.direction = 'B'
            return self.grid.turn()
        elif self.grid.snake.direction == 'D':
            if action == 0:
                self.grid.snake.direction = 'R'
            elif action == 1:
                self.grid.snake.direction = 'L'
            return self.grid.turn()