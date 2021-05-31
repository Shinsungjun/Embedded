import time
import random
import numpy as np
from colorsys import hsv_to_rgb
import board
from digitalio import DigitalInOut, Direction
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
from Character import Penguins
from MyBoard import Display
from Background import Background
from Obstacle import Obstacle

def main(Display, Background):
    # Get Object
    Penguin = Penguins()

    # Get drawing object to draw on image.
    image = Image.new("RGBA", (Display.width, Display.height))
    draw = ImageDraw.Draw(image)

    # Clear display.
    draw.rectangle((0, 0, Display.width, Display.height), outline=0, fill=(255, 0, 0, 100))
    Display.disp.image(image)

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    # Font
    fnt = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 15)
    game_over_fnt = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 38)

    # Game parameter setting
    curr_time = 0
    prev_time = time.time()
    sec = 0
    num = 0
    background = Background.background_list[num]
    back_count = 0
    speed = 1 # 1 ~ 7
    obstacles = []
    obstacle_rate_count = 0
    obstacle_rate = int(random.random() * 10 + 10)
    speed_up = 0
    collision = 0
    coltime = 0
    power_time = 0
    score = 0
    event_animation = 0
    rest_meter = 2500
    ending = 0
    jump_sequence = 999
    while True:
        # Draw Background (White)
        draw.rectangle((0, 0, Display.width, Display.height), outline=0, fill=(255,255,255,255))

        # Game Over Check
        if Penguin.life == 0:
            while True:
                draw.rectangle((0, 0, Display.width, Display.height), outline=0, fill=(255,255,255,255))
                draw.text((3, 100), "GAME OVER", font=game_over_fnt, fill=(0,0,0))
                Display.disp.image(image)

        # Collision Check    
        if Penguin.state == 0: #Only move state
            for obstacle in obstacles :
                collision = collision or obstacle.collision_check(Penguin)

        # Power Mode Time Check
        if Penguin.state == 3 or Penguin.state == 4:
            after_power_time = time.time()
            if after_power_time - power_time > 2 : #Power Mode 2 second
                print("power off")
                Penguin.state = 0 #move state
        
        # Collision Event
        if collision :
            score = score - int(200 / 7 * speed)
            event_animation = 0
            speed = 1
            back_count = 8-speed-1
            collision = 0
            speed_up = 0
            if Penguin.life > 0:
                Penguin.life -= 1
            coltime = time.time()

        # Background Update depending on Speed
        if back_count == 8-speed :
            if num == 12:
                num = 0
            else :
                num += 1
            background = Background.background_list[num]
            back_count = 0

        # Collision Time Check
        after_coltime = time.time()
        if Penguin.state == 2 : #collision state
            if after_coltime - coltime > 2.2:
                print("collision event over ")
                power_time = time.time()
                Penguin.state = 3 #power state
            else :
                if event_animation == 7:
                    event_animation = 0
                Penguin.col_move(event_animation)
                
                event_animation += 1

        # In Game State Move(0) Jump(1) Collision(2) Power Mode(3)
        if Penguin.state != 2:
            score = score + int(10 / 7 * speed)
            hori = 0
            if speed_up == 25:
                if speed < 7:
                    speed += 1
                    back_count = 8-speed-1
                speed_up = 0

            # Button Check
            if not Display.button_U.value:  # up pressed
                if not ending :
                    if speed < 7 :
                        speed += 1
                        back_count = 8-speed-1

            if not Display.button_D.value:  # down pressed
                if not ending :
                    if speed > 1 :
                        speed -= 1
                        back_count = 8-speed-1

            if not Display.button_L.value:  # left pressed
                hori = 10

            if not Display.button_R.value:  # right pressed
                hori = -10

            if not Display.button_C.value:  # center pressed
                pass

            if not Display.button_A.value:  # A pressed
                pass

            if not Display.button_B.value:  # B pressed
                if jump_sequence > 11 and Penguin.state != 1:
                    if Penguin.state == 0:
                        Penguin.state = 1
                    elif Penguin.state == 3:
                        Penguin.state = 4
                    jump_sequence = 0

                
            # Time check
            curr_time = time.time()
            sec = curr_time - prev_time
            fps = 1/(sec)
            prev_time = curr_time
            #print(fps) About 10 fps

            # Penguin move step
            if rest_meter != 0:
                Penguin.move(hori)

            if jump_sequence < 12:
                Penguin.jump(jump_sequence)
                jump_sequence += 1
            if jump_sequence == 12:
                jump_sequence += 1
                Penguin.state = 0
            # Random obstacle create
            if not ending :
                if obstacle_rate_count == obstacle_rate :
                    obstacle_rate = int(random.random() * 10 + 10)
                    obstacle_rate_count = 0
                    random_num1 = random.random()
                    position = 0
                    if random_num1 < 0.75 :
                        random_num = random.random()
                        if random_num < 0.33 :
                            position = 0
                        elif random_num < 0.66 :
                            position = 1
                        else :
                            position = 2
                        obstacles.append(Obstacle(speed, position))
                    else :
                        obstacles.append(Obstacle(speed, 0))
                        obstacles.append(Obstacle(speed, 2))

        # Draw Obstacles update & Obstacles
        for obstacle in obstacles :
            if Penguin.state != 2:
                obstacle.step(speed)
            draw.ellipse((obstacle.prev_x1, obstacle.prev_y1, obstacle.prev_x2, obstacle.prev_y2), outline = None, fill=(255,255,255,255))
            draw.ellipse((obstacle.curr_x1, obstacle.curr_y1, obstacle.curr_x2, obstacle.curr_y2), outline = 0, fill="#84cdfd")

        # Draw Background
        image.paste(background, (0,0), background)

        # Draw Ending Scene
        if ending :
            if rest_meter < 10 :
                image.paste(Background.ending_list[8], (0,0), Background.ending_list[8])
                speed = 0
                back_count = 999

            elif rest_meter < 30 :
                image.paste(Background.ending_list[7], (0,0), Background.ending_list[7])
                if speed > 2 :
                    speed -= 1

            elif rest_meter < 50 :
                image.paste(Background.ending_list[6], (0,0), Background.ending_list[6])
                if speed > 3 :
                    speed -= 1

            elif rest_meter < 80 :
                image.paste(Background.ending_list[5], (0,0), Background.ending_list[5])
                if speed > 4 :
                    speed -= 1

            elif rest_meter < 120 :
                image.paste(Background.ending_list[4], (0,0), Background.ending_list[4])
                if speed > 5 :
                    speed -= 1

            elif rest_meter < 180 :
                image.paste(Background.ending_list[3], (0,0), Background.ending_list[3])
                if speed > 5 :
                    speed -= 1

            elif rest_meter < 250 :
                image.paste(Background.ending_list[2], (0,0), Background.ending_list[2])
                if speed > 6 :
                    speed -= 1

            elif rest_meter < 320 :
                image.paste(Background.ending_list[1], (0,0), Background.ending_list[1])
                if speed > 6 :
                    speed -= 1

            elif rest_meter < 400 :
                image.paste(Background.ending_list[0], (0,0), Background.ending_list[0])
                

        # Check finish motion
        if rest_meter == 0:
            Penguin.finish()
            
        # Draw Penguin Shadow
        image.paste(Penguin.shadow, (0,0), Penguin.shadow)

        # Draw Penguin appearance
        image.paste(Penguin.appearance, (0,0), Penguin.appearance)

        # Fix background (Because of my poor drawing .. . . .)
        draw.rectangle((0,0, 240, 32), 0, 0)

        # SPEED DISPLAY
        for i in range(speed) :
            draw.rectangle((188+i*7, 17,193+i*7, 30), "#FFFFFF", "#FFFFFF")
        draw.text((130, 15), "SPEED ", font=fnt, fill=(255,255,255))

        # LIFE DISPLAY
        for i in range(Penguin.life) :
            image.paste(Penguin.life_images[i], (0,0), Penguin.life_images[i])
        draw.text((0, 15), "LIFE ", font=fnt, fill=(255,255,255))

        # REST DISPLAY
        draw.text((130, 0), "REST ", font=fnt, fill=(255,255,255))
        draw.text((180, 0), str(rest_meter)+"M", font=fnt, fill=(255,255,255))

        # SCORE DISPLAY
        draw.text((0, 0), "SCORE ", font=fnt, fill=(255,255,255))
        draw.text((55, 0), str(score), font=fnt, fill=(255,255,255))

        # Obstacle list clear for memory
        obstacles = [obstacle for obstacle in obstacles if obstacle.count < obstacle.max_count]

        # Game Params Update
        back_count += 1
        speed_up += 1
        if Penguin.state != 2:
            obstacle_rate_count += 1
        

        # Rest Meter Update
        if rest_meter < 5 :
            rest_meter = 0

        elif rest_meter <= 100 :
            rest_meter -= 3

        elif rest_meter < 400 and rest_meter > 100 :
            rest_meter -= 5
            ending = 1
            
        elif rest_meter >= 400 :
            if Penguin.state != 2:
                rest_meter = rest_meter - int(11/7 * speed)

        Display.disp.image(image)

if __name__ == "__main__":
    disp = Display()
    background = Background()

    main(disp, background)