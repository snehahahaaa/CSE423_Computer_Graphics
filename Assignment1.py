#Task_1

from OpenGL.GL import *     
from OpenGL.GLUT import *   
from OpenGL.GLU import *    
import random

WINDOW_WIDTH, WINDOW_HEIGHT = 1000, 1000

B = 0.0
b_target = 0.0
rains = []
speed = 2
wind = 0.0 
w_target = 0.0 
w_step = 0.1
w_max = 3.2
angle = 5.0


def sky():
    glColor3f(1.0*b_target, 1.0*b_target, 1.0*b_target)
    glBegin(GL_TRIANGLES)
    glVertex2f(0,650)
    glVertex2f(1000,650)
    glVertex2f(1000,1000)
    glVertex2f(0,650)
    glVertex2f(1000,1000)
    glVertex2f(0,1000)
    glEnd()

def house():
    glBegin(GL_TRIANGLES)

    glColor3f(0.4, 0.0, 1.0)
    glVertex2f(300, 530)
    glVertex2f(700, 530)
    glVertex2f(500, 670)
    glEnd()

    glBegin(GL_TRIANGLES)
    glColor3f(1.0, 1.0, 1.0)
    glVertex2f(320, 530)
    glVertex2f(320, 400)
    glVertex2f(680, 400)
    glVertex2f(320, 530)
    glVertex2f(680, 530)
    glVertex2f(680, 400)
    glEnd()
    
    glBegin(GL_TRIANGLES)
    glColor3f(0.0, 0.8, 1.0)
    glVertex2f(460, 500)
    glVertex2f(540, 400)
    glVertex2f(460, 400)
    glVertex2f(460, 500)
    glVertex2f(540, 500)
    glVertex2f(540, 400)
    glEnd()
    
    glBegin(GL_TRIANGLES)
    glColor3f(0.0, 0.8, 1.0)
    glVertex2f(580, 500)
    glVertex2f(630, 450)
    glVertex2f(580, 450)
    glVertex2f(580, 500)
    glVertex2f(630, 450)
    glVertex2f(630, 500)   
    glVertex2f(370, 500)
    glVertex2f(370, 450)
    glVertex2f(420, 450)
    glVertex2f(420, 450)
    glVertex2f(420, 500)
    glVertex2f(370, 500)
    glEnd()

def soil():
    glBegin(GL_TRIANGLES)
    glColor3f(0.4, 0.25, 0.1)
    glVertex2f(0, 650)
    glVertex2f(0, 0)
    glVertex2f(1000, 0)

    glVertex2f(1000, 0)
    glVertex2f(0, 650)
    glVertex2f(1000, 650)
    glEnd()

def trees():
    x = 510
    y = 620
    glBegin(GL_TRIANGLES)
    for i in range(0, 1000, 80):
        glColor3f(0.0, 1.0, 0.0)
        glVertex2f(i, x)
        glVertex2f(i+40, y)
        glColor3f(0.0, 0.5, 0.0)
        glVertex2f(i+80, x)
    glEnd()


def house_edit():
    glColor3f(0.0, 0.0, 0.0)
    glPointSize(5)         
    glBegin(GL_POINTS)      
    glVertex2f(520, 450) 
    glEnd() 
    
    glLineWidth(2)
    glBegin(GL_LINES)
    glColor3f(0.0, 0.0, 0.0) 
    glVertex2f(605, 450) 
    glVertex2f(605, 500) 
    glVertex2f(580, 475) 
    glVertex2f(630, 475)
    glVertex2f(370, 475) 
    glVertex2f(420, 475) 
    glVertex2f(395, 450) 
    glVertex2f(395, 500)     
    glEnd()  

def make_rains():
    global rains
    rains = []
    max = 360
    for i in range(max):
        a = random.randint(0, 1000)
        b = random.randint(0, 1000)
        rain_len = random.randint(12, 30)
        blue = (random.random() < 0.50)
        rains.append([a, b, rain_len, blue])

def rain_draw():
    glLineWidth(1)
    glBegin(GL_LINES)
    for a, b, rain_len, blue in rains:
        if blue:
            glColor3f(0.0, 0.0, 1.0)  
        else:
            glColor3f(1.0, 1.0, 1.0)
        
        glVertex2f(a,b)
        glVertex2f(a + wind*angle, b-rain_len)

    glEnd()

def keyboard_listener(key, a, b):
    global b_target
    if key == b'p':
        b_target = 1.0
    elif key ==  b'k':
        b_target = 0.0

