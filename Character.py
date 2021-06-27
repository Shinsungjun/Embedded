from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import random
import numpy as np

class Penguins:
    def __init__(self):
        self.stand = Image.open('./images/penguin/penguin_center.png').convert('RGBA')
        self.right = Image.open('./images/penguin/penguin_right_center.png').convert('RGBA')
        self.left = Image.open('./images/penguin/penguin_left_center.png').convert('RGBA')
        self.shadow_image_full = Image.open('./images/shadow/shadow_0.png').convert('RGBA')
        self.shadow_image_middle = Image.open('./images/shadow/shadow_1.png').convert('RGBA')
        self.shadow_image_small = Image.open('./images/shadow/shadow_2.png').convert('RGBA')
        self.appearance = self.stand.transform(self.stand.size, Image.AFFINE, (1,0,0,0,1,-70))
        self.shadow = self.shadow_image_full.transform(self.shadow_image_full.size, Image.AFFINE, (1,0,0,0,1,0))
        self.position_x = self.stand.width/2#120, 160 init
        self.position_y = self.stand.height/2+90
        self.collision_point_x = self.position_x
        self.collision_point_y = self.position_y + 4
        self.verti_shadow = -99
        self.hori_record = 0
        self.verti_record = -70
        self.direction = 0
        self.state = 'move' #0 move 1 jump 2 collision 3 power 4 jump & power
        self.life = 4
        self.life_images = []
        self.life_image = Image.open('./images/life/fish.png').convert('RGBA')
        self.life_images.append(self.life_image.transform(self.life_image.size, Image.AFFINE, (1,0,75,0,1,97)))
        self.life_images.append(self.life_image.transform(self.life_image.size, Image.AFFINE, (1,0,55,0,1,97)))
        self.life_images.append(self.life_image.transform(self.life_image.size, Image.AFFINE, (1,0,35,0,1,97)))
        self.life_images.append(self.life_image.transform(self.life_image.size, Image.AFFINE, (1,0,15,0,1,97)))
        self.count = 0

    def move(self, hori):
        if self.position_x - hori < 35:
            if self.direction == 0 : #current = right
                self.appearance = self.left.transform(self.appearance.size, Image.AFFINE, (1, 0, self.hori_record, 0, 1, self.verti_record))
                self.direction = 1
            else :
                self.appearance = self.right.transform(self.appearance.size, Image.AFFINE, (1, 0, self.hori_record, 0, 1, self.verti_record))
                self.direction = 0
            self.shadow = self.shadow_image_full.transform(self.shadow.size, Image.AFFINE, (1, 0, self.hori_record, 0, 1, self.verti_shadow))
            if self.state == 'power' :
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
            self.shadow = self.shadow_image_full.transform(self.shadow.size, Image.AFFINE, (1, 0, self.hori_record, 0, 1, self.verti_shadow))
            if self.state == 'power' :
                if self.count == 0:
                    brightness = ImageEnhance.Brightness(self.appearance)
                    self.appearance = brightness.enhance(10)
                    self.count = 1
                else :
                    self.count = 0
            return
            
        self.hori_record += hori

        if self.direction == 0 : #current = right
            self.appearance = self.left.transform(self.appearance.size, Image.AFFINE, (1, 0, self.hori_record, 0, 1, self.verti_record))
            self.shadow = self.shadow_image_full.transform(self.shadow.size, Image.AFFINE, (1, 0, self.hori_record, 0, 1, self.verti_shadow))
            self.direction = 1
            
        else :
            self.appearance = self.right.transform(self.appearance.size, Image.AFFINE, (1, 0, self.hori_record, 0, 1, self.verti_record))
            self.shadow = self.shadow_image_full.transform(self.shadow.size, Image.AFFINE, (1, 0, self.hori_record, 0, 1, self.verti_shadow))
            self.direction = 0
        if self.state == 'power' :
                if self.count == 0:
                    brightness = ImageEnhance.Brightness(self.appearance)
                    self.appearance = brightness.enhance(1000)
                    self.count = 1
                else :
                    self.count = 0
        self.position_x = self.position_x - hori
        self.collision_point_x = self.position_x
        self.collision_point_y = self.position_y + 4

    def jump(self, jump_sequence):
        if jump_sequence < 6:
            self.verti_record += 3
            self.appearance = self.right.transform(self.appearance.size, Image.AFFINE, (1, 0, self.hori_record, 0, 1, self.verti_record))
            if jump_sequence > 3:
                self.shadow = self.shadow_image_small.transform(self.shadow.size, Image.AFFINE, (1, 0, self.hori_record, 0, 1, self.verti_shadow))
            elif jump_sequence > 1:
                self.shadow = self.shadow_image_middle.transform(self.shadow.size, Image.AFFINE, (1, 0, self.hori_record, 0, 1, self.verti_shadow))

        elif jump_sequence >= 6 and jump_sequence < 12:
            self.verti_record -= 3
            self.appearance = self.right.transform(self.appearance.size, Image.AFFINE, (1, 0, self.hori_record, 0, 1, self.verti_record))
            if jump_sequence > 9:
                self.shadow = self.shadow_image_middle.transform(self.shadow.size, Image.AFFINE, (1, 0, self.hori_record, 0, 1, self.verti_shadow))
            elif jump_sequence >= 6:
                self.shadow = self.shadow_image_small.transform(self.shadow.size, Image.AFFINE, (1, 0, self.hori_record, 0, 1, self.verti_shadow))
        
        if self.state == 'jump&power' : #jump & power
                if self.count == 0:
                    brightness = ImageEnhance.Brightness(self.appearance)
                    self.appearance = brightness.enhance(1000)
                    self.count = 1
                else :
                    self.count = 0

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
        if self.state == 'move':
            self.appearance = self.appearance.transform(self.appearance.size, Image.AFFINE, (1,0,0,0,1,10)) 
            self.shadow = self.shadow_image_full.transform(self.shadow.size, Image.AFFINE, (1, 0, self.hori_record, 0, 1, self.verti_shadow))
            self.state = 'jump'
        else :
            self.appearance = self.appearance.transform(self.appearance.size, Image.AFFINE, (1,0,0,0,1,-10))
            self.shadow = self.shadow_image_small.transform(self.shadow.size, Image.AFFINE, (1, 0, self.hori_record, 0, 1, self.verti_shadow))
            self.state = 'move'

    def game_over_check(self):
        if self.life == 0:
            return 1
        return 0