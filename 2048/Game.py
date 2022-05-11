from operator import pos
import random

PROBA4 = 0.1

class Game:
    def __init__(self, grille=None) -> None:
        if grille is None:
            self.grille = [[0 for j in range(4)] for i in range(4)]
            self.placement()
            self.placement()
        else:
            self.grille = [[grille[i][j] for j in range(4)] for i in range(4)]

    
    def place(self):
        l = []
        for i in range(4):
            for j in range(4):
                if self.grille[i][j] == 0:
                    l.append((i, j))
        return l
    
    def placement(self):
        l = self.place()
        n = len(l)
        indice = random.randint(0, n-1)
        i, j = l[indice]
        if PROBA4 > random.random():
            number = 4
        else:
            number = 2
        
        self.grille[i][j] = number

    def deplacement_haut(self):
        fusionnable = [[True for j in range(4)] for i in range(4)]
        for _ in range(4):
            for i in range(1, 4):
                for j in range(4):
                    if self.grille[i][j] != 0:
                        if self.grille[i-1][j] == 0: # Déplacement
                           self.grille[i-1][j] = self.grille[i][j]
                           self.grille[i][j]   = 0
                        elif self.grille[i-1][j] == self.grille[i][j] and fusionnable[i-1][j] and fusionnable[i][j]: # Fusion
                            self.grille[i-1][j] *= 2
                            self.grille[i][j]    = 0
                            fusionnable[i-1][j] = False

    
    def deplacement(self, x):
        """
        0 up
        1 right
        2 down
        3 left
        """
        if x == 0:
            self.deplacement_haut()
        elif x == 2:
            self.retournement()
            self.deplacement_haut()
            self.retournement()
        elif x == 1:
            self.rotationG()
            self.deplacement_haut()
            self.rotationD()
        elif x == 3:
            self.rotationD()
            self.deplacement_haut()
            self.rotationG()
        else:
            raise ValueError
    
    def variante(self):
        return Game(grille=self.grille)
    
    def is_same(self, grille):
        for i in range(4):
            for j in range(4):
                if grille[i][j] != self.grille[i][j]:
                    return False
        return True
    
    def jeux_possible(self):
        possibilite = []
        for x in range(4):
            v = self.variante()
            v.deplacement(x)
            if not self.is_same(v.grille):
                possibilite.append(x)
            del v
        if possibilite == []:
            return False, []
        else:
            return True, possibilite

    def score(self):
        val = 0
        for i in range(4):
            for j in range(4):
                val += self.grille[i][j]
        return val

    def info(self):
        self.possible, self.possibilite = self.jeux_possible()
        return self.possible, self.possibilite, self.score()

    def jeux(self, x):
        if not x in self.possibilite:
            print("Mouveemnt impossible") 
        else:
            self.deplacement(x)
            self.placement()
        return self.info()


    def affichage(self):
        for i in range(4):
            for j in range(4):
                c = str(self.grille[i][j])
                n = len(c)
                space = " "*((5-n)//2)
                if n%2==1: # centré
                    print(space, c, space, end="")
                else:
                    print(space, c, space, end=" ")
            print()

    def rotationD(self):
        for i in range(2):
            for j in range(2):
                self.grille[i][j], self.grille[3-j][i], self.grille[3-i][3-j], self.grille[j][3-i] \
                    = self.grille[3-j][i], self.grille[3-i][3-j],  self.grille[j][3-i], self.grille[i][j]
    
    def rotationG(self):
        for i in range(2):
            for j in range(2):
                self.grille[i][j], self.grille[3-j][i], self.grille[3-i][3-j], self.grille[j][3-i] \
                    = self.grille[j][3-i], self.grille[i][j], self.grille[3-j][i], self.grille[3-i][3-j]
    
    def retournement(self):
        for i in range(2):
            for j in range(4):
                self.grille[i][j], self.grille[3-i][j] = self.grille[3-i][j], self.grille[i][j]


if __name__ == "__main__":
    game = Game()
    jeux_possible, possibilite, score = game.info()

    while jeux_possible:
        game.affichage()
        print(f"Score : {score}\n")
        # x = random.choice(possibilite)
        x = int(input("Mouvement : ")) # 0, 1, 2 ou 3
        jeux_possible, possibilite, score = game.jeux(x)

    game.affichage()
    print(f"Score : {score}\n")

    


        
        

    