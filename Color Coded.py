
import httplib2
import re
import pygame
import sys
import random
from collections import namedtuple
##
##
##
##def delete_quotes(a_str):    
##    actual_content = ""
##    for char in a_str:
##        if char != '"':
##            actual_content+=char
##    return actual_content
##
##def bytes_to_dict(BYTES):
##    pattern = '([^:{]+)(:)(\[[^]]+\])'
##    m = re.search(pattern,BYTES)
##    data = {}
##
##    while m:
##        key = m.group(1)
##        value = m.group(3)
##        data[key] = value
##        last = BYTES.find(value[-1])+1
##        BYTES = BYTES[last+1:]
##        m = re.search(pattern,BYTES)
##    return data
##
##
##def str_to_list(a_dict):
##    for k,v in a_dict.items():
##        a_dict[k] = v[1:-1].split(',')
##    return a_dict
##
##def str_to_float(a_dict):
##    for k,v in a_dict.items():
##        if k!= 'activity':
##            float_list = []
##            for a_str in v:
##                float_list.append(float(a_str))
##            a_dict[k] = float_list
##    return a_dict
##
##def get_data(id) -> dict:
##    h = httplib2.Http(".cache") 
##    timeInterval = "24"
##    requestAdd = "http://128.195.54.59:8004/DataWarehouse/requestData?id="+ id + "&timeInterval=" + timeInterval 
##    resp, content = h.request(requestAdd, "GET") 
##    content_str = content.decode(encoding = "utf-8")
##    actual_content = delete_quotes(content_str)
##    data_dict = bytes_to_dict(actual_content)
##    data_dict = str_to_list(data_dict)
##    return str_to_float(data_dict)
##
##def backup_data() -> dict:
##    result = {'activity':[]}
##    infile = open('ActivityLabel.txt', 'r')
##    activity = infile.read().split(',')
##    for level in activity:
##        if len(level) != 0:
##            result['activity'].append(level)
##    infile.close()
##    print("Using Laleh sample file")
##    return result
##    
##id = input("Enter the ID number associated to the activity collector app \
##(Press ENTER if you don't have one): ").strip()
##try:
##    data = get_data(id)
##    if len(data) <= 0:
##        print("Sorry - No data found")
##        try:
##            data = backup_data()
##        except:
##            data = {'activity':[]}
##except:
##    try:
##        backup_data()
##    except:
##        data = {'activity':[]}
##    
##
data = {'activity': []}
slow_timer = {'Very Low': 0, 'Low': .001, 'Medium': .01,
              'High': 2, 'Very High': 5}
slow_time_remaining = 0
for level in slow_timer:
    slow_time_remaining += data['activity'].count(level)*slow_timer[level]

#############################################
pygame.init()
Target = namedtuple('Target', 'color x y health')
Shot = namedtuple('Shot', 'color x y')
Star = namedtuple('Shot', 'color x y size')
BLACK = (0,0,0)
PURPLE = (140, 20, 170)
GREEN = (65, 255, 25)
WHITE = (255, 255, 255)
RED = (255,0,0)
BLUE = (0,0, 255)
BROWN = (255,115,0)
YELLOW = (255, 255, 0)
ULTIMATE_COLOR = (0,255,255)

clock = pygame.time.Clock()
size = (1200, 600)
target_x = size[0]-100
screen = pygame.display.set_mode(size)


###################################################################
def exit_game():
    '''Closes pygame window if user clicks on exit button'''
    pygame.quit()
    sys.exit()

def blit_text(message, size, color, x, y):
    font = pygame.font.SysFont('georgia', size)
    screen.blit(font.render(message, 1, color), (x, y))

###################################################################

def make_star():
    return Star(WHITE, random.randrange(size[0], size[0] + 1000),
                random.randrange(size[1]), random.randrange(1,10))

star_list = []
def make_star_list():
    for i in range(20):
        star_list.append(make_star())
            
make_star_list()

