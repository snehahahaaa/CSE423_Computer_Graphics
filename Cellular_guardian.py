from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import time
import random

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800

T_Radius = 250
T_Length = 4200
T_Segments = 48
T_Rings = 110
F_Limit = 100.0
Sheild_time = 4.0
GLOBAL_QUAD = None

checker_offset = 0.0
scroll_speed = 210.0
flow_rotate = 0.0
flow_rotate_speed = 0.75
end_wave_score = 0

s_time = time.time()
l_time = time.time()

fever = 0.0
shield_time = 0.0
score = 0
boost_time = 0.0
game_over = False

P_x = 0.0
P_y = -35.0
P_z = -260.0
P_radius = 42.0
P_scale = 0.46
P_base_speed = 230.0
P_wobble = 0.0
P_wobble_decay = 2.8

first_person = False

cam_ht = 42.0
cam_dist = 110.0
cam_side_offset = 0.0
cam_angle_offset = 0.0

first_person_yaw = 0.0
first_person_pitch = 0.0

fovY = 50.0

rbc = []
blood_parts = []
immunity_picks = []

E = []
boss = None
E_spawn_time = 0.0
wave_num = 1
boss_spawn = False
E_defeated_in_wave = 0

speed_boost = []

class SpikeVirus:
    def __init__(self, d_speed):
        angle = random.uniform(0, 2 * math.pi)
        dist = random.uniform(10, T_Radius - 75)
        self.x = math.cos(angle) * dist
        self.y = math.sin(angle) * dist
        self.z = - T_Length

        self.speed = random.uniform(290, 380) * d_speed
        self.rot = random.uniform(0, 360)
        self.rot_vel = random.uniform(50, 110)
        self.radius = 34.0
        self.pulse_phase = random.uniform(0, 5)

    def draw(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)
        glRotatef(self.rot, 1, 0.5, 0.2)
        p = 1.0 + 0.08 * math.sin(curr_time() * 5 + self.pulse_phase)
        glScalef(p, p, p)

        glColor3f(0.75, 0.1, 0.25)

        gluSphere(GLOBAL_QUAD, 25, 20, 20)

        glColor3f(0.4, 0.0, 0.1)
        for i in range(8):
            glPushMatrix()
            glRotatef(i * 45, 1, 1, 0)
            gluCylinder(GLOBAL_QUAD, 4.5, 1.0, 48, 12, 12)
            glTranslatef(0, 0, 48)
            glColor3f(0.9, 0.2, 0.4)
            gluSphere(GLOBAL_QUAD, 6, 10, 10)
            glPopMatrix()


        glPopMatrix()

class CrystalVirus:
    def __init__(self, ds):
        angle = random.uniform(0, 2 * math.pi)
        dist = random.uniform(10, T_Radius - 80)
        self.x = math.cos(angle) * dist
        self.y = math.sin(angle) * dist
        self.z = -T_Length

        self.speed = random.uniform(170, 240) * ds
        self.rot = random.uniform(0, 360)
        self.rot_vel = random.uniform(30, 70)
        self.radius = 48.0

    def draw(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)
        glRotatef(self.rot, 0.3, 1, 0.5)

        cube_clr = [(0.4, 0.0, 0.8), (0.5, 0.1, 0.9), (0.3, 0.0, 0.6)]
        for i in range(3):
            glPushMatrix()
            glRotatef(i * 45, 1, 0, 1)
            glColor3f(*cube_clr[i])
            glutSolidCube(44)
            glPushMatrix()
            glColor3f(0.8, 0.5, 1.0)
            glScalef(0.55, 0.55, 0.55)
            glutSolidCube(44)
            glPopMatrix()
            glPopMatrix()
        glPopMatrix()

