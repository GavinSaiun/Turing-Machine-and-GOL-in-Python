# -*- coding: utf-8 -*-
"""
Game of life script with animated evolution

Created on Tue Jan 15 12:37:52 2019

@author: shakes
"""
import conway

# N = 64
N = 1024
N = 64
"""
Below are the initial patterns that are greater than 20x20


https://conwaylife.com/wiki

"""


#create the game of life object
life = conway.GameOfLife(N, fastMode=True)
# life.insertBlinker((0,0))
# life.insertGlider((0,0))

# I ADDED THIS
# life.insertGliderGun((10,20))

# MULTIPLE INITiAL PAtTERNS GREATER THAN 20x20

# with open('54p94.cells', "r") as text_file:
#         cellString = text_file.read()
# life.insertFromPlainText(cellString, 10)

# with open('117p18.cells', "r") as text_file:
#         cellString = text_file.read()
# life.insertFromPlainText(cellString, 10)

# with open('66p62.cells', "r") as text_file:
#         cellString = text_file.read()
# life.insertFromPlainText(cellString, 10)

"""

change fastMode to True:

"""

# with open('256x256.cells', "r") as text_file:
#         cellString = text_file.read()
# life.insertFromPlainText(cellString, 10)

# with open('dragon.rle', "r") as text_file:
#         rleString = text_file.read()
# life.insertFromRLE(rleString, 30)

# with open('110p62.rle', "r") as text_file:
#         rleString = text_file.read()A
# life.insertFromRLE(rleString, 10)

# with open('p184gun.rle', "r") as text_file:
#         rleString = text_file.read() 
# life.insertFromRLE(rleString, 10)


cells = life.getStates() #initial state

#-------------------------------
#plot cells
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig = plt.figure()

plt.gray()

img = plt.imshow(cells, animated=True)

def animate(i):
    """perform animation step"""
    global life
    
    life.evolve()
    cellsUpdated = life.getStates()
    
    img.set_array(cellsUpdated)
    
    return img,

interval = 200 #ms

#animate 24 frames with interval between them calling animate function at each frame
ani = animation.FuncAnimation(fig, animate, frames=24, interval=interval, blit=True)

plt.show()
