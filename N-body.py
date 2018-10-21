import sys
from random import random, uniform
import math
from time import time
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import configparser
from astropy.time import Time as astrotime
import datetime
import threading

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
GRAV_CONS = float(config['CONFIGURE']['GRAV_CONS']) * 1E-9 #Convert meter cubed to kilometer cubed
NORM_DELTA_T = float(config['CONFIGURE']['NORM_DELTA_T'])
FINE_DELTA_T = float(config['CONFIGURE']['FINE_DELTA_T'])
SEC_PER_DAY = float(config['CONFIGURE']['SEC_PER_DAY'])
EXPONENT = float(config['CONFIGURE']['EXPONENT'])
bool_T = True

'''
Class holds attributes of a single body
'''
class Body(object):
    global_ident = 0
    def __init__(self, ident=None, time=None, x=None, y=None,z=None,Vx=None,Vy=None,Vz=None,mass=None,radius=None,color1=None,color2=None,color3=None):
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
        if color1 == None:
            self.color1 = random()
        else:
            self.color1 = color1
        if color2 == None:
            self.color2 = random()
        else:
            self.color2 = color2
        if color3 == None:
            self.color3 = random()
        else:
            self.color3 = color3
        self.coord = []
        self.zeroF()
        self.collisions = ""

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
              + ", radius = " + str(self.radius)
              + ", color1 = " + str(self.color1)
              + ", color2 = " + str(self.color2)
              + ", color3 = " + str(self.color3))

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
        self.Vx += self.Fx * planet_system.DELTA_T / self.mass
        self.Vy += self.Fy * planet_system.DELTA_T / self.mass
        self.Vz += self.Fz * planet_system.DELTA_T / self.mass

    def cal_position(self):
        self.x += self.Vx * planet_system.DELTA_T
        self.y += self.Vy * planet_system.DELTA_T
        self.z += self.Vz * planet_system.DELTA_T
        self.coord.append((self.x,self.y,self.z))



'''
Class holds bodies
'''
class Asystem:
    def __init__(self,input):
        self.DELTA_T = NORM_DELTA_T
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
            if fields[0] != 'ident':
                body = Body(str(fields[0]),
                            float(fields[1]),
                            float(fields[2]),
                            float(fields[3]),
                            float(fields[4]),
                            float(fields[5]),
                            float(fields[6]),
                            float(fields[7]),
                            float(fields[8]),
                            float(fields[9]),
                            float(fields[10]),
                            float(fields[11]),
                            float(fields[12]))
                bodies.append(body)
        return bodies

    def write_to_file(self,file):
        data = ''
        for body in self.system:
            body_data = (str(body.ident) + ", "
                         + str(body.time) + ", "
                         + str(body.x) + ", "
                         + str(body.y) + ", "
                         + str(body.z) + ", "
                         + str(body.Vx) + ", "
                         + str(body.Vy) + ", "
                         + str(body.Vz) + ", "
                         + str(body.mass) + ", "
                         + str(body.radius) + ", "
                         + str(body.color1) + ", "
                         + str(body.color2) + ", "
                         + str(body.color3) + "\n")
            data += body_data
        data += "Collisions: " + self.collisions + '\n\n'
        file.write(data)

    def compute1(self,body):

        body.zeroF()
        for other_body in self.system:
            if body != other_body:
                body.cal_netforce(other_body)
        body.cal_velocity()

    def compute2(self,body):
        body.cal_position()
        body.time += self.DELTA_T / SEC_PER_DAY

        '''
        for body in self.system:
            body.zeroF()
            for other_body in self.system:
                if body != other_body:
                    body.cal_netforce(other_body)
            body.cal_velocity()
        for body in self.system:
            body.cal_position()
            body.time += self.DELTA_T / SEC_PER_DAY
        '''
    def if_collision(self):
        self.collisions = ""
        if_T = False
        for i in range(len(self.system)):
            for j in range(len(self.system)):
                if i > j:
                    x_dif = self.system[i].x - self.system[j].x
                    y_dif = self.system[i].y - self.system[j].y
                    z_dif = self.system[i].z - self.system[j].z
                    distance = (x_dif**2 + y_dif**2 + z_dif**2)**0.5
                    if distance <= 2*(self.system[i].radius + self.system[j].radius):
                        if_T = True
                    if distance <= self.system[i].radius + self.system[j].radius:
                        self.collisions += str(self.system[i].ident) + " and " + str(self.system[j].ident) + ", "
        if self.collisions != "":
            string = self.collisions[:-2]
            print("Collision: " + string +  " @ " + astrotime(self.system[i].time, format = 'jd').iso)
            self.glut_print(10, 25, GLUT_BITMAP_9_BY_15, "Collision: " + string, 1.0, 1.0, 1.0, 1.0)
        else:
            self.collisions = "None"
            self.glut_print(10, 25, GLUT_BITMAP_9_BY_15, "Collision: " + self.collisions, 1.0, 1.0, 1.0, 1.0)
        if bool_T == False:
            planet_system.DELTA_T = 0
        elif if_T == True:
            self.DELTA_T = FINE_DELTA_T
            self.write_to_file(write_file)
        else:
            self.DELTA_T = NORM_DELTA_T



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

        self.glut_print(10, 10, GLUT_BITMAP_9_BY_15, astrotime(self.system[0].time, format = 'jd').iso, 1.0, 1.0, 1.0, 1.0)
        for body in self.system:
            glPushMatrix()
            glTranslated(init.SCALE * body.x, init.SCALE * body.y, init.SCALE * body.z)
            glColor3f(body.color1/255, body.color2/255, body.color3/255)
            glutSolidSphere(BALL_SIZE * (body.radius**init.EXPONENT), 20, 20)
            glPopMatrix()
            glLineWidth(1)
            glBegin(GL_LINE_STRIP)
            glColor(body.color1/255,body.color2/255,body.color3/255)
            for point in body.coord:
                glVertex3f(init.SCALE * point[0], init.SCALE * point[1], init.SCALE * point[2])
            glEnd()
        self.if_collision()


        glutSwapBuffers()

    '''
    Display text
    '''
    def glut_print(self, x, y, font, text, r, g, b, a):
        self.blending = False
        if glIsEnabled(GL_BLEND):
            self.blending = True

        # glEnable(GL_BLEND)
        glColor3f(r, g, b)
        glWindowPos2f(x, y)
        for ch in text:
            glutBitmapCharacter(font, ctypes.c_int(ord(ch)))

        if not self.blending:
            glDisable(GL_BLEND)

    def animate(self):

        calc1 = []
        for body in self.system:
            calc1.append(threading.Thread(target=self.compute1, args=(body,)))
            calc1[-1].start()
        for i in calc1:
            i.join()
        calc2 = []
        for body in self.system:
            calc2.append(threading.Thread(target=self.compute2, args=(body,)))
            calc2[-1].start()
        for i in calc2:
            i.join()
        self.display()