class Boss_virus:
    def __init__(self):
        self.x, self.y = 0, 0
        self.z = -T_Length
        self.speed = 240.0
        self.health = 3
        self.rot = 0
        self.radius = 130.0
        self.active = True

    def draw(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)
        glRotatef(self.rot, 0, 0, 1)
        glScalef(2.6, 2.6, 2.6)

        glColor3f(0.1, 0.6, 0.2)

        gluSphere(GLOBAL_QUAD, 42, 32, 32)
        for i in range(12):
            glPushMatrix()
            glRotatef(i * 30, 0.8, 0.4, 0.4)
            glColor3f(0.05, 0.3, 0.1)
            gluCylinder(GLOBAL_QUAD, 8, 3, 70, 15, 15)
            glTranslatef(0, 0, 70)
            glColor3f(0.3, 0.9, 0.4)
            gluSphere(GLOBAL_QUAD, 9, 12, 12)
            glPopMatrix()


        glPopMatrix()

def curr_time():
    return time.time() - s_time

def get_pulse_speed():

    base_beats_ps = 1.45
    fever_speed_boost = 1.0 + (fever / 100.0) * 2.8
    return 2 * math.pi * base_beats_ps * fever_speed_boost

def get_pulse_scale():
    t = curr_time()
    beat = math.sin(t * get_pulse_speed())
    beat = max(0.0, beat)

    pulse_strength = 0.022 + (fever / 100.0) * 0.050
    return 1.0 - pulse_strength * (beat ** 2)

def get_ring_radius(z_pos):
    return T_Radius * get_pulse_scale()

def clamp_player_tunnel():
    global P_x, P_y
    safe_rad = T_Radius - (P_radius * P_scale) - 18
    dist = math.sqrt(P_x * P_x + P_y * P_y)

    if dist > safe_rad:
        ang = math.atan2(P_y, P_x)
        P_x = math.cos(ang) * safe_rad
        P_y = math.sin(ang) * safe_rad

def text_draw(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1, 1, 1)

    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glRasterPos2f(x, y)

    for a in text:
        glutBitmapCharacter(font, ord(a))

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def sphere_draw(radius, slices=20, stacks=20):

    gluSphere(GLOBAL_QUAD, radius, slices, stacks)


def draw_rect_2d(x, y, w, h):
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + w, y)
    glVertex2f(x + w, y + h)
    glVertex2f(x, y + h)
    glEnd()

def draw_outline_2d(x, y, w, h, t=2):
    draw_rect_2d(x, y, w, t)
    draw_rect_2d(x, y + h - t, w, t)
    draw_rect_2d(x, y, t, h)
    draw_rect_2d(x + w - t, y, t, h)

def draw_flat_ring(inner_rad, outer_rad, segments=36):
    glBegin(GL_QUADS)
    for i in range(segments):
        a1 = 2 * math.pi * i / segments
        a2 = 2 * math.pi * (i + 1) / segments
        glVertex3f(math.cos(a1) * outer_rad, math.sin(a1) * outer_rad, 0)
        glVertex3f(math.cos(a2) * outer_rad, math.sin(a2) * outer_rad, 0)
        glVertex3f(math.cos(a2) * inner_rad, math.sin(a2) * inner_rad, 0)
        glVertex3f(math.cos(a1) * inner_rad, math.sin(a1) * inner_rad, 0)
    glEnd()

def draw_checker_tunnel():
    ring_step = T_Length / T_Rings
    angle_step = (2 * math.pi) / T_Segments

    glPushMatrix()
    for ring in range(T_Rings):
        z1 = -ring * ring_step + checker_offset
        z2 = z1 - ring_step

        r1 = get_ring_radius(z1)
        r2 = get_ring_radius(z2)

        depth = ring / float(T_Rings)

        spiral1 = flow_rotate + abs(z1) * 0.0016
        spiral2 = flow_rotate + abs(z2) * 0.0016

        for seg in range(T_Segments):
            a1_front = seg * angle_step + spiral1
            a2_front = (seg + 1) * angle_step + spiral1
            a1_back = seg * angle_step + spiral2
            a2_back = (seg + 1) * angle_step + spiral2

            x1 = r1 * math.cos(a1_front)
            y1 = r1 * math.sin(a1_front)

            x2 = r1 * math.cos(a2_front)
            y2 = r1 * math.sin(a2_front)

            x3 = r2 * math.cos(a2_back)
            y3 = r2 * math.sin(a2_back)

            x4 = r2 * math.cos(a1_back)
            y4 = r2 * math.sin(a1_back)

            if (ring + seg) % 2 == 0:
                red = 0.33 + 0.15 * (1.0 - depth)
                green = 0.015
                blue = 0.03
            else:
                red = 0.62 + 0.12 * (1.0 - depth)
                green = 0.03
                blue = 0.05

            glColor3f(red, green, blue)

            glBegin(GL_QUADS)
            glVertex3f(x1, y1, z1)
            glVertex3f(x2, y2, z1)
            glVertex3f(x3, y3, z2)
            glVertex3f(x4, y4, z2)
            glEnd()
    glPopMatrix()

