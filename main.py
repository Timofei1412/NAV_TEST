import pygame
import math
import time
pygame.init()
# Создание окна
width_window = 1200
height_window = 1000

SIZE_OF_TRAJ = 100


screen = pygame.display.set_mode((width_window, height_window))
image = pygame.image.load('image.png')
text = pygame.font.SysFont('calibri', 15)
# Контроль FPS
clock = pygame.time.Clock()
FPS = 120
# Игровые переменные
running = True

# Plane
speed = 1
heading = 0
angle = 0
Radius = 0


x = 20
y = 100
width_plane = 21
height_plane = 10

x_point = 0
y_point = 0

x_point2 = 1
y_point2 = 1

x1 = 0
y1 = 0
x_new = 0
y_new = 0

prev_loc = []
prev_loc_ptr = -1

target_heading = 0

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
            if event.button == 3:
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
                if event.key == pygame.K_q:
                     prev_loc = []
                     prev_loc_ptr = -1
                if event.key == pygame.K_r:
                     target_heading += 10
                if event.key == pygame.K_f:
                     target_heading -= 10
                target_heading %= 360
                
    
    '''
    pid on dif heading

    p = error * kp
    i += error * dt
    
    '''
    
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
    if(time.time()*1000 - tmr >= 50):
        if(Radius != 0):
            heading += math.degrees(speed / Radius)

        x1 = Radius * math.cos(math.radians(heading))
        y1 = Radius * math.sin(math.radians(heading))
        
        x_new = x1 * math.cos(math.radians(90)) - y1 * math.sin(math.radians(90))
        y_new = x1 * math.sin(math.radians(90)) + y1 * math.cos(math.radians(90))
    

        x += speed * math.cos(math.radians(heading))
        y += speed * math.sin(math.radians(heading))

     #    heading %= 360
     #    error =  (target_heading - heading) % 360
     #    pid_error = error * 0.007
     #    angle += pid_error
     #    print(heading, " ", target_heading," ", error, " ", pid_error)

        tmr = time.time() * 1000



    m = (y_point2 - y_point) / (x_point2 - x_point)
    b = y_point - m * x_point


    #----ОТРИСОВКА-----------------------------------------------------------------------------------------------------------------------
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

            
    if(prev_loc_ptr == -1 and len(prev_loc) < SIZE_OF_TRAJ):
        prev_loc.append((x, y))
    elif(prev_loc_ptr == -1 and len(prev_loc) >= SIZE_OF_TRAJ):
            prev_loc_ptr = 0

    if(len(prev_loc) == SIZE_OF_TRAJ and prev_loc_ptr != -1) :
            prev_loc[prev_loc_ptr] = (x, y)
            prev_loc_ptr += 1
    if(prev_loc_ptr == SIZE_OF_TRAJ):
            prev_loc_ptr = 0


    formula  = text.render("y = " +  str(m) + "x + " + str(b), True, (255, 0, 0))
    screen.blit(formula, (10,0))
    pygame.display.flip()
pygame.quit()