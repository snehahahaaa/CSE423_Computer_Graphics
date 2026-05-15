from OpenGL.GL import *
from OpenGL.GLUT import *
import random
import time

WINDOW_WIDTH , WINDOW_HEIGHT = 1200, 900
score = 0
game_over = False
game_pause = False
cheat_mode = False
time_var = 0.0

cat_x = WINDOW_WIDTH//2
cat_y = 40
cat_width = 180
cat_height = 40
cat_speed = 400.0

D_x, D_y = 0, 0
D_half =18
D_speed = 150.0
D_acceleration = 8.0
D_color = (1.0, 1.0, 0.0)

button_y = WINDOW_HEIGHT -40
restart = {"x": 65, "y": button_y, "size": 25}
pause = {"x": WINDOW_WIDTH // 2, "y": button_y, "size": 25}
exit = {"x": WINDOW_WIDTH - 65, "y": button_y, "size": 25}
button_click = 24

def convert_coordinate(x, y):
    return x, WINDOW_HEIGHT - y

def bright_color():
    return (random.uniform(0.5, 1.0), random.uniform(0.5, 1.0),random.uniform(0.5, 1.0))

def catcher_inside():
    global cat_x
    half_w = cat_width / 2

    if cat_x - half_w < 0:
        cat_x = half_w
    if cat_x + half_w > WINDOW_WIDTH:
        cat_x = WINDOW_WIDTH - half_w

def collision():
    cat_left = cat_x - cat_width / 2
    cat_right = cat_x + cat_width / 2
    cat_bottom = cat_y - cat_height / 2
    cat_top = cat_y + cat_height / 2
    D_left = D_x - D_half
    D_right = D_x + D_half
    D_bottom = D_y - D_half
    D_top = D_y + D_half

    return (cat_left < D_right and cat_right > D_left and cat_bottom < D_top and cat_top > D_bottom)

def point_drawing(points, color):
    glColor3f(color[0], color[1], color[2])
    glBegin(GL_POINTS)
    for a, b in points:
        glVertex2f(a, b)
    glEnd()

def find_zone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    if abs(dx) >= abs(dy):
        if dx >= 0 and dy >= 0:
            return 0
        elif dx < 0 and dy >= 0:
            return 3
        elif dx < 0 and dy < 0:
            return 4
        else:
            return 7
    else:
        if dx >= 0 and dy >= 0:
            return 1
        elif dx < 0 and dy >= 0:
            return 2
        elif dx < 0 and dy < 0:
            return 5
        else:
            return 6

def convert_to_zone_zero(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return y, -x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return -y, x
    else:
        return x, -y

def convert_from_zone_zero(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return -y, x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return y, -x
    else:
        return x, -y
    
def midpoint_line_points(x1, y1, x2, y2):
    zone = find_zone(x1, y1, x2, y2)

    x1, y1 = convert_to_zone_zero(x1, y1, zone)
    x2, y2 = convert_to_zone_zero(x2, y2, zone)

    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
    dx = x2 - x1
    dy = y2 - y1
    d = 2 * dy - dx
    E = 2 * dy
    NE = 2 * (dy - dx)
    x = x1
    y = y1
    points = []

    while x <= x2:
        a, b = convert_from_zone_zero(x, y, zone)
        points.append((a, b))

        if d > 0:
            d += NE
            y += 1
        else:
            d += E
        x += 1
    return points

def line_drawing(x1, y1, x2, y2, color):
    points = midpoint_line_points(int(round(x1)), int(round(y1)),int(round(x2)), int(round(y2)))
    point_drawing(points, color)

def diamond_drawing(p, q, half_size, color):
    top = (p, q + half_size)
    right = (p + half_size, q)
    bottom = (p, q - half_size)
    left = (p - half_size, q)
    line_drawing(top[0], top[1], right[0], right[1], color)
    line_drawing(right[0], right[1], bottom[0], bottom[1], color)
    line_drawing(bottom[0], bottom[1], left[0], left[1], color)
    line_drawing(left[0], left[1], top[0], top[1], color)

def catcher_drawing(p, q, width, height, color):
    left = p - width / 2
    right = p + width / 2
    top_y = q + height / 2
    bottom_y = q - height / 2
    top_left = (left, top_y)
    top_right = (right, top_y)
    bottom_left = (left + 20, bottom_y)
    bottom_right = (right - 20, bottom_y)

    line_drawing(bottom_left[0], bottom_left[1], bottom_right[0], bottom_right[1], color)   
    line_drawing(top_left[0], top_left[1], bottom_left[0], bottom_left[1], color)          
    line_drawing(bottom_right[0], bottom_right[1], top_right[0], top_right[1], color)       
    line_drawing(top_left[0], top_left[1], top_right[0], top_right[1], color)    
        
def restart_button():
    x = restart["x"]
    y = restart["y"]
    s = restart["size"]
    color = (0.0, 0.9, 1.0)

    line_drawing(x + s, y, x - s, y, color)
    line_drawing(x - s, y, x - 2, y + s, color)
    line_drawing(x - s, y, x - 2, y - s, color)

def pause_play_button():
    x = pause["x"]
    y = pause["y"]
    s = pause["size"]
    color = (1.0, 0.75, 0.0)

    if game_pause == True:
        line_drawing(x - s / 2, y - s, x - s / 2, y + s, color)
        line_drawing(x - s / 2, y + s, x + s, y, color)
        line_drawing(x + s, y, x - s / 2, y - s, color)
    else:
        line_drawing(x - 5, y - s, x - 5, y + s, color)
        line_drawing(x + 5, y - s, x + 5, y + s, color)

def exit_button():
    x = exit["x"]
    y = exit["y"]
    s = exit["size"]
    color = (1.0, 0.0, 0.0)
    line_drawing(x - s, y - s, x + s, y + s, color)
    line_drawing(x - s, y + s, x + s, y - s, color)

def diamond_reset():
    global D_x, D_y, D_color
    D_x = random.randint(80, WINDOW_WIDTH - 80)
    D_y = WINDOW_HEIGHT - 100
    D_color = bright_color()

def game_restart():
    global score, game_over, game_pause, cheat_mode
    global cat_x, D_speed, time_var

    score = 0
    game_over = False
    game_pause = False
    cheat_mode = False
    cat_x = WINDOW_WIDTH / 2
    D_speed = 180.0
    time_var = time.time()

    diamond_reset()
    print("Starting Over!")

def game_finish():
    global game_over
    game_over = True
    print("Game Over! Score:", score)

def game_update(dt):
    global D_y, D_speed, score, cat_x

    if game_over or game_pause:
        return
    if cheat_mode:
        if cat_x < D_x:
            cat_x += cat_speed * dt
            if cat_x > D_x:
                cat_x = D_x
        elif cat_x > D_x:
            cat_x -= cat_speed * dt
            if cat_x < D_x:
                cat_x = D_x

        catcher_inside()

    D_y -= D_speed * dt
    D_speed += D_acceleration * dt

    if collision():
        score += 1
        print("Score:", score)
        diamond_reset()
        return

    if D_y + D_half < 0:
        game_finish()

def keyboard_listener(key, x, y):
    global cheat_mode

    if key == b'c' or key == b'C':
        if game_over == False:
            cheat_mode = not cheat_mode
            if cheat_mode:
                print("Cheat Mode: ON")
            else:
                print("Cheat Mode: OFF")

def special_listener(key, x, y):
    global cat_x

    if game_over or game_pause or cheat_mode:
        return
    move_amount = 28

    if key == GLUT_KEY_LEFT:
        cat_x -= move_amount
        catcher_inside()

    elif key == GLUT_KEY_RIGHT:
        cat_x += move_amount
        catcher_inside()

def mouse_listener(button, state, x, y):
    global game_pause

    if button != GLUT_LEFT_BUTTON or state != GLUT_DOWN:
        return

    p, q = convert_coordinate(x, y)

    if (restart["x"] - button_click <= p <= restart["x"] + button_click and restart["y"] - button_click <= q <= restart["y"] + button_click):
        game_restart()
        return

    if (pause["x"] - button_click <= p <= pause["x"] + button_click and pause["y"] - button_click <= q <= pause["y"] + button_click):
        if game_over == False:
            game_pause = not game_pause
            print("Paused" if game_pause else "Resumed")
        return

    if (exit["x"] - button_click <= p <= exit["x"] + button_click and exit["y"] - button_click <= q <= exit["y"] + button_click):
        print("Goodbye! Score:", score)
        glutLeaveMainLoop()
    
def display():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)

    restart_button()
    pause_play_button()
    exit_button()
     
    if game_over == True:
        cat_color = (1.0, 0.0, 0.0) 
    else:
        cat_color = (1.0, 1.0, 1.0)
    catcher_drawing(cat_x, cat_y, cat_width, cat_height, cat_color)

    if game_over == False:
        diamond_drawing(D_x, D_y, D_half, D_color)

    glutSwapBuffers()

def animate():
    global time_var

    curr_time = time.time()
    dt = curr_time - time_var
    time_var = curr_time

    if dt > 0.03:
        dt = 0.03

    game_update(dt)
    glutPostRedisplay()

def init():
    glClearColor(0, 0, 0, 1)
    glPointSize(2)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT, 0, 1)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def main():
    global time_var

    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitWindowPosition(100, 50)
    glutCreateWindow(b"Assignment 02")

    init()
    game_restart()
    time_var = time.time()
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard_listener)
    glutSpecialFunc(special_listener)
    glutMouseFunc(mouse_listener)
    glutIdleFunc(animate)

    glutMainLoop()
if __name__ == "__main__":
    main()
