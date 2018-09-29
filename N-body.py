import sys
from random import random, uniform
import math
from time import time
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import configparser
from astropy.time import Time as astrotime

config = configparser.ConfigParser()
config.read('configure.ini')

WIDTH = int(config['CONFIGURE']['WIDTH'])
HEIGHT = int(config['CONFIGURE']['HEIGHT'])
POINT_SIZE = float(config['CONFIGURE']['POINT_SIZE'])
POSITION_X = int(config['CONFIGURE']['POSITION_X'])
POSITION_Y = int(config['CONFIGURE']['POSITION_Y'])
WORLD_LEFT = float(config['CONFIGURE']['WORLD_LEFT'])
WORLD_RIGHT = float(config['CONFIGURE']['WORLD_RIGHT'])
WORLD_BOTTOM = float(config['CONFIGURE']['WORLD_BOTTOM'])
WORLD_TOP = float(config['CONFIGURE']['WORLD_TOP'])
VIEW_ANGLE = float(config['CONFIGURE']['VIEW_ANGLE'])
RHO = float(config['CONFIGURE']['RHO'])
WORLD_NEAR = float(config['CONFIGURE']['WORLD_NEAR'])
WORLD_FAR = float(config['CONFIGURE']['WORLD_FAR'])
SCALE = float(config['CONFIGURE']['SCALE'])
BALL_SIZE = float(config['CONFIGURE']['BALL_SIZE'])
REFRESH_RATE = float(config['CONFIGURE']['REFRESH_RATE'])
LINE_SIZE = float(config['CONFIGURE']['LINE_SIZE'])
GRAV_CONS = float(config['CONFIGURE']['GRAV_CONS'])
SEC_PER_YEAR = float(config['CONFIGURE']['SEC_PER_YEAR'])
NO_SECONDS = float(config['CONFIGURE']['NO_SECONDS'])
DAYS_PER_SECOND = float(config['CONFIGURE']['DAYS_PER_SECOND'])
DELTA_T = SEC_PER_YEAR * NO_SECONDS

'''
Class holds attributes of a single body
'''
class Body(object):
    global_ident = 0
    def __init__(self, ident=None, time=None, x=None, y=None,z=None,Vx=None,Vy=None,Vz=None,mass=None,radius=None):
        if ident == None:
            self.ident = Body.global_ident
            Body.global_ident += 1
        else:
            self.ident = ident
        if time == None:
            self.x = 2452170.375 #2001-09-17T21:00:00.000
        else:
            self.time = time
        if x == None:
            self.x = random()
        else:
            self.x = x
        if y == None:
            self.y = random()
        else:
            self.y = y
        if z == None:
            self.z = random()
        else:
            self.z = z
        if Vx == None:
            self.Vx = random()
        else:
            self.Vx = Vx
        if Vy == None:
            self.Vy = random()
        else:
            self.Vy = Vy
        if Vz == None:
            self.Vz = random()
        else:
            self.Vz = Vz
        if mass == None:
            self.mass = random()
        else:
            self.mass = mass
        if radius == None:
            self.radius = random()
        else:
            self.radius = radius
        self.zeroF()

    def zeroF(self):
        self.Fx = 0
        self.Fy = 0
        self.Fz = 0

    def print(self):
        print("ident = " + str(self.ident)
              + ", time =  " + str(self.time) + " = " + str(astrotime(self.time, format = "jd", scale = 'utc').isot)
              + ", x = " + str(self.x)
              + ", y = " + str(self.y)
              + ", z = " + str(self.z)
              + ", Vx = " + str(self.Vx)
              + ", Vy = " + str(self.Vy)
              + ", Vz = " + str(self.Vz)
              + ", mass = " + str(self.mass)
              + ", radius = " + str(self.radius))

    def cal_netforce(self, other_body):
        Dx = other_body.x - self.x
        Dy = other_body.y - self.y
        Dz = other_body.z - self.z
        distance = math.sqrt(Dx**2 + Dy**2 + Dz**2)
        con = GRAV_CONS * self.mass * other_body.mass / (distance**2)
        gd = con / distance
        self.Fx += gd * Dx
        self.Fy += gd * Dy
        self.Fz += gd * Dz

    def cal_velocity(self):
        self.Vx += self.Fx / self.mass
        self.Vy += self.Fy / self.mass
        self.Vz += self.Fz / self.mass

    def cal_position(self):
        self.x += self.Vx * DELTA_T
        self.y += self.Vy * DELTA_T
        self.z += self.Vz * DELTA_T



