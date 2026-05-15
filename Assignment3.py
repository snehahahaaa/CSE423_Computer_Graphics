from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random

cam_pos = (0, 15, 18)
fovY = 60 
grid_len = 10
random_var = 423

arena_limit = 10.0
player_y = 1.0
enemy_count = 5
enemy_speed = 0.001

player_pos = [0.0, player_y, 0.0]
gun_angle = 0.0
B = []
E = []
score = 0
lives = 5
missed_bullets = 0
cheat = False
first_person = False
game_over = False
auto_follow = False

cam_height = 7.5
cam_angle = 0.0
cam_dist = 15.5

def boundary(v, lo, hi):
    return max(lo, min(hi, v))

def respawn_enemy():
    while True:
        xx = random.uniform(-9, 9)
        zz = random.uniform(-9, 9)
        if math.hypot(xx - player_pos[0], zz - player_pos[2]) > 3.0:
            return {'pos': [xx, player_y, zz],'scale': random.uniform(0.9, 1.1),'scale_dir': random.choice([-1.0, 1.0]),}
        
def restart_game():
    global player_pos, gun_angle, B, E, score, lives, missed_bullets, enemy_count, cheat, first_person, game_over, auto_follow, cam_height, cam_angle, cam_dist, cam_pos

    player_pos = [0.0, player_y, 0.0]
    gun_angle = 0.0
    B = []
    E = []
    for i in range(enemy_count):
       E.append(respawn_enemy())
    score = 0
    lives = 5
    missed_bullets = 0
    cheat= False
    first_person = False
    game_over = False
    auto_follow = False

    cam_height = 7.5
    cam_angle = 0.0
    cam_dist = 15.5
    cam_pos = (0, 15, 18)
    
def draw_text(x, y, text, font= GLUT_BITMAP_HELVETICA_18):
    glColor3f(1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity() 
    gluOrtho2D(0, 1000, 0, 800)
   

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    
def draw_player():
    if first_person == True and game_over == False:
        return

    glPushMatrix()
    glTranslatef(player_pos[0], player_pos[1], player_pos[2])
    glRotatef(gun_angle, 0, 1, 0)

    if game_over:
      glTranslatef(0, -0.15, 0)
      glRotatef(90, 0, 0, 1)

    glColor3f(0.45, 0.52, 0.25)
    glPushMatrix()
    glScalef(0.55, 1.05, 0.35)
    glutSolidCube(1.0)
    glPopMatrix()

    glColor3f(0.85, 0.85, 0.80)
    glPushMatrix()
    glTranslatef(0.0, 0.10, 0.18)
    glScalef(0.18, 0.34, 0.08)
    gluSphere(gluNewQuadric(), 1.0, 20, 20)
    glPopMatrix()

    glColor3f(0.0, 0.0, 0.0)
    glPushMatrix()
    glTranslatef(0.0, 0.85, 0.0)
    gluSphere(gluNewQuadric(), 0.24, 20, 20)
    glPopMatrix()

    glColor3f(0.95, 0.80, 0.65)
    glPushMatrix()
    glTranslatef(-0.34, 0.22, 0.0)
    glRotatef(90, 0, 0, 1)
    gluCylinder(gluNewQuadric(), 0.10, 0.10, 0.22, 16, 16)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-0.28, 0.22, 0.0)
    gluSphere(gluNewQuadric(), 0.10, 16, 16)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0.34, 0.22, 0.0)
    glRotatef(-90, 0, 0, 1)
    gluCylinder(gluNewQuadric(), 0.10, 0.10, 0.22, 16, 16)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0.28, 0.22, 0.0)
    gluSphere(gluNewQuadric(), 0.10, 16, 16)
    glPopMatrix()

    glColor3f(0.88, 0.82, 0.72)
    glPushMatrix()
    glTranslatef(0.30, 0.18, 0.0)
    glScalef(0.45, 0.10, 0.12)
    glutSolidCube(1.0)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0.52, 0.18, 0.0)
    glRotatef(90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 0.08, 0.01, 0.48, 12, 12)
    glPopMatrix()

    glColor3f(0.05, 0.0, 0.1)
    glPushMatrix()
    glTranslatef(-0.14, -0.55, 0.0)
    glRotatef(-90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 0.09, 0.04, 0.45, 12, 12)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0.14, -0.55, 0.0)
    glRotatef(-90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 0.09, 0.04, 0.45, 12, 12)
    glPopMatrix()

    glPopMatrix()


    
