import random
import numpy as np
from Obstacle import Obstacle

class Obstacles:
    def __init__(self):
        self.obstacle_list = []

    def step(self, draw, state, speed):
        for obstacle in self.obstacle_list:
            if state != 'collision':
                obstacle.step(speed)
            draw.ellipse((obstacle.prev_x1, obstacle.prev_y1, obstacle.prev_x2, obstacle.prev_y2), outline = None, fill=(255,255,255,255))
            draw.ellipse((obstacle.curr_x1, obstacle.curr_y1, obstacle.curr_x2, obstacle.curr_y2), outline = 0, fill="#84cdfd")
    
    def make_obstacle(self, _speed):
        position = 0
        random_num = random.random()
        if random_num < 0.75 :
            random_num_2 = random.random()
            if random_num_2 < 0.33 :
                position = 0
            elif random_num_2 < 0.67 :
                position = 1
            else :
                position = 2
            self.obstacle_list.append(Obstacle(_speed, position))
        else :
            self.obstacle_list.append(Obstacle(_speed, 0))
            self.obstacle_list.append(Obstacle(_speed, 2))

    def clean_list(self):
        self.obstacle_list = [obstacle for obstacle in self.obstacle_list if obstacle.curr_y1 < 240]
   
    def collision_check(self, Penguin):
        collision = 0
        for obstacle in self.obstacle_list:
            collision = collision or obstacle.collision_check(Penguin)

        return collision