def draw_far_end_cover():
    far_z = -T_Length - 80
    rad = T_Radius * 0.98

    rings = 10
    segments = T_Segments
    angle_step = (2 * math.pi) / segments
    ring_step = rad / rings

    glPushMatrix()
    for r in range(rings):
        inner_r = r * ring_step
        outer_r = (r + 1) * ring_step

        for s in range(segments):
            a1 = s* angle_step
            a2 = (s + 1) * angle_step

            x1 = inner_r * math.cos(a1)
            y1 = inner_r * math.sin(a1)

            x2 = inner_r * math.cos(a2)
            y2 = inner_r * math.sin(a2)

            x3 = outer_r * math.cos(a2)
            y3 = outer_r * math.sin(a2)

            x4 = outer_r * math.cos(a1)
            y4 = outer_r * math.sin(a1)

            glColor3f(0.10, 0.005, 0.01)

            glBegin(GL_QUADS)
            glVertex3f(x1, y1, far_z)
            glVertex3f(x2, y2, far_z)
            glVertex3f(x3, y3, far_z)
            glVertex3f(x4, y4, far_z)
            glEnd()
    glPopMatrix()

def player_dark_factor():

    darkest_gray = 0.42

    if game_over or fever >= 100:
        return darkest_gray

    return max(darkest_gray, 1.0 - (fever / 100.0) * (1.0 - darkest_gray))

def draw_cell_part(x, y, z, rad, r, g, b):
    dark_factor = player_dark_factor()

    glPushMatrix()
    glTranslatef(x, y, z)
    glColor3f(r * dark_factor, g * dark_factor, b * dark_factor)
    sphere_draw(rad, 20, 20)
    glPopMatrix()

def draw_wbc():
    glPushMatrix()
    glTranslatef(P_x, P_y, P_z)
    glScalef(P_scale, P_scale, P_scale)

    T = curr_time()
    b = 1.0 + 0.028 * math.sin(T * 3.0)
    glScalef(b, b, b)

    wobble_angle = math.sin(T) * P_wobble * 9.0
    glRotatef(wobble_angle, 0, 0, 1)
    glRotatef(wobble_angle * 0.45, 1, 0, 0)

    if shield_time > 0:
        if int(shield_time * 10) % 2 == 0:
            base_r, base_g, base_b = 1.0, 1.0, 1.0
        else:
            base_r, base_g, base_b = 0.3, 0.95, 1.0
    elif boost_time > 0:
        base_r, base_g, base_b = 1.0, 0.88, 0.22
    else:
        base_r, base_g, base_b = 0.94, 0.94, 0.92

    draw_cell_part(0, 0, 0, 31, base_r, base_g, base_b)
    draw_cell_part(-28, 2, 5, 24, 0.96, 0.96, 0.94)
    draw_cell_part(28, 2, 5, 24, 0.96, 0.96, 0.94)
    draw_cell_part(0, 28, 4, 23, 0.98, 0.98, 0.96)
    draw_cell_part(0, -28, 3, 23, 0.92, 0.92, 0.91)
    draw_cell_part(-18, -20, 6, 22, 0.95, 0.95, 0.93)
    draw_cell_part(18, -20, 6, 22, 0.95, 0.95, 0.93)
    draw_cell_part(-9, 7, 22, 14, 0.99, 0.99, 0.97)
    draw_cell_part(11, -4, 21, 13, 0.98, 0.98, 0.96)
    draw_cell_part(0, 0, 28, 11, 1.0, 1.0, 0.98)
    glPopMatrix()