def first_person_view():
    if first_person== False or game_over== True:
        return

    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluPerspective(fovY, 1.25, 0.1, 100.0)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glTranslatef(0.0, -0.95, -1.75)

    glColor3f(0.92, 0.82, 0.70)

    glPushMatrix()
    glTranslatef(-0.18, -0.08, 0.02)
    glRotatef(-28, 0, 0, 1)
    glRotatef(-80, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 0.045, 0.04, 0.34, 14, 14)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0.18, -0.08, 0.02)
    glRotatef(28, 0, 0, 1)
    glRotatef(-80, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 0.045, 0.04, 0.34, 14, 14)
    glPopMatrix()

    glColor3f(0.75, 0.75, 0.78)
    glPushMatrix()
    glTranslatef(0.0, 0.00, -0.16)
    glRotatef(-90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 0.07, 0.04, 0.44, 18, 18)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0.0, -0.03, -0.02)
    glScalef(0.14, 0.12, 0.16)
    glutSolidCube(1.0)
    glPopMatrix()

    glColor3f(0.15, 0.15, 0.15)
    glPushMatrix()
    glTranslatef(0.0, 0.06, -0.14)
    glScalef(0.025, 0.06, 0.08)
    glutSolidCube(1.0)
    glPopMatrix()

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_enemy(pos, scale):
    glPushMatrix()
    glTranslatef(*pos)
    glScalef(scale, scale, scale)

    glColor3f(1.0, 0.0, 0.0)
    gluSphere(gluNewQuadric(), 0.48, 18, 18)

    glColor3f(0.05, 0.05, 0.05)
    glPushMatrix()
    glTranslatef(0, 0.62, 0)
    gluSphere(gluNewQuadric(), 0.28, 18, 18)
    glPopMatrix()

    glPopMatrix()

def draw_bullet(pos):
    glPushMatrix()
    glTranslatef(*pos)
    glColor3f(1.0, 1.0, 0.0)
    glutSolidCube(0.18)
    glPopMatrix()

def nearest_enemy():
    near_enemy = None
    best_dist = 1e9

    for i in E:
        dx = i['pos'][0] - player_pos[0]
        dz = i['pos'][2] - player_pos[2]
        d = math.hypot(dx, dz)
        if d < best_dist:
            best_dist = d
            near_enemy = i

    if near_enemy is None:
        return None

    dx = near_enemy['pos'][0] - player_pos[0]
    dz = near_enemy['pos'][2] - player_pos[2]
    return math.degrees(math.atan2(dx, dz))


def fire_bullet():
    if game_over== True:
        return
    if len(B) >= 1:
        return
     
    speed = 0.1
    rad = math.radians(gun_angle)
    B.append({'pos': [player_pos[0], player_pos[1] + 0.5, player_pos[2]],'vel': [math.sin(rad) * speed, 0.0, math.cos(rad) * speed]})
    
def keep_player_inside():
    m = 1.0
    player_pos[0] = boundary(player_pos[0], -arena_limit + m, arena_limit - m)
    player_pos[2] = boundary(player_pos[2], -arena_limit + m, arena_limit - m)

def angle_diff(a, b):
    return (a - b + 180) % 360 - 180

