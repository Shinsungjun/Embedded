from PIL import Image, ImageDraw, ImageFont
import random
import numpy as np

class Background:
    def __init__(self):
        self.background_list = []
        name = "back_"
        for i in range(13) :
            background = Image.open('./images/background/'+name+str(i)+'.png').convert('RGBA')
            self.background_list.append(background)
        self.ending_list = []
        name = "flag_"
        for i in range(9) :
            flag = Image.open('./images/flag/'+name+str(i)+'.png').convert('RGBA')
            self.ending_list.append(flag)

    def step(self, params, background):
        if params['back_count']  == 8-params['speed'] :
            if params['picture_num'] == 12:
                params['picture_num'] = 0
            else :
                params['picture_num'] += 1
            background = self.background_list[params['picture_num']]
            params['back_count'] = 0
        return background

        
    def ending(self, rest_meter, image, speed, back_count):
        if rest_meter < 5 :
            image.paste(self.ending_list[8], (0,0), self.ending_list[8])
            speed -= 1
            back_count = 999

        elif rest_meter < 30 :
            image.paste(self.ending_list[7], (0,0), self.ending_list[7])
            if speed > 2 :
                speed -= 1

        elif rest_meter < 50 :
            image.paste(self.ending_list[6], (0,0), self.ending_list[6])
            if speed > 3 :
                speed -= 1

        elif rest_meter < 80 :
            image.paste(self.ending_list[5], (0,0), self.ending_list[5])
            if speed > 4 :
                speed -= 1

        elif rest_meter < 120 :
            image.paste(self.ending_list[4], (0,0), self.ending_list[4])
            if speed > 5 :
                speed -= 1

        elif rest_meter < 180 :
            image.paste(self.ending_list[3], (0,0), self.ending_list[3])
            if speed > 5 :
                speed -= 1

        elif rest_meter < 250 :
            image.paste(self.ending_list[2], (0,0), self.ending_list[2])
            if speed > 6 :
                speed -= 1

        elif rest_meter < 320 :
            image.paste(self.ending_list[1], (0,0), self.ending_list[1])
            if speed > 6 :
                speed -= 1

        elif rest_meter < 400 :
            image.paste(self.ending_list[0], (0,0), self.ending_list[0])

        return speed, back_count
