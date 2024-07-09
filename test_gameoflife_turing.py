# -*- coding: utf-8 -*-
"""
Game of life script with animated evolution

Created on Tue Jan 15 12:37:52 2019

@author: shakes
"""



"""
The Turing machine is a abstract machine that manipulates symbols on a infinite tape according to its source code.
It is capable to implementing all computer algorithms, tho may take some time.

Turing completeness: the ability of a computational system to simulate a turing machine
To show that something is Turing-complete, it is enough to demonstrate that it can be used to simulate some Turing-complete system

https://en.wikipedia.org/wiki/Turing_machine#:~:text=A%20Turing%20machine%20is%20a,A%20physical%20Turing%20machine%20model.
http://rendell-attic.org/gol/tm.htm



Turing Machine in GOL:
The turing machine reads input symbols from the turing tape,
performs computations based on the rules in the FSM, and then updates the tape
accordingly. Repeat until the computation halts or completion of computation.

Components:
1. Turing Tape
    Uses 2 stacks. The tape moves back and forth past the FSM read/write head
    first stack is for popping
    second stack is for pushing


2. FSM: 
    Contains memory cells arranged in rows and columns, Each memory cell represents a specific state in the TM
    FSM uses row and column addressing to access specific memory cells
    row address determines the current state
    column address represents the symbol read from the stack
    At the selected memory cell, a collision occurs, resulting an output of stored pattern of gliders
    output is collected by 8 LWSSes, inverted and inputted into the signal Detector

    Input: Input symbol and Current state
    Output: Whether to Push/Pop next state and what symbol to Push/Pop, in 8 glider format (e.g. DVVVSSSS)

3. Signal Detector
    Links the FSM to the Turing Tape
    Detects output from FSM and generates inputs for the CONTROL CONVERSION logic
    Sends back next state to FSM
    provides a method for halting the machine



4. Control Conversion
    Input: Signal detector offers 2 inputs, the 8 glider stream (Push/Pop and what symbol) and presence of signal
    Output: Controls stack operations (Pop or Push)

5. Stack
    Memory/Symbol values is stored in the Stack cells. 
    This stack can increase the number of cells to fit its need (infinite)

6. Push and Pop operations
    How TM push (add symbol):
    1. create new stack cell and places new symbol into that cell
    2. all cells are moved one cell away from control end

    HOW TM pops (reads/remove symbol):
    1. removes topmost stack cell from stack, sends symbol into FSM
    2. all cells are moved once cell towards control end

    

Is this GOL Turing Complete?

To be turing complete, it must be able to compute anything that a TM can do.
i.e. it must have a FSM with a tape and head

Criteria of a TM

1. Infinite long Tape
This critieria if fulfilled as the Stack can be POP and PUSH, making storage realistically infinite,
as the GOL when needed to, can simply create a empty cell when pushing

2. Head
GOL has a read/write head positioned over a single cell on the tape, and
is able to read/write/move the cell

3. Tape Alphabet
tape alphabet is {1, 0, _}

4. Transition Rules for tape
This is governed by whether the FSM decides to Pop or Push
if Push, push all cells right
if Pop, push all cells left

5. Reject state
idk


FSM COMPONENT 
1. Alphabet
alphabet is {1,0} or i think?

2. States
The GOL FSM has 3 states and 3 symbols

3. Transition Function
transition function is seen in the memory cells in FSM.
When the FSM receives a symbol and state, it will locate a memory cell using row 
and column addressing, which will output the next symbol and state in the form of 8 gliders 


4. Accept state
"It will stop with twice this number on the right"
From this sentence, i assume the GOL's accept state is when the initial state's
symbols are doubled in size

5. Initial State
"It is shown in this picture starting with a 2 1's on the tape to the right".
From this sentence, i assume the intial state is 110 or 11 _


Overall, beacuse the GOL fulfills are criterias for a TM
this GOL is turing complete.


http://rendell-attic.org/gol/tm.htm

"""



import conway

padding = 10

#read RLE file
#~ with open("gosperglidergun.rle", "r") as text_file:
with open("turingmachine.rle", "r") as text_file:
        rleString = text_file.read()
        

#create the game of life object, Set fastMode to True for convolution
life = conway.GameOfLife(fastMode=True, N=2048)
life.insertFromRLE(rleString, padding)
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

interval = 50 #ms

#animate 24 frames with interval between them calling animate function at each frame
ani = animation.FuncAnimation(fig, animate, frames=24, interval=interval, blit=True)
#~ animate(0)

plt.show()
