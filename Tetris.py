import tkinter as tk
from threading import Thread
from time import sleep
import numpy as np
import Utils.Utils as Utils
import Utils.tetrisUtils as tetrisUtils
import keyboard


root = tk.Tk()
root.geometry("600x600")

genLabel = tk.Label(master=root)
genLabel.pack()

canvas = tk.Canvas(root, width=600, height=600)
canvas.pack()
gen = 0


L = tetrisUtils.Block(np.array([[5, 5], [5, 6], [5, 7], [6, 5]]), np.array([5,5]))

def foo():
    global gen
    board = tetrisUtils.Board(canvas, blockSize=25)
    board.generateBlock(L)
    while True:
        if keyboard.is_pressed('left'):
            board.moveLeft()
        elif keyboard.is_pressed('right'):
            board.moveRight()
        elif keyboard.is_pressed('up'):
            board.rotateCCL()
        elif keyboard.is_pressed('down'):
            board.rotateCL()
        board.run()
        sleep(0.3)
    x = True



t = Thread(target=foo)
t.start()
root.mainloop()



