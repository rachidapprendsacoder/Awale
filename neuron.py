import copy

import numpy as np
import math as mt
import random as ra
from ouverture import *
from middle import *
from end import *
import time as ti
import threading
import ast
COMPO = [8,3,1]
def muter( var, magn=5):
    return var + ra.randint(-magn*1000, magn*1000)/1000
def sigmoid(x):
    if abs(x) < 99:
        return 1 / (1 + mt.exp(-x))
    elif x < 0 :
        return 0
    return 1


def scalaire(li1, li2):
    somme = 0
    for ele1, ele2 in zip(li1, li2):
        somme += ele1 * ele2
    return somme


class AiNeural:

    def __init__(self, gen_mode = "zero", copy_data = []) :

        if gen_mode == "zero":
            li = lambda x: np.array([0.0 for i in range(x)])
            # Neurones : a => Valeur neurones, weights => Importance de l'entrée associée,
            # biases => Changement positionel de l'activation du sigmoïde (fonction de la neurone)
            self.a = [li(i) for i in COMPO]
            self.biases = [li(i) for i in COMPO[1:]]
            self.weights = [[[0.0 for k in range(COMPO[i])] for j in range(comp)] for i,comp in
                            enumerate(COMPO[1:])]
            """
            self.weights = [np.array([[0.0 for j in range(14)] for i in range(7)]),
                            np.array([[0.0 for j in range(7)] for i in range(6)]),
                            np.array([[0.0 for j in range(6)] for i in range(3)])]
            """
        elif gen_mode == "hasard":
            rai = lambda x : ra.randint(-x*100, x*100)/100
            li_rai = lambda x, x1: np.array([rai(x1) for i in range(x)])

            # Neurones : a => Valeur neurones, weights => Importance de l'entrée associée,
            # biases => Changement positionel de l'activation du sigmoïde (fonction de la neurone)
            self.a = [li_rai(i, 0) for i in COMPO]
            self.biases = [li_rai(i, 10) for i in COMPO[1:]]
            self.weights = [[[rai(10) for k in range(COMPO[i])] for j in range(comp)] for i, comp in
                            enumerate(COMPO[1:])]
        elif gen_mode == "copy":
            # Recopiage des données à copier
            li = lambda x: np.array([0.0 for i in range(x)])

            self.a = [li(i) for i in COMPO]
            self.weights = copy_data["weights"]
            self.biases = copy_data["biases"]
    def nprint(self):
        print("{")
        print("\"weights\" : [", end="")
        for i in range(len(self.biases)):
            print([[f for f in j] for j in self.weights[i]])
            if i != len(self.biases)-1:
                print(",",end = "")
        print("],")
        print("\"biases\" : [", end="")
        for i in range(len(self.biases)):
            print([j for j in self.biases[i]])
            if i != len(self.biases)-1:
                print(",", end="")
        print("]")
        print("}")
    def nwrite(self, titre = 'copy_data.txt'):
        with open(titre, 'w') as f:
            # Append data to the file
            f.write('copy data: \n')
            f.write("{")
            f.write("\"weights\" : [")
            for i in range(len(self.weights)):
                f.write(str([[f for f in j] for j in self.weights[i]]))
                if i != len(self.biases) - 1:
                    f.write(",")
            f.write("],")
            f.write("\"biases\" : [")
            for i in range(len(self.biases)):
                f.write(str([j for j in self.biases[i]]))
                if i != len(self.biases) - 1:
                    f.write(",")
            f.write("]")
            f.write("}\n")
            f.write("________________\n")



    def _input(self,vector, mode_list = "list"):
        if mode_list == "np_processed":
            self.a[0] = vector
        else:
            #
            self.a[0] = list(interpret_game(vector))


    def _output(self):
        for i in range(2):
            # [12,9,10]
            # [3,-1,19]
            # => zip = [(12,3),(9,-1),(10,19)]
            self.a[i+1] = np.array([sigmoid(scalaire(self.a[i], w) + b) for b, w in zip(self.biases[i], self.weights[i])])
        return self.a[-1][0] * 200 - 100
    def erreur(self):
        somme = 0
        lon = len(self.b_d)

        for donnees in self.b_k:
            etude = ast.literal_eval(donnees)
            attendu = sigmoid(self.b_d[donnees]/1000) * 200 - 100
            self._input(etude)
            somme += (attendu - self._output()) ** 2
            #somme += (attendu - value_game(situation = etude)) ** 2
        return somme / lon
    def erreur_model(self):
        somme = 0
        lon = len(self.b_d)

        for donnees in self.b_k:
            etude = ast.literal_eval(donnees)
            attendu = sigmoid(self.b_d[donnees] / 1000) * 200 - 100
            self._input(etude)

            somme += (attendu - (sigmoid(value_game(situation = etude) / 1000) * 200 - 100)) ** 2
        return somme / lon
    def deriv_poids(self,i, j, k):
        old_weight = self.weights[i][j][k]
        self.weights[i][j][k] += 0.000_1
        derive = (self.erreur() - self.Ei) * 10_000
        self.weights[i][j][k] = old_weight
        return derive
    def deriv_biais(self, i, j):
        old_biases = self.biases[i][j]
        self.biases[i][j] += 0.00_1
        derive = (self.erreur() - self.Ei) * 10_000
        self.biases[i][j] = old_biases
        return derive
    def apprend(self, base_donnee, pas = 0.0004, iteration = 300):
        old_amel = 0
        amel = 0
        var_pas = pas
        self.b_d = base_donnee
        self.b_k = list(self.b_d.keys())
        self.E0 = self.erreur()
        for k in range(iteration):

            # Taux erreur initial
            self.Ei = self.erreur()
            print("Taux erreurs init. : ", self.Ei)
            self.grad_poids = []
            l_weights = len(self.weights)
            tot = 31
            o = 0
            for i in range(l_weights):
                self.grad_poids.append([])
                for j in range(len(self.weights[i])):
                    self.grad_poids[i].append([])
                    for k in range(len(self.weights[i][j])):
                        self.grad_poids[i][-1].append(self.deriv_poids(i, j, k)*pas)
                        o += 1
                    #print("prog. : ", o/tot *100,"%")

            grad_biais = []
            for i in range(len(self.biases)):
                grad_biais.append([])
                for j in range(len(self.biases[i])):
                    grad_biais[-1].append(self.deriv_biais(i,j)*pas)
                    o +=1
                #print("prog. : ",o/tot*100, "%")
            print(self.grad_poids)
            old_weights = copy.deepcopy(self.weights)
            old_biases = copy.deepcopy(self.biases)
            self.weights = [np.subtract(ws, np.array(self.grad_poids[i])) for i, ws in enumerate(self.weights)]
            self.biais = [np.subtract(ba, np.array(grad_biais[i])) for i, ba in enumerate(self.biases)]

            # Taux erreur final
            Ef = self.erreur()
            amel = (self.Ei - Ef)/self.Ei * 100
            print("=> Taux erreurs init. : ", self.Ei)
            print("=> Taux erreurs final : ", Ef)
            print("=> Taux erreurs models : ", self.erreur_model())
            print("%Amélioration : ", amel, "%")

            print("-> pour un pas de ",pas)
            if amel < 0:
                print("<!> Aprentissage erroné")
                self.weights = old_weights
                self.biases = old_biases
                pas /=5
            elif amel <1:
                pas *= 2
            print("%Amélioration total : ", (self.E0 - Ef)/self.E0 *100," %")
            print("COPY DATA =>")
            self.nprint()
            self.nwrite()
            print("_____________________")
        self.nwrite("terminus.txt")

