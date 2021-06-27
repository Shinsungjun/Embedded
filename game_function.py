import time
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def step(params, Display, obstacles, Penguin):
    #BUTTON CHECK
    if not Display.button_U.value:  # up pressed
        speed_up(params)
    if not Display.button_D.value:  # down pressed
        speed_down(params)
    if not Display.button_L.value:  # left pressed
        params['move'] = 10
    if not Display.button_R.value:  # right pressed
        params['move'] = -10
    if not Display.button_B.value:  # B pressed
        jump_button_event(params, Penguin)
    # Random obstacle create
    if not params['ending']:
        make_obstacle(params, obstacles)
    #Penguin Move
    penguin_step(params, Penguin)
    #Update Game Parameters
    update(params, Penguin)
    
def collision_event(params, Penguin):
    Penguin.state = 'collision' #collision state
    params['score'] = params['score'] - int(200 / 7 * params['speed'])
    params['event_animation'] = 0
    params['speed'] = 1
    params['back_count'] = 7-params['speed']
    params['collision'] = 0
    params['speed_up_count'] = 0
    if Penguin.life > 0:
        Penguin.life -= 1
    params['collition_time'] = time.time()

def collision_animation(params, Penguin):
    after_coltime = time.time()
    if after_coltime - params['collition_time'] > 2.2: #Collision animation 2.2 sec 
        print("collision event over")
        params['power_time'] = time.time()
        Penguin.state = 'power'
    else :
        if params['event_animation'] == 7:
            params['event_animation'] = 0
        Penguin.col_move(params['event_animation'])
        params['event_animation'] += 1

def power_time_check(params, Penguin):
    after_power_time = time.time()
    if after_power_time - params['power_time'] > 2 : #Power Mode 2 second
        print("power off")
        Penguin.state = 'move'

def speed_up(params):
    if params['speed'] < 7 :
        params['speed'] += 1
        params['back_count'] = 7-params['speed']

def speed_down(params):
     if params['speed'] > 1 :
        params['speed'] -= 1
        params['back_count'] = 7-params['speed']

def penguin_step(params, Penguin):
    if params['rest_meter'] != 0:
        Penguin.move(params['move'])
    if params['jump_sequence'] < 12:
        Penguin.jump(params['jump_sequence'])
        params['jump_sequence'] += 1
    if params['jump_sequence'] == 12:
        params['jump_sequence'] += 1
        Penguin.state = 'move'

def jump_button_event(params, Penguin):
    if params['jump_sequence'] > 11 and Penguin.state != 'jump':
        if Penguin.state == 'move':
            Penguin.state = 'jump'
        elif Penguin.state == 'power':
            Penguin.state = 'jump&power'
        params['jump_sequence'] = 0

def make_obstacle(params, obstacles):
    if params['obstacle_rate_count'] == params['obstacle_rate'] :
        params['obstacle_rate'] = int(random.random() * 10 + 4)
        params['obstacle_rate_count'] = 0
        obstacles.make_obstacle(params['speed'])

def update(params, Penguin):
    params['move'] = 0
    if params['speed_up_count'] == 25:
        if params['speed'] < 7:
            params['speed'] += 1
            params['back_count'] = 7-params['speed']
        params['speed_up_count'] = 0
    params['back_count'] += 1
    params['speed_up_count'] += 1
    score = params['score']
    params['score'] = params['score'] + int(10 / 7 * params['speed'])
    if Penguin.state != 'collision':
        params['obstacle_rate_count'] += 1
    # Rest Meter Update
    if params['rest_meter'] < 5 :
        params['rest_meter'] = 0
        params['score'] = score
    elif params['rest_meter'] <= 100 :
        params['rest_meter'] -= 3
    elif params['rest_meter'] < 400 and params['rest_meter'] > 100 :
        params['rest_meter'] -= 5
        params['ending'] = 1
    elif params['rest_meter'] >= 400 :
        if Penguin.state != 'collision':
            params['rest_meter'] = params['rest_meter'] - int(11/7 * params['speed'])

def game_over(draw, image, Display):
    game_over_fnt = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 38)   
    while True:
        draw.rectangle((0, 0, Display.width, Display.height), outline=0, fill=(255,255,255,255))
        draw.text((3, 100), "GAME OVER", font=game_over_fnt, fill=(0,0,0))
        Display.disp.image(image)