def create_rbc():
    angle = random.uniform(0, 2 * math.pi)
    dist = random.uniform(55, T_Radius - 55)

    x = math.cos(angle) * dist
    y = math.sin(angle) * dist
    z = random.uniform(-T_Length, -450)

    return {
        "x": x, "y": y, "z": z,
        "speed": random.uniform(85, 145),
        "size": random.uniform(12, 20),
        "rot_x": random.uniform(0, 360),
        "rot_y": random.uniform(0, 360),
        "rot_z": random.uniform(0, 360),
        "tilt": random.uniform(-35, 35),
        "spin_x": random.uniform(20, 70),
        "spin_y": random.uniform(15, 55),
        "spin_z": random.uniform(30, 90)
    }

def init_rbc():
    global rbc
    rbc = []
    for i in range(18):
        rbc.append(create_rbc())

def update_rbc(dt):
    for cell in rbc:
        cell["z"] += cell["speed"] * dt
        cell["rot_x"] += cell["spin_x"] * dt
        cell["rot_y"] += cell["spin_y"] * dt
        cell["rot_z"] += cell["spin_z"] * dt

        if cell["z"] > P_z + 300:
            new_cell = create_rbc()
            cell.update(new_cell)
            cell["z"] = -T_Length

def draw_rbc():
    for cell in rbc:
        glPushMatrix()
        glTranslatef(cell["x"], cell["y"], cell["z"])
        glRotatef(cell["tilt"], 1, 0, 0)
        glRotatef(cell["rot_x"], 1, 0, 0)
        glRotatef(cell["rot_y"], 0, 1, 0)
        glRotatef(cell["rot_z"], 0, 0, 1)

        glColor3f(0.78, 0.08, 0.03)
        glScalef(1.9, 1.35, 0.25)
        sphere_draw(cell["size"], 16, 16)
        glPopMatrix()

def create_blood_parts():
    angle = random.uniform(0, 2 * math.pi)
    distance = random.uniform(20, T_Radius - 35)

    x = math.cos(angle) * distance
    y = math.sin(angle) * distance
    z = random.uniform(-T_Length, -250)

    return {
        "x": x, "y": y, "z": z,
        "speed": random.uniform(180, 330),
        "size": random.uniform(2.5, 5.5),
        "phase": random.uniform(0, 2 * math.pi)
    }

def init_blood_parts():
    global blood_parts
    blood_parts = []
    for i in range(70):
        blood_parts.append(create_blood_parts())

def update_blood_parts(dt):
    t = curr_time()
    for p in blood_parts:
        p["z"] += p["speed"] * dt
        p["x"] += math.sin(t * 2.0 + p["phase"]) * 3.0 * dt
        p["y"] += math.cos(t * 2.3 + p["phase"]) * 3.0 * dt

        if p["z"] > P_z + 300:
            new_p = create_blood_parts()
            p.update(new_p)
            p["z"] = -T_Length

def blood_parts_draw():
    for p in blood_parts:
        glPushMatrix()
        glTranslatef(p["x"], p["y"], p["z"])

        if int(p["phase"] * 10) % 2 == 0:
            glColor3f(0.95, 0.18, 0.04)
        else:
            glColor3f(1.0, 0.33, 0.08)

        sphere_draw(p["size"], 8, 8)
        glPopMatrix()

def create_immunity_picks(close_one=False):
    if close_one:
        x, y, z = 0.0, -35.0, -950.0
    else:
        angle = random.uniform(0, 2 * math.pi)
        dist = random.uniform(40, T_Radius - 55)
        x = math.cos(angle) * dist
        y = math.sin(angle) * dist
        z = random.uniform(-T_Length, -900)

    return {
        "x": x, "y": y, "z": z,
        "speed": random.uniform(115, 155),
        "size": 13,
        "rot": random.uniform(0, 360)
    }

