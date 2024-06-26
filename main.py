import pyxel
import bot
import random
import copy
import numpy as np
import time
import threading

# <!> Pour l'apprentissage, le but est d'avoir le plus de maitres de dojo
# (présent dans la liste : li_coefs_maitres). Puis lorsque c'est bon, re-copier la liste donnée au console de dojo
# pour sauvegarder la progression


# Vous pouvez testez des combinaisons, ça peut marcher.
# Si vous voyez lors de l'apprentissage que Le Z a perdu alors les coefs ne sont pas bons pour rentrer dans le dojo
coefs = [ 13.40763236,  1.58133603, 16.28904883, -4.00178322, -3.72866397,
  -4.83352731, 105.74406986]

# LE DERNIER MAITRE EST CELUI QUI JOUE AU MODE JOUEUR
li_coefs_maitres = [[0, 0, 0, 0, 0, 0, 100],
                    [-0.15, -0.14, -0.1025, 1.09, 1.2, -4.2998, 101.1],
                    [-0.4115, -0.114, -1.1025, 1.069, 3.4905000000000004, -1.5759999999999998, 101.79],
                    [-1.3639999999999999, 3.313, -3.3755, 0.9005, -0.677, 2.1189999999999998, 106.33600000000001],
                    [1.2839999999999998, 1.1365000000000003, -5.167, -3.1109999999999998, 4.173500000000001, 6.7775, 105.95000000000002]]



mode = int(input("mode 1-joueur, 0-apprentissage : ")) == 1
def convertisseur(simu, type):
    if type=='jeu':
        result = simu[0]+simu[1][5:-8:-1]
        return result
    elif type=='visu':
        result = simu[:6] , simu[12:5:-1]
        return result
screen_size_x, screen_size_y = 400, 200