star_speed = 10
def draw_stars():
    global draw
    if draw:
        global star_speed
        visible_stars = []
        remove_list = []
        for i in range(len(star_list)):
            star_list[i] = star_list[i]._replace(x = (star_list[i].x-star_speed))
            pygame.draw.circle(screen, star_list[i].color,
                             (star_list[i].x, star_list[i].y),
                              star_list[i].size, star_list[i].size)
            if star_list[i].x <= size[0]:
                visible_stars.append(star_list[i])
            if star_list[i].x <= 0:
                remove_list.append(star_list[i])
        if len(visible_stars) >= len(star_list):
            make_star_list()
        for star in remove_list:
            star_list.remove(star)
            
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    draw = False

###################################################################

def instructions() -> bool:
    instruction_string = '''COLOR CODED

Shoot colored targets using artillery of the same color.
Deal more damage and string together combos by
using the correct color

Shoot using the            
Move using the UP and DOWN arrow keys.
Press F to unleash an Ultimate attack.

Hold SPACE to slow time - so long as you have slowing power.
Gain slowing power by exercising with the data collector app.

Press 'P' to play.
'''
    line_list = []
    y = 0
    for line in instruction_string.split("\n"):
            line_list.append((line, y))
            y += 40
            
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_game()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                return True
            
    screen.fill(BLACK)
    for line in line_list:
        blit_text(line[0], 30, PURPLE, int(size[0]/2-(len(line[0])*7)), line[1])
        
    controls = [('Q', RED), ('W', BLUE), (' E', YELLOW), (' R', WHITE), (' keys',PURPLE)]
    for i in range(len(controls)):
        blit_text(controls[i][0], 30, controls[i][1], 630+(30*i), 240)
    pygame.display.flip()

def game_screen():
    screen.fill(BLACK)
    controls = [('Q', RED), ('W', BLUE), ('E', YELLOW), ('R', WHITE)]
    for i in range(len(controls)):
        blit_text(controls[i][0], 20, controls[i][1], 25, (25*i))
        pygame.draw.rect(screen, controls[i][1],
                         (50,5+(i*25),cooldown[controls[i][1]]*10,15))
    blit_text("Level: " + str(LEVEL), 50, WHITE, int(size[0]-200), 0)
    blit_text("Combo: " + str(points), 50, WHITE, int(size[0]/2-200), 0)

    draw_stars()
def lost(tip: str):
    global game_over
    global shot_list
    global target_list
    global points
    global LEVEL
    global ultimate
    global combo_counter
    global slow_time_remaining
    slow_time_remaining = 0
    for level in slow_timer:
        slow_time_remaining += data['activity'].count(level)*slow_timer[level]
    shot_list.clear()
    target_list.clear()
    ultimate = 0
    combo_counter = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_game()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                LEVEL = 1
                points = 0
                target_list = make_target_list(LEVEL)
                game_over = False
    screen.fill(BLACK)
    blit_text("TIP: " + tip, 20, WHITE, 0,150)
    blit_text("GAME OVER", 50, RED, int(size[0]/2-200), int(size[1]/2))
    blit_text("Press 'P' to play again", 50, PURPLE,
              int(size[0]/2-258), int(size[1]/2+100))
    blit_text("Level: " + str(LEVEL), 50, WHITE, int(size[0]-200), 0)
    if len(point_list) > 0:
        blit_text("Max Combo: " + str(max(point_list)), 50, WHITE, int(size[0]/2-200), 0)
    else:
        blit_text("Max Combo: 0", 50, WHITE, int(size[0]/2-200), 0)
    pygame.display.flip()
    
###################################################################

def make_target(x: int, y: int) -> Target:
    global base_health
    n = random.randrange(4)
    element_color = {0: RED, 1: BLUE, 2: YELLOW, 3: WHITE}
    return Target(element_color[n], x, y, base_health)

def make_target_list(level: int) -> [Target]:
    global target_x
    L = [1]
    result = []
    x = target_x
    if level%10 == 0:
        number_of_targets = 10
    else:
        number_of_targets = level%10
    for n in range(number_of_targets):
        y = int(L[-1]*(size[1]/5))
        if y>=size[1]:
            L.clear()
            L.append(1)
            y = int(L[-1]*(size[1]/5))
            x += 100
        result.append(make_target(x,y))
        L.append(L[-1]+1)
    return result


