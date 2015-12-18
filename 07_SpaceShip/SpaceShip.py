# program template for Spaceship (sound format: mp3)
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
initial_lives = 3
lives = initial_lives
time = 0
# initial setup
thrust = False
rotate_acc = 0.1 # rock's rotating acceleration
rotate_vel = 0 # rock's initial rotating velocity
ship_acc = 0.7 # ship's acceleration
ship_vel = 0 # ship's initial velocity
friction = 0.05 # ship's friction
rock_vel = [1, 3] # rock's velocity range
missile_acc = 5 # missile's acceleration
max_num_of_rock = 12 # max number of rocks in the space
age_increment = 0.7 # missile's age increment
score_increment = 20 # score for each rock
init_min_rock_spawn_range = 200
started = False
rock_group = set([])
missile_group = set([])
explosion_group = set([])
class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 30)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


def process_sprite_group(group, canvas):
    remove_group = set()
    for element in group:
        element.draw(canvas)
        if element.update():
            remove_group.add(element)
    group.difference_update(remove_group)
        
def group_collide(group, other_obj):
    global lives, score
    collision = False
    for element in set(group):
        if element.collide(other_obj):
            collision = True
            explosion = Sprite(element.pos, [0, 0], element.angle, 0, explosion_image, explosion_info)
            explosion_group.add(explosion)
            explosion_sound.rewind()
            explosion_sound.play()
            score += score_increment
            if other_obj == my_ship:
                lives -= 1
            group.discard(element)
    return collision

def group_group_collide(group1, group2):
    global score
    #remove_group = set()
    for element in set(group2):
        if group_collide(group1, element):
            #remove_group.add(element)
            group2.discard(element)
    #group2.difference_update(remove_group)
    
def game_starts():
    global started, lives, score, min_rock_spawn_range
    started = True
    timer.start()
    score = 0
    lives = initial_lives
    soundtrack.rewind()
    soundtrack.play()
    min_rock_spawn_range = init_min_rock_spawn_range
def game_ends():
    global started, rock_group
    started = False
    timer.stop()
    rock_group = set()
    soundtrack.pause()

# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()

    def draw(self,canvas):
        if thrust:
            self.image_center[0] = 45 + ship_info.get_size()[0]
        else:
            self.image_center[0] = 45
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        self.angle_vel = rotate_vel
        self.angle += self.angle_vel
        for i in range(2):
            self.vel[i] *= (1 - friction)
            self.vel[i] += ship_vel * angle_to_vector(self.angle)[i]
            self.pos[i] += self.vel[i]
        self.pos[0] = self.pos[0] % WIDTH
        self.pos[1] = self.pos[1] % HEIGHT
        
    def shoot(self):
        missile_vel = [0, 0]
        missile_pos = [0, 0]
        cannon_len = 40
        for i in range(2):
            missile_vel[i] = self.vel[i] + missile_acc * angle_to_vector(self.angle)[i]
            missile_pos[i] = self.pos[i] + cannon_len * angle_to_vector(self.angle)[i]
        a_missile = Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound)
        missile_group.add(a_missile)
        return missile_group   
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        if self.animated:
            self.age += 0.2
            pos_index = self.age % self.lifespan // 1 #* self.lifespan / 60 // 1
            canvas.draw_image(self.image, [self.image_center[0] + pos_index * self.image_size[0], self.image_center[1]], self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        
    def update(self):
        self.angle += self.angle_vel
        for i in range(2):
            self.pos[i] += self.vel[i]
        self.pos[0] = self.pos[0] % WIDTH
        self.pos[1] = self.pos[1] % HEIGHT
        self.age += age_increment
        if self.age <= self.lifespan:
            return False
        else:
            return True
        
    
    def collide(self, other_obj):
        self.collision = False
        distance = dist(self.pos, other_obj.pos)
        if distance < (self.radius+ other_obj.radius):
            self.collision = True
        else:
            self.collision = False
        return self.collision
        
           
def draw(canvas):
    global time, started
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw ship and sprites
    my_ship.draw(canvas)
    process_sprite_group(missile_group, canvas)
    process_sprite_group(rock_group, canvas)
    process_sprite_group(explosion_group, canvas)
    if started:
        if lives <= 0:
            game_ends()
    else:
        canvas.draw_image(splash_image, splash_info.get_center(), splash_info.get_size(), (WIDTH / 2, HEIGHT / 2), splash_info.get_size())
    # update ship and sprites
    my_ship.update()
    group_collide(rock_group, my_ship)
    group_group_collide(rock_group, missile_group)
    
    # update game info
    canvas.draw_text('Lives: ' + str(lives), (0.1 * WIDTH, 0.1 * HEIGHT), 24, 'White')
    canvas.draw_text('Score: ' + str(score), (0.8 * WIDTH, 0.1 * HEIGHT), 24, 'White')
        
        
        
# key handler to control space ship
def keydown(key):
    global thrust, rotate_vel, ship_vel, a_missile
    if key == simplegui.KEY_MAP['up']:
        thrust = True
        ship_vel += ship_acc
        ship_thrust_sound.set_volume(0.5)
        ship_thrust_sound.rewind()
        ship_thrust_sound.play()
    elif key == simplegui.KEY_MAP['left']:
        rotate_vel = -rotate_acc
    elif key == simplegui.KEY_MAP['right']:
        rotate_vel = rotate_acc
    elif key == simplegui.KEY_MAP['space']:
        a_missile = my_ship.shoot()
        timer_shoot.start()

def keyup(key):
    global thrust, rotate_vel, ship_vel
    if key == simplegui.KEY_MAP['up']:
        thrust = False
        ship_thrust_sound.pause()
        ship_vel = 0
    elif key == simplegui.KEY_MAP['left']:
        if rotate_vel < 0:
            rotate_vel = 0
    elif key == simplegui.KEY_MAP['right']:
        if rotate_vel > 0:
            rotate_vel = 0
    elif key == simplegui.KEY_MAP['space']:
        timer_shoot.stop()

def mouse_click(pos):
    global started
    inwidth = ((WIDTH - splash_info.get_size()[0]) / 2 < pos[0] < (WIDTH + splash_info.get_size()[0]) / 2)
    inheight = ((HEIGHT - splash_info.get_size()[1]) / 2 < pos[1] < (HEIGHT + splash_info.get_size()[1]) / 2)
    if (not started) and inwidth and inheight:
        game_starts()
        
# timer handler that spawns a rock    
def rock_spawner():
    global rock_group, min_rock_spawn_range 
    sign = random.randrange(-1, 2, 2)
    vel = [random.randrange(rock_vel[0], rock_vel[1]), random.randrange(rock_vel[0], rock_vel[1])]
    for i in range(2):
        vel[i] *= sign * (0.1 * score / score_increment + 1)
    angle = 2 * math.pi * random.random()
    angle_vel = 0.1 * sign * random.random()
    pos = [WIDTH * (2 * random.random() - 1), HEIGHT * (2 * random.random() - 1)]
    spawn_range = dist(pos, my_ship.pos)
    if min_rock_spawn_range <= 0.8 * (WIDTH / 2):
        min_rock_spawn_range = init_min_rock_spawn_range * (0.1 * score / score_increment + 1)            
    if spawn_range > min_rock_spawn_range:
        a_rock = Sprite(pos, vel, angle, angle_vel, asteroid_image, asteroid_info)
        rock_group.add(a_rock)    
    if len(rock_group) > max_num_of_rock:
        rock_group.pop()

        
def ship_shoot():
    my_ship.shoot()
    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info, ship_thrust_sound)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(mouse_click)

timer = simplegui.create_timer(1000.0, rock_spawner)
timer_shoot = simplegui.create_timer(150, ship_shoot)
# get things rolling
frame.start()
