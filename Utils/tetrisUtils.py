import numpy as np
import tkinter as tk
import random
import time

id = 0

class Block:
    def __init__(self, schema, pivot):
        global id
        self.points = schema
        self.pivot = pivot
        self.ids = [i for i in range(id, id+5)]

def generateRandomBlock():
    r = random.randint(0,6)
    startpos = [5,0]
    if r == 0:
        return Block(np.array([startpos, startpos + np.array([0,1]), startpos + np.array([0,2]), startpos + np.array([1,0])]), np.array(startpos)) # L
    elif r == 1:
        return Block(np.array([startpos, startpos + np.array([0,1]), startpos + np.array([1,1]), startpos + np.array([1,0])]), np.array(startpos)) # Keypad
    elif r == 2:
        return Block(np.array([startpos, startpos + np.array([0,1]), startpos + np.array([1,0]), startpos + np.array([-1,0])]), np.array(startpos)) # Square
    elif r == 3:
        return Block(np.array([startpos, startpos + np.array([0,1]), startpos + np.array([0,2]), startpos + np.array([-1,0])]), np.array(startpos))  # L-Reverse
    elif r == 4:
        return Block(np.array([startpos, startpos + np.array([0,1]), startpos + np.array([0,-1]), startpos + np.array([0,-2])]), np.array(startpos))  # Line
    elif r == 5:
        return Block(np.array(
            [startpos, startpos + np.array([0, 1]), startpos + np.array([-1, 1]), startpos + np.array([1, 0])]),
              np.array(startpos))  # Z
    elif r == 6:
        return Block(np.array(
            [startpos, startpos + np.array([-1, 0]), startpos + np.array([0, 1]), startpos + np.array([1, 1])]),
            np.array(startpos))  # Z-Reverse


class Board:
    def __init__(self, canvas, blockSize = 10):
        self.matrix = np.zeros((10, 20, 3))
        self.blockSize = blockSize
        self.center = 300
        self.walls = [self.center-5*blockSize, self.center+5*blockSize]
        self.canvas = canvas
        self.canvas.create_line(0,0, 600, 0)
        self.canvas.create_line(600, 600, 600, 0)
        self.canvas.create_line(0, 600, 600, 600)
        self.canvas.create_line(0, 0, 0, 600)
        self.b = True

    def draw(self):
        t1 = time.time()
        for i in range(10):
            for j in range(20):
                if self.matrix[i,j,:].any():
                    self.canvas.create_rectangle(self.walls[0] + i*self.blockSize, j*self.blockSize, self.walls[0] + i*self.blockSize+self.blockSize, j*self.blockSize+self.blockSize, fill="white", tags=(str(self.b)))
        self.b = not self.b
        self.canvas.delete(str(self.b))
        t2 = time.time()
        print(t2-t1)

    def generateBlock(self, block):
        self.block = block
        for i in block.points:
            if i[1] >= 0:
                self.matrix[i[0], i[1]] = [1,0,0]
        self.draw()

    def rotateCCL(self):
        k = []
        for i in range(1, 4):
            k.append((self.block.points[i] - self.block.pivot).dot(
                np.array([[0, -1], [1, 0]])) + self.block.pivot)

        safe = True
        for i in k:
            if i[0] < 0 or i[0] > 9 or i[1] > 19 or i[1] < 0:
                safe = False
                break
        if safe:
            for i in self.block.points:
                self.matrix[i[0], i[1]] = [0, 0, 0]
            for i in range(1, 4):
                self.block.points[i] = k[i-1]
            for i in self.block.points:
                self.matrix[i[0], i[1]] = [1, 0, 0]
            self.draw()

    def rotateCL(self):
        k = []
        for i in range(1, 4):
            k.append((self.block.points[i] - self.block.pivot).dot(
                np.array([[0, -1], [1, 0]])) + self.block.pivot)

        safe = True
        for i in k:
            if i[0] < 0 or i[0] > 9 or i[1] > 19 or i[1] < 0:
                safe = False
                break
        if safe:
            for i in self.block.points:
                self.matrix[i[0], i[1]] = [0, 0, 0]
            for i in range(1, 4):
                self.block.points[i] = k[i-1]
            for i in self.block.points:
                self.matrix[i[0], i[1]] = [1, 0, 0]
            self.draw()

    def moveLeft(self):
        safe = True
        for i in self.block.points:
            b = not (np.equal(i + np.array([-1, 0]), self.block.points).all(axis=1).any())
            if b and (i[0] <= 0 or self.matrix[i[0]-1, i[1]].any()):
                safe = False
                break
        if safe:
            for i in self.block.points:
                self.matrix[i[0], i[1]] = [0, 0, 0]

            for i in range(4):
                self.block.points[i] -= np.array([1,0])

            for i in self.block.points:
                self.matrix[i[0], i[1]] = [1, 0, 0]
            self.block.pivot -= np.array([1,0])
            self.draw()

    def moveRight(self):
        safe = True
        for i in self.block.points:
            b = not (np.equal(i + np.array([1,0]), self.block.points).all(axis=1).any())
            if b and (i[0] >= 9 or self.matrix[i[0]+1, i[1]].any()):
                safe = False
                break
        if safe:
            for i in self.block.points:
                self.matrix[i[0], i[1]] = [0, 0, 0]

            for i in range(4):
                self.block.points[i] += np.array([1, 0])

            for i in self.block.points:
                self.matrix[i[0], i[1]] = [1, 0, 0]
                self.block.pivot += np.array([1, 0])
            self.draw()

    def run(self):
        safe = True
        for i in self.block.points:
            b = not(np.equal(i + np.array([0,1]), self.block.points).all(axis=1).any())
            if b and (i[1] >= 19 or self.matrix[i[0], i[1]+1].any()):
                safe = False
                break
        if safe:
            self.block.pivot += np.array([0, 1])
            for i in self.block.points:
                self.matrix[i[0], i[1]] = [0, 0, 0]
            for i in range(4):
                self.block.points[i] += np.array([0,1])
            for i in self.block.points:
                self.matrix[i[0], i[1]] = [1, 0, 0]
        else:
            self.next()
        self.draw()

    def next(self):
        self.generateBlock(generateRandomBlock())



