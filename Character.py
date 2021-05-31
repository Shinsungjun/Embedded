from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import random
import numpy as np

class Penguin:
    def __init__(self):
        self.stand = Image.open('./images/penguin/penguin_center.png').convert('RGBA')
        self.right = Image.open('./images/penguin/penguin_right_center.png').convert('RGBA')
        self.left = Image.open('./images/penguin/penguin_left_center.png').convert('RGBA')
        self.shadow_image = Image.open('./images/shadow/shadow_0.png').convert('RGBA')
        self.appearance = self.stand.transform(self.stand.size, Image.AFFINE, (1,0,0,0,1,-70))
        self.shadow = self.shadow_image.transform(self.shadow_image.size, Image.AFFINE, (1,0,0,0,1,0))
        self.position_x = self.stand.width/2#120, 160 init\
        self.position_y = self.stand.height/2+90
        self.collision_point_x = self.position_x
        self.collision_point_y = self.position_y + 4
        self.verti_shadow = -99
        self.hori_record = 0
        self.verti_record = -70
        self.direction = 0
        self.state = 0 #0 move 1 jump 2 collision 3 power
        self.life = 4
        self.life_images = []
        self.life_image = Image.open('./images/life/fish.png').convert('RGBA')
        #self.life_images.append(self.life_image.transform(self.life_image.size, Image.AFFINE, (1,0,100,0,1,100)))
        self.life_images.append(self.life_image.transform(self.life_image.size, Image.AFFINE, (1,0,75,0,1,97)))
        self.life_images.append(self.life_image.transform(self.life_image.size, Image.AFFINE, (1,0,55,0,1,97)))
        self.life_images.append(self.life_image.transform(self.life_image.size, Image.AFFINE, (1,0,35,0,1,97)))
        self.life_images.append(self.life_image.transform(self.life_image.size, Image.AFFINE, (1,0,15,0,1,97)))
        self.count = 0

    def move(self, verti, hori):
        if self.position_x - hori < 35:
            if self.direction == 0 : #current = right
                self.appearance = self.left.transform(self.appearance.size, Image.AFFINE, (1, 0, self.hori_record, 0, 1, self.verti_record))
                self.direction = 1
            else :
                self.appearance = self.right.transform(self.appearance.size, Image.AFFINE, (1, 0, self.hori_record, 0, 1, self.verti_record))
                self.direction = 0
            self.shadow = self.shadow_image.transform(self.shadow.size, Image.AFFINE, (1, 0, self.hori_record, 0, 1, self.verti_shadow))
            if self.state == 3 :
                if self.count == 0:
                    brightness = ImageEnhance.Brightness(self.appearance)
                    self.appearance = brightness.enhance(10)
                    self.count = 1
                else :
                    self.count = 0
            return

        elif self.position_x - hori > 210:
            if self.direction == 0 : #current = right
                self.appearance = self.left.transform(self.appearance.size, Image.AFFINE, (1, 0, self.hori_record, 0, 1, self.verti_record))
                self.direction = 1
            else :
                self.appearance = self.right.transform(self.appearance.size, Image.AFFINE, (1, 0, self.hori_record, 0, 1, self.verti_record))
                self.direction = 0
            self.shadow = self.shadow_image.transform(self.shadow.size, Image.AFFINE, (1, 0, self.hori_record, 0, 1, self.verti_shadow))
            if self.state == 3 :
                if self.count == 0:
                    brightness = ImageEnhance.Brightness(self.appearance)
                    self.appearance = brightness.enhance(10)
                    self.count = 1
                else :
                    self.count = 0
            return
            
        self.hori_record += hori
        self.verti_record += verti

        if self.direction == 0 : #current = right
            self.appearance = self.left.transform(self.appearance.size, Image.AFFINE, (1, 0, self.hori_record, 0, 1, self.verti_record))
            self.shadow = self.shadow_image.transform(self.shadow.size, Image.AFFINE, (1, 0, self.hori_record, 0, 1, self.verti_shadow))
            self.direction = 1
            
        else :
            self.appearance = self.right.transform(self.appearance.size, Image.AFFINE, (1, 0, self.hori_record, 0, 1, self.verti_record))
            self.shadow = self.shadow_image.transform(self.shadow.size, Image.AFFINE, (1, 0, self.hori_record, 0, 1, self.verti_shadow))
            self.direction = 0
        if self.state == 3 :
                if self.count == 0:
                    brightness = ImageEnhance.Brightness(self.appearance)
                    self.appearance = brightness.enhance(1000)
                    self.count = 1
                else :
                    self.count = 0
        self.position_x = self.position_x - hori
        self.collision_point_x = self.position_x
        self.collision_point_y = self.position_y + 4

    def col_move(self, animation):
        if animation < 3:
            if self.direction == 0:
                self.appearance = self.appearance.transform(self.appearance.size, Image.AFFINE, (1, 0, -2, 0, 1, 0))
                self.shadow = self.shadow.transform(self.shadow.size, Image.AFFINE, (1, 0, -2, 0, 1, 0))

            else :
                self.appearance = self.appearance.transform(self.appearance.size, Image.AFFINE, (1, 0, 2, 0, 1, 0))
                self.shadow = self.shadow.transform(self.shadow.size, Image.AFFINE, (1, 0, 2, 0, 1, 0))
        
    def finish(self):
        self.appearance = self.stand.transform(self.appearance.size, Image.AFFINE, (1, 0, self.hori_record, 0, 1, self.verti_record))
        self.shadow = self.shadow_image.transform(self.shadow.size, Image.AFFINE, (1, 0, self.hori_record, 0, 1, self.verti_shadow))

    def jump(self):
        if self.state == 0:
            self.appearance = self.appearance.transform(self.appearance.size, Image.AFFINE, (1,0,0,0,1,10)) 
            self.state = 1
        else :
            self.appearance = self.appearance.transform(self.appearance.size, Image.AFFINE, (1,0,0,0,1,-10)) 
            self.state = 0
            
    
            