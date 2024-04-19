import random
import time

# bot
wc = 0.5
ca = 0.6
cl = 0.1

owc = 4
oca = 10
ocl = 8

ac = 5
oac = 5
sd = 10
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
        if 0 < case < 3:
            weak_case += 1
            for j in (k % 12 for k in range(i, 12+i)):
                if 0 < situation[0][j] < 3:
                    chain_length += 1
                else:
                    break
            chain_amount += chain_length*cl + ca
        elif 5 < (i+case) % 12:
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


def legal_moves(simulation,joueur):
    #donne une liste de bon coup pour le joueur concerné
    legal_moves = []
    if joueur: #BOT
        #If the player's hungry ...
        if simulation[0][1] == [0, 0, 0, 0, 0, 0]:
            #... We're looking for a full cell, nearest, forcing him to play this move
            for i in range(6):
                if simulation[0][0][i] > i:
                    legal_moves.append(i)
                    return legal_moves
            return []
        #If all goes well, we just look for cases which are not empty
        else:
            for i in range(6):
                if simulation[0][0][i] != 0:
                    legal_moves.append(i)
            return legal_moves

    else: #PLAYER
        # If the bot's hungry ...
        if simulation[0][0] == [0, 0, 0, 0, 0, 0]:
            # We're looking for a full cell, the nearest one, in the other sense than for the bot
            for i in range(5,-1,-1):
                if simulation[0][1][i] > 5-i:
                    legal_moves.append(i)
                    return legal_moves
        # If all goes well, we just look for cases which are not empty
        else:
            for i in range(6):
                if simulation[0][1][i] != 0:
                    legal_moves.append(i)
            return legal_moves


def bot_move(situation):
    #print(situation)
    time.sleep(1)
    if legal_moves(situation,True)!= []:
        print(legal_moves(situation,True))
        next_move = random.choice(legal_moves(situation,True))

        return next_move

sim = [[0, 0, 0,0, 0, 0], [0, 0, 0, 0, 0, 1]],True,0,0

print(bot_move(sim))

