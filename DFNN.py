import numpy as np
import scipy as sp
import scipy.special
import math
import random

class DFNN:

    def __init__(self, layers, NpL, rando = False):
        #layers is an int
        #layers will always be at least one

        layers = (int)(layers)
        if layers < 1:
            layers = 1

        self.num_layers = layers

        #NpL is nodes per layer
        #   NpL is a list of int
        
        self.layers = [] #will have num layers of elements

        #NpL[0] corresponds to the number of nodes in the first (inner) layer
        prev = 10
        for x in NpL:
            self.layers.append(np.zeros((x, prev),dtype=np.float64))
            prev = x

        if rando:
            self.randomize()

    def randomize(self):
        #initialize the array with random elements
        #not auto called in cases of copying or genetically modifying
        # new DFNN's to save computations

        for x in self.layers:
            (n, m) = x.shape
            for i in range(n):
                for j in range(m):
                    x[i, j] = random.random()*2 - 1

    def compute(self, inputs):
        #imputs should be a size 10 column vector
        inputs = sp.special.expit(inputs)
        for x in self.layers:
            inputs = x * inputs
            inputs = sp.special.expit(inputs)

        return inputs
