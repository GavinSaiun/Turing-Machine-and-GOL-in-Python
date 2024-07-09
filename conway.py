# -*- coding: utf-8 -*-
"""
The Game of Life (GoL) module named in honour of John Conway

This module defines the classes required for the GoL simulation.

Created on Tue Jan 15 12:21:17 2019

@author: shakes
"""
import numpy as np
from scipy import signal
import rle

class GameOfLife:
    '''
    Object for computing Conway's Game of Life (GoL) cellular machine/automata
    '''

    def __init__(self, N=256, finite=False, fastMode=False):
        self.grid = np.zeros((N,N), np.int64)
        self.neighborhood = np.ones((3,3), np.int64) # 8 connected kernel
        self.neighborhood[1,1] = 0 #do not count centre pixel
        self.finite = finite
        self.fastMode = fastMode
        self.aliveValue = 1
        self.deadValue = 0
        
    def getStates(self):
        '''
        Returns the current states of the cells
        '''
        return self.grid
    
    def getGrid(self):
        '''
        Same as getStates()
        '''
        return self.getStates()
               
    def evolve(self):
        '''
        Given the current states of the cells, apply the GoL rules:
        - Any live cell with fewer than two live neighbors dies, as if by underpopulation.
        - Any live cell with two or three live neighbors lives on to the next generation.
        - Any live cell with more than three live neighbors dies, as if by overpopulation.
        - Any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction
        '''
        #get weighted sum of neighbors
        #PART A & E CODE HERE

        # # Convolution Method
        """
        how does direct convolve work:
        the kernal matrix is flipped around, however, because the kernal matrix is symmetrical, the result is the same
        the kernel matrix is slid across each element in the grid

        each element in the kernal matrix is multiplied by its corresponding grid element and summed together
        this would produce a output greater than the input, 
        mode = 'same' ensures that the grid's size is constrained within self.grid

        method is defaulted to auto, thus, chooses either direct of FFt (fourier transform) depending on which is fastest
        fft is used with large inputs

        how fftconvolve works is that each element in the kernel and grid is treated as a polynomial function
        the coefficients of the functions are complex numbers evenly spaced within the complex plane
        This allows the function to have a lot of redundancy in its different terms

        computational time of fft is Nlog(N) compared to direct which is N^2


        How does fft apply in gol:
        1. compute the fft of both grid and kernel (treating the values as a polynomial with coefficients in the complex plane)
        2. multiply pointwise the grid and kernel
        3. compute a inverse fourier transform on the output to obtain the convolution

        https://www.youtube.com/watch?v=KuXjwB4LzSA&t=656s
        https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.convolve.html
        
        """
        if self.fastMode == True:
            newGrid = np.copy(self.grid)
            # weighted_sum = signal.convolve2d(self.grid, self.neighborhood, mode='same', boundary='wrap')
  
            # returns an array containing the weightedSums of the alive neighbours
            weightedSum = signal.convolve(self.grid, self.neighborhood, mode='same')

            # Boolean Array Indexing Method
            # newGrid[(self.grid == self.aliveValue) & ((weightedSum < 2) | (weightedSum > 3))] = self.deadValue
            # newGrid[(self.grid == self.deadValue) & (weightedSum == 3)] = self.aliveValue

            # Numpy Where Method
            newGrid = np.where((self.grid == self.aliveValue) & ((weightedSum < 2) | (weightedSum > 3)), self.deadValue, self.grid)
            newGrid = np.where((self.grid == self.deadValue) & (weightedSum == 3), self.aliveValue, newGrid)
            self.grid = newGrid


        if self.fastMode == False:
            #Create a Copy of the grid
            newGrid = np.copy(self.grid)

            # Find the numbers of rows and columns in the Grid
            rows, columns = self.grid.shape

            # Iterate through each cell
            for row in range(rows):
                for column in range(columns):
                    aliveNeighbours = 0

                    # Find the neighbouring cells state
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            # Skip the current cell
                            if i == 0 and j == 0:
                                continue
                            
                            neighborRow = row + i
                            neighborColumn = column + j
                            # Check if the neighbor is within bounds
                            if 0 <= neighborRow < rows and 0 <= neighborColumn < columns:
                                # If the neighbor is alive, increment aliveValues
                                if self.grid[neighborRow][neighborColumn] == self.aliveValue:
                                    aliveNeighbours += 1

                    # GOL conditions
                    if aliveNeighbours < 2 or aliveNeighbours > 3:
                        newGrid[row][column] = self.deadValue

                        
                    else:  # For dead cells
                        if aliveNeighbours == 3:
                            newGrid[row][column] = self.aliveValue

            #implement the GoL rules by thresholding the weights
            #PART A CODE HERE
            
            #update the grid
            self.grid = newGrid #UNCOMMENT THIS WITH YOUR UPDATED GRID
    
    def insertBlinker(self, index=(0,0)):
        '''
        Insert a blinker oscillator construct at the index position
        '''
        self.grid[index[0], index[1]+1] = self.aliveValue
        self.grid[index[0]+1, index[1]+1] = self.aliveValue
        self.grid[index[0]+2, index[1]+1] = self.aliveValue
        
    def insertGlider(self, index=(0,0)):
        '''
        Insert a glider construct at the index position
        '''
        self.grid[index[0], index[1]+1] = self.aliveValue
        self.grid[index[0]+1, index[1]+2] = self.aliveValue
        self.grid[index[0]+2, index[1]] = self.aliveValue
        self.grid[index[0]+2, index[1]+1] = self.aliveValue
        self.grid[index[0]+2, index[1]+2] = self.aliveValue
        
    def insertGliderGun(self, index=(0,0)):
        '''
        Insert a glider construct at the index position
        '''
        self.grid[index[0]+1, index[1]+25] = self.aliveValue
        
        self.grid[index[0]+2, index[1]+23] = self.aliveValue
        self.grid[index[0]+2, index[1]+25] = self.aliveValue
        
        self.grid[index[0]+3, index[1]+13] = self.aliveValue
        self.grid[index[0]+3, index[1]+14] = self.aliveValue
        self.grid[index[0]+3, index[1]+21] = self.aliveValue
        self.grid[index[0]+3, index[1]+22] = self.aliveValue
        self.grid[index[0]+3, index[1]+35] = self.aliveValue
        self.grid[index[0]+3, index[1]+36] = self.aliveValue
        
        self.grid[index[0]+4, index[1]+12] = self.aliveValue
        self.grid[index[0]+4, index[1]+16] = self.aliveValue
        self.grid[index[0]+4, index[1]+21] = self.aliveValue
        self.grid[index[0]+4, index[1]+22] = self.aliveValue
        self.grid[index[0]+4, index[1]+35] = self.aliveValue
        self.grid[index[0]+4, index[1]+36] = self.aliveValue
        
        self.grid[index[0]+5, index[1]+1] = self.aliveValue
        self.grid[index[0]+5, index[1]+2] = self.aliveValue
        self.grid[index[0]+5, index[1]+11] = self.aliveValue
        self.grid[index[0]+5, index[1]+17] = self.aliveValue
        self.grid[index[0]+5, index[1]+21] = self.aliveValue
        self.grid[index[0]+5, index[1]+22] = self.aliveValue
        
        self.grid[index[0]+6, index[1]+1] = self.aliveValue
        self.grid[index[0]+6, index[1]+2] = self.aliveValue
        self.grid[index[0]+6, index[1]+11] = self.aliveValue
        self.grid[index[0]+6, index[1]+15] = self.aliveValue
        self.grid[index[0]+6, index[1]+17] = self.aliveValue
        
        # Incorrect position, should be +1
        # self.grid[index[0]+6, index[1]+17] = self.aliveValue
        self.grid[index[0]+6, index[1]+18] = self.aliveValue

        self.grid[index[0]+6, index[1]+23] = self.aliveValue
        self.grid[index[0]+6, index[1]+25] = self.aliveValue
        
        self.grid[index[0]+7, index[1]+11] = self.aliveValue
        self.grid[index[0]+7, index[1]+17] = self.aliveValue
        self.grid[index[0]+7, index[1]+25] = self.aliveValue
        
        self.grid[index[0]+8, index[1]+12] = self.aliveValue
        self.grid[index[0]+8, index[1]+16] = self.aliveValue
        
        self.grid[index[0]+9, index[1]+13] = self.aliveValue
        self.grid[index[0]+9, index[1]+14] = self.aliveValue
        
    def insertFromPlainText(self, txtString, pad=0):
        '''
        Assumes txtString contains the entire pattern as a human readable pattern without comments
        '''

        
        lines = txtString.split('\n')
        for rowNum, row in enumerate(lines):

            # Ignore any lines containing information other than the initial pattern
            if "!" in row:
                continue

            # Inserts a live cell in grid if the element contains O i.e. alive
            for columnNum, column in enumerate(row):
                if column == 'O':
                   self.grid[rowNum + pad, columnNum + pad] = self.aliveValue

            
    def insertFromRLE(self, rleString, pad=0):
        '''
        Given string loaded from RLE file, populate the game grid

        How to read RLE files:
        1. b: dead cell, c: alive cell, $: end of line
        2. Dead cells at the end of line do not need to be encoded
        3. whitespaces are not permitted
        4. lines must not exceed 70 characters
        5. Anything after the ! is ignored
        6. e.g. 2bo with column = 5, == bbobb




        How does RLE class work:
        1. calling rle calls both its method populateAttribute and populatePattern
        2. populateAttribute parses the string and allocates each attribute to its corresponding value
        3. populatePattern makes the initial pattern to be in a readable form, e.g. fills in the empty spaces
        4. pattern_2d_array is the result of populatePattern, i.e. the readable form of rle

        '''

        # Create a instance of RLE, this initiates populateAttribute and populatePattern
        rleInstance = rle.RunLengthEncodedParser(rle_string=rleString)

        # pattern_2d contains the initial position of live cells, if any element contains 'o', insert a live cell in grid
        for rowNum, row in enumerate(rleInstance.pattern_2d_array):       
            for columnNum, column in enumerate(row):

                if column == 'o':
                    self.grid[rowNum + pad, columnNum + pad] = self.aliveValue

            