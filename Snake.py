import tkinter as tk
from threading import Thread
from time import sleep
import random
import numpy as np
import shipUtils
import Utils
import snakeUtils
import keyboard

root = tk.Tk()
root.geometry("600x600")

genLabel = tk.Label(master=root)
genLabel.pack()

stepsLabel = tk.Label(master=root)
stepsLabel.pack()

canvas = tk.Canvas(root, width=600, height=600)
canvas.pack()

gen = 0

def drawSnake(snake):
    for co in snake.getDrawableCoordinates():
        canvas.create_rectangle(co, fill="white", tags=("Snake"))

def foo():
    global gen
    done = False
    nChromosomes = 200
    popSize = 25
    genomes = []
    walls = [0, 600, 0, 600]
    terrain = snakeUtils.Terrain(canvas, walls, blockSize= 10)
    # snake = snakeUtils.Snake(pos=[70, 70], terrain=terrain)
    terrain.addFood([300, 300])
    while not done:
        # canvas.delete("Snake")
        # genLabel['text'] = "Score: " + str(snake.score)
        # drawSnake(snake)
        # if keyboard.is_pressed('right'):
        #     snake.move(1)
        # elif keyboard.is_pressed('left'):
        #     snake.move(2)
        # elif keyboard.is_pressed('q'):
        #     quit()
        # else:
        #     snake.move(0)
        # sleep(0.1)
        # if not snake.alive:
        #     sleep(3)
        #     snake = snakeUtils.Snake(pos=[70, 70], terrain=terrain)
        if gen%2 == 0:
            nChromosomes += 50
            for genome in genomes:
                genome.path += snakeUtils.generatePathSequence(50)
                genome.size += 50
        canvas.delete("all")
        terrain.addFood([300, 300])
        genLabel['text'] = "Generation: " + str(gen)
        stepsLabel['text'] = "Number of steps: " + str(nChromosomes)
        for i in range(popSize):
            if not gen:
                snake = snakeUtils.Snake(pos=[70, 70],initSize=4, terrain=terrain)
                snakeGenome = snakeUtils.snakeGenome(snake, size=nChromosomes)
                genomes.append(snakeGenome)
            else:
                snake = snakeUtils.Snake(pos=[70, 70],initSize=4, terrain=terrain)
                genomes[i].snake = snake
        print(genomes[0].size)
        genomes.sort(key=lambda x: x.checkFitness(), reverse=True)
        for i in range(nChromosomes):
                canvas.delete("Snake")
                b = True
                for j in range(popSize):
                    snake = genomes[j].snake
                    if snake.alive:
                        snake.aliveTime += 1
                        b = False
                        for co in snake.getDrawableCoordinates():
                            canvas.create_rectangle(co, fill = "white", tags=("Snake"))
                        snake.move(genomes[j].path[i])
                sleep(0.01)
                if b:
                    break
        aTemp = []
        for i in range(popSize):
            p1, p2 = Utils.generateDistinctPair(popSize // 2)
            g1 = genomes[p1]
            g2 = genomes[p2]
            aTemp.append(g1.cross(g2))
        genomes = aTemp
        print([x.checkFitness() for x in genomes])
        gen+=1



t = Thread(target=foo)
t.start()
root.mainloop()