def interpret_game(situation):
    plateau = situation[0]
    score_diff = situation[2] - situation[3]
    nb_graines = situation[2] + situation[3]
    mobilite = 0
    greniers = 0
    blocus = 0
    mobil_score = 0
    len_dyn = 0

    gr, blo, mob, ogr, oblo, omob, sd = [1.2839999999999998, 1.1365000000000003, -5.167, -3.1109999999999998, 4.173500000000001, 6.7775, 105.95000000000002]

    for i, p in enumerate(plateau[0:5]):

        if i < 3:
            if 10 + i <= p <= 12 + i + 3:
                greniers += 1
            else :
                greniers -= 0.5
        elif i != 3:
            if 2 <= p:
                blocus += 1
        mobil_score += p
        if 5 > mobil_score and p < 4:
            len_dyn += 1
        else :

            mobilite += len_dyn
            len_dyn = 0
            mobil_score = 0

    mobilite += len_dyn
    res = [(1.5 + greniers)/3.5, mobilite/6,blocus/2]

    mobilite = 0
    ogreniers = 0
    oblocus = 0
    mobil_score = 0
    len_dyn = 0
    for i, p in enumerate(plateau[6:12]):
        if i < 3:
            if 10 + i <= p <= 12 + i + 3:
                ogreniers += 1
            else :
                ogreniers -= 0.5
        elif i != 3:
            if 2 <= p:
                oblocus += 1
        mobil_score += p
        if 5 > mobil_score and p < 4:
            len_dyn += 1
        else:
            mobilite += len_dyn
            len_dyn = 0
            mobil_score = 0

    mobilite += len_dyn
    return res + [(1.5 + ogreniers)/3.5, mobilite/6, blocus/2, score_diff/48, nb_graines/48]

    res = res + omob * mobilite + ogr * ogreniers + oblo * blocus + sd * score_diff + gr * greniers
