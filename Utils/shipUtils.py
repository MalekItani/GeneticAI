import numpy as np
import random

def degToRad(angle):
    return angle*np.pi/180

class Pawn:
    def __init__(self, pos = np.array([0,0]), size = 2, rot = 0):
        x, y = pos
        self.rotation = 0
        self.size = size
        self.isAlive = True
        self.coordinates = ((x, y),(x+size*10, y+size*5), (x, y+size*10), (x+size*3, y+size*5))

    def rotate(self, angle):
        angInRad = degToRad(angle)
        self.rotation += angInRad
        co = np.asarray(self.coordinates).astype(float)
        temp = [0,0]
        for i in range(len(co)):
            temp += co[i]
        center = 1/len(co)*temp
        for i in range(len(co)):
            co[i] = (co[i]-center).dot([[np.cos(angInRad), -np.sin(angInRad)],
                               [np.sin(angInRad), np.cos(angInRad)]]) + center
        self.coordinates = tuple(map(tuple, co))

    def getCentroid(self):
        co = np.asarray(self.coordinates).astype(float)
        temp = [0, 0]
        for i in range(len(co)):
            temp += co[i]
        center = 1 / len(co) * temp
        return center

    def moveForward(self, speed = 1):
        co = np.asarray(self.coordinates)
        co[:,0] += int(speed*np.cos(self.rotation))
        co[:,1] -= int(speed*np.sin(self.rotation))
        self.coordinates = tuple(map(tuple, co))

    def kill(self):
        self.coordinates = ((0,0))
        self.isAlive = False

    def collidesWith(self, xwidth, ywidth):
        x,y = self.getCentroid()
        if x >= xwidth[0] and x < xwidth[1] and y >= ywidth[0] and y < ywidth[1]:
            return True
        return False

def generatePathSequence(size):
    path = np.zeros(size)
    for i in range(size):
        path[i] = random.random()*10 - 5
    return path

class pawnGenome:
    def __init__(self, size, pawn, l = None, mutationRate = 0.01):
        self.mutationRate = mutationRate
        self.size = size
        self.pawn = pawn
        if l is None:
            self.path = generatePathSequence(size)
        else:
            self.path = l

        self.mutate()

    def checkFitness(self, target, margin = 50):
        x, y = target
        if not self.pawn.isAlive:
            return 99999
        elif self.pawn.getCentroid()[0] >= x and self.pawn.getCentroid()[0] < x+margin and self.pawn.getCentroid()[1] >= y and self.pawn.getCentroid()[1] < y+margin:
            return 0
        else:
            return np.sqrt((self.pawn.getCentroid()[0]-x)**2 + (self.pawn.getCentroid()[1]-y)**2)

    def cross(self, g2, target):
        f1 = self.checkFitness(target)
        f2 = self.checkFitness(target)
        gen2 = pawnGenome(self.size, self.pawn)
        try:
            norm = f2/(f1+f2)*100
        except ZeroDivisionError:
            return f1
        for i in range(len(self.path)):
            rdn = random.randint(0,100)
            if rdn <= norm:
                gen2.path[i] = self.path[i]
            else:
                gen2.path[i] = g2.path[i]
        return gen2

    def mutate(self):
        for i in range(len(self.path)):
            rdn = random.randint(0,100)
            if rdn <= self.mutationRate*100:
                self.path[i] = random.random()*10 - 5
