import pygame
import math
import random

DIFF_FACT = 4
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

SPEED_VALUES = [0.008, 0.008]

scoreTOT = 0

class Block(pygame.sprite.Sprite):
    """ This class represents the object"""

    def __init__(self, screen_width, screen_height, object_sizes):
        super().__init__()

        # start positions
        self.x0, self.y0 = 0, 0
        # exit angle
        self.angle = 0
        # position
        self.parameter = 0
        # object speed
        self.speed = 1
        self.decrease_rate = 1
        # contains x, y of object when chosen
        self.chosen = []
        self.rejected = []
        self.c = 0
        self.decrease = 0
        self.dim = 0
        self.decrease_step = 0
        self.done = False
        self.radius = 0
        self.NN = 0
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.object_sizes = object_sizes

    def reset(self, side, speed, decrease):
        """
        initialize object
        """
        self.results = 7 * [0]
        self.decrease = decrease
        self.side = side
        self.chosen = []
        self.rejected = []
        self.x0 = side * self.screen_width
        self.y0 = self.screen_height * 0.1
        self.radius = self.screen_height * 0.5
        self.angle = 3 / 2 * math.pi

        if self.side == 0:
            self.speed = random.choice(SPEED_VALUES)
        else:
            self.speed = -(random.choice(SPEED_VALUES))

        self.parameter = 0
        self.image = pygame.Surface(random.choice(self.object_sizes))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.dim = self.rect.w
        self.dim_ini = self.dim
        self.rect.x = self.x0
        self.rect.y = self.y0
        if self.x0 == 0:
            self.rect.x = (self.x0 - self.dim) + self.parameter * math.sin(self.angle)
        else:
            self.rect.x = self.x0 + self.parameter * math.sin(self.angle)
        self.rect.y = self.y0 + self.parameter * math.cos(self.angle)
        self.decrease_step = DIFF_FACT * self.decrease  #
        self.decrease_rate = self.rect.w / self.decrease_step
        self.c = 0

    def update(self):
        global results
        # global NN
        if self.chosen:  # reduce
            self.speed = 0
            if self.c > 0:
                self.c = 0
            if self.rect.w and self.rect.h:
                self.dim = self.dim - self.decrease_rate
                self.image = pygame.Surface([round(self.dim), round(self.dim)])
                self.image.fill(BLACK)
                self.rect = self.image.get_rect()
                self.rect.x, self.rect.y = self.chosen

            else:
                self.NN += 1
                self.results = [self.NN, self.side, 1, self.dim_ini, self.decrease]
                self.c = 0
                self.chosen = 0

        elif self.rejected:

            self.c += 1
            self.rect.x = self.x0 + self.radius * math.cos(self.angle)
            self.rect.y = self.y0 - self.radius * math.sin(self.angle)
            self.angle = self.angle + self.speed

            if self.rect.x < -self.rect.w or self.rect.x > self.screen_width + self.rect.w or self.rect.y < -self.rect.h:
                self.NN += 1
                self.results = [self.NN, self.side, 0, self.dim_ini, self.decrease]
                self.c = 0
                self.rejected = 0

        elif self.speed == 0:
            self.rect.x = self.x0 + self.radius * math.cos(self.angle)
            self.rect.y = self.y0 - self.radius * math.sin(self.angle)
            self.angle = self.angle + self.speed

        else:
            self.c += 1
            self.rect.x = self.x0 + self.radius * math.cos(self.angle)
            self.rect.y = self.y0 - self.radius * math.sin(self.angle)
            self.parameter += self.speed
            self.angle = self.angle + self.speed

            if self.rect.x < -self.rect.w or self.rect.x > self.screen_width + self.rect.w or self.rect.y < -self.rect.h:
                self.c = 0

    def reset_circle(self, side, speed, decrease, image):
        """
        initialize object
        """
        self.results = 7 * [0]
        self.decrease = decrease
        self.side = side

        self.chosen = []
        self.rejected = []
        self.x0 = side * self.screen_width

        self.y0 = self.screen_height * 0.1
        self.radius = self.screen_height * 0.5
        self.angle = 3 / 2 * math.pi
        # self.results = 7*[0]

        if self.side == 0:
            self.speed = self.speed * 60 / FPS
        else:
            self.speed = -self.speed * 60 / FPS

        self.parameter = 0

        self.image = pygame.Surface([image, image])
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.dim = self.rect.w
        self.dim_ini = self.dim
        self.rect.x = self.x0
        self.rect.y = self.y0

        if self.x0 == 0:
            self.rect.x = (self.x0 - self.dim) + self.parameter * math.sin(self.angle)
        else:
            self.rect.x = self.x0 + self.parameter * math.sin(self.angle)
        self.rect.y = self.y0 + self.parameter * math.cos(self.angle)

        self.decrease_step = DIFF_FACT * self.decrease * FPS / 60  #
        self.decrease_rate = self.rect.w / self.decrease_step

        self.c = 0

    def update_circle(self):
        global results
        # global NN
        if self.chosen:  # reduce

            self.speed = 0
            if self.c > 0:
                self.c = 0
            if self.rect.w and self.rect.h:
                self.dim = self.dim - self.decrease_rate
                self.image = pygame.Surface([round(self.dim), round(self.dim)])
                self.image.fill(BLACK)
                self.rect = self.image.get_rect()
                self.rect.x, self.rect.y = self.chosen

            else:
                self.NN += 1

                self.results = [self.NN, self.side, 1, self.dim_ini, self.decrease]
                self.c = 0
                self.chosen = 0
                if scoreTOT > self.screen_width:
                    self.done = True

        elif self.rejected:

            self.c += 1
            self.rect.x = self.x0 + self.radius * math.cos(self.angle)
            self.rect.y = self.y0 - self.radius * math.sin(self.angle)
            self.angle = self.angle + self.speed

            if self.rect.x < -self.rect.w or self.rect.x > self.screen_width + self.rect.w or self.rect.y < -self.rect.h:
                self.NN += 1

                self.results = [self.NN, self.side, 0, self.dim_ini, self.decrease]
                self.c = 0
                self.rejected = 0

        elif self.speed == 0:
            self.rect.x = self.x0 + self.radius * math.cos(self.angle)
            self.rect.y = self.y0 - self.radius * math.sin(self.angle)
            self.angle = self.angle + self.speed

        else:
            self.c += 1
            self.rect.x = self.x0 + self.radius * math.cos(self.angle)
            self.rect.y = self.y0 - self.radius * math.sin(self.angle)
            self.angle = self.angle + self.speed

            if self.rect.x < -self.rect.w or self.rect.x > self.screen_width + self.rect.w or self.rect.y < -self.rect.h:
                self.c = 0

    def reset_line(self, side, speed0, decrease, image):
        """
        initialize object
        """
        self.results = 7 * [0]
        self.decrease = decrease
        self.side = side

        self.chosen = []
        self.rejected = []
        self.x0 = self.screen_width // 2
        self.y0 = self.screen_height
        self.radius = self.screen_height / 2
        if speed0 == 0:
            self.speed = 0
        else:
            # angle_max = (math.asin((self.y0 * 0.1 ) /(self.radius - OBJ_SIZE_max)
            # self.speed = SCREEN_HEIGHT / (math.asin((self.y0 * 0.1 ) /(self.radius - OBJ_SIZE_max)) + math.pi/(2 * speed0))
            angolo = math.pi / 2 + math.asin((self.y0 * 0.1) / (self.radius))
            num_passi = angolo / speed0
            self.speed = self.screen_height / num_passi * 60 / FPS
            # print(self.speed,speed0, math.asin((self.y0 * 0.1 ) /(self.radius - OBJ_SIZE_max)) + math.pi, (math.asin((self.y0 * 0.1 ) /(self.radius - OBJ_SIZE_max)) + math.pi/(2 * speed0)) )
        self.parameter = 0
        self.angle = math.pi
        self.image = pygame.Surface([image, image])
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.dim = self.rect.w
        self.dim_ini = self.dim
        self.rect.x = self.x0
        self.rect.y = self.y0
        self.decrease_step = DIFF_FACT * self.decrease  #
        self.decrease_rate = self.rect.w / self.decrease_step
        self.angle = math.pi // 2
        self.c = 0

    def update_line(self):
        global results
        # global NN
        if self.chosen:  # reduce

            self.speed = 0
            if self.c > 0:
                self.c = 0
            if self.rect.w and self.rect.h:
                self.dim = self.dim - self.decrease_rate
                self.image = pygame.Surface([round(self.dim), round(self.dim)])
                self.image.fill(BLACK)
                self.rect = self.image.get_rect()
                self.rect.x, self.rect.y = self.chosen

            else:
                self.NN += 1

                self.results = [self.NN, self.side, 1, self.dim_ini, self.decrease]
                self.c = 0
                self.chosen = 0
                if scoreTOT > self.screen_width:
                    self.done = True

        elif self.rejected:
            self.c += 1
            self.rect.x = self.x0
            self.rect.y = self.y0 - self.parameter
            self.parameter = self.parameter + self.speed

            if self.rect.x < -self.rect.w or self.rect.x > self.screen_width + self.rect.w or self.rect.y < -self.rect.h:
                self.NN += 1

                self.results = [self.NN, self.side, 0, self.dim_ini, self.decrease]
                self.c = 0
                self.rejected = 0

        elif self.speed == 0:
            self.rect.x = self.x0
            self.rect.y = self.y0 - self.parameter
            self.parameter = self.parameter + self.speed

        else:
            self.c += 1
            self.rect.x = self.x0
            self.rect.y = self.y0 - self.parameter
            self.parameter = self.parameter + self.speed

            if self.rect.x < -self.rect.w or self.rect.x > self.screen_width + self.rect.w or self.rect.y < -self.rect.h:
                self.c = 0