def value_game(situation, verif = False):
    global tour_bot
    plateau = situation[0]
    score_diff = situation[2] - situation[3]
    gr, blo, mob, ogr, oblo, omob, sd = [1.2839999999999998, 1.1365000000000003, -5.167, -3.1109999999999998, 4.173500000000001, 6.7775, 105.95000000000002]
    mobilite = 0
    greniers = 0
    blocus = 0
    mobil_score = 0
    len_dyn = 0
    for i, p in enumerate(plateau[0:5]):

        if i < 3:
            if 10 + i <= p <= 12 + i + 3:
                greniers += 1
            else :
                greniers -= 0.5
        elif i != 3:
            if 2 <= p:
                blocus += 1
        mobil_score += p
        if 5 > mobil_score and p < 4:
            len_dyn += 1
        else :

            mobilite += len_dyn
            len_dyn = 0
            mobil_score = 0

    mobilite += len_dyn
    res = mob * mobilite + blo * blocus

    mobilite = 0
    ogreniers = 0
    oblocus = 0
    mobil_score = 0
    len_dyn = 0
    for i, p in enumerate(plateau[6:12]):
        if i < 3:
            if 10 + i <= p <= 12 + i + 3:
                ogreniers += 1
            else :
                ogreniers -= 0.5
        elif i != 3:
            if 2 <= p:
                oblocus += 1
        mobil_score += p
        if 5 > mobil_score and p < 4:
            len_dyn += 1
        else:
            mobilite += len_dyn
            len_dyn = 0
            mobil_score = 0

    mobilite += len_dyn

    return res + omob * mobilite + ogr * ogreniers + oblo * blocus + sd * score_diff + gr * greniers

Herture = AiNeural(gen_mode = "copy", copy_data =
{
"weights" : [[[9.989278865910848, -2.5876656620334684, 3.174422470675123, 3.81, -0.8390066834812501, 1.0804224706732266, -6.317859951936865, 0.8207512970036969], [-6.250055004671212, 5.619962957980045, 0.6440771934832746, 2.54, 6.729785384722074, 4.6956534387509725, -0.08176983780306679, 0.5041204352027187], [-0.0807366178649317, -4.452631313880568, -4.391155990125146, 0.0, -7.944495481086331, -4.391155990125146, 10.07511403614601, 0.03129668734690881]]
,[[8.870362468410699, -8.81562009729283, 18.878469109752356]]
],
"biases" : [[6.52, -0.3, 0]
,[0]
]
} )

#Changer souvent entre dic_end, dic_ouv, dic_mid surtout si l'amélioration est médiocre
Herture.apprend(dic_ouv())