import sys, pygame, time
from geometry import calculateIntersectPoint
pygame.init()

size = width, height = 500, 500
speed = [0, 0]
black = pygame.Color('black')
yellow = pygame.Color('yellow')

terrain_points = ((0,height),(100,height-20), (width, height-10))
terrain_segments = zip(terrain_points, terrain_points[1:])

screen = pygame.display.set_mode(size)

lander_sprite = pygame.image.load("lander.gif")
lander_box = lander_sprite.get_rect()

gameRunning = True

def intersects_polyline(box, polyline):
    sides = [(box.topleft, box.topright), (box.topright, box.bottomright), (box.bottomright, box.bottomleft), (box.bottomleft, box.topleft)]
    for side in sides:
        for segment in polyline:
            sideStart,sideEnd = side
            segmentStart, segmentEnd = segment
            if calculateIntersectPoint(sideStart, sideEnd, segmentStart, segmentEnd) is not None:
                return True
    return False

def touchedDown(box, polyline):
    return intersects_polyline(box, polyline) or (box.top > height)

while gameRunning:
    time.sleep(0.05)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    up_is_pressed =  pygame.key.get_pressed()[pygame.K_UP]
    right_is_pressed =  pygame.key.get_pressed()[pygame.K_RIGHT]
    left_is_pressed =  pygame.key.get_pressed()[pygame.K_LEFT]

    original_fall_speed = speed[1]
    original_lateral_speed = speed[0]

    if up_is_pressed:
        speed[1] = original_fall_speed - 0.5
    else:
        speed[1] = original_fall_speed + 0.5

    if right_is_pressed:
        speed[0] = original_lateral_speed + 0.1
    if left_is_pressed:
        speed[0] = original_lateral_speed - 0.1


    lander_box = lander_box.move(speed)

    screen.fill(black)
    screen.blit(lander_sprite, lander_box)
    pygame.draw.lines(screen, yellow, False, terrain_points)
    pygame.display.flip()
    gameRunning = not touchedDown(lander_box, terrain_segments)
