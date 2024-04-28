import pyxel
import bot
import random

def convertisseur(simu,type):
    if type=='jeu':
        result = simu[0]+simu[1][5:-8:-1]
        return result
    elif type=='visu':
        result = simu[:6] , simu[12:5:-1]
        return result
screen_size_x, screen_size_y = 300,200

def legal_moves(simulation):
    legal_moves = []
    plateau_visu = simulation[0]
    tour = simulation[1]
    scoreA = simulation[2]
    scoreB = simulation[3]
    if not tour:  # PLAYER
        # If the bot's hungry ...
        if plateau_visu[0] == [0, 0, 0, 0, 0, 0]:
            # We're looking for a full cell, the nearest one
            for i in range(5, -1, -1):
                if plateau_visu[1][i] > 5 - i:
                    legal_moves.append(i)
                    return legal_moves
            return []
        # If all goes well, we just look for cases which are not empty
        else:
            for i in range(6):
                if plateau_visu[1][i] != 0:  # Déjà, il ne faut pas que ce soit un zéro ...
                    legal_moves.append(i)
                    '''# Ensuite, on simule si on jouait ce coup-là
                    simulation2 = repartition_sim(simulation, 11 - i)[0]
                    if simulation2[:6] != [0, 0, 0, 0, 0,
                                           0]:  # Si en jouant ce coup, l'adversaire n'est pas affamé, ça passe'''

            return legal_moves

def recuperation_graines_sim(simulation, num):
    i = num
    plateau_jeu = simulation[0] #jeu
    tour = simulation[1]
    scoreA = simulation[2]
    scoreB = simulation[3]
    while plateau_jeu[i] in [2, 3]:
        if tour and 6 <= i <= 11:
            scoreA += plateau_jeu[i]
            plateau_jeu[i] = 0
        elif not tour and 0 <= i <= 5:
            scoreB += plateau_jeu[i]
            plateau_jeu[i] = 0
        i = (i + 1) % 12
    return (plateau_jeu, tour, scoreA, scoreB)

def repartition_sim(simulation, num):
    i = 0
    plateau_jeu = convertisseur(simulation[0], 'jeu')
    tour = simulation[1]
    scoreA = simulation[2]
    scoreB = simulation[3]
    # Tant que la case où on puise les graines est pleine, on remplit
    while plateau_jeu[num] != 0:
        plateau_jeu[(num + i) % 12] += 1
        plateau_jeu[(num) % 12] -= 1
        i = (i - 1) % 12
    if plateau_jeu[(num+i+1)%12] in [2,3]:
        return recuperation_graines_sim((plateau_jeu,tour, scoreA, scoreB),(num+i+1)%12)
    return (plateau_jeu, tour, scoreA, scoreB)



