from math import *
import numpy as np
import matplotlib.pyplot as plt

class SOM():
    def __init__(self, inputs, weights, sigma=1, learning_rate=1, sigma_decrease_rate=0):
        self.inputs = np.array(inputs) # all the inputs for the network
        self.w = np.array(weights) # weight matrix ( also defines the number of neurons )
        self.sigma = sigma # neighbor kernel size for hk
        self.eta = learning_rate
        self.sigma_decrease_rate = sigma_decrease_rate
        print("\n")
        print("<>"*25)
        print("INSTANTIATING A SELF-ORGANIZING MAP!")
        print("\n> PARAMETERS LIST:\n")
        print("Initial weights: \n{}\n".format(self.w))
        print("Inputs: \n{}\n".format(self.inputs))
        print("Neighbor kernel size: \n{}\n".format(self.sigma))
        print("Learning rate: \n{}\n".format(self.eta))
        print("Sigma decreasing rate: \n{}\n".format(self.sigma_decrease_rate))
        print("<>"*25)
        print("\n")

    def _euc_dist(self, v1, v2):
        if len(v1) != len(v2):
            print("Error: Vectors of diferent sizes...")
            return -1
        _sum = 0
        for i in range(len(v1)): _sum += (v1[i]-v2[i])**2
        return sqrt(_sum)

    def hk(self, wk, wj):
        delta = wk-wj
        coeficient = delta**2
        square_base = 2*(self.sigma**2)
        coeficient = coeficient/square_base
        e = 1/exp(coeficient)
        #e = exp(-((delta)**2)/(2*(self.sigma**2)))
        print("para {} e {}".format(wk, wj))
        print("\te: ", e)
        print("\tSigma: ",self.sigma)
        self.sigma -= self.sigma_decrease_rate
        return e

    def delta_w(self,k,x,ignore_hk=False):
        # k = winner idx
        # x = input
        delta_w = np.zeros(self.w.shape)
        for j in range(len(self.w)):
            for idx in range(len(self.w[j])):
                if ignore_hk:
                    if k == j:
                        delta_w[j][idx] = self.eta * (x[idx] - self.w[k][idx])
                else:
                    delta_w[j][idx] = self.eta * self.hk(self.w[k][idx], self.w[j][idx]) * (x[idx] - self.w[k][idx])
        return delta_w

    def find_k(self, x):
        # k = winner idx
        s = [self._euc_dist(x, weight) for weight in self.w]
        return np.argmin(s)

    def train(self, ignore_hk=False, display=False):
        np.set_printoptions(precision = 2, suppress=True)
        for iteration, x in enumerate(self.inputs):
            delta_w = self.delta_w(self.find_k(x),x, ignore_hk)
            if display:
                print("="*50)
                print("ITERATION <{}>".format(iteration+1))
                print("w = \n{}\n".format(self.w))
                print("input = \n{}\n".format(x))
                print("delta w = \n{}\n".format(delta_w))
                print("new w = \n{}\n".format(delta_w + self.w))
            self.w = delta_w + self.w

    def linear2matrix(self,linear,matrix):
        row = int(linear/len(matrix))
        col = int(linear%len(matrix))
        return (row, col)

    def _med(self,p1,p2):
        # median point
        M  = ( (p1[0] + p2[0])/2, (p1[1] + p2[1])/2 )
        # angular coeficient of (p1,p2).
        m1 = (p1[1]-p2[1])/(p1[0]-p2[0])
        # angular coeficient of the perpendicular line of (p1,p2) that pass throught the median
        mM = -1/m1
        # y - My = mM * (x - Mx)
        return (M,mM)

    def prediction_line(self,display=False):
        # works only if there is 2 neurons
        p, m = self._med(self.w[0],self.w[1])
        print( "y - {} = {} * (x - {})".format(p[1],m,p[0]) )
        print( "---> y = ({})*x + ({})".format(m,m*p[0]-p[1]))
        return (p,m)

    def predict(self, inputs, ignore_hk=False, display=False):
        neurons = []
        for x in inputs:
            x = np.array(x)
            neuron = [self._euc_dist(x,weight) for weight in self.w]
            idx = neuron.index(max(neuron))
            neuron = [1 if i==idx else 0 for i in range(len(neuron))]
            neurons.append(neuron)
            if display: print( "{} - {}".format(x,neuron) )
        return neurons

