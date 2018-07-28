import tkinter as tk
from threading import Thread
from time import sleep
import random
import Utils

root = tk.Tk()
root.geometry("400x400")

genLabel = tk.Label(master=root)
genLabel.pack()

shi = tk.Label(master=root,text="Hello")
shi.pack()

gen = 0
target = "France will win the 2018 World Cup"

def foo():
    global gen
    l = []
    done = False
    while not done:
        genLabel['text'] = "Generation: " + str(gen)
        for i in range(30):
            if gen > 0:
                genome = l[i]
            else:
                genome = Utils.textGenome(len(target))
            shi['text'] = genome.chromosome
            l.append(genome)
            if genome.checkFitness(target) == 1:
                print("Done")
                done = True
                break
            sleep(0.01)
        l.sort(key=lambda x: x.checkFitness(target), reverse=True)
        lTemp = []
        for i in range(len(l)):
            c1, c2 = Utils.generateDistinctPair(len(l)//2)
            lTemp.append(Utils.cross(l[c1], l[c2], target))
        l = lTemp
        gen += 1

t = Thread(target=foo)
t.start()
root.mainloop()