def whole_game_logic():
    global lives, missed_bullets, score, gun_angle, game_over, first_person, enemy_speed

    if game_over == True:
        return

    if cheat:
        if auto_follow == True:
            target_angle = nearest_enemy()
            if target_angle is not None:
                gun_angle = target_angle
                target_in_front = False
                for enemy in E:
                    dx = enemy['pos'][0] - player_pos[0]
                    dz = enemy['pos'][2] - player_pos[2]
                    enemy_angle = math.degrees(math.atan2(dx, dz))
                    if abs(angle_diff(enemy_angle, gun_angle)) < 5:
                        target_in_front = True
                        break
                if target_in_front:
                    fire_bullet()
        else:
            gun_angle = (gun_angle + 0.5) % 360
            for enemy in E:
                dx = enemy['pos'][0] - player_pos[0]
                dz = enemy['pos'][2] - player_pos[2]
                enemy_angle = math.degrees(math.atan2(dx, dz))
                if abs(angle_diff(enemy_angle, gun_angle)) < 4:
                    fire_bullet()
                    break

    for enemy in E:
        dx = player_pos[0] - enemy['pos'][0]
        dz = player_pos[2] - enemy['pos'][2]
        dist = math.hypot(dx, dz)

        if dist > 0.01:
            enemy['pos'][0] += dx / dist * enemy_speed
            enemy['pos'][2] += dz / dist * enemy_speed

        enemy['scale'] += enemy['scale_dir'] * 0.015
        if enemy['scale'] > 1.2 or enemy['scale'] < 0.8:
            enemy['scale_dir'] *= -1

        if dist < 0.85:
            lives -= 1
            enemy.update(respawn_enemy())
            if lives <= 0:
                game_over = True
                first_person = False

    for bul in B[:]:
        bul['pos'][0] += bul['vel'][0]
        bul['pos'][2] += bul['vel'][2]

        if abs(bul['pos'][0]) > arena_limit or abs(bul['pos'][2]) > arena_limit:
            B.remove(bul)
            missed_bullets += 1
            if missed_bullets >= 10:
                game_over = True
                first_person = False
            continue

        for e in E:
            dx = bul['pos'][0] - e['pos'][0]
            dz = bul['pos'][2] - e['pos'][2]
            if math.hypot(dx, dz) < 0.78:
                if bul in B:
                    B.remove(bul)
                score += 10
                e.update(respawn_enemy())
                break
            
def draw_shapes():
    
    for ix in range(-10, 10):
        for iz in range(-10, 10):
            if (ix + iz) % 2 == 0:
                glColor3f(0.85, 0.85, 0.85)
            else:
                glColor3f(0.55, 0.35, 0.85)

            glBegin(GL_QUADS)
            glVertex3f(ix, 0, iz)
            glVertex3f(ix + 1, 0, iz)
            glVertex3f(ix + 1, 0, iz + 1)
            glVertex3f(ix, 0, iz + 1)
            glEnd()

    wall_h = 2.3

    glColor3f(0.0, 0.0, 1.0)
    glPushMatrix()
    glTranslatef(-10.0, wall_h / 2, 0)
    glScalef(0.15, wall_h, 20.0)
    glutSolidCube(1)
    glPopMatrix()

    glColor3f(0.0, 1.0, 0.0)
    glPushMatrix()
    glTranslatef(10.0, wall_h / 2, 0)
    glScalef(0.15, wall_h, 20.0)
    glutSolidCube(1)
    glPopMatrix()

    glColor3f(0.0, 1.0, 1.0)
    glPushMatrix()
    glTranslatef(0, wall_h / 2, -10.0)
    glScalef(20.0, wall_h, 0.15)
    glutSolidCube(1)
    glPopMatrix()

    glColor3f(1.0, 1.0, 1.0)
    glPushMatrix()
    glTranslatef(0, wall_h / 2, 10.0)
    glScalef(20.0, wall_h, 0.15)
    glutSolidCube(1)
    glPopMatrix()

    draw_player()

    if not game_over:
        for e in E:
            draw_enemy(e['pos'], e['scale'])

        for bul in B:
            draw_bullet(bul['pos'])

        first_person_view()

