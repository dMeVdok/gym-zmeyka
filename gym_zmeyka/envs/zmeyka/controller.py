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
        self.grid.info = self.look(self.body)
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
            reward -= 200
            print("GAME OVER!")
            return self.grid.pixels, reward, True, self.grid.info
        self.grid.set_pixel(self.body[-1],0)
        if r==0 or r==2:
            self.grid.set_pixel(self.body[0],1)
            if r!=2: 
                self.body = self.body[:-1]
                reward += 50 * (10 - math.sqrt((self.body[0][0]-self.grid.food[0])**2 + (self.body[0][1]-self.grid.food[1])**2) / math.sqrt(2))
            else:
                self.grid.spawn_food()
                reward += 200
        return self.grid.pixels, reward, False, self.grid.info
    
    def look(self,body):
        the_look = {}
        if self.direction   == 'L':
            the_look['FRONT'] = self.grid.pixels[self.body[0][0]][self.body[0][1]-1] # in front of the head
            the_look['LEFT'] = self.grid.pixels[self.body[0][0]+1][self.body[0][1]] # to the left of the head
            the_look['RIGHT'] = self.grid.pixels[self.body[0][0]-1][self.body[0][1]] # to the right of the head
        elif self.direction == 'R':
            the_look['FRONT'] = self.grid.pixels[self.body[0][0]][self.body[0][1]+1] # in front of the head
            the_look['LEFT'] = self.grid.pixels[self.body[0][0]-1][self.body[0][1]] # to the left of the head
            the_look['RIGHT'] = self.grid.pixels[self.body[0][0]+1][self.body[0][1]] # to the right of the head
        elif self.direction == 'U':
            the_look['FRONT'] = self.grid.pixels[self.body[0][0]-1][self.body[0][1]] # in front of the head
            the_look['LEFT'] = self.grid.pixels[self.body[0][0]][self.body[0][1]-1] # to the left of the head
            the_look['RIGHT'] = self.grid.pixels[self.body[0][0]][self.body[0][1]+1] # to the right of the head
        elif self.direction == 'D':
            the_look['FRONT'] = self.grid.pixels[self.body[0][0]+1][self.body[0][1]] # in front of the head
            the_look['LEFT'] = self.grid.pixels[self.body[0][0]][self.body[0][1]+1] # to the left of the head
            the_look['RIGHT'] = self.grid.pixels[self.body[0][0]][self.body[0][1]-1] # to the right of the head
        the_look['YPROJ'] = body[0][0]-self.grid.food[0]
        the_look['XPROJ'] = body[0][1]-self.grid.food[1]
        return the_look

    def die(self):
        self.grid.gameover()

class Grid:

    def __init__(self,width=10,height=10):
        row = [1 for i in range(width+2)]
        self.pixels = [row] + [[1] + [0 for j in range(width)] + [1] for i in range(height)] + [row]
        self.food = None
        self.spawn_food()
        self.snake = Snake((15,15),self)
        self.rewards = 0
        self.info = {}
        self.done = False
        
    def spawn_food(self):
        free_pixels = []
        for x in range(len(self.pixels)):
            for y in range(len(self.pixels[0])):
                if self.pixels[x][y] == 0:
                    free_pixels.append((x,y))
        self.food = random.choice(free_pixels)
        self.set_pixel(self.food,2)
        print("FOOD_SPAWN\t",self.food)
    
    def turn(self):
        return self.snake.step()
        
    def set_pixel(self,coord,c):
        self.pixels[coord[0]][coord[1]] = c
        
    def check_pixel(self,coord):
        return self.pixels[coord[0]][coord[1]]
        
class Controller:
    def __init__(self, controller_params=None):
        self.grid = Grid(30,30)
        
    def step(self,action):
        print("ACTION\t\t",action)
        if self.grid.snake.direction ==   'L':
            if action == 0:
                self.grid.snake.direction = 'D'
            elif action == 1:
                self.grid.snake.direction = 'U'
        elif self.grid.snake.direction == 'U':
            if action == 0:
                self.grid.snake.direction = 'L'
            elif action == 1:
                self.grid.snake.direction = 'R'
        elif self.grid.snake.direction == 'R':
            if action == 0:
                self.grid.snake.direction = 'U'
            elif action == 1:
                self.grid.snake.direction = 'D'
        elif self.grid.snake.direction == 'D':
            if action == 0:
                self.grid.snake.direction = 'R'
            elif action == 1:
                self.grid.snake.direction = 'L'
        print("DIRECTION\t",self.grid.snake.direction)
        return self.grid.turn()