def draw_targets(speed: int) -> None:
    for i in range(len(target_list)):
        target_list[i] = target_list[i]._replace(x = (target_list[i].x-speed))
        pygame.draw.rect(screen, target_list[i].color,
                         (target_list[i].x, target_list[i].y, 60,60))
        pygame.draw.rect(screen, GREEN,
                         (target_list[i].x, target_list[i].y -20,
                         target_list[i].health*15, 10))


###################################################################

        
def make_shot(color) -> Shot:
    return Shot(color, 30, shooter['center']-5)

def make_shot_list(color):
    shot_list.append(make_shot(color))
    
def draw_shots(speed: int):
    for i in range(len(shot_list)):
        shot_list[i] = shot_list[i]._replace(x = (shot_list[i].x+speed))
        pygame.draw.rect(screen, shot_list[i].color,
                         (shot_list[i].x, shot_list[i].y, 20, 10))


###################################################################

master_cooldown = 0
cooldown = {RED:0, BLUE:0, YELLOW:0, WHITE:0}

def shooter_shots():
    keys = pygame.key.get_pressed()
    elements = {pygame.K_q: RED, pygame.K_w: BLUE,
            pygame.K_e: YELLOW, pygame.K_r: WHITE}
    global cooldown
    global master_cooldown
    master_cooldown += 1
    for k in cooldown:
        cooldown[k] += 1
        if cooldown[k] >= 15:
            cooldown[k] = 15
    if master_cooldown >= 15:
        master_cooldown = 15
    for k in elements:
        if keys[k] and master_cooldown >= 15:
            make_shot_list(elements[k])
            cooldown[elements[k]] = 0
            master_cooldown = 0

###################################################################


def shooter_movement():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and shooter['y'] > 0:
        shooter['y'] += -8
    if keys[pygame.K_DOWN] and shooter['y']+100 < size[1]:
        shooter['y'] += 8
    shooter['center'] = shooter['y']+50

def draw_shooter(shooter: dict):
    pygame.draw.rect(screen, shooter['color'], (shooter['x'], shooter['y'],
                                                20,100))
    pygame.draw.rect(screen, shooter['color'], (20, shooter['center']-5,10,10))
    sight()



###################################################################
ultimate = 0
def use_ultimate():
    global ultimate
    global combo_counter
    if ultimate >= 100:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_f] and len(shot_list) < 10:
            for x in range(0,150, 50):
                for i in range(0,size[1],11):
                    shot_list.append(Shot(ULTIMATE_COLOR,
                                          x, i))
            ultimate += -100
            combo_counter = 0

def draw_ultimate():
    global ultimate
    blit_text('F', 25, GREEN, 910,size[1]-28)
    pygame.draw.rect(screen, YELLOW, (0,size[1]-21, 901, 17),1)
    pygame.draw.rect(screen, YELLOW, (300,size[1]-21, 300, 17),1)
    pygame.draw.rect(screen, GREEN, (0,size[1]-20,ultimate*3, 15))
    if 100 < ultimate <= 200:
        pygame.draw.rect(screen, GREEN, (0,size[1]-20,300, 15))
        pygame.draw.rect(screen, BLUE, (300,size[1]-20,(ultimate-100)*3, 15))
    elif ultimate > 200:
        pygame.draw.rect(screen, GREEN, (0,size[1]-20,300, 15))
        pygame.draw.rect(screen, BLUE, (300,size[1]-20,300, 15))
        pygame.draw.rect(screen, RED, (600,size[1]-20,(ultimate-200)*3, 15))
    blit_text('ULTIMATE',20, BLACK, 0, size[1]-25)
    
