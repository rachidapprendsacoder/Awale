import pyxel

screen_size_x, screen_size_y = 300,200



class App:
    def __init__(self):
        pyxel.init(screen_size_x, screen_size_y)
        pyxel.load('res.pyxres')

        self.scoreA, self.scoreB = 0, 0
        self.last_posA, self.last_posB = 0, 0
        self.run = self.scoreA != 24 or self.scoreB != 24
        self.tour = True
        pyxel.mouse(True)
        self.plateau_visu = self.plateau_jeu = [4,4,4,4,4,4,4,4,4,4,4,4]

    def repartition(self,num):
        contenu = self.plateau_jeu[num]
        i = 0
        while self.plateau_jeu[num] != 0:
            self.plateau_jeu[(num + i) % 12] += 1
            self.plateau_jeu[(num) % 12] -= 1
            i = (i - 1) % 12
        print()
        if 2 <= self.plateau_jeu[(num+i+1)%12] <=3:
            print('ohb')
            self.recuperation_graines((num+i+1)%12)

    def recuperation_graines(self,num):
        i = num
        global nba, nbb
        while 2 <= self.plateau_jeu[i] <= 3:
            if self.tour:
                self.scoreA += self.plateau_jeu[i]
            else:
                self.scoreB += self.plateau_jeu[i]
            self.plateau_jeu[i] = 0
            i = (i+1)%12

    def start(self):
        pyxel.run(self.update, self.draw)
    def update(self):
        if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and pyxel.frame_count%3==0:
            pos = pyxel.mouse_x, pyxel.mouse_y

            for i in range(6):
                if 30+i*40 < pos[0] < 62+i*40:
                    if 40 < pos[1] < 72:
                        self.repartition(i)
                        if self.tour:
                            self.last_posA = i
                        else:
                            self.last_posB = i
                        self.tour = not self.tour
                    elif 110 < pos[1] < 140:
                        self.repartition(11-i)
                        if self.tour:
                            self.last_posA = 11-i
                        else:
                            self.last_posB = 11-i
                        self.tour = not self.tour
            print(self.plateau_jeu)

            '''if 30 < pos[0] < 62:
                if 40 < pos[1] < 72:
                    self.repartition(0)
                    if self.tour:
                        self.last_posA=0
                    else:
                        self.last_posB=0
                    self.tour = not self.tour

                elif 110 < pos[1] < 140:
                    self.repartition(11)
                    self.tour = not self.tour
            if 70 < pos[0] < 102:
                if 40 < pos[1] < 72:
                    self.repartition(1)
                    self.tour = not self.tour
                elif 110 < pos[1] < 140:
                    self.repartition(10)
                    self.tour = not self.tour
            if 110 < pos[0] < 142:
                if 40 < pos[1] < 72:
                    self.repartition(2)
                    self.tour = not self.tour
                elif 110 < pos[1] < 140:
                    self.repartition(9)
                    self.tour = not self.tour
            if 150 < pos[0] < 182:
                if 40 < pos[1] < 72:
                    self.repartition(3)
                    self.tour = not self.tour
                elif 110 < pos[1] < 140:
                    self.repartition(8)
                    self.tour = not self.tour
            if 190 < pos[0] < 222:
                if 40 < pos[1] < 72:
                    self.repartition(4)
                elif 110 < pos[1] < 140:
                    self.repartition(7)
                    self.tour = not self.tour
            if 230 < pos[0] < 262:
                if 40 < pos[1] < 72:
                    self.repartition(5)
                    self.tour = not self.tour
                elif 110 < pos[1] < 140:
                    self.repartition(6)
                    self.tour = not self.tour'''
    def draw(self):
        pyxel.cls(2)

        #Dessin du player
        if self.tour:
            pyxel.blt(90,10,0,0,32,224,16,0)
        else:
            pyxel.blt(90, 150, 0, 0, 48, 224, 16, 0)
        self.plateau_visu = self.plateau_jeu[:6] , self.plateau_jeu[12:5:-1]
        pyxel.rect(22,35,240,110,5)
        pyxel.line(22,90,260,90,7)
        pyxel.text(10,80,str(self.scoreA),7)
        pyxel.text(280, 80, str(self.scoreB), 7)
        # Dessin des trous du plateau
        for i in range(6):
            for j in range(2):
                pyxel.blt(26+i*40,40+70*j,0,0,0,32,32,0)
                pyxel.text(40+i*40,55+70*j,str(self.plateau_visu[j][i]),8)


jeu = App()
jeu.start()