def special_key_listener(key, a, b):
    global w_target
    if key == GLUT_KEY_LEFT:
        w_target = -w_max
    elif key == GLUT_KEY_RIGHT:
        w_target = w_max
    elif key == GLUT_KEY_DOWN:
        w_target = 0.0


def animate():
    global B, wind
      
    B += (b_target - B) * 0.0009

    wind += (w_target - wind) * w_step

    for i in rains:
        i[1] -= speed  

        if i[1] < 0:
            i[0] = random.randint(0, 1000)
            i[1] = 1000 + random.randint(0, 200)
            i[2] = random.randint(12, 30)
            i[3] = (random.random() < 0.50)

    glutPostRedisplay()


def setup_projection():
    glViewport(0, 0, 1000, 1000)     
    glMatrixMode(GL_PROJECTION)   
    glLoadIdentity()               
    glOrtho(0.0, 1000, 0.0, 1000, 0.0, 1.0)  
    glMatrixMode(GL_MODELVIEW) 


def display():
    glClear(GL_COLOR_BUFFER_BIT)  
    glLoadIdentity()                                   
    setup_projection()  
    sky()                               
    glColor3f(1.0, 0.0, 1.0)                            
    soil()
    trees() 
    house()    
    house_edit()  
    rain_draw()                          
    glutSwapBuffers()
 

def main():
    glutInit()                              
    glutInitDisplayMode(GLUT_RGBA)          
    glutInitWindowSize(1000, 1000)            
    glutInitWindowPosition(0, 0)           
    glutCreateWindow(b"Assignment1 Task1")   
    make_rains()
    glutSpecialFunc(special_key_listener)
    glutKeyboardFunc(keyboard_listener)
    glutIdleFunc(animate)
    glutDisplayFunc(display)                 
    glutMainLoop() 
        

if __name__ == "__main__":
    main()




#Task_2

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

WINDOW_WIDTH, WINDOW_HEIGHT = 1000, 800

balls = []
ball_speed = 0.3
size = 6

blink = False
count = 0

stop = False


def convert_coordinate(X, Y):
    a = float(X)
    b = float(WINDOW_HEIGHT - Y)
    return a, b


def init():
    glClearColor(0, 0, 0, 1)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT)
    glMatrixMode(GL_MODELVIEW)



def display():
    global WINDOW_WIDTH, WINDOW_HEIGHT
    WINDOW_WIDTH, WINDOW_HEIGHT = max(1, WINDOW_WIDTH), max(1, WINDOW_HEIGHT)

    glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    glPointSize(size)
    glBegin(GL_POINTS)

    for x, y, dx, dy, r, g, b in balls:
        if blink == True and (count % 500 < 250):
            glColor3f(0, 0, 0)
        else:
            glColor3f(r, g, b)

        glVertex2f(x, y)
    
    glEnd()

    glutSwapBuffers()

def ball_update():
    global count

    if not stop:
        for i in balls:
            i[0] += i[2] * ball_speed
            i[1] += i[3] * ball_speed

            if i[0] <= 0 or i[0] >= WINDOW_WIDTH:
                i[2] *= -1

            if i[1] <= 0 or i[1] >= WINDOW_HEIGHT:
                i[3] *= -1

        if blink:
            count += 1

    glutPostRedisplay()

def mouse_listener(button, state, x, y):
    global blink

    if state != GLUT_DOWN:
        return
    if stop:
        return

    if button == GLUT_RIGHT_BUTTON:
        x, y = convert_coordinate(x, y)
        dx = random.choice([-1, 1])
        dy = random.choice([-1, 1])
        r = random.random()
        g = random.random()
        b = random.random()
        balls.append([x, y, dx, dy, r, g, b])

    elif button == GLUT_LEFT_BUTTON:
        blink = not blink


def special_key_listener(key, x, y):
    global ball_speed

    if stop:
        return

    if key == GLUT_KEY_UP:
        ball_speed += 0.5
    elif key == GLUT_KEY_DOWN:
        ball_speed = max(0.1, ball_speed - 0.5)


def keyboard_listener(key, x, y):
    global stop
    if key == b' ':
        stop = not stop

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutCreateWindow(b"Assignment1 Task2")

    init()

    glutDisplayFunc(display)
    glutMouseFunc(mouse_listener)
    glutSpecialFunc(special_key_listener)
    glutKeyboardFunc(keyboard_listener)
    glutIdleFunc(ball_update)  

    glutMainLoop()


if __name__ == "__main__":
    main()