def keyboardListener(key, x, y):
    global gun_angle, cheat, auto_follow
     
    key = key.decode('utf-8').lower()
    if game_over == True and key != 'r':
      return
    rad = math.radians(gun_angle)
    speed = 0.2

    if key == 'w':
        player_pos[0] += math.sin(rad) * speed
        player_pos[2] += math.cos(rad) * speed
        keep_player_inside()

    elif key == 's':
        player_pos[0] -= math.sin(rad) * speed
        player_pos[2] -= math.cos(rad) * speed
        keep_player_inside()

    elif key == 'a':
        gun_angle -= 3.0

    elif key == 'd':
        gun_angle += 3.0

    elif key == 'c':
        cheat = not cheat
        if not cheat:
            auto_follow = False

    elif key == 'v':
        if cheat:
            auto_follow = not auto_follow

    elif key == 'r':
        restart_game()

    glutPostRedisplay()

def specialKeyListener(key, x, y):
    
    global cam_height, cam_angle, cam_pos

    if key == GLUT_KEY_UP:
        cam_height += 0.5

    elif key == GLUT_KEY_DOWN:
        cam_height = max(1.0, cam_height - 0.5)

    elif key == GLUT_KEY_LEFT:
        cam_angle -= 3.0

    elif key == GLUT_KEY_RIGHT:
        cam_angle += 3.0

    cam_x = cam_dist * math.sin(math.radians(cam_angle))
    cam_z = cam_dist * math.cos(math.radians(cam_angle))
    cam_pos = (cam_x, cam_height, cam_z)

    glutPostRedisplay()
    
def mouseListener(button, state, x, y):
    global first_person

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        fire_bullet()

    elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        first_person = not first_person

    glutPostRedisplay()
    
def setupCamera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, 1.25, 0.1, 1500)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    if game_over:
        gluLookAt(0, 18, 24, 0, 0.8, 0, 0, 1, 0)

    elif first_person:
        follow_angle = gun_angle

        if cheat and auto_follow:
            target = nearest_enemy()
            if target is not None:
                follow_angle = target

        dx = math.sin(math.radians(follow_angle))
        dz = math.cos(math.radians(follow_angle))

        eye_x = player_pos[0] - dx * 0.35
        eye_y = player_pos[1] + 1.1
        eye_z = player_pos[2] - dz * 0.35

        c_x = player_pos[0] + dx * 4.0
        c_y = player_pos[1] + 1.0
        c_z = player_pos[2] + dz * 4.0

        gluLookAt(eye_x, eye_y, eye_z,c_x, c_y, c_z,0, 1, 0)
    else:
        cam_x, cam_y, cam_z = cam_pos
        gluLookAt(cam_x, cam_y, cam_z,0, 0.8, 0,0, 1, 0)
        
def idle():
    whole_game_logic()
    glutPostRedisplay()


def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 800)

    setupCamera()
    draw_shapes()

    if game_over:
        draw_text(70, 700, f"Game is Over. Your Score is {score}.", font= GLUT_BITMAP_HELVETICA_18)
        draw_text(70, 660, 'Press "R" to RESTART the Game.', font= GLUT_BITMAP_HELVETICA_18)
    else:
        draw_text(10, 770, f"Player Life Remaining: {lives}")
        draw_text(10, 740, f"Game Score: {score}")
        draw_text(10, 710, f"Player Bullet Missed: {missed_bullets}")

        if cheat:
            draw_text(10, 680, "Cheat Mode: ON")

        if cheat and auto_follow and first_person:
            draw_text(10, 650, "Auto Follow: ON (First Person View)")
        elif cheat and auto_follow:
            draw_text(10, 650, "Auto Follow: ON (Switch to First Person to see it)")

    glutSwapBuffers()

def init():
    restart_game()
    
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 800)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"Bullet Frenzy Game")

    init()

    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)

    glutMainLoop()


if __name__ == "__main__":
    main()
