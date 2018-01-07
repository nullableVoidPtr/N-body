import pandas as pd
import re
import random

body = {'ident':0, 'x':1, 'y':2, 'z':3, 'Vx_old':4, 'Vy_old':5, 'Vz_old':6, 'Vx_new':7, 'Vy_new':8, 'Vz_new':9, 'mass':10}

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




class Body(object):
    global_ident = 0
    def __init__(self, ident=None, x=None, y=None,z=None,Vx=None,Vy=None,Vz=None,Vx_new=None,Vy_new=None,Vz_new=None,mass=None):
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
        self.Vx_new = Vx
        self.mass _new
        self.Vy_new = Vy_new
        self.Vz_new = Vz_new
        if mass == None:
            self.mass = random.random()
        else:
            self.mass = mass
    def print(self):
        print("ident: " + str(self.ident) + ", x = " + str(self.x) + ", y = " + str(self.y) +", z = " + str(self.z) +", Vx = " + str(self.Vx) +", Vy = " + str(self.Vy) +", Vz = " + str(self.Vz) +", Vx_new = " + str(self.Vx_new) +", Vy_new = " + str(self.Vy_new) +", Vz_new = " + str(self.Vz_new) + ", mass = " + str(self.mass))

class Asystem:
    def __init__(self,n_bodies=10):
        self.n_bodies = n_bodies
        self.system = []
        for i in range(self.n_bodies):
            self.system.append(Body())
    def print(self):
        for body in self.system:
            body.print()

if __name__ == "__main__":
    solar_system = Asystem()
    solar_system.print()

