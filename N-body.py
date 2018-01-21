import pandas as pd
import re
import random
import math
from time import time
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

body = {'ident':0,
        'x':1,
        'y':2,
        'z':3,
        'Vx':4,
        'Vy':5,
        'Vz':6,
        'mass':7}
WIDTH = 800
HEIGHT = 800
POINT_SIZE = 1
POSITION_X = 112
POSITION_Y = 20
WORLD_LEFT = -1000
WORLD_RIGHT = 1000
WORLD_BOTTOM = -1000
WORLD_TOP = 1000
VIEW_ANGLE = 45
RHO = 100
WORLD_NEAR = 0.1
WORLD_FAR = 1000000
SCALE = 1
BALL_SIZE = 0.5
REFRESH_RATE = 0.001
LINE_SIZE = 1000

'''
file = 'N-body.csv'

df = pd.read_csv(file) #reads file

fb = re.search("\n",repr(df)) #searches for first break
hn = fb.start() #obtains last string index of heading
heading = repr(df)[:hn].split()

vals = repr(df).split()

count = 11
global bodies
bodies = []
no_body = int(len(vals) / 12)
one_body = []
while count < len(vals):
    count+=1
    one_body.append(vals[count - 1])
    if (count + 1) % 12 == 0:
        bodies.append(one_body)
        one_body = []

print(bodies)
print(bodies[2][body['x']])
'''


'''
Class holds attributes of a single body
'''

class Body(object):
    global_ident = 0
    def __init__(self, ident=None, x=None, y=None,z=None,Vx=None,Vy=None,Vz=None,mass=None):
        if ident == None:
            self.ident = Body.global_ident
            Body.global_ident += 1
        else:
            self.ident = ident
        if x == None:
            self.x = random.random()
        else:
            self.x = x
        if y == None:
            self.y = random.random()
        else:
            self.y = y
        if z == None:
            self.z = random.random()
        else:
            self.z = z
        if Vx == None:
            self.Vx = random.random()
        else:
            self.Vx = Vx
        if Vy == None:
            self.Vy = random.random()
        else:
            self.Vy = Vy
        if Vz == None:
            self.Vz = random.random()
        else:
            self.Vz = Vz
        if mass == None:
            self.mass = random.random()
        else:
            self.mass = mass
        self.zeroF()

    def zeroF(self):
        self.Fx = 0
        self.Fy = 0
        self.Fz = 0

    def print(self):
        print("ident: " + str(self.ident)
              + ", x = " + str(self.x)
              + ", y = " + str(self.y)
              + ", z = " + str(self.z)
              + ", Vx = " + str(self.Vx)
              + ", Vy = " + str(self.Vy)
              + ", Vz = " + str(self.Vz)
              + ", mass = " + str(self.mass))

    def cal_netforce(self, other_body):
        dx = other_body.x - self.x
        dy = other_body.y - self.y
        dz = other_body.z - self.z
        distance = math.sqrt(dx**2 + dy**2 + dz**2)
        force = Asystem.GRAV_CONS * self.mass * other_body.mass / (distance**2)
        angleBAM = math.asin(dz/distance)
        angleMAN = math.atan(dy/dx)
        AM = force * math.cos(angleBAM)
        self.Fx += AM * math.cos(angleMAN)
        self.Fy += AM * math.sin(angleMAN)
        self.Fz += force * math.sin(angleBAM)

    def cal_velocity(self, delta_t):
        self.Vx = self.Vx + (self.Fx * delta_t / self.mass)
        self.Vy = self.Vy + (self.Fy * delta_t / self.mass)
        self.Vz = self.Vz + (self.Fz * delta_t / self.mass)

    def cal_position(self, delta_t):
        self.x = self.Vx * delta_t + self.x
        self.y = self.Vy * delta_t + self.y
        self.z = self.Vz * delta_t + self.z

'''
Class holds bodies
'''

class Asystem:
    GRAV_CONS = 6.67248E-11
    delta_t = 0.5

    def __init__(self,input):
        if type(input) == int:
            self.n_bodies = input
            self.system = []
            for i in range(self.n_bodies):
                self.system.append(Body())
        elif type(input) == str:
            self.system = self.read_from_file(input)
        else:
            raise Exception("Invalid input type for init of Asystem")

    def print(self):
        for body in self.system:
            body.print()

    def read_from_file(self,file_name):
        bodies = []
        for line in open(file_name):
            fields = line.split(",")
            if fields[1] != 'x':
                body = Body(str(fields[0]),
                            float(fields[1]),
                            float(fields[2]),
                            float(fields[3]),
                            float(fields[4]),
                            float(fields[5]),
                            float(fields[6]),
                            float(fields[7]))
                bodies.append(body)
        return bodies

    def write_to_file(self,file_name):
        data = 'ident,x,y,z,Vx,Vy,Vx,mass\n'
        for body in self.system:
            body_data = (body.ident + ","
                         + str(body.x) + ","
                         + str(body.y) + ","
                         + str(body.z) + ","
                         + str(body.Vx) + ","
                         + str(body.Vy) + ","
                         + str(body.Vz) + ","
                         + str(body.mass) + "\n")
            data += body_data
        file = open(file_name,'w')
        file.write(data)
        file.close()

    def compute(self):
        for body in self.system:
            body.zeroF()
            for other_body in self.system:
                if body != other_body:
                    body.cal_netforce(other_body)
            body.cal_velocity(self.delta_t)
        for body in self.system:
            body.cal_position(self.delta_t)
    '''
    This function redraws the screen after the positions of particles have been updated
    '''
    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(eyeRho * math.sin(eyePhi) * math.sin(eyeTheta), eyeRho * math.cos(eyePhi),
                  eyeRho * math.sin(eyePhi) * math.cos(eyeTheta),
                  look[0], look[1], look[2],
                  0, upY, 0)

        for body in self.system:
            glPushMatrix()
            glTranslated(SCALE * body.x, SCALE * body.y, SCALE * body.z)
            glutSolidSphere(BALL_SIZE, 10, 10)
            glPopMatrix()

    def animate(self):
        self.compute()
        self.display()


'''
Initialization of graphics
'''
def init():
    glClearColor(1.0,1.0,1.0,0.0)
    glColor3f(0.0,0.0,0.0)
    glPointSize(POINT_SIZE)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    #init lighting

    mat_specular = (1.0, 1.0, 1.0, 1.0)
    mat_shininess = (50)
    light_position = (1.0, 1.0, 0.0, 0.0)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialfv(GL_FRONT, GL_SHININESS, mat_shininess)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_DEPTH_TEST)

    global previousTime, eyeTheta, eyePhi, eyeRho, look, windowWidth, windowHeight, upY
    displayRatio = 1 * WIDTH / HEIGHT
    windowWidth = WIDTH
    windowHeight = HEIGHT
    previousTime = time()
    eyeTheta = 0
    eyePhi = math.pi * 0.5
    eyeRho = RHO
    upY = 1
    look = (0, 0, 0)
    gluPerspective(VIEW_ANGLE, displayRatio, WORLD_NEAR, WORLD_FAR)

if __name__ == "__main__":

    planet_system = Asystem(10)

    glutInit()
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(WIDTH, HEIGHT)
    glutInitWindowPosition(POSITION_X, POSITION_Y)
    glutCreateWindow("N-Body")

    glutDisplayFunc(planet_system.display)
    glutIdleFunc(planet_system.animate)

    init()

    glutMainLoop()
