import numpy as np
import math as mt
import random as ra
from ouverture import *
from middle import *
from end import *
import time as ti
import threading
import ast

def muter( var, magn=5):
    return var + ra.randint(-magn*1000, magn*1000)/1000
def sigmoid(x):
    if abs(x) < 99:
        return 1 / (1 + mt.exp(-x))
    elif x < 0 :
        return 0
    return 1
class AiNeural:

    def __init__(self, gen_mode = "zero", copy_data = []) :

        if gen_mode == "zero":
            npList = lambda x: np.array([0.0 for i in range(x)])
            # Neurones : a => Valeur neurones, weights => Importance de l'entrée associée,
            # biases => Changement positionel de l'activation du sigmoïde (fonction de la neurone)
            self.a = [npList(14), npList(7), npList(6), npList(3)]
            self.biases = [npList(7), npList(6), npList(3)]
            self.weights = [np.array([[0.0 for j in range(14)] for i in range(7)]),
                            np.array([[0.0 for j in range(7)] for i in range(6)]),
                            np.array([[0.0 for j in range(6)] for i in range(3)])]
        elif gen_mode == "hasard":
            rai = lambda x : ra.randint(-x*100, x*100)/100
            npList = lambda x, x1: np.array([rai(x1) for i in range(x)])

            # Neurones : a => Valeur neurones, weights => Importance de l'entrée associée,
            # biases => Changement positionel de l'activation du sigmoïde (fonction de la neurone)
            self.a = [npList(14, 0), npList(7, 0), npList(6, 0), npList(3, 0)]
            self.biases = [npList(7, 10), npList(6, 10), npList(3, 0)]
            self.weights = [np.array([[rai(10) for j in range(14)] for i in range(7)]),
                            np.array([[rai(10) for j in range(7)] for i in range(6)]),
                            np.array([[rai(10) for j in range(6)] for i in range(3)])]
        elif gen_mode == "copy":
            # Recopiage des données à copier
            npList = lambda x: np.array([0 for i in range(x)])
            # Neurones : a => Valeur neurones, weights => Importance de l'entrée associée,
            # biases => Changement positionel de l'activation du sigmoïde (fonction de la neurone)
            self.a = [npList(14), npList(7), npList(6), npList(3)]
            self.weights = copy_data["weights"]
            self.biases = copy_data["biases"]
    def mutation(self, Ai_parent, magn=5):
        bs = Ai_parent.biases
        ws = Ai_parent.weights
        self.biases = [np.array([muter(bs[0][i], magn) for i in range(7)]),
                       np.array([muter(bs[1][i], magn) for i in range(6)]),
                       np.array([muter(bs[2][i], magn) for i in range(3)])]
        self.weights = [np.array([[muter(ws[0][i][j], magn) for j in range(14)] for i in range(7)]),
                        np.array([[muter(ws[1][i][j], magn) for j in range(7)] for i in range(6)]),
                        np.array([[muter(ws[2][i][j], magn) for j in range(6)] for i in range(3)])]
        return self
    def nprint(self):
        print("{")
        print("\"weights\" : [", end="")
        for i in range(3):
            print("np.array(",end = "")
            print([[f for f in j] for j in self.weights[i]], end=")")
            if i != 2:
                print(",",end = "")
        print("],")
        print("\"biases\" : [", end="")
        for i in range(3):
            print(" np.array(", end="")
            print([j for j in self.biases[i]], end=")")
            if i != 2:
                print(",", end="")
        print("]")
        print("}")
    def nwrite(self, titre = 'copy_data.txt'):
        with open(titre, 'w') as f:
            # Append data to the file
            f.write('copy data: \n')
            f.write("{")
            f.write("\"weights\" : [")
            for i in range(3):
                f.write("np.array(")
                f.write(str([[f for f in j] for j in self.weights[i]]) + ")")
                if i != 2:
                    f.write(",")
            f.write("],")
            f.write("\"biases\" : [")
            for i in range(3):
                f.write(" np.array(")
                f.write(str([j for j in self.biases[i]]) + ")")
                if i != 2:
                    f.write(",")
            f.write("]")
            f.write("}\n")
            f.write("________________\n")



    def _input(self,vector, mode_list = "list"):
        if mode_list == "np_processed":
            self.a[0] = vector
        else:
            #
            self.a[0] = np.array([i/48 for i in vector[0:12]] +
                                 [sigmoid(vector[12])] +
                                 [sigmoid(-0.4*vector[13]+14)] )
    def _output(self):
        for i in range(3):
            # [12,9,10]
            # [3,-1,19]
            # => zip = [(12,3),(9,-1),(10,19)]
            self.a[i+1] = np.array([sigmoid(np.dot(self.a[i],w) + b) for b, w in zip(self.biases[i], self.weights[i])])
        res = self.a[-1]
        return ((res[0] * 100 + res[1] * 10 + res[2]) - 55.5)/0.555
    def erreur(self):
        somme = 0
        lon = len(self.b_d)

        for donnees in self.b_k:
            etude = ast.literal_eval(donnees)
            attendu = sigmoid(self.b_d[donnees]/1000) * 200 - 100
            self._input(etude[0] + [etude[2] - etude[3]] + [etude[2] + etude[3]])
            somme += (attendu - self._output()) ** 2
            #somme += (attendu - value_game(situation = etude)) ** 2
        return somme / lon
    def deriv_poids(self,i, j, k):
        old_weight = self.weights[i][j][k]
        self.weights[i][j][k] += 0.01
        derive = (self.erreur() - self.Ei) * 100
        self.weights[i][j][k] = old_weight
        return derive
    def deriv_biais(self, i, j):
        old_biases = self.biases[i][j]
        self.biases[i][j] += 0.01
        derive = (self.erreur() - self.Ei) * 100
        self.biases[i][j] = old_biases
        return derive
    def apprend(self, base_donnee, pas = 100, iteration = 300):
        old_amel = 0
        amel = 0
        var_pas = pas
        for k in range(iteration):
            if k%2 == 1 and k != 1:
                pas += amel - old_amel - 1
            elif k%2 != 1:
                old_amel = amel
                pas += 1
            self.b_d = base_donnee
            self.b_k = list(self.b_d.keys())
            # Taux erreur initial
            self.Ei = self.erreur()
            self.grad_poids = []
            l_weights = len(self.weights)
            tot = 167
            o = 0
            for i in range(l_weights):
                self.grad_poids.append([])
                for j in range(len(self.weights[i])):
                    self.grad_poids[i].append([])
                    for k in range(len(self.weights[i][j])):
                        self.grad_poids[i][-1].append(self.deriv_poids(i, j, k)*pas)
                        o += 1
                    print("progresssion : ", o/tot *100,"%")

            grad_biais = []
            for i in range(len(self.biases)):
                grad_biais.append([])
                for j in range(len(self.biases[i])):
                    grad_biais[-1].append(self.deriv_biais(i,j)*pas)
            print("progresssion : ", o / tot *100, "%")

            self.weights = [np.subtract(ws, np.array(self.grad_poids[i])) for i, ws in enumerate(self.weights)]
            self.biais = [np.subtract(ba, np.array(grad_biais[i])) for i, ba in enumerate(self.biases)]

            # Taux erreur final
            Ef = self.erreur()
            amel = (self.Ei - Ef)/self.Ei * 100
            print("Taux erreurs init. : ", self.Ei)
            print("Taux erreurs final : ", Ef)
            print("Amélioration : ", amel, "%")

            print("COPY DATA =>")
            self.nprint()
            self.nwrite()
            print("_____________________")
        self.nwrite("terminus.txt")

