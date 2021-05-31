from PIL import Image, ImageDraw, ImageFont
import random
import numpy as np

class Obstacle:
    def __init__(self, speed, position):
        self.random = random.random()
        self.num_obstacle = 0
        self.speed = speed
        self.position = position
        if self.position == 0:
            self.x = 103
            self.fin_x = 60
            
        
        elif self.position == 1:
            self.x = 113
            self.fin_x = 125
            
        else :
            self.x = 123
            self.fin_x = 190

        self.y = 93
        self.fin_y = 220
        self.rate = (40-(self.speed-1) * 4.5)
        self.x_rate = (self.fin_x-self.x) / self.rate
        self.y_rate = (self.fin_y-self.y) / self.rate
        self.position = 0
        self.prev_x1 = 0
        self.prev_x2 = 0
        self.curr_x1 = 0
        self.curr_x2 = 0
        self.prev_y1 = 0
        self.prev_y2 = 0
        self.curr_y1 = 0
        self.curr_y2 = 0
        self.center_x = int((self.x + self.fin_x)/2)
        self.center_y = int((self.y + self.fin_y)/2)
        self.count = 0
        self.max_count = self.rate + 10
        self.col_count = 0
        
    def step(self, speed):
        if self.speed < speed:
            # if self.max_count - self.count < 4:
            #     self.count += 1
            self.speed = speed
            self.rate = (40-(self.speed-1) * 4.5)
            self.x_rate = (self.fin_x-self.x) / self.rate
            self.y_rate = (self.fin_y-self.y) / self.rate
        
        if self.count < self.max_count :
            self.prev_x1 = int((self.x + self.x_rate * self.count) - 30/self.rate * self.count)
            self.prev_x2 = int((self.x + self.x_rate * self.count) + 30/self.rate * self.count)
            self.prev_y1 = int((self.y + self.y_rate * self.count) - 6/self.rate * self.count)
            self.prev_y2 = int((self.y + self.y_rate * self.count) + 6/self.rate * self.count)
            self.count += 1
            self.curr_x1 = int((self.x + self.x_rate * self.count) - 30/self.rate * self.count)
            self.curr_x2 = int((self.x + self.x_rate * self.count) + 30/self.rate * self.count)
            self.curr_y1 = int((self.y + self.y_rate * self.count) - 6/self.rate * self.count)
            self.curr_y2 = int((self.y + self.y_rate * self.count) + 6/self.rate * self.count)
            self.center_x = int((self.curr_x1 + self.curr_x2)/2)
            self.center_y = int((self.curr_y1 + self.curr_y2)/2)

    def collision_check(self, Penguin):
        if Penguin.state == 0:
            if self.col_count == 0:
                if self.curr_y1 > 180:
                    if (Penguin.collision_point_x >= self.curr_x1 and Penguin.collision_point_x <= self.curr_x2
                        and Penguin.collision_point_y >= self.curr_y1 and Penguin.collision_point_y <= self.curr_y2):
                        print("collision!" + str(self.col_count)) 
                        Penguin.state = 2 #collision state
                        return 1
        return 0