def init_immunity_picks():
    global immunity_picks
    immunity_picks = [create_immunity_picks(True)]
    for i in range(3):
        immunity_picks.append(create_immunity_picks(False))

def reset_immunity_picks(item):
    new_item = create_immunity_picks(False)
    item.update(new_item)
    item["z"] = -T_Length - random.uniform(0, 900)

def update_immunity_picks(dt):
    for item in immunity_picks:
        item["z"] += item["speed"] * dt
        item["rot"] += 90 * dt

        if item["z"] > P_z + 300:
            reset_immunity_picks(item)

def draw_immunity_picks_model(item):
    t = curr_time()
    pulse = 1.0 + 0.12 * math.sin(t * 6.0 + item["rot"] * 0.02)

    glPushMatrix()
    glTranslatef(item["x"], item["y"], item["z"])
    glRotatef(item["rot"], 0, 1, 0)
    glScalef(pulse, pulse, pulse)

    glColor3f(0.0, 1,1)
    sphere_draw(item["size"], 18, 18)

    glColor3f(1.0, 1.0, 1.0)
    glPushMatrix()
    glScalef(0.32, 1.10, 0.32)
    glutSolidCube(item["size"] * 1.35)
    glPopMatrix()

    glPushMatrix()
    glScalef(1.10, 0.32, 0.32)
    glutSolidCube(item["size"] * 1.35)
    glPopMatrix()

    glColor3f(0.3, 1.0, 0.45)
    draw_flat_ring(item["size"] * 1.55, item["size"] * 1.75, 40)
    glPopMatrix()

def draw_immunity_picks():
    for item in immunity_picks:
        draw_immunity_picks_model(item)

def check_immunity_collection():
    global shield_time
    for item in immunity_picks:
        dx, dy, dz = item["x"] - P_x, item["y"] - P_y, item["z"] - P_z
        dist = math.sqrt(dx*dx + dy*dy + dz*dz)
        if dist < 38 + (P_radius * P_scale):
            shield_time = Sheild_time
            reset_immunity_picks(item)

def update_immunity(dt):
    global shield_time
    if shield_time > 0:
        shield_time = max(0.0, shield_time - dt)

def create_speed_boost():
    angle = random.uniform(0, 2 * math.pi)
    distance = random.uniform(40, T_Radius - 55)

    return {
        "x": math.cos(angle) * distance,
        "y": math.sin(angle) * distance,
        "z": random.uniform(-T_Length, -1500),
        "speed": random.uniform(130, 170),
        "size": 15,
        "rot": random.uniform(0, 360)
    }

def init_speed_boosts():
    global speed_boost
    speed_boost = []
    for i in range(2):
        speed_boost.append(create_speed_boost())

def update_speed_boosts(dt):
    for item in speed_boost:
        item["z"] += item["speed"] * dt
        item["rot"] += 120 * dt

        if item["z"] > P_z + 300:
            new_item = create_speed_boost()
            item.update(new_item)
            item["z"] = -T_Length - random.uniform(0, 1000)

def draw_speed_boosts():
    t = curr_time()
    for item in speed_boost:
        pulse = 1.0 + 0.15 * math.sin(t * 8.0)

        glPushMatrix()
        glTranslatef(item["x"], item["y"], item["z"])
        glRotatef(item["rot"], 1, 1, 0)
        glScalef(pulse, pulse, pulse)

        glColor3f(1.0, 0.85, 0.1)
        sphere_draw(item["size"], 16, 16)

        glColor3f(1.0, 1.0, 1.0)
        sphere_draw(item["size"] * 0.4, 8, 8)
        glPopMatrix()

def check_speed_boost_collection():
    global boost_time
    for item in speed_boost:
        dx, dy, dz = item["x"] - P_x, item["y"] - P_y, item["z"] - P_z
        dist = math.sqrt(dx*dx + dy*dy + dz*dz)
        collect_dist = 40 + (P_radius * P_scale)
        if dist < collect_dist:
            boost_time = 5.0
            new_item = create_speed_boost()
            item.update(new_item)
            item["z"] = -T_Length - random.uniform(0, 1000)

