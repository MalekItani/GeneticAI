import tkinter as tk
from threading import Thread
from time import sleep
import random
import numpy as np
import Utils.shipUtils as shipUtils
import Utils.Utils as Utils


root = tk.Tk()
root.geometry("600x600")

genLabel = tk.Label(master=root)
genLabel.pack()

canvas = tk.Canvas(root, width=600, height=600)
canvas.pack()
canvas.create_rectangle(500, 275, 550, 325, fill="red")
canvas.create_rectangle(275, 200, 325, 400, fill="green")
gen = 0


def foo():
    global gen
    size = 200
    done = False
    popSize = 25
    target = [500,275]
    start = [75, 300]
    barrier = [[275, 325],[200, 400]]
    genomes = []
    x = True
    while not done:
        genLabel['text'] = "Generation: " + str(gen)
        for i in range(popSize):
            if gen == 0:
                pawn = shipUtils.Pawn(pos=np.array(start), size=3)
                genome = shipUtils.pawnGenome(size, pawn)
                genomes.append(genome)
            else:
                pawn = shipUtils.Pawn(pos=np.array(start), size=3)
                genomes[i].pawn = pawn
        for i in range(size):
            for j in range(popSize):
                Pawn = genomes[j].pawn
                if Pawn.isAlive:
                    canvas.create_polygon(Pawn.coordinates, fill="blue", tags=('pawn' + str(x)))
                    Pawn.moveForward(speed=4)
                    Pawn.rotate(genomes[j].path[i])
                    if Pawn.collidesWith(barrier[0], barrier[1]):
                        Pawn.kill()
                    genomes[j].pawn = Pawn
            x = not x
            canvas.delete("pawn" + str(x))
            sleep(0.005)

        genomes.sort(key=lambda x: x.checkFitness(target))
        aTemp = []
        for i in range(popSize):
            p1, p2 = Utils.generateDistinctPair(popSize // 3)
            g1 = genomes[p1]
            g2 = genomes[p2]
            if not g1.pawn.isAlive:
                g1 = shipUtils.pawnGenome(g1.size, g1.pawn)
            if not g2.pawn.isAlive:
                g2 = shipUtils.pawnGenome(g2.size, g2.pawn)
            aTemp.append(g1.cross(g2, target))

        genomes = aTemp
        for i in range(len(genomes)):
            if genomes[i].checkFitness(target) <= 50:
                done = True
                print("Done")
                break
        print([x.checkFitness(target) for x in genomes])
        gen += 1


t = Thread(target=foo)
t.start()
root.mainloop()



