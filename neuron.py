import numpy as np
import math as mt
import random as ra
import time as ti

sigmoid = lambda x: 1/(1+mt.exp(-x))
def muter( var, magn=5):
    return var + ra.randint(-magn*1000, magn*1000)/1000

class AiNeural:
    def __init__(self, gen_mode = "zero", copy_data = []) :

        if gen_mode == "zero":
            npList = lambda x: np.array([0 for i in range(x)])
            # Neurones : a => Valeur neurones, weights => Importance de l'entrée associée,
            # biases => Changement positionel de l'activation du sigmoïde (fonction de la neurone)
            self.a = [npList(15), npList(7), npList(6), npList(3)]
            self.biases = [npList(7), npList(6), npList(3)]
            self.weights = [np.array([[0 for j in range(15)] for i in range(7)]),
                            np.array([[0 for j in range(7)] for i in range(6)]),
                            np.array([[0 for j in range(6)] for i in range(3)])]
        elif gen_mode == "hasard":
            rai = lambda x : ra.randint(-x*100, x*100)/100
            npList = lambda x, x1: np.array([rai(x1) for i in range(x)])

            # Neurones : a => Valeur neurones, weights => Importance de l'entrée associée,
            # biases => Changement positionel de l'activation du sigmoïde (fonction de la neurone)
            self.a = [npList(15, 0), npList(7, 0), npList(6, 0), npList(3, 0)]
            self.biases = [npList(7, 10), npList(6, 10), npList(3, 0)]
            self.weights = [np.array([[rai(10) for j in range(15)] for i in range(7)]),
                            np.array([[rai(10) for j in range(7)] for i in range(6)]),
                            np.array([[rai(10) for j in range(6)] for i in range(3)])]
        elif gen_mode == "copy":
            # Recopiage des données à copier
            npList = lambda x: np.array([0 for i in range(x)])
            # Neurones : a => Valeur neurones, weights => Importance de l'entrée associée,
            # biases => Changement positionel de l'activation du sigmoïde (fonction de la neurone)
            self.a = [npList(15), npList(7), npList(6), npList(3)]
            self.weights = copy_data["weights"]
            self.biases = copy_data["biases"]
    def nprint(self):
        print("{")
        print("\"weights\" : [", end="")
        for i in range(3):
            print("np.array(",end = "")
            print([[f for f in j] for j in self.weights[i]], end=")")
            if i != 3:
                print(",",end = "")
        print("],")
        print("\"biases\" : [", end="")
        for i in range(3):
            print(" np.array(", end="")
            print([j for j in self.biases[i]], end=")")
            if i != 3:
                print(",", end="")
        print("]")
        print("}")

    def mutation(self, Ai_parent, magn = 5):
        bs = Ai_parent.biases
        ws = Ai_parent.weights
        self.biases = [np.array([muter(bs[0][i], magn) for i in range(7)]), np.array([muter(bs[1][i], magn) for i in range(6)]), np.array([muter(bs[2][i], magn) for i in range(3)])]
        self.weights = [np.array([[muter(ws[0][i][j], magn) for j in range(15)] for i in range(7)]),
                        np.array([[muter(ws[1][i][j], magn) for j in range(7)] for i in range(6)]),
                        np.array([[muter(ws[2][i][j], magn) for j in range(6)] for i in range(3)])]
        return self
    def _input(self,vector, mode_list = "list"):
        if mode_list == "np_processed":
            self.a[0] = vector
        else:
            # sigmoid(0.4*x-4)
            self.a[0] = np.array([i/48 for i in vector[0:12]] +
                                 [sigmoid(0.4*vector[12]-4)] +
                                 [sigmoid(0.5 * vector[13]-9), sigmoid(0.5*vector[14]-9)])
    def _output(self):
        for i in range(3):
            # [12,9,10]
            # [3,-1,19]
            # => zip = [(12,3),(9,-1),(10,19)]
            self.a[i+1] = np.array([sigmoid(np.dot(self.a[i],w) + b) for b, w in zip(self.biases[i], self.weights[i])])
        res = self.a[-1]
        return ((res[0] * 100 + res[1] * 10 + res[2]) - 55.5)/0.555