def add_fever_damage(amount):
    global fever
    if shield_time > 0:
        return
    fever = min(F_Limit, fever + amount)

def add_score(points):
    global score
    if game_over:
        return
    score += points

def update_enemy_subsystem(dt):
    global E, boss, E_spawn_time, score, fever, wave_num, boss_spawn, P_scale, P_wobble, end_wave_score
    if game_over: return
    spawn_rate = max(0.4, 2.2 - (wave_num * 0.25))
    diff_mult = 1.0 + (wave_num * 0.18)
    E_spawn_time += dt
    if E_spawn_time >= spawn_rate and not boss:
        if random.random() > 0.4:
            E.append(SpikeVirus(diff_mult))
        else:
            E.append(CrystalVirus(diff_mult))
        E_spawn_time = 0
    if score >= 100 and not boss_spawn:
        E = []
        boss = Boss_virus()
        boss_spawn = True

    for e in E[:]:
        e.z += e.speed * dt
        e.rot += e.rot_vel * dt
        dx = e.x - P_x
        dy = e.y - P_y
        dz = e.z - P_z
        dist = math.sqrt(dx*dx + dy*dy + dz*dz)
        hitbox = e.radius + (P_radius * P_scale)
        if dist < hitbox:
            if shield_time > 0:
                E.remove(e)
                continue
            P_scale = min(1.2, P_scale + 0.04)
            add_score(20)
            P_wobble = 1.2
            E.remove(e)
            if score >= end_wave_score + 60:
                wave_num += 1
                end_wave_score = score
            continue
        if e.z > P_z + 180:
            add_fever_damage(12.0)
            E.remove(e)
    if boss:
        boss.z += boss.speed * dt
        boss.rot += 35 * dt

        dx = boss.x - P_x
        dy = boss.y - P_y
        dz = boss.z - P_z
        dist = math.sqrt(dx**2 + dy**2 + dz**2)
        hitbox = boss.radius + (P_radius * P_scale)

        if dist < hitbox:
            if shield_time > 0:
                boss.z -= 550
            else:
                boss.health -= 1
                boss.z -= 550
                P_wobble = 1.5
            if boss.health <= 0:
                add_score(250)
                boss = None
                wave_num += 1
        elif boss.z > P_z + 180:
            add_fever_damage(100.0)
            boss = None

def draw_wave_status():
    text_draw(20, 615, f"CURRENT WAVE: {wave_num}")
    if boss:
        text_draw(400, 750, "!!! BOSS DETECTED !!!", GLUT_BITMAP_HELVETICA_18)
        for i in range(boss.health):
            glColor3f(1.0, 0.1, 0.1)
            glBegin(GL_QUADS)
            glVertex2f(400 + (i * 40), 720)
            glVertex2f(430 + (i * 40), 720)
            glVertex2f(430 + (i * 40), 740)
            glVertex2f(400 + (i * 40), 740)
            glEnd()
def draw_fever_bar():
    bar_x, bar_y = 220, 720
    bar_w, bar_h = 240, 22
    glColor3f(1, 1, 1)
    draw_outline_2d(bar_x, bar_y, bar_w, bar_h)
    fill_width = (fever / F_Limit) * bar_w
    if fever < 40:
        glColor3f(0.0, 0.85, 0.1)
    elif fever < 75:
        glColor3f(1.0, 0.85, 0.0)
    else:
        glColor3f(1.0, 0.0, 0.0)

    glBegin(GL_QUADS)
    glVertex2f(bar_x, bar_y)
    glVertex2f(bar_x + fill_width, bar_y)
    glVertex2f(bar_x + fill_width, bar_y + bar_h)
    glVertex2f(bar_x, bar_y + bar_h)
    glEnd()

def draw_immunity_bar():
    bar_x, bar_y = 220, 680
    bar_w, bar_h = 240, 18
    glColor3f(1, 1, 1)
    draw_outline_2d(bar_x, bar_y, bar_w, bar_h)
    fill_width = (shield_time / Sheild_time) * bar_w
    glColor3f(0.1, 0.9, 0.2)
    glBegin(GL_QUADS)
    glVertex2f(bar_x, bar_y)
    glVertex2f(bar_x + fill_width, bar_y)
    glVertex2f(bar_x + fill_width, bar_y + bar_h)
    glVertex2f(bar_x, bar_y + bar_h)
    glEnd()

