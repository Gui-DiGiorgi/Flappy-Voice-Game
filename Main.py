import numpy as np
import math
import aubio
import pyaudio
import pygame
from pygametexting import pyg_text
import random
from time import time

class player():
    def __init__(self, size, x, w_ysize, frames, gravity, scream_force, color, vol_detection, mode):
        self.size = size
        self.x = x
        self.w_ysize = w_ysize
        self.y = int(w_ysize/2)
        self.frames = frames
        self.gravity = gravity*(1/frames)
        self.y_vel = 0
        self.vol_detection = vol_detection
        
        
        self.mode = mode
        
        if self.mode == 0:
        
            # counter gravity mode --> Harder
            self.scream_force = scream_force*self.gravity
        
        else:
            
            # jump mode --> Easier
            self.scream_force = -scream_force
        
        self.color = color
        
        self.box = pygame.image.load("Images\Playing_Player.png")
        
        self.box = self.box.convert_alpha()                                          
        
    def scream(self,vol):
        if vol>self.vol_detection:
            
            if self.mode == 0:

                # counter gravity mode --> Harder
                self.y_vel -= self.scream_force

            else:

                # jump mode --> Easier
                self.y_vel = self.scream_force
        
    def p_move(self):
        
        self.y_vel += self.gravity
        
        if self.y_vel < -3:
            self.y_vel = -3
        
        self.y = int(self.y+self.y_vel)
        
        
        if self.y+self.size/2>=self.w_ysize:
            self.y = self.w_ysize - self.size/2
            self.y_vel = 0
            
        
            
        
    def draw(self, window, angle):
        true_box = pygame.transform.rotate(self.box,angle)
    
        rotator_pos = true_box.get_rect()

        rotator_pos.center = (self.x,self.y)
    
        window.blit(true_box, rotator_pos)
        
class pipe():
    def __init__(self, win_size_x, win_size_y, speed, size, passage_loc, passage_size):

        self.win_size_x = win_size_x
        self.win_size_y = win_size_y
        self.x = win_size_x
        self.speed = speed

        self.pipe_img = pygame.image.load("Images\Pipe.png")
        pipe_size = self.pipe_img.get_rect().size[0]
        
        if size > pipe_size:
            self.size = pipe_size
            
        else:
            self.size = size

        self.passage_loc = passage_loc
        self.passage_size = passage_size

        
    def pipe_move(self):
         self.x -= self.speed 
        
    def draw(self, window):
        
        border = 5
        
        hole = self.passage_loc + self.passage_size
        
        pygame.draw.rect(window, (0,0,0), (self.x-border,0,self.size+2*border,self.passage_loc+border))
        pygame.draw.rect(window, (0,0,0), (self.x-border,hole-border,self.size+2*border,self.win_size_y-hole+border))
    
        window.blit(self.pipe_img, (self.x, 0), area = (0, 0, self.size, self.passage_loc))
        window.blit(self.pipe_img, (self.x, hole), area = (0, 0, self.size, self.win_size_y - hole))
        

# PyAudio object.
p = pyaudio.PyAudio()

RATE = 44100
CHUNK = 1024

# Open stream.
stream = p.open(format=pyaudio.paFloat32,
    channels=1, rate=RATE, input=True,
    frames_per_buffer=CHUNK)

pygame.init()

win_sizes = (600,600)

wind = pygame.display.set_mode(win_sizes)

pygame.display.set_caption("Flappy Voice")

txt = pyg_text(20,(0,0,0),"comicsansms", Win = wind)

clock = pygame.time.Clock()

clock_time = 30

run = True

pipe_hole = 300

hole_size = 100

pipe_speed = 5

pipe_size = 75

pipe_x_limit = int(win_sizes[0]*(3/5))

hole_limit = 50

score = 0

violation = False

scoring = False

score_detection = False

BG = pygame.image.load("Images\BG.png")

Menu = True

Play = False

Replay = False

about_to_start = False

transition = [False,0]

vol_limit = 100

