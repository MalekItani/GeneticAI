import numpy as np
import random

_ID = 0

def generatePathSequence(size):
    l = []
    for i in range(size):
        l.append([random.randint(0,1), random.randint(0,600)])
    return l

def generateInt(max):
    return random.randint(0, max)


class JumperGenome(object):
    def __init__(self, Player, path=None, size=200, mutationRate = 0.01):
        self.mutationRate = mutationRate
        self.size = size
        self.Player = Player
        if path is None:
            self.path = np.random.randint(0, 100, (600, 600))
        else:
            self.path = path
        self.score = 0
        self.mutate()

    def checkFitness(self):
        return self.score

    def cross(self, g2):
        f1 = self.checkFitness()
        f2 = self.checkFitness()
        gen2 = JumperGenome(self.Player, size=self.size)
        if f1 <= 0 and f2 <= 0:
            return gen2
        else:
            norm = f1/ (f1 + f2) * 100
        mat = np.random.randint(0, 100, (600, 600))//norm
        gen2.path = gen2.path*mat + (1-mat)*self.path
        # for j in range(600):
        #     for i in range(len(self.path)):
        #         rdn = random.randint(0, 100)
        #         if rdn <= norm:
        #             gen2.path[i,j] = self.path[i,j]
        #         else:
        #             gen2.path[i,j] = g2.path[i,j]
        return gen2

    def mutate(self):
        mask = 1-np.random.randint(0, 100, (600, 600))//(100-self.mutationRate*100)
        self.path = self.path*mask



class Block:
    def __init__(self, pos, h, w, id = None):
        self.coordinates = pos # Bottom left corner
        self.height = h
        self.width = w
        if id is None:
            global _ID
            self.id = _ID + 1
            _ID += 1
        else:
            self.id = id

class Obstacle(Block):
    def __init__(self, pos=None, h=None, w=None, id=None, obstacle = None):
        if obstacle is None:
            Block.__init__(self, pos, h, w, id)
        if pos is None:
            Block.__init__(self, pos = obstacle.coordinates, h=obstacle.height, w=obstacle.width, id = id)

class Player(Block):
    def __init__(self, pos=None, h=None, w=None, Player=None, id=None):
        if Player is None:
            Block.__init__(self, pos=pos, h=h, w=w)
            self.alive = True
            self.force = 5
            self.locked = False
            self._speed = 0
            self.score = 0
        elif pos is None:
            Block.__init__(self, pos=Player.coordinates, h=Player.height, w=Player.width, id=id)
            self.alive = Player.alive
            self.force = Player.force
            self.locked = Player.locked
            self._speed = Player._speed
            self.score = Player.score
    def addForce(self, f):
        self.force -= f
    def jump(self):
        self.coordinates -= np.array([0,1])
        if not self.locked:
            self.addForce(22)
            self.locked = True
            self.score -= 10
    def getSpeed(self):
        return self._speed + self.force
    def kill(self):
        self.coordinates = [0,0]
        self.width = 0
        self.height = 0
        self.alive = False

class Terrain(object):
    def __init__(self, canvas, ground):
        self.canvas = canvas
        self.ground = ground
        self.canvas.create_line(0, ground, 600, ground, fill="green")
        self.obstacles = []
        self.players = []
    def run(self, speed = 4):
        new = []
        if len(self.obstacles) == 0 or (self.obstacles[-1].coordinates[0] <= 400 and generateInt(100) <= 1):
            self.generateObstacle()

        if len(self.obstacles) > 0 and self.obstacles[0].coordinates[0] < -self.obstacles[0].width:
            self.canvas.delete(self.obstacles[0].id)
            self.obstacles.pop(0)

        for obs in self.obstacles:
            obs.coordinates -= np.array([1,0])*speed
            id = self.canvas.create_rectangle(obs.coordinates[0], obs.coordinates[1],
                                              obs.coordinates[0] + obs.width, obs.coordinates[1] - obs.height,
                                              fill="blue")
            new.append(Obstacle(obstacle=obs, id=id))
        self.deleteObstacles()
        self.obstacles = new
        new = []
        for player in self.players:
            if player.alive:
                player.score += 1
            if len(self.obstacles) and player.coordinates[0]+player.width > self.obstacles[0].coordinates[0] and player.coordinates[1] > self.obstacles[0].coordinates[1]-self.obstacles[0].height:
                player.kill()
                new.append(Player(Player=player, id=player.id))
            else:
                if player.coordinates[1] >= self.ground or player.coordinates[1] + player.getSpeed() >= self.ground:
                    player.coordinates[1] = self.ground
                    player.force = 5
                    player.score += 3
                    player.locked = False
                else:
                    player.coordinates[1] += player.getSpeed()

                player.addForce(-2)
                id = self.canvas.create_rectangle(player.coordinates[0], player.coordinates[1],
                                                  player.coordinates[0] + player.width,
                                                  player.coordinates[1] - player.height, fill="red")
                new.append(Player(Player=player, id=id))
        self.deletePlayers()
        self.players = new

    def deleteObstacles(self):
        for obs in self.obstacles:
            self.canvas.delete(obs.id)
        self.obstacles = []

    def deletePlayers(self):
        for player in self.players:
            self.canvas.delete(player.id)
        self.players = []

    def addPlayer(self, player):
        id = self.canvas.create_rectangle(player.coordinates[0], player.coordinates[1], player.coordinates[0] + player.width, player.coordinates[1] - player.height, fill="red")
        self.players.append(Player(Player=player, id=id))

    def generateObstacle(self):
        startX = 500
        id = self.canvas.create_rectangle(startX, self.ground, startX + 20, self.ground + 40, fill="blue")
        o = Obstacle([startX, self.ground], 40, 20)
        obs = Obstacle(obstacle=o, id=id)
        self.obstacles.append(obs)

    def clear(self):
        self.deletePlayers()
        self.deleteObstacles()

    def reset(self):
        self.clear()
        self.generateObstacle()

    def getAlive(self):
        s = 0
        for i in self.players:
            if i.alive:
                s+=1
        return s