###################################################################
combo_counter = 0
def target_damage(shot: Shot, target: Target) -> Target:
    global point_list
    global points
    global combo_counter
    global ultimate
    damage = {RED: 1, BLUE: 1, YELLOW: 1, WHITE: 1}
    if shot.color == target.color:
        combo_counter += 1
        ultimate += combo_counter
        points += 1
        if ultimate >= 300:
            ultimate = 300
        return target._replace(health = 0)
    elif shot.color == ULTIMATE_COLOR:
        return target._replace(health = 0)
    else:
        point_list.append(points)
        points = 0
        combo_counter = 0
        if 0 < ultimate <= 100:
            ultimate = 0
        if 100 < ultimate <= 200:
            ultimate = 100
        elif ultimate > 200:
            ultimate = 200
        return target._replace(health = target.health - damage[shot.color])

def shot_target_collision():
    global points
    global combo_counter
    target_delete = []
    shot_delete = []
    for shot in shot_list:
        for i in range(len(target_list)):
            if shot.x > target_list[i].x and\
               shot.y in range(target_list[i].y-10, target_list[i].y+60):
                shot_delete.append(shot)
                target_list[i] = target_damage(shot, target_list[i])
                if target_list[i].health <= 0:
                    target_delete.append(target_list[i])
            elif shot.x > size[0]:
                shot_delete.append(shot)
    for shot in shot_delete:
        try:
            shot_list.remove(shot)
        except:
            pass
    for target in target_delete:
        try:
            target_list.remove(target)
        except ValueError:
            pass


###################################################################
        
def level_up():
    global LEVEL
    global target_list
    global shot_list
    global speed
    if len(target_list) == 0:
        shot_list.clear()
        LEVEL += 1
        target_list = make_target_list(LEVEL)

###################################################################    
def slow():
    global speed
    global star_speed
    global slow_time_remaining
    
    keys = pygame.key.get_pressed()
    if slow_time_remaining > 0 and keys[pygame.K_SPACE]:
            speed = 1
            star_speed = 1
            slow_time_remaining += -.1
            if slow_time_remaining < 0:
                slow_time_remaining = 0
    else:
        speed = 1 + int(LEVEL/5)
        if speed >5:
            speed =5
        star_speed = 10
        
def draw_slow():
    global slow_time_remaining
    blit_text('SPACE', 25, WHITE, 910,size[1]-58)
    pygame.draw.rect(screen, WHITE, (0,size[1]-51, 901, 17),1)
    pygame.draw.rect(screen, BLUE, (0,size[1]-50,int(slow_time_remaining)*3, 15))
    
def sight():
    global sighted
    ENDPOINT = size[0]
    if sighted == True:
        for target in target_list:
            if shooter['center'] in range(target.y, target.y+60):
                ENDPOINT = target.x
                break
        pygame.draw.line(screen, RED,
                         (40,shooter['center']),
                         (ENDPOINT,shooter['center']))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    sighted = False

## DYNAMIC VARAIBLES
LEVEL = 0
base_health = 4
target_list = []
shot_list = []
point_list = []
shooter = {'color': PURPLE,
           'x': 0,
           'y': int(size[1]/2)-50}
points = 0
TIPS = {0: "Make sure to string combos together",
        1: "You can gather slowing power by exercising with the data collector app",
        2: "Remember to press 'F' when you have an ULTIMATE charge",
        3: "You can press 'S' to add a lazer sight",
        4: "You can press 'D' to add aesthetic stars"}
 
started = False
game_over = False
sighted = False
draw = False
while True:        
    ##########################
    ##   EVENT PROCESSING   ##
    ##########################
    while not started:
        started = instructions()
    
    use_ultimate()
    slow()
    shooter_movement()
    shooter_shots()
    
    ### END CONDITION
    for target in target_list:
        if target.x <= 0:
            game_over = True
            tip = TIPS[random.randrange(len(TIPS))]
    while game_over:
        lost(tip)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_game()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                sighted = True
            if event.key == pygame.K_d:
                draw = True

    ##########################
    ##      GAME LOGIC      ##
    ##########################
    level_up()
    shot_target_collision()
    ##########################
    ##       DRAWING        ##
    ##########################
    
    game_screen()
     
    draw_shots(20)
    draw_ultimate()
    draw_slow()
    draw_targets(speed)
    draw_shooter(shooter)
    pygame.display.flip()
    clock.tick(60)
