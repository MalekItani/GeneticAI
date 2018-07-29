import random
import Utils
import numpy as np
random.seed(7183924761)

class Terrain:
    def __init__(self, canvas, walls, blockSize = 5):
        self.canvas = canvas
        self.blockSize = blockSize
        self.walls = walls
        self.max_id = 0
        self.food = []
    def addFood(self, pos, color="red"):
        size = self.blockSize
        self.canvas.create_rectangle(pos[0],pos[1], pos[0]+size, pos[1] + size, fill=color, tags=("Food"))
        self.food.append(pos)
    def removeFood(self):
        self.canvas.delete("Food")
        self.food.pop()
        a, b = Utils.generateDistinctPair(600/self.blockSize)
        self.addFood([a*self.blockSize, b*self.blockSize])

class Snake:
    def __init__(self, pos, terrain = None, initSize=4):
        if terrain is None:
            raise Exception('Must specify a terrain')
        self.size = initSize
        self.blockSize = terrain.blockSize;
        self.alive = True
        self.coordinates = []
        self.terrain = terrain
        self.score = 0
        self.aliveTime = 0
        for i in range(initSize):
            self.coordinates.append(pos - np.array([self.blockSize*i,0]))

    def move(self, dir, food = []):
        k = self.coordinates.copy()
        A = k[0] - k[1]
        if dir == 0: # Move forward
            self.coordinates[0] = k[0] + A
        elif dir == 1: # Move right
            self.coordinates[0] = k[0] + np.flip(A, 0)
        else: # Move left
            self.coordinates[0] = k[0] + [A[1],-A[0]]

        for i in range(1, self.size):
            self.coordinates[i] = k[i - 1]

        if self.eats():
            self.coordinates.append(k[i])
            self.size += 1

        if self.wallCollision() or self.selfCollision():
            self.kill()


    def eats(self):
        for i in self.terrain.food:
            if self.coordinates[0][0] == i[0] and self.coordinates[0][1] == i[1]:
                self.terrain.removeFood()
                self.score += 1
                return True
        return False

    def wallCollision(self):
        if self.coordinates[0][0] in self.terrain.walls or self.coordinates[0][1] in self.terrain.walls:
            self.kill()

    def selfCollision(self):
        b = False
        for i in range(1, self.size):
            if self.coordinates[0][0] == self.coordinates[i][0] and self.coordinates[0][1] == self.coordinates[i][1]:
                b = True
        return b

    def kill(self):
        self.alive = False
        self.size = 0
        self.coordinates = [0,0]

    def getDrawableCoordinates(self):
        c = []
        for i in range(len(self.coordinates)):
            c.append(np.array([self.coordinates[i][0], self.coordinates[i][1], self.coordinates[i][0]+self.blockSize, self.coordinates[i][1]+self.blockSize]))
        return tuple(map(tuple, c))

def generatePathSequence(size):
    l = []
    for i in range(size):
        l.append(random.randint(0,2))
    return l

class snakeGenome:
    def __init__(self, snake, path = None, size = 200, mutationRate = 0.01):
        self.snake = snake
        self.size = size
        self.mutationRate = mutationRate
        if path is None:
            self.path = generatePathSequence(size)
        else:
            self.path = path
        self.mutate()

    def checkFitness(self):
        if not self.snake.alive:
            return 30*self.snake.score*self.size + self.snake.aliveTime
        else:
            return 20 + 30*self.snake.score*self.size + self.snake.aliveTime

    def cross(self, g2):
        f1 = self.checkFitness()
        f2 = g2.checkFitness()
        gen2 = snakeGenome(self.snake, size = self.size)
        try:
            norm = f1 / (f1 + f2) * 100
        except ZeroDivisionError:
            return gen2
        for i in range(self.size):
            rdn = random.randint(0, 100)
            if rdn <= norm:
                gen2.path[i] = self.path[i]
            else:
                gen2.path[i] = g2.path[i]
        return gen2

    def mutate(self):
        for i in range(self.size):
            rdn = random.randint(0,100)
            if rdn <= 1:
                self.path[i] = random.randint(0,2)