def value_game(situation):
    plateau = situation[0]
    score_diff = situation[2] - situation[3]
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
    res = res + omob * mobilite + ogr * ogreniers + oblo * blocus + sd * score_diff + gr * greniers
    return sigmoid(res / 1000) * 200 - 100




Herture = AiNeural(gen_mode = "copy", copy_data={
"weights" : [np.array([[22.846323476953373, -13.258330286684298, 13.897532341627027, 8.99339915082112, 16.4896790662132, 21.10723328777341, 5.27928207668921, 17.910672724329487, 7.235095584159601, 26.50132149864247, 1.8359148029951022, 19.32942328799315, 65.9278030493042, 152.1722264467977], [6.196970047429117, 6.211483906706009, -7.117743044928503, 7.2759845279085855, 1.1539872690851918, 1.296303643860738, 1.352034172474756, -9.73253693900854, -4.815369708232, 9.434415333665354, -4.361078557574511, 2.277318824004382, 6.529655471336067, 8.104205369502422], [-3.7270519271323574, -4.932225440382987, -5.807311876179301, -0.9963546785430224, -6.90393906804797, -6.04107267084837, -6.566643354985339, 0.25252549460739804, -12.699289275028422, -6.970265666618653, -23.525487919513544, -2.0571884395957465, -25.840467484894994, -71.3309302470343], [10.092353963928355, -5.617357872675581, -0.47092919848536274, 3.040845826099657, -2.511677672092395, 2.7529471721778105, 7.829402380767307, 3.43935847525741, 4.343960002434178, -11.303399453640331, -6.21322356598248, 7.654934933809273, -25.084768942538503, -27.026266683550524], [-48.42336922905641, -55.751624978665525, -47.40961506017873, -46.6468698115334, -61.49072150473398, -59.304450084241864, -28.257066295710274, -46.14356420831304, -69.26073948184646, -49.66310239509102, -48.56026997425925, -55.531205014017154, -255.12181100239434, -605.4000518760646], [77.08112171147685, 21.77991107010294, 45.36627586887573, 56.35757845763309, 37.74572081160621, 63.21104255154313, 20.68091603706364, 46.30891476210384, 43.75704465951538, 46.081426235131836, 68.23675806900845, 73.30494221055446, 282.83849096244074, 581.7652941024388], [-34.780832247362675, -29.837115983464408, -50.13084504861749, -47.50617786465219, -44.50809851217826, -48.44770171728465, -23.040564607154693, -41.20510408501886, -50.907062674171, -49.54188461352669, -36.69311825383233, -58.36550739669436, -263.4031471063301, -541.5854435793864]]),np.array([[-660.1508795961535, -667.9517290869574, 3.5261050046194, -2.5187018461069965, -1.626118123585301, -661.6808264502954, -2.8309588393671437], [6.614156963651883, -3.5418031776114063, 4.796766811808717, -0.6907055840342364, -3.950829575830838, -1.920309825706907, -2.4717210702531447], [8260.720889400363, 8253.701326268481, -5.804209184261417, -3.163610429788154, -5.214001926567406, 8256.200936442829, 10.46736995059735], [1031649.3086342277, 1031658.4275453512, -8.625009594780016, 13.386906461173144, 7.1077790345991385, 1031647.3419095499, 34.12096553229631], [-28.02706351426686, -399.69530253174224, 0.475640777198743, -9.879062829274538, -321.1099620700194, -229.19783869283927, -10.981318429182604], [5.587748018550308, -70.6151978365664, 13.28347149967123, 3.4982471989421464, -45.50120413875792, -3.9708601710302753, 7.788232159825624]]),np.array([[-7.2186162412066475, 8.30620315456527, 279142.28238137125, 2589.383229797886, 2087.9540830119518, 2113.912447232473], [-653.1563355129737, -1.127192387496005, 51.98037756033408, -762.0605226581926, -8.365322859654698, 1.447029247237544], [9.022996948736225, -2.0133877583426947, -423595.20598965057, -424529.7278761311, 5.3149710019437775, 5.313974855563778]])],
"biases" : [ np.array([-4.133000000000001, 8.257, -4.426, 0.1429999999999998, -6.371, 9.155000000000001, 2.053]), np.array([-1.791, 1.912, 0.5440000000000005, -0.9200000000000004, 8.487, -9.907]), np.array([-4.067, -5.695, 1.09])]
})
Herture.mutation(Herture)
Herture.apprend(dic_ouv())