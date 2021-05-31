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

        
        