class App:
    def __init__(self):
        pyxel.init(screen_size_x, screen_size_y)
        pyxel.load('res2.pyxres')
        pyxel.mouse(True)
        self.initialise()

    def initialise(self):
        self.scoreA, self.scoreB = 0, 0
        self.last_posA, self.last_posB = 0, 0
        self.run = True
        self.tour = str(input("Qui commence?: BOT ; Joueur:>> ")) == 'BOT'
        self.plateau_jeu = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        self.plateau_visu = [[4, 4, 4, 4, 4, 4], [4, 4, 4, 4, 4, 4]]

    def repartition(self,num):
        i = 0

        # Tant que la case où on puise les graines est pleine, on remplit
        while self.plateau_jeu[num] != 0:
            self.plateau_jeu[(num + i) % 12] += 1
            self.plateau_jeu[(num) % 12] -= 1
            i = (i - 1) % 12

        if self.plateau_jeu[(num+i+1)%12] in [2,3]:
            self.recuperation_graines((num+i+1)%12)

    def recuperation_graines(self,num):
        i = num
        while self.plateau_jeu[i] in [2,3]:
            if self.tour and 6<=i<=11:
                self.scoreA += self.plateau_jeu[i]
                self.plateau_jeu[i] = 0
            elif not self.tour and 0<=i<=5:
                self.scoreB += self.plateau_jeu[i]
                self.plateau_jeu[i] = 0
            i = (i+1)%12

    def start(self):
        pyxel.run(self.update, self.draw)

    def player_control(self):
        if self.legal_moves() != []:
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                pos = pyxel.mouse_x, pyxel.mouse_y
                if 110 < pos[1] < 142:
                    for i in range(6):
                        # if : #On doit pas pouvoir jouer une case vide et ainsi laisser le tour à l'adversaire
                        if 30 + i * 40 < pos[0] < 62 + i * 40:
                            if i in self.legal_moves():
                                self.last_posB = i
                                return i
        else:
            self.recuperation_final()
            self.run = False


    def in_game(self,choix):
        if choix is not None:
            #print("super choix:"+str(choix))
            if self.tour:  # Vérifie le tour du joueur
                self.repartition(choix)

            elif not self.tour:  # Vérifie le tour du joueur
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
        return self.plateau_visu, self.tour, self.scoreA,self.scoreB
    def init_button(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            if 10<pyxel.mouse_x<30 and 8<pyxel.mouse_y<18:
                self.initialise()

    def legal_moves(self):
        #donne une liste de bon coup pour le joueur concerné
        legal_moves = []
        if not self.tour: #PLAYER
            # If the bot's hungry ...
            if self.plateau_visu[0] == [0, 0, 0, 0, 0, 0]:
                # We're looking for a full cell, the nearest one
                for i in range(5,-1,-1):
                    if self.plateau_visu[1][i] > 5-i:
                        legal_moves.append(i)
                        return legal_moves
                return []
            # If all goes well, we just look for cases which are not empty
            else:
                for i in range(6):
                    if self.plateau_visu[1][i] != 0:  # Déjà, il ne faut pas que ce soit un zéro ...

                        legal_moves.append(i)
                '''# Ensuite, on simule si on jouait ce coup-là
                        simulation2 = repartition_sim(self.get_game(), 11 - i)
                        if simulation2[:6][0] != [0, 0, 0, 0, 0, 0]:  # Si en jouant ce coup, l'adversaire n'est pas affamé, ça passe'''

                return legal_moves


    def update(self):
        if self.run:
            if self.tour:
                bot_move = bot.bot_move(self.get_game())
                if bot_move == None:
                    self.recuperation_final()
                    self.run = False
                else:
                    self.last_posA = bot_move
                    self.in_game(bot_move)
            else:
                self.in_game(self.player_control())

        self.init_button()

    def draw(self):
        pyxel.cls(2)
        if self.tour:
            pyxel.blt(90,10,0,0,32,224,16,0)
        else:
            pyxel.blt(90, 150, 0, 0, 48, 224, 16, 0)
        self.plateau_visu = self.plateau_jeu[:6] , self.plateau_jeu[12:5:-1]
        pyxel.rect(22,35,240,110,4)
        pyxel.line(22,90,260,90,7)

        pyxel.text(2,90, 'Robot',7)
        pyxel.text(10,80,str(self.scoreA),7)
        pyxel.text(280, 80, str(self.scoreB), 7)
        pyxel.text(270,90, 'Joueur',7)
        # Dessin des trous du plateau
        for i in range(6):
            for j in range(2):
                pyxel.blt(26+i*40,40+70*j,0,0,0,32,32,0)
                if i ==self.last_posA and j==0:
                    pyxel.blt(26 + i * 40, 40, 0, 32, 0, 32, 32, 0)
                if i == self.last_posB and j==1:
                    pyxel.blt(26 + i * 40, 110, 0, 32, 0, 32, 32, 0)
                pyxel.text(40 + i * 40, 54 + 70 * j, str(self.plateau_visu[j][i]), 8)
                seeds_count = self.plateau_visu[j][i]
                # Dessin de chaque graine dans le trou
                for k in range(seeds_count):
                    # Ajustement de la coordonnée y pour superposer les graines
                    seed_x = 26 + i * 40 + (k % 3) * 10
                    seed_y = 40 + 70 * j + (k // 3) * 5  # Ajustement de la coordonnée y
                    # Dessin de la graine
                    pyxel.blt(seed_x, seed_y, 0, 64, 0, 15, 15, 0)

        if 8<pyxel.mouse_x<31 and 8<pyxel.mouse_y<18:
            pyxel.rect(8, 8, 23, 10, 11)
            pyxel.text(10, 10, 'Reset', 0)
        else:
            pyxel.rect(8, 8, 23, 10, 5)
            pyxel.text(10, 10, 'Reset', 7)
        if not self.run:
            if self.scoreA > self.scoreB:
                pyxel.text(110,80,"Le Robot a gagne !",7)
            elif self.scoreA < self.scoreB:
                pyxel.text(110, 80, "Le Joueur a gagne !",7)
            else:
                pyxel.text(130, 80, "Ex aequo !", 7)

jeu = App()
jeu.start()