import random
import neuron as ne
import time
import copy
import threading
# bot
gr = 10 # case à kroue
mob = 10 # case à kroue perime
blo = 0 # nombre graines

#versions ennemies
ogr = 10
omob = 10
oblo = 10
sd = 100

#global wc,ca,cl,owc,oca,ocl,ac,oac,sd


def repartition_sim(simulation, num):
    i = 1
    simulation = copy.deepcopy(simulation)
    while simulation[0][num]-i > -1:
        simulation[0][(num - i) % 12 - i // 12] += 1
        i += 1
    simulation[0][num] = 0
    if simulation[0][(num - i + 1) % 12 - (i-1) // 12] in [2, 3]:
        u = copy.deepcopy(simulation)
        sim = recuperation_graines_sim(simulation, (num - i + 1) % 12 - (i+1) // 12)

        if sim[0:6] == [0 for i in range(6)]:
            sim = u[0:6] + sim[6:12]
        elif sim[6:12] == [0 for i in range(6)]:
            sim = sim[0:6] + u[6:12]
        return sim
    return simulation

def in_game_sim(simulation,choix):
    if choix is not None:
        simulation[1] = not simulation[1]
        tour = simulation[1]
        if tour:
            return repartition_sim(simulation, 11 - choix)

        else:
            return repartition_sim(simulation, 5-choix)


def recuperation_graines_sim(simulation, num):
        i = num
        tour = simulation[1]
        while simulation[0][i] in [2, 3]:
            if not tour and 6 <= i <= 11:
                simulation[2] += simulation[0][i]
                simulation[0][i] = 0
            elif tour and 0 <= i <= 5:
                simulation[3] += simulation[0][i]
                simulation[0][i] = 0
            else :
                break
            i = (i+1) % 12
        return simulation


def legal_moves(simulation, tour):
    legalmoves = []
    if not tour:  # PLAYER
        for i in range(6):
            if simulation[1][i] != 0:  # Déjà, il ne faut pas que ce soit un zéro ...
                if simulation[0] != [0, 0, 0, 0, 0, 0] or simulation[1][i] > 5 - i:
                    legalmoves.append(i)

        '''# Ensuite, on simule si on jouait ce coup-là
            simulation2 = repartition_sim(self.get_game(), 11 - i)
            if simulation2[:6][0] != [0, 0, 0, 0, 0, 0]:  # Si en jouant ce coup, l'adversaire n'est pas affamé, ça passe'''

    else:
        # If the player's hungry ...
        for i in range(6):
            if simulation[0][5 - i] != 0:  # Déjà, il ne faut pas que ce soit un zéro ...
                if simulation[1] != [0, 0, 0, 0, 0, 0] or simulation[0][5 - i] > 5 - i:
                    legalmoves.append(i)

    '''# Ensuite, on simule si on jouait ce coup-là
    simulation2 = repartition_sim(self.get_game(), 11 - i)
    if simulation2[:6][0] != [0, 0, 0, 0, 0, 0]:  # Si en jouant ce coup, l'adversaire n'est pas affamé, ça passe'''

    return legalmoves

def evaluation(sim, simulation, max, depth, depth_current, Ai_ = None):
    global nb_positions

    if str(sim) in pos_simules.keys():
        return pos_simules[str(sim)]
    else:
        if abs(simulation[2] - simulation[3]) <= 10 or nb_positions < 100000:
            val = minmax(sim, not max, depth=depth, depth_current=depth_current - 1, Ai_=Ai_)
            pos_simules[str(sim)] = val
            return val
        else:
            val = (simulation[2] - simulation[3]) * sd * 2
            pos_simules[str(sim)] = val
            return val

def minmax(simulation,max, depth = 4, depth_current = 4, Ai_ = None):
    global nb_positions, sd, pos_simules
    global TH_MAX, th_len
    nb_positions += 1
    # Si max == True : le tour du robot
    plateau = simulation[0]
    tour = simulation[1]
    lm = legal_moves([plateau[:6], plateau[12:5:-1]], tour)
    if depth_current <= 0 or lm == []:
        # Si la simulation est fini ou profondeur atteint
        if Ai_ is None:
            return value_game(simulation)
        else:
            Ai_._input(simulation[0] + [simulation[1]] + [simulation[2]] + [simulation[3]])
            return Ai_._output()
    else :
        values = {}
        th_liste = []
        for move in lm:
            sim = in_game_sim(copy.deepcopy(simulation), move)
            if TH_MAX > th_len:
                th = threading.Thread(target = evaluation, args = (sim, simulation, max, depth, depth_current, Ai_))
                th_liste.append((str(sim), move, th))
                th.start()
                th_len += 1
            else:
                values[move] = evaluation(sim,simulation, max, depth, depth_current, Ai_)

        if th_liste != []:
            for sim, move, th in th_liste:

                th.join()
                th_len -= 1
                values[move] = pos_simules[sim]

        minmax_value = None
        best_move = None

        if max:
            for move, value in values.items():
                if minmax_value is None:
                    best_move = move
                    minmax_value = value
                elif minmax_value < value:
                    best_move = move
                    minmax_value = value
        else:
            for move, value in values.items():
                if minmax_value is None:
                    best_move = move
                    minmax_value = value
                elif minmax_value > value:
                    best_move = move
                    minmax_value = value
        if depth_current == depth:
            return best_move
        else:
            return minmax_value

pos_simules = {}
nb_positions = 0
TH_MAX = 10
th_len = 0
def bot_move(situation,coefs = None, Ai_ = None ):
    global gr, blo, mob, ogr, oblo, omob, sd
    global nb_positions, pos_simules
    pos_simules = {}
    nb_positions = 0
    if coefs is not None :
        gr, blo, mob, ogr, oblo, omob, sd = coefs
    if situation[1]:
        sim = copy.deepcopy(situation)
    else :
        sim = copy.deepcopy([situation[0][6:12]+situation[0][0:6],True,situation[3],situation[2]])
    if situation[2]+situation[3] > 40:
        choix = minmax(sim, True, Ai_=Ai_, depth= 6, depth_current=6)
    else :

        choix = minmax(sim,True, Ai_ = Ai_, depth=5,depth_current=5)
    TH_MAX = 10
    th_len = 0
    return choix
def mutation(coefs, a_muter = [0,9] ,magn = 1):
    coefs = copy.deepcopy(coefs)
    for i, c in enumerate(coefs):
        coefs[i] = c + random.randint(-10000, 10000)/10000 * magn

    return coefs
def value_game(situation, verif = False):
    global tour_bot
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
    return res + omob * mobilite + ogr * ogreniers + oblo * blocus + sd * score_diff + gr * greniers