while run:
    clock.tick(clock_time)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
    if Menu or Replay:
        
        wind.fill(pygame.Color("black"))
            
        if time()-transition[1]>=0.5:
            transition = [False,0]
            
        if about_to_start:
            
            pp = player(20, 300, 600, clock_time, 10, 3, (0,0,255), vol_limit, mode)
            
            pipe_hole = 300
            
            pipes = [pipe(win_sizes[0], win_sizes[1], pipe_speed, pipe_size, pipe_hole, hole_size)]
            
            score = 0
            
            about_to_start = False
            
            Play = True
            
            Menu = False
            
            Replay = False
            
            
    if Menu:
        
        txt.screen_text_centerpos("Flappy Voice", int(win_sizes[0]/2), 150, size = 30, color = (255,255,255))
            
        if txt.screen_button_centerpos("Play Balance", int(win_sizes[0]/2), 300, transition[0], color = (255,255,255)) and not transition[0]:
            pygame.time.delay(100)
            
            mode = 0
            
            about_to_start = True
            
        if txt.screen_button_centerpos("Play Jump", int(win_sizes[0]/2), 400, transition[0], color = (255,255,255)) and not transition[0]:
            pygame.time.delay(100)
            
            mode = 1
            
            about_to_start = True
            
            
    if Replay:
        
        txt.screen_text_centerpos("You Died", int(win_sizes[0]/2), 150, size = 30, color = (255,255,255))
        
        txt.screen_text_centerpos("Score: {0}".format(score),int(win_sizes[0]/2),200, color = (255,255,255))
        
        if txt.screen_button_centerpos("Play Again", int(win_sizes[0]/2), 300, transition[0], color = (255,255,255)):
            pygame.time.delay(100)
            transition = [True,time()]
            
            about_to_start = True
            
        if txt.screen_button_centerpos("Back to Menu", int(win_sizes[0]/2), 450, transition[0], color = (255,255,255)):
            pygame.time.delay(100)
            transition = [True,time()]
            
            Menu = True
            
            Replay = False
            
    
    if Play:

        wind.blit(BG, (0, 0))
            
        data = stream.read(CHUNK)

        samples = np.frombuffer(data,
            dtype=aubio.float_type)

        # Compute the energy (volume) of the
        # current frame.

        volume = np.sum(samples**2)/len(samples)

        volume = int(volume*10**6)

        if volume == 0:
            pass
        else:
            volume = int(math.log(volume)*10**2)

        y_vol = int(volume/2)

        for i in pipes:
            i.pipe_move()

        if pipes[len(pipes)-1].x <= pipe_x_limit:

            if random.choice([False,True]):

                pipe_hole += random.randint(0,100)

                if pipe_hole > win_sizes[1] - hole_size - hole_limit:

                    pipe_hole = win_sizes[1] - hole_size - hole_limit

            else:

                pipe_hole -= random.randint(0,100)

                if pipe_hole < hole_limit:

                    pipe_hole = hole_limit

            pipes.append(pipe(win_sizes[0], win_sizes[1], pipe_speed, pipe_size, pipe_hole, hole_size))

        if pipes[0].x < -pipes[0].size:
            pipes.pop(0)

        pp.scream(volume)
        pp.p_move()

        # mouse_pos = pygame.mouse.get_pos()
        # pp.y = mouse_pos[1]

        scoring = True

        for i in pipes:

            half_size = int(pp.size/2)

            x_cond_1 = (i.x <= pp.x + half_size <= i.x + i.size)
            x_cond_2 = (i.x <= pp.x - half_size <= i.x + i.size)

            if x_cond_1 or x_cond_2:

                scoring = False
                score_detection = True

                y_cond_1 = (i.passage_loc <= pp.y + half_size <= i.passage_loc+ i.passage_size)
                y_cond_2 = (i.passage_loc <= pp.y - half_size <= i.passage_loc+ i.passage_size)

                if  y_cond_1 and y_cond_2:
                    pass

                else:
                    #i.color = (255,0,0)
                    violation = True
                    Play = False
                    Replay = True

                break

        if scoring and score_detection:
            if not violation:
                score += 1
            violation = False
            score_detection = False

        true_angle = -math.atan(pp.y_vel/2)*(180/math.pi)

        for i in pipes:

            i.draw(wind)

        pp.draw(wind,true_angle)

        txt.screen_button_initpos("State:",0,0)

        active = ["Inactive",(255,0,0)]

        if volume > vol_limit:

            active = ["Active",(0,0,255)]

        txt.screen_button_initpos(active[0],60,0,color = active[1])

        txt.screen_text_initpos("Score: {0}".format(score),0,25)
    
    pygame.display.update()

stream.stop_stream()
stream.close()

p.terminate()

pygame.quit()
