import tkinter as tk
from threading import Thread
from time import sleep
import Utils.JumperUtils as JumperUtils
import Utils.Utils as Utils

root = tk.Tk()
root.geometry("600x600")
genLabel = tk.Label(master=root)
genLabel.pack()

canvas = tk.Canvas(root, width=600, height=600)
canvas.pack()
gen = 0


def foo():
    ground = 300
    popSize = 10
    size = 2000
    terrain = JumperUtils.Terrain(canvas, ground)
    player = JumperUtils.Player(pos=[10, ground], h=20, w=20)
    terrain.addPlayer(player)
    terrain.generateObstacle()
    genomes = []
    gen = 0
    while True:
        genLabel['text'] = "Generation: " + str(gen)
        for i in range(popSize):
            if gen == 0:
                player = JumperUtils.Player(pos=[10, ground], h=20, w=20)
                genome = JumperUtils.JumperGenome(Player=player, size=size)
                genomes.append(genome)
                terrain.addPlayer(player)
            else:
                player = JumperUtils.Player(pos=[10, ground], h=20, w=20)
                genomes[i].Player = player
                terrain.addPlayer(player)
        i = 0
        while(terrain.getAlive() and i < size):
            terrain.run(6)
            if len(terrain.obstacles):
                fOb = terrain.obstacles[0]
                x1 = fOb.coordinates[0]
            else:
                x1 = 599
            if len(terrain.obstacles)>1:
                sOb = terrain.obstacles[0]
                x2 = sOb.coordinates[0]
            else:
                x2 = 599
            for j in range(popSize):
                if not genomes[j].path[x1, x2]:
                    terrain.players[j].jump()
                    genomes[j].score = terrain.players[j].score
            i += 1
            sleep(0.02)
        genomes.sort(key=lambda x: x.checkFitness(), reverse=True)
        print([x.checkFitness() for x in genomes])
        aTemp = []
        for i in range(popSize):
            p1, p2 = Utils.generateDistinctPair(popSize // 3)
            g1 = genomes[p1]
            g2 = genomes[p2]
            aTemp.append(g1.cross(g2))
        genomes = aTemp
        terrain.reset()
        gen += 1
        # terrain.run(5)
        # if seq[i]:
        #     print('1')
        #     for i in range(len(terrain.players)):
        #         terrain.players[i].jump()
        # sleep(0.1)
        # i += 1
        # if len(terrain.players) == 0:
        #     print("Called")
        #     terrain.reset()
        #     terrain.addPlayer(JumperUtils.Player(pos=[10, ground], h=20, w=20))

t = Thread(target=foo)
t.start()
root.mainloop()




