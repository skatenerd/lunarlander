import sys, pygame, time
from geometry import segment_intersects_polyline

pygame.init()


class Game(object):
    def __init__(self):
        self.width = 500
        self.height = 500
        self.size = (self.width, self.height)
        self.speed = [0, 0]
        self.darkblue = pygame.Color(0,0,50,255)
        self.yellow = pygame.Color('yellow')

        self.terrain_points = ((0,self.height),(100,self.height-50), (self.width, self.height-10))
        self.terrain_segments = zip(self.terrain_points, self.terrain_points[1:])

        self.screen = pygame.display.set_mode(self.size)
        self.lander_sprite = pygame.image.load("lander.gif")
        self.lander_box = self.lander_sprite.get_rect().move(self.width/2, 0)

        self.gameRunning = True

    def touchedDown(self, old_lander_box, new_lander_box):
       return segment_intersects_polyline((old_lander_box.center, new_lander_box.center), self.terrain_segments)

    def main(self):
        while self.gameRunning:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()

            time.sleep(0.05)

            # KEYBOARD CHECKS
            up_is_pressed =  pygame.key.get_pressed()[pygame.K_UP]
            right_is_pressed =  pygame.key.get_pressed()[pygame.K_RIGHT]
            left_is_pressed =  pygame.key.get_pressed()[pygame.K_LEFT]

            # VELOCITY ADJUSTMENT
            original_fall_speed = self.speed[1]
            original_lateral_speed = self.speed[0]
            if up_is_pressed:
                self.speed[1] = original_fall_speed - 0.5
            else:
                self.speed[1] = original_fall_speed + 0.5

            if right_is_pressed:
                self.speed[0] = original_lateral_speed + 0.1
            if left_is_pressed:
                self.speed[0] = original_lateral_speed - 0.1

            # MOVE THE SHIP!
            old_lander_box = self.lander_box
            new_lander_box = old_lander_box.move(self.speed)

            # Yuck, update state of object
            self.lander_box = new_lander_box

            # (RE-)-DRAWING THE WORLD
            self.screen.fill(self.darkblue)
            self.screen.blit(self.lander_sprite, self.lander_box)
            pygame.draw.lines(self.screen, self.yellow, False, self.terrain_points)
            pygame.display.flip()
            self.gameRunning = not self.touchedDown(old_lander_box, new_lander_box)

if __name__ == '__main__':
    Game().main()