class App:
    def __init__(self):
        self.old_tour = None
        self.initialise()

        if mode:
            self.mode = mode
            pyxel.init(screen_size_x, screen_size_y)
            pyxel.load('res2.pyxres')
            pyxel.mouse(True)
            pyxel.run(self.update, self.draw)
        else :
            self.mode = mode
            print("nut")
            pyxel.init(screen_size_x, screen_size_y)
            pyxel.load('res2.pyxres')
            pyxel.mouse(True)
            self.scoreMutant = 0
            self.scoreOriginel = 0
            self.old_positions = []
            self.rounds = 1
            self.afZ = 0
            self.prochain = coefs
            self.afH = 0
            self.matchA, self.matchB = 0, 0
            self.dojo_i = len(li_coefs_maitres)-1
            pyxel.run(self.apprend, self.draw)

    def initialise(self):
        self.scoreA, self.scoreB = 0, 0
        self.last_posA, self.last_posB = 0, 0
        self.run = True
        # self.tour = str(input("Qui commence?: BOT ; Joueur:>> ")) == 'BOT'
        if self.old_tour is None:
            alea = random.randint(0, 1)
            if alea == 0:
                self.tour = True
            else:
                self.tour = False

            self.old_tour = self.tour
        else:
            self.tour = not self.old_tour
            self.old_tour = self.tour
        self.plateau_jeu = [4 for i in range(12)]
        self.old_positions = []
        self.plateau_visu = [[4 for i in range(6)], [4 for i in range(6)]]
        self.trigger = False
        self.old_score = []

    def repartition(self, num):
        i = 0

        # Tant que la case où on puise les graines est pleine, on remplit
        while self.plateau_jeu[num] != 0:
            self.plateau_jeu[(num + i) % 12] += 1
            self.plateau_jeu[(num) % 12] -= 1
            i = (i - 1) % 12

        if self.plateau_jeu[(num+i+1)%12] in [2, 3]:
            u = copy.deepcopy(self.plateau_jeu)
            s = self.scoreB, self.scoreA
            self.recuperation_graines((num+i+1)%12)
            if self.plateau_jeu[0:6] == [0 for i in range(6)]:
                self.plateau_jeu = u[0:6] + self.plateau_jeu[6:12]
                self.scoreB, self.scoreA = s
            elif self.plateau_jeu[6:12] == [0 for i in range(6)]:
                self.plateau_jeu = self.plateau_jeu[0:6] + u[6:12]
                self.scoreB, self.scoreA = s



    def recuperation_graines(self, num):
        i = num
        while self.plateau_jeu[i] in [2, 3]:
            if self.tour and 6<=i<=11:
                self.scoreA += self.plateau_jeu[i]
                self.plateau_jeu[i] = 0
            elif not self.tour and 0<=i<=5:
                self.scoreB += self.plateau_jeu[i]
                self.plateau_jeu[i] = 0
            i = (i+1)%12


    def player_control(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            pos = pyxel.mouse_x, pyxel.mouse_y
            if 110 < pos[1] < 142:
                for i in range(6):
                    # if : #On doit pas pouvoir jouer une case vide et ainsi laisser le tour à l'adversaire
                    if 26 + i * 40 < pos[0] < 58 + i * 40:
                        return i



    def in_game(self, choix):
        if choix is not None and choix in self.legal_moves():
            self.old_positions.append(copy.copy(self.plateau_jeu))
            self.old_score.append(copy.copy((self.scoreA, self.scoreB)))
            #print("super choix:"+str(choix))
            if self.tour:  # Vérifie le tour du joueur

                self.repartition(5 - choix)



            else:  # Vérifie le tour du joueur
                self.repartition(11 - choix)


            self.tour = not self.tour


    def recuperation_final(self):
        for i in range(6):
            self.scoreA += self.plateau_jeu[i]
            self.plateau_jeu[i] = 0
        for i in range(6, 12):
            self.scoreB += self.plateau_jeu[i]
            self.plateau_jeu[i] = 0


    def get_game(self):
        return copy.deepcopy([self.plateau_jeu, self.tour, self.scoreA, self.scoreB])


    def init_button(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            if 10<pyxel.mouse_x<30 and 8<pyxel.mouse_y<18:
                self.initialise()

    def back_button(self):
        if 35 < pyxel.mouse_x < 55 and 8 < pyxel.mouse_y < 18 and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and len(self.old_positions)>=2 :
            #Maj du plateau
            self.plateau_jeu = self.old_positions[-2]
            #Maj de la mémoire
            self.old_positions = self.old_positions[:len(self.old_positions)-2]
            #Maj des scores
            self.scoreA = self.old_score[-2][0]
            self.scoreB = self.old_score[-2][1]
            #Maj de la mémoire
            self.old_score = self.old_score[:len(self.old_score)-2]


    def legal_moves(self):
        #donne une liste de bon coup pour le joueur concerné
        # donne une liste de bon coup pour le joueur concerné
        legal_moves = []
        if not self.tour:  # PLAYER

            for i in range(6):
                if self.plateau_visu[1][i] != 0:  # Déjà, il ne faut pas que ce soit un zéro ...
                    if self.plateau_visu[0] != [0, 0, 0, 0, 0, 0] or self.plateau_visu[1][i] > 5 - i:
                        legal_moves.append(i)

        else:
            # If the player's hungry ...
            for i in range(6):
                if self.plateau_visu[0][5 - i] != 0:  # Déjà, il ne faut pas que ce soit un zéro ...
                    if self.plateau_visu[1] != [0, 0, 0, 0, 0, 0] or self.plateau_visu[0][5 - i] > 5 - i:
                        legal_moves.append(i)



        return legal_moves

    def update(self):
        self.plateau_visu = self.plateau_jeu[:6], self.plateau_jeu[12:5:-1]
        self.init_button()
        self.back_button()
        if self.run:
            if self.legal_moves() == [] or (self.plateau_jeu in self.old_positions and self.trigger):
                self.recuperation_final()
                self.run = False
            else :
                if self.plateau_jeu in self.old_positions:
                    self.trigger = 2
                elif self.trigger == 2 :
                    self.trigger = True


            if self.tour:

                bot_move = bot.bot_move(self.get_game(), coefs=li_coefs_maitres[-1])
                self.in_game(bot_move)
                self.last_posA = 5 - bot_move
            else:
                self.in_game(self.player_control())
                self.last_posB = self.player_control()



    def apprend(self):
        global coefs, li_coefs_maitres

        self.plateau_visu = self.plateau_jeu[:6], self.plateau_jeu[12:5:-1]
        self.init_button()
        if self.run and self.matchA <= self.matchB:
            if self.legal_moves() == [] or self.scoreA >= 25 or self.scoreB >= 25 or self.plateau_jeu in self.old_positions:
                self.recuperation_final()
                self.run = False
            else:
                self.old_positions.append(copy.copy(self.plateau_jeu))
                #A modofier par rapport à self.update()
                if self.tour:
                    bot_move,dic = bot.bot_move(self.get_game(), coefs=li_coefs_maitres[self.dojo_i], dico_get=True)
                    self.in_game(bot_move)
                    self.last_posA = 5 - bot_move
                    #self.prochain = Herture.apprend_coefs(dic, self.prochain)
                else:
                    # self.in_game(self.player_control())
                    bot_move = bot.bot_move(self.get_game(), coefs=coefs)
                    self.in_game(bot_move)
                    self.last_posB = bot_move


        elif self.rounds <= 0 or self.matchA > self.matchB:
            if self.scoreA > self.scoreB:
                self.matchA += 1
            elif self.scoreA < self.scoreB:
                self.matchB += 1
            else:
                self.matchA += 0.5
                self.matchB += 0.5
            if self.matchA < self.matchB:
                if self.dojo_i <= 0:
                    print(f"!!!!!!!!!!!!!!!!Disciple A GAGNE (+ {self.afZ})!!!!!!!!!!!!!!!!!")
                    print("__coefs : gagnant - Disciple")
                    print(coefs)
                    print("dojo =>")
                    li_coefs_maitres.append(coefs)
                    print(li_coefs_maitres)
                    coefs = bot.mutation(coefs, magn=2)

                    self.dojo_i = len(li_coefs_maitres) - 1
                else:
                    print("___________")
                    print(f" => Le Disciple a gagne le {self.dojo_i + 1}th maitre")
                    print("Score Disciple :", self.matchB)
                    print(f"Score {self.dojo_i + 1}th maitre :", self.matchA)
                    self.dojo_i -= 1

                if self.afH == 0:
                    self.afZ += 1
                else:
                    self.afH = 0
                    self.afZ = 1

            else:

                print(f"_______le {self.dojo_i + 1}th MAITRE A GAGNE ({len(li_coefs_maitres)} maitres tot.)_______")
                print("gagnant - DOJO")
                print(li_coefs_maitres)
                if self.afZ == 0:
                    self.afH += 1
                else:
                    self.afZ = 0
                    self.afH = 1
                print("Score Disciple :", self.matchB)
                print(f"Score {self.dojo_i + 1}th maitre :", self.matchA)
                ## Avec mutation
                coefs = bot.mutation(li_coefs_maitres[-1], magn=5)
                ## Avec descente de gradient
                #coefs = self.prochain
                self.dojo_i = len(li_coefs_maitres) - 1

            self.old_positions = []
            self.initialise()
            # Pour montrer qui a gagner
            self.scoreA, self.scoreB = int(self.matchA), int(self.matchB)
            self.matchA, self.matchB = 0, 0

            self.rounds = 1
            time.sleep(0.5)
        else:
            if self.scoreA > self.scoreB:
                self.matchA += 1
            elif self.scoreA < self.scoreB:
                self.matchB += 1
            else:
                self.matchA += 0.5
                self.matchB += 0.5
            self.old_positions = []
            self.initialise()
            self.tour = random.randint(0, 1)
            self.rounds -= 1

    def draw(self):
        pyxel.cls(2)
        if self.run :
            if self.tour:
                pyxel.blt(90, 10, 0, 0, 32, 112, 16, 0)
            else:
                if self.mode :
                    pyxel.blt(90, 150, 0, 0, 48, 112, 16, 0)
                else :
                    pyxel.blt(90, 150, 0, 0, 32, 112, 16, 0)

        pyxel.rect(22, 35, 240, 110, 4)
        pyxel.line(22, 90, 260, 90, 7)

        if self.mode:
            pyxel.text(332, 50, f'{len(li_coefs_maitres)}eme AWIN :', 7)
        else :
            if self.dojo_i == 0:
                pyxel.text(340, 50, '1er M.:', 7)
            else :
                pyxel.text(340, 50, f'{self.dojo_i+1}eme M.:', 7)
        #Corners
        pyxel.blt(22, 35, 0, 176, 0, 15, 15, 0)
        pyxel.blt(22, 130, 0, 176, 16, 15, 15, 0)
        pyxel.blt(247, 35, 0, 192, 0, 15, 15, 0)
        pyxel.blt(247, 130, 0, 192, 16, 15, 15, 0)

        pyxel.text(380, 50, str(self.scoreA), 7)
        pyxel.text(310, 50, str(self.scoreB), 7)
        if self.mode :
            pyxel.text(270, 50, 'Joueur :', 7)
            if 35 < pyxel.mouse_x < 55 and 8 < pyxel.mouse_y < 18:
                pyxel.rect(35, 8, 20, 10, 11)
                pyxel.text(38, 10, 'Back', 0)
            else:
                pyxel.rect(35, 8, 20, 10, 5)
                pyxel.text(38, 10, 'Back', 7)
        else :
            pyxel.text(270, 50, 'Disciple:', 7)
        # Dessin des trous du plateau
        for i in range(6):
            for j in range(2):
                pyxel.blt(26+i*40, 40+70*j, 0, 0, 0, 32, 32, 0)
                if i ==self.last_posA and j==0:
                    pyxel.blt(26 + i * 40, 40, 0, 32, 0, 32, 32, 0)
                if i == self.last_posB and j==1:
                    pyxel.blt(26 + i * 40, 110, 0, 32, 0, 32, 32, 0)
                seeds_count = self.plateau_visu[j][i]
                # Dessin de chaque graine dans le trou
                for k in range(seeds_count):
                    # Ajustement de la coordonnée y pour superposer les graines
                    seed_x = 26 + i * 40 + (k % 3) * 10
                    seed_y = 40 + 70 * j + (k // 3) * 5  # Ajustement de la coordonnée y
                    # Dessin de la graine
                    pyxel.blt(seed_x, seed_y, 0, 64, 0, 15, 15, 0)
                pyxel.text(40 + i * 40, 54 + 70 * j - 1, str(seeds_count), 7)
                pyxel.text(40 + i * 40, 54 + 70 * j + 1, str(seeds_count), 7)
                pyxel.text(40 + i * 40+1, 54 + 70 * j , str(seeds_count), 7)
                pyxel.text(40 + i * 40-1, 54 + 70 * j , str(seeds_count), 7)
                pyxel.text(40 + i * 40, 54 + 70 * j, str(seeds_count), 0)

        plateau1_x = 350
        plateau1_y = 70
        pyxel.blt(plateau1_x, plateau1_y, 0, 128, 0, 48, 48, 0)

        plateau2_x = 280
        pyxel.blt(plateau2_x, plateau1_y, 0, 128, 0, 48, 48, 0)



        if 8<pyxel.mouse_x<31 and 8<pyxel.mouse_y<18:
            pyxel.rect(8, 8, 23, 10, 11)
            pyxel.text(10, 10, 'Reset', 0)
        else:
            pyxel.rect(8, 8, 23, 10, 5)
            pyxel.text(10, 10, 'Reset', 7)
        if not self.run:
            if self.scoreA > self.scoreB:
                if self.mode:
                    pyxel.text(80, 80, "Victoire AWINLE : On les win tous !", 7)
                else:
                    if self.dojo_i == 0:
                        pyxel.text(110, 80, f"Le 1er Maitre a gagne !", 7)
                    else :
                        pyxel.text(110, 80, f"Le {self.dojo_i+1}eme Maitre a gagne !", 7)
            elif self.scoreA < self.scoreB:
                if self.mode:
                    pyxel.text(80, 80, "Victoire Joueur : On a lose : <", 7)
                else:
                    pyxel.text(110, 80, "Disciple a gagne !", 7)
            else:
                pyxel.text(130, 80, "Ex aequo !", 7)

        for k in range(self.scoreA):
            if k < 28 :
                seed_x = plateau1_x - 2 + (k % 4) * 7
                seed_y = plateau1_y - 2 + (k // 4) * 6
                pyxel.blt(seed_x, seed_y, 0, 112, 0, 15, 15, 0)
            else:
                pyxel.text(365, 120, "+", 8)
                pyxel.text(370, 120, "+", 8)
                pyxel.text(375, 120, "+", 8)


        for k in range(self.scoreB):
            if k < 28 :
                seed_x = plateau2_x - 2 + (k % 4) * 7
                seed_y = plateau1_y - 2 + (k // 4) * 6
                pyxel.blt(seed_x, seed_y, 0, 96, 0, 15, 15, 0)
            else:
                pyxel.text(305, 120, "+", 8)
                pyxel.text(295, 120, "+", 8)
                pyxel.text(300, 120, "+", 8)

jeu = App()