'''
Class holds bodies
'''
class Asystem:


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
            if fields[0] != '     ident':
                body = Body(str(fields[0]),
                            float(fields[1]),
                            float(fields[2]),
                            float(fields[3]),
                            float(fields[4]),
                            float(fields[5]),
                            float(fields[6]),
                            float(fields[7]),
                            float(fields[8]),
                            float(fields[9]))
                bodies.append(body)
        return bodies

    def write_to_file(self,file_name):
        data = 'ident, time, , x, y, z, Vx, Vy, Vx, mass, radius\n'
        for body in self.system:
            body_data = (str(body.ident) + ","
                         + str(body.time) + ","
                         + str(body.x) + ","
                         + str(body.y) + ","
                         + str(body.z) + ","
                         + str(body.Vx) + ","
                         + str(body.Vy) + ","
                         + str(body.Vz) + ","
                         + str(body.mass) + ","
                         + str(body.radius) + "\n")
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
            body.cal_velocity()
        for body in self.system:
            body.cal_position()
            body.time += DELTA_T * DAYS_PER_SECOND

    def if_collision(self):
        for i in range(len(self.system)):
            for j in range(len(self.system)-i):
                if i != j:
                    x_dif = self.system[i].x - self.system[j].x
                    y_dif = self.system[i].y - self.system[j].y
                    z_dif = self.system[i].z - self.system[j].z
                    distance = (x_dif**2 + y_dif**2 + z_dif**2)**0.5
                    if distance <= self.system[i].radius + self.system[j].radius:
                        print("Collision of " + str(self.system[i].ident) + " and " + str(self.system[j].ident) + " @ " + astrotime(self.system[i].time, format = 'jd').iso)
    '''
    This function redraws the screen after the positions of particles have been updated
    '''
    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(init.eyeRho * math.sin(init.eyePhi) * math.sin(init.eyeTheta),
                  init.eyeRho * math.cos(init.eyePhi),
                  init.eyeRho * math.sin(init.eyePhi) * math.cos(init.eyeTheta),
                  init.look[0], init.look[1], init.look[2],
                  0, init.upY, 0)

        for body in self.system:
            glPushMatrix()
            glTranslated(init.SCALE * body.x, init.SCALE * body.y, init.SCALE * body.z)
            glutSolidSphere(BALL_SIZE * body.radius, 20, 20)
            glPopMatrix()
            glutSwapBuffers()

    def animate(self):
        self.compute()
        self.display()
        self.if_collision()


class Definition:
    def __init__(self):             #Initialization of graphics
        glClearColor(0.0,0.0,0.0,0.0)
        glColor3f(1.0,1.0,1.0)
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

        #global previousTime, eyeTheta, eyePhi, eyeRho, look, windowWidth, windowHeight, upY
        self.displayRatio = 1 * WIDTH / HEIGHT
        self.windowWidth = WIDTH
        self.windowHeight = HEIGHT
        self.previousTime = time()
        self.eyeTheta = 0
        self.eyePhi = math.pi * 0.5
        self.eyeRho = RHO
        self.upY = 1
        self.look = [0, 0, 0]
        self.SCALE = SCALE
        gluPerspective(VIEW_ANGLE, self.displayRatio, WORLD_NEAR, WORLD_FAR)
        glutKeyboardFunc(self.keyboard)
        glutReshapeFunc(self.reshape)
    def keyboard(self, theKey, mouseX, mouseY): #Manipulate with the image
        if (theKey == b'x' or theKey == b'X'):
            sys.exit()
        if (theKey == b'i' or theKey == b'I'):
            self.eyePhi -= math.pi / 20
        if (theKey == b'0'):
            self.eyePhi = 2 * math.pi
        elif (theKey == b'o' or theKey == b'O'):
            self.eyePhi += math.pi / 20
        elif (theKey == b'j' or theKey == b'J'):
            self.eyeTheta -= math.pi / 20
        elif (theKey == b'k' or theKey == b'K'):
            self.eyeTheta += math.pi / 20
        elif (theKey == b'n' or theKey == b'N'):
            self.eyeRho += 0.5
        elif (theKey == b'm' or theKey == b'M'):
            self.eyeRho -= 0.5
        elif (theKey == b'w' or theKey == b'W'):
            self.look[1] += 0.5
        elif (theKey == b's' or theKey == b'S'):
            self.look[1] -= 0.5
        elif (theKey == b'a' or theKey == b'A'):
            self.look[0] -= 0.5
        elif (theKey == b'd' or theKey == b'D'):
            self.look[0] += 0.5
        elif (theKey == b'e' or theKey == b'e'):
            self.SCALE *= 1.1
        elif (theKey == b'q' or theKey == b'q'):
            self.SCALE *= 0.9
        if math.sin(self.eyePhi) > 0: self.upY = 1
        else: self.upY = 1
    def reshape(self, width, height):             #Manipulate with the window
        self.displayRatio = 1 * width / height
        self.windowWidth = width
        self.windowHeight = height
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(VIEW_ANGLE, self.displayRatio, WORLD_NEAR, WORLD_FAR)
        glViewport(0, 0, self.windowWidth, self.windowHeight)



'''
Randomly generates planetary system
'''
def planet_system(n_bodies):
    system = Asystem(0)
    system.system.append(Body(1,2452170.375,0,0,0,0,0,0,500,20))
    position = 20
    velocity = 1000
    for i in range(n_bodies):
        system.system.append(Body(i,2452170.375,uniform(-1 * position,position),uniform(-1 * position,position),uniform(-1 * position,position),uniform(-1 * velocity,velocity),uniform(-1 * velocity,velocity),uniform(-1 * velocity,velocity),uniform(0,10),uniform(0,10)))
    return system



if __name__ == "__main__":

    #planet_system = Asystem("Solar_system.csv")
    planet_system = planet_system(10)
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(WIDTH, HEIGHT)
    glutInitWindowPosition(POSITION_X, POSITION_Y)
    glutCreateWindow("N-Body")

    glutDisplayFunc(planet_system.display)
    glutIdleFunc(planet_system.animate)

    init = Definition()

    glutMainLoop()
