import time
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from Character import Penguins
from MyBoard import Display
from Background import Background
from Obstacle import Obstacle
from Obstacles import Obstacles
import game_function as game

def main(Display, Background):
    # Get Object
    Penguin = Penguins()

    # Get drawing object to draw on image
    image = Image.new("RGBA", (Display.width, Display.height))
    draw = ImageDraw.Draw(image)

    # Clear display
    draw.rectangle((0, 0, Display.width, Display.height), outline=0, fill=(255, 0, 0, 100))
    Display.disp.image(image)

    # Get drawing object to draw on image
    draw = ImageDraw.Draw(image)

    # Font
    fnt = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 15)

    # Game parameter setting
    params = {'picture_num' : 0, 'back_count' : 0, 'speed' : 1, 'obstacle_rate_count' : 0, 
            'obstacle_rate' : 15, 'speed_up_count' : 0, 'collision' : 0, 'collision_time' : 0,
            'power_time' : 0, 'score' : 0, 'event_animation' : 0, 'rest_meter' : 3000,
            'ending' : 0, 'jump_sequence' : 999, 'move': 0}
    background = Background.background_list[params['picture_num']]
    obstacles = Obstacles()

    while True:
        #* Draw Background (White)
        draw.rectangle((0, 0, Display.width, Display.height), outline=0, fill=(255,255,255,255))

        #! --- GAME UPDATE AND CHECK SECTION --- #
        #* Game Over Check
        if Penguin.game_over_check():
            game.game_over(draw, image, Display)
            
        #* Collision Check
        params['collision'] = obstacles.collision_check(Penguin)

        #* Collision Event
        if params['collision'] :
            game.collision_event(params, Penguin)

        #* Collision Time Check
        if Penguin.state == 'collision' : #collision state
            game.collision_animation(params, Penguin)

        #* Power Mode Time Check
        if Penguin.state == 'power' or Penguin.state == 'jump&power': #Power || Power & Jump state
            game.power_time_check(params, Penguin)
            
        #* Background Update depending on Speed
        background = Background.step(params, background)

        #* Game Step when penguin is not collision
        if Penguin.state != 'collision':
            game.step(params, Display, obstacles, Penguin)
            

        #! --- DRAW SECTION --- #
        #* Obstacle Draw & Update
        obstacles.step(draw, Penguin.state, params['speed'])

        #* Draw Background
        image.paste(background, (0,0), background)

        #* Draw Ending Scene
        if params['ending'] :
            params['speed'], params['back_count'] = Background.ending(params['rest_meter'], image, params['speed'], params['back_count'] )

        #* Check finish motion
        if params['rest_meter'] == 0:
            Penguin.finish()
            
        #* Draw Penguin Shadow
        image.paste(Penguin.shadow, (0,0), Penguin.shadow)

        #* Draw Penguin appearance
        image.paste(Penguin.appearance, (0,0), Penguin.appearance)

        #* Fix background (Because of my poor drawing . . . . .)
        draw.rectangle((0,0, 240, 32), 0, 0)

        #* SPEED DISPLAY
        for i in range(params['speed']) :
            draw.rectangle((188+i*7, 17,193+i*7, 30), "#FFFFFF", "#FFFFFF")
        draw.text((130, 15), "SPEED ", font=fnt, fill=(255,255,255))

        #* LIFE DISPLAY
        for i in range(Penguin.life) :
            image.paste(Penguin.life_images[i], (0,0), Penguin.life_images[i])
        draw.text((0, 15), "LIFE ", font=fnt, fill=(255,255,255))

        #* REST DISPLAY
        draw.text((130, 0), "REST ", font=fnt, fill=(255,255,255))
        draw.text((180, 0), str(params['rest_meter'])+"M", font=fnt, fill=(255,255,255))

        #* SCORE DISPLAY
        draw.text((0, 0), "SCORE ", font=fnt, fill=(255,255,255))
        draw.text((55, 0), str(params['score']), font=fnt, fill=(255,255,255))

        #* Obstacle list clear for memory
        obstacles.clean_list()

        Display.disp.image(image)

if __name__ == "__main__":
    disp = Display()
    background = Background()

    main(disp, background)