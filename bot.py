import random
import time
import copy
# bot
wc = 10
ca = 10
cl = 10

owc = 100
oca = 10
ocl = 10

ac = 3
oac = 3
sd = 100
#global wc,ca,cl,owc,oca,ocl,ac,oac,sd
def mutation(coefs,magn = 1):
    coefs = copy.deepcopy(coefs)
    for i, coef in enumerate(coefs):
        coefs[i] = coef + random.randint(-1000,1000)/1000 * magn
    return coefs
def value_game(situation):

    weak_case = 0
    chain_amount = 0
    chain_length = 0

    opp_weak_case = 0
    opp_chain_amount = 0

    attack_case = 0
    opp_attack_case = 0
    plateau = situation[0]
    score_diff = situation[2]-situation[3]
    for i, case in enumerate(plateau[0:6]):
        idx = (i+case) % 11 + i//11
        if 0 < case < 3:
            weak_case += 1
            for j in (k % 12 for k in range(i, 12+i)):
                if 0 < situation[0][j] < 3:
                    chain_length += 1
                else:
                    break
            chain_amount += chain_length*cl + ca
        elif 5 < idx and 0<plateau[idx]<3:
            attack_case += 1

    for i, case in enumerate(plateau[6:12]):
        if 0 < case < 3:
            opp_weak_case += 1
            for j in (k % 12 for k in range(i+6, 18+i)):
                if 0 < plateau[j] < 3:
                    chain_length += 1
                else:
                    break
            chain_amount += chain_length*ocl + oca
        elif (i + case+6) % 12 < 6:
            opp_attack_case += 1

    #value of position


    return owc*opp_weak_case - wc*weak_case + opp_chain_amount - chain_amount + attack_case*ac + opp_attack_case*oac + score_diff*sd

def repartition_sim(simulation, num):
    i = 0

    # Tant que la case où on puisse les graines est pleine, on remplit
    while simulation[0][num] != 0:
        simulation[0][(num + i) % 12] += 1
        simulation[0][(num) % 12] -= 1
        i = (i - 1) % 12
    if simulation[0][(num+i+1)%12] in [2,3]:
        return recuperation_graines_sim(simulation, (num+i+1)%12)
    return simulation
def legal_moves(simulation,joueur):
    #donne une liste de bon coup pour le joueur concerné
    legal_moves = []
    if not joueur: #PLAYER
        # If the bot's hungry ...
        if simulation[0] == [0, 0, 0, 0, 0, 0]:
            # We're looking for a full cell, the nearest one
            for i in range(5,-1,-1):
                if simulation[1][i] > 5-i:
                    legal_moves.append(i)
                    return legal_moves
            return []
        # If all goes well, we just look for cases which are not empty
        else:
            for i in range(6):
                if simulation[1][i] != 0:
                    legal_moves.append(i)
            return legal_moves


def in_game_sim(simulation,choix):
    if choix is not None:
        tour = simulation[1]
        simulation[1] = not tour
        if tour:  # Vérifie le tour du joueur
            return repartition_sim(simulation, choix)

        else:  # Vérifie le tour du joueur
            return repartition_sim(simulation, 11 - choix)
def recuperation_graines_sim(simulation,num):
        i = num
        tour = simulation[1]
        while simulation[0][i] in [2,3]:
            if tour and 6<=i<= 11:
                simulation[2] += simulation[0][i]
                simulation[0][i] = 0
            elif not tour and 0<=i<=5:
                simulation[3] += simulation[0][i]
                simulation[0][i] = 0
            i = (i+1)%12
        return simulation


def legal_moves(simulation,joueur):
    global tour_bot
    #donne une liste de bon coup pour le joueur concerné
    legal_moves = []
    if tour_bot: #BOT
        #If the player's hungry ...
        if simulation[1] == [0, 0, 0, 0, 0, 0]:
            #... We're looking for a full cell, nearest, forcing him to play this move
            for i in range(6):
                if simulation[0][i] > i:
                    legal_moves.append(i)
                    return legal_moves
            return []
        #If all goes well, we just look for cases which are not empty
        else:
            for i in range(6):
                if simulation[0][i] != 0:
                    legal_moves.append(i)
            return legal_moves

    else: #PLAYER
        # If the bot's hungry ...
        if simulation[0] == [0, 0, 0, 0, 0, 0]:
            # We're looking for a full cell, the nearest one, in the other sense than for the bot
            for i in range(5,-1,-1):
                if simulation[1][i] > 5-i:
                    legal_moves.append(i)
                    return legal_moves
        # If all goes well, we just look for cases which are not empty
        else:
            for i in range(6):
                if simulation[1][i] != 0:
                    legal_moves.append(i)
            return legal_moves
def minmax(simulation,joueur, depth = 6, depth_current = 6):

    plateau = simulation[0]
    lm = legal_moves([plateau[:6], plateau[12:5:-1]], joueur)
    if depth_current <= 0 or lm == [] or lm is None:
        if depth_current == depth:
            return 0
        if joueur :
            return value_game(simulation)
        else:
            return value_game(simulation) - 5
    else :
        values = {}

        for move in lm:
            sim = in_game_sim(copy.deepcopy(simulation), move)
            values[move] = minmax(sim, not joueur, depth_current = depth_current-1)
        minmax_value = None
        best_move = None
        if joueur :
            for move, value in values.items():
                if minmax_value is None:
                    best_move = move
                    minmax_value = value
                elif minmax_value < value :
                    best_move = move
                    minmax_value = value
        else:
            for move, value in values.items():
                if minmax_value is None:
                    best_move = move
                    minmax_value = value
                elif minmax_value > value :
                    best_move = move
                    minmax_value = value
        if depth_current == depth:
            return best_move
        else:
            return minmax_value
tour_bot = True

def bot_move(situation,coefs):
    global tour_bot
    global wc, ca, cl, owc, oca, ocl, ac, oac, sd
    wc, ca, cl, owc, oca, ocl, ac, oac, sd = coefs
    tour_bot = situation[-1]
    sim = copy.deepcopy(situation)
    choix = minmax(sim,True)
    return choix


