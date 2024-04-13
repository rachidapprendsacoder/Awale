import pyxel
import bot

screen_size_x, screen_size_y = 300,200



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
        self.tour = True
        self.plateau_visu = self.plateau_jeu = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]

    def nourrissage(self):
        #Si joueur n'a plus de graine et que c'est le tour du bot
        if self.plateau_jeu[6:12]==[0,0,0,0,0,0] and self.tour :
            print(5)
            for i in range(6):

                if self.plateau_jeu[i]!=0:
                    print(74)
                    self.repartition(i)
                    self.tour = not self.tour
                    break

        #s'il n'a tjrs pas de graine mais que c'est à son tour
        elif self.plateau_jeu[6:12]==[0,0,0,0,0,0] and not self.tour :
            self.run = False

        #Si bot n'a plus de graines et que tour au joueur
        elif self.plateau_jeu[0:6]==[0,0,0,0,0,0] and not self.tour:
            print(5)
            for i in range(5,11):
                if self.plateau_jeu[i] != 0:
                    print(74)
                    self.repartition(i)
                    self.tour = not self.tour
                    break
        #Si bot tjrs pas de graine
        elif self.plateau_jeu[0:6]==[0,0,0,0,0,0] and self.tour :
            self.run = False

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
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            pos = pyxel.mouse_x, pyxel.mouse_y
            if 110 < pos[1] < 142:
                for i in range(6):

                    # if : #On doit pas pouvoir jouer une case vide et ainsi laisser le tour à l'adversaire
                    if 30 + i * 40 < pos[0] < 62 + i * 40:
                        return i
    def in_game(self,choix):
        if choix is not None:
            print("super choix:"+str(choix))
            if self.tour:  # Vérifie le tour du joueur
                self.repartition(choix)

            elif not self.tour:  # Vérifie le tour du joueur
                self.repartition(11 - choix)
            self.tour = not self.tour
    def get_game(self):
        return self.plateau_visu, self.tour, self.scoreA,self.scoreB
    def init_button(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            if 10<pyxel.mouse_x<30 and 10<pyxel.mouse_y<15:
                self.initialise()
    def update(self):
        if self.run:
            #On commence par vérifier si l'un des joueurs n'est pas affamé
            self.nourrissage()

            if self.tour:
                self.in_game(bot.bot_random_move(self.get_game()))
            else:
                self.in_game(self.player_control())

            self.init_button()
        else:
            #Récupération des graines manquantes sur le plateau
            for i in range(6):
                self.scoreA+=self.plateau_jeu[i]
                self.plateau_jeu[i]=0
            for i in range(6,12):
                self.scoreB+=self.plateau_jeu[i]
                self.plateau_jeu[i] = 0

    def draw(self):
        pyxel.cls(2)

        #Dessin du player
        if self.tour:
            pyxel.blt(90,10,0,0,32,224,16,0)
        else:
            pyxel.blt(90, 150, 0, 0, 48, 224, 16, 0)
        self.plateau_visu = self.plateau_jeu[:6] , self.plateau_jeu[12:5:-1]
        pyxel.rect(22,35,240,110,4)
        pyxel.line(22,90,260,90,7)
        pyxel.text(10,80,str(self.scoreA),7)
        pyxel.text(280, 80, str(self.scoreB), 7)
        # Dessin des trous du plateau
        for i in range(6):
            for j in range(2):
                pyxel.blt(26+i*40,40+70*j,0,0,0,32,32,0)
                pyxel.text(40+i*40,54+70*j,str(self.plateau_visu[j][i]),8)
        pyxel.text(10,10,'Reset',7)
        if 10<pyxel.mouse_x<30 and 10<pyxel.mouse_y<15:
            pyxel.text(10, 10, 'Reset', 10)
        if not self.run:
            if self.scoreA > self.scoreB:
                pyxel.text(110,80,"Le Robot a gagne !",7)
            else:
                pyxel.text(110, 80, "Le Joueur a gagne !",7)

print(bot.bot_random_move(0))

jeu = App()
jeu.start()