def draw_immunity_icon(cx, cy, r):
    glColor3f(0.0, 0.95, 0.18)
    draw_rect_2d(cx - r, cy - r, r * 2, r * 2)

    glColor3f(1, 1, 1)
    draw_rect_2d(cx - 2, cy - 8, 4, 16)
    draw_rect_2d(cx - 8, cy - 2, 16, 4)

def draw_hud():
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glDisable(GL_DEPTH_TEST)
    text_draw(20, 760, f"SCORE: {score}")
    text_draw(20, 725, f"FEVER: {int(fever)}/{int(F_Limit)}")
    draw_fever_bar()
    draw_immunity_icon(34, 690, 11)
    if shield_time > 0:
        text_draw(52, 685, f"SHIELD ACTIVE: {shield_time:.1f}s")
    else:
        text_draw(52, 685, "SHIELD: inactive")

    if boost_time > 0:
        text_draw(20, 640, f"SPEED BOOST: {boost_time:.1f}s")
    else:
        text_draw(20, 640, "SPEED BOOST: inactive")

    draw_wave_status()

    if game_over:
        text_draw(680, 760, "CAMERA: GAME OVER VIEW")
    elif first_person:
        text_draw(700, 760, "CAMERA: FIRST PERSON")
    else:
        text_draw(690, 760, "CAMERA: THIRD PERSON")
    if game_over:
        text_draw(390, 430, "GAME OVER")
        text_draw(330, 395, "Fever reached maximum")
        text_draw(345, 365, "Press R to Restart")

    glEnable(GL_DEPTH_TEST)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def setupCamera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, WINDOW_WIDTH / WINDOW_HEIGHT, 0.1, 6000)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    if first_person and not game_over:
        yaw_rad = math.radians(first_person_yaw)
        pitch_rad = math.radians(first_person_pitch)

        cam_x, cam_y, cam_z = P_x, P_y + 4, P_z + 12
        look_x = cam_x + math.sin(yaw_rad) * 500
        look_y = cam_y + math.sin(pitch_rad) * 350
        look_z = cam_z - math.cos(yaw_rad) * 900
        gluLookAt(cam_x, cam_y, cam_z, look_x, look_y, look_z, 0, 1, 0)
    else:
        side_rad = math.radians(cam_side_offset)
        if game_over:
            cam_x = P_x + math.sin(side_rad) * 95
            cam_y = P_y + 80
            cam_z = P_z + 190
            look_x, look_y = P_x, P_y - 8
            look_z = P_z - 420
        else:
            cam_x = P_x + math.sin(side_rad) * 80
            cam_y = P_y + cam_ht
            cam_z = P_z + cam_dist
            look_x, look_y = P_x, P_y - 12
            look_z = P_z - 950 + cam_angle_offset

        gluLookAt(cam_x, cam_y, cam_z, look_x, look_y, look_z, 0, 1, 0)

def keyboardListener(key, x, y):
    global P_x, P_y, fever, P_wobble, first_person

    key = key.lower()

    if key == b'r':
        reset_game()
        return
    if key == b'c':
        first_person = not first_person
        glutPostRedisplay()
        return

    if game_over:
        return

    speed = P_base_speed / P_scale
    if boost_time > 0:
        speed *= 2.0

    step = speed * 0.035
    moved = False

    if key == b'w':
        P_y += step; moved = True
    elif key == b's':
        P_y -= step; moved = True
    elif key == b'a':
        P_x -= step; moved = True
    elif key == b'd':
        P_x += step; moved = True

    if moved:
        P_wobble = min(1.0, P_wobble + 0.35)

    clamp_player_tunnel()
    glutPostRedisplay()

