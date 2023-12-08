#draws a cardioid animation, that has a sinusoidal beat, and color interpolation for the lines

import pygame
import math
import sys

class Cardioid():
    def __init__(self,app):
        self.app = app
        self.radius = 400
        self.num_lines = 200
        self.translate = self.app.screen.get_width() // 2 , self.app.screen.get_height() // 2
        self.counter, self.increment = 0, 0.01

    #linearly interpolate the colors from red to green
    def color(self):
        self.counter += self.increment
        if 0 < self.counter < 1 :
            pass
        else:
            self.counter, self.increment = max(min(self.counter,1),0) , -self.increment

        return pygame.Color("red").lerp("green", self.counter)

    def draw(self):
        thetime = pygame.time.get_ticks()
        #make the radius vary according to a sine function
        self.radius = 400*abs(math.sin(thetime*0.004) -0.5)

        #factor that multiplies with the angle theta
        epsilon = 1e-4
        factor = 1 + epsilon*thetime
        print(factor)

        for i in range(self.num_lines):
            theta = (2*math.pi / self.num_lines)*i
            x1 = int(self.radius*math.cos(theta)) + self.translate[0]
            y1 = int(self.radius * math.sin(theta)) + self.translate[1]

            x2 = int(self.radius*math.cos(factor*theta))+ self.translate[0]
            y2 = int(self.radius * math.sin(factor*theta))+ self.translate[1]

            pygame.draw.aaline(self.app.screen, self.color(), (x1,y1), (x2,y2), 2)

    def update(self):
        pass

class App:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode([1600,900])
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.cardioid = Cardioid(self)

    def update(self):
        self.cardioid.update()
        pygame.display.update()

    def draw(self):
        black = (0,0,0)
        self.screen.fill(black)
        self.cardioid.draw()
        pygame.display.flip()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit(0)

    def run(self):
        while True:
            self.clock.tick(self.fps)
            self.check_events()
            self.update()
            self.draw()

def main():
    app = App()
    app.run()

main()