class Definition:
    def __init__(self):             #Initialization of graphics
        glClearColor(0.1,0.0,0.15,0.0)
        glColor3f(1.0,1.0,1.0)
        glPointSize(POINT_SIZE)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        #init lighting
        '''
        mat_specular = (1.0, 1.0, 1.0, 1.0)
        mat_shininess = (50)
        light_position = (1.0, 1.0, 1.0, 0.0)
        glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
        glMaterialfv(GL_FRONT, GL_SHININESS, mat_shininess)
        glLightfv(GL_LIGHT0, GL_POSITION, light_position)

        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_DEPTH_TEST)
        '''
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
        self.EXPONENT = EXPONENT
        self.bool_T = True
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
            self.eyeRho *= 1.1
        elif (theKey == b'm' or theKey == b'M'):
            self.eyeRho /= 1.1
        elif (theKey == b'w' or theKey == b'W'):
            self.look[1] += 0.5
        elif (theKey == b's' or theKey == b'S'):
            self.look[1] -= 0.5
        elif (theKey == b'a' or theKey == b'A'):
            self.look[0] -= 0.5
        elif (theKey == b'd' or theKey == b'D'):
            self.look[0] += 0.5
        elif (theKey == b'e' or theKey == b'E'):
            self.SCALE *= 1.1
        elif (theKey == b'q' or theKey == b'Q'):
            self.SCALE *= .9
        elif (theKey == b','):
            self.EXPONENT *= 1.01
        elif (theKey == b'.'):
            self.EXPONENT *= 0.99
        elif (theKey == b' '):
            global bool_T
            bool_T = not bool_T
        '''
        if math.sin(self.eyePhi) > 0: self.upY = 1
        else: self.upY = 1
        '''
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
    system.system.append(Body(0,2452170.375,0,0,0,0,0,0,100000000000000000000,10,253,184,19))
    position = 5
    velocity = 1
    for i in range(n_bodies):
        if i != 0:
            mass_radius = uniform(1,1000)
            system.system.append(Body(i,2452170.375,uniform(-1 * position,position),uniform(-1 * position,position),uniform(-1 * position,position),uniform(-1 * velocity,velocity),uniform(-1 * velocity,velocity),uniform(-1 * velocity,velocity),mass_radius,mass_radius/1000,uniform(0,255),uniform(0,255),uniform(0,255)))
    return system



if __name__ == "__main__":
    write_file = open(str(datetime.datetime.now()) + ".csv", 'w')
    write_file.write('ident,             JDTDB,                      X,                      Y,                      Z,              VX (km/s),              VY (km/s),              VZ (km/s),             mass (kg),          radius (km),  color1,   color2,    color3,\n')
    planet_system = Asystem("Solar_system.csv")
    #planet_system = planet_system(10)
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(WIDTH, HEIGHT)
    glutInitWindowPosition(POSITION_X, POSITION_Y)
    glutCreateWindow("N-Body")

    glutDisplayFunc(planet_system.display)
    glutIdleFunc(planet_system.animate)

    init = Definition()

    glutMainLoop()

    write_file.close()