def specialKeyListener(key, x, y):
    global cam_ht, cam_side_offset, first_person_yaw, first_person_pitch

    if first_person:
        if key == GLUT_KEY_LEFT: first_person_yaw -= 4
        elif key == GLUT_KEY_RIGHT: first_person_yaw += 4
        elif key == GLUT_KEY_UP: first_person_pitch += 3
        elif key == GLUT_KEY_DOWN: first_person_pitch -= 3
        first_person_pitch = max(-35, min(first_person_pitch, 35))
    else:
        if key == GLUT_KEY_UP: cam_ht += 5
        elif key == GLUT_KEY_DOWN: cam_ht -= 5
        elif key == GLUT_KEY_LEFT: cam_side_offset -= 5
        elif key == GLUT_KEY_RIGHT: cam_side_offset += 5
        cam_ht = max(-20, min(cam_ht, 120))
        cam_side_offset = max(-90, min(cam_side_offset, 90))

    glutPostRedisplay()

def mouseListener(button, state, x, y):
    global first_person
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        first_person = not first_person
        glutPostRedisplay()

def update_game(dt):
    global checker_offset, boost_time, game_over, flow_rotate, P_wobble

    if game_over:
        return

    checker_offset += scroll_speed * dt
    ring_step = T_Length / T_Rings
    if checker_offset > ring_step:
        checker_offset -= ring_step
    flow_rotate += flow_rotate_speed * dt
    if flow_rotate > 2 * math.pi:
        flow_rotate -= 2 * math.pi

    update_rbc(dt)
    update_blood_parts(dt)
    update_immunity_picks(dt)
    check_immunity_collection()
    update_immunity(dt)

    update_speed_boosts(dt)
    check_speed_boost_collection()

    update_enemy_subsystem(dt)

    if P_wobble > 0:
        P_wobble = max(0, P_wobble - P_wobble_decay * dt)

    if boost_time > 0:
        boost_time = max(0, boost_time - dt)

    if fever >= F_Limit:
        game_over = True

def idle():
    global l_time
    now = time.time()
    dt = min(now - l_time, 0.05)
    l_time = now

    update_game(dt)
    glutPostRedisplay()

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)

    setupCamera()

    draw_far_end_cover()
    draw_checker_tunnel()
    blood_parts_draw()
    draw_rbc()
    draw_immunity_picks()

    draw_speed_boosts()

    for enemy in E:
        enemy.draw()
    if boss:
        boss.draw()

    if (not first_person) or game_over:
        draw_wbc()

    draw_hud()
    glutSwapBuffers()

def reset_game():
    global P_x, P_y, P_z, P_scale
    global fever, score, boost_time, shield_time, game_over, checker_offset
    global first_person, cam_ht, cam_dist, cam_side_offset, cam_angle_offset
    global first_person_yaw, first_person_pitch, flow_rotate, P_wobble
    global E, boss, wave_num, boss_spawn, E_spawn_time, end_wave_score

    P_x, P_y, P_z = 0.0, -35.0, -260.0
    P_scale = 0.46

    fever, score, boost_time, shield_time = 0.0, 0, 0.0, 0.0
    game_over = False
    checker_offset = 0.0
    first_person = False

    cam_ht, cam_dist = 42.0, 110.0
    cam_side_offset, cam_angle_offset = 0.0, 0.0
    first_person_yaw, first_person_pitch = 0.0, 0.0

    flow_rotate, P_wobble = 0.0, 0.0

    E = []
    boss = None
    wave_num = 1
    boss_spawn = False
    E_spawn_time = 0.0
    end_wave_score = 0

    init_rbc()
    init_blood_parts()
    init_immunity_picks()
    init_speed_boosts()

def main():
    global GLOBAL_QUAD
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitWindowPosition(50, 50)
    glutCreateWindow(b"Cellular Guardian Game")
    GLOBAL_QUAD = gluNewQuadric()

    glEnable(GL_DEPTH_TEST)
    glClearColor(0.06, 0.0, 0.01, 1.0)

    init_rbc()
    init_blood_parts()
    init_immunity_picks()
    init_speed_boosts()

    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)

    glutMainLoop()

main()
