import pygame
import math
import time
pygame.init()
# Создание окна
width_window = 1200
height_window = 1000


screen = pygame.display.set_mode((width_window, height_window))
image = pygame.image.load('/home/tim/Desktop/Python/image.png')
# Контроль FPS
clock = pygame.time.Clock()
FPS = 120
# Игровые переменные
running = True

# Plane
speed = 20
heading = 50
angle = 10
Radius = 0


x = width_window / 2
y = height_window / 2
width_plane = 21
height_plane = 10

x_point = 0
y_point = 0

x_point2 = 0
y_point2 = 0

x1 = 0
y1 = 0
x_new = 0
y_new = 0

prev_loc = []

tmr = time.time() * 1000
# Игровой цикл
while running:
    clock.tick(FPS)
    

    if height_window - y <= height_plane or y <= 0:
        y = height_window / 2
        x = width_window / 2
    if width_window - x <= width_plane or x <= 0:
        x = width_window / 2
        y = height_window / 2
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pos = pygame.mouse.get_pos()
                x_point = pos[0]
                y_point = pos[1]
            if event.button == 2:
                pos = pygame.mouse.get_pos()
                x_point2 = pos[0]
                y_point2 = pos[1]
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                     angle -= 1
                if event.key == pygame.K_d:
                     angle += 1
                if event.key == pygame.K_w:
                     speed += 1
                if event.key == pygame.K_s:
                     speed -= 1
    if(angle >= 45):
         angle = 45 
    if(angle <= -45):
         angle = 45 

    if(speed >= 30):
         speed = 30 
    if(speed <=  0):
         speed = 0 
         
    if(angle != 0):
        Radius = (speed * speed) / (9.81 * math.tan(math.radians(angle)))
    else:
         Radius = 0
    if(time.time()*1000 - tmr >= 100):
        if(Radius != 0):
            heading += math.degrees(speed / Radius)

        x1 = Radius * math.cos(math.radians(heading))
        y1 = Radius * math.sin(math.radians(heading))
        
        
        
        x_new = x1 * math.cos(math.radians(90)) - y1 * math.sin(math.radians(90))
        y_new = x1 * math.sin(math.radians(90)) + y1 * math.cos(math.radians(90))
        print(angle, " ", speed," ", Radius)

        x += speed * math.cos(math.radians(heading))
        y += speed * math.sin(math.radians(heading))

        
        tmr = time.time() * 1000

    screen.fill((0, 0, 0))
    pygame.draw.circle(screen, (255, 255, 0), (x_point, y_point), 4)
    pygame.draw.circle(screen, (255, 255, 0), (x_point2, y_point2), 4)
    # pygame.draw.line(screen, (0, 255, 0), (x, y), (x + x1, y + y1), 3)
    pygame.draw.line(screen, (0, 255, 100), (x , y), (x + x_new, y + y_new), 3)
    pygame.draw.circle(screen, (255, 0, 0), ((x + x_new, y + y_new)), 5)
    pygame.draw.line(screen, (255, 20, 0), (x_point2, y_point2), (x_point, y_point), 3)

    image_rot = pygame.transform.rotate(image, -heading)
    screen.blit(image_rot, (x - width_plane / 2 , y - height_plane / 2))
    #pygame.draw.rect(screen, (255, 255, 255), (x - width_plane / 2 , y - height_plane / 2, width_plane, height_plane),)
    for i in prev_loc:
         pygame.draw.circle(screen, (55, 55, 55), (i[0], i[1]), 1)
    prev_loc.append([x, y])
  
    pygame.display.flip()
pygame.quit()