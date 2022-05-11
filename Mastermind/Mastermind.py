import random

class Mastermind:

    def __init__(self, rangee=None, nb_boule=8) -> None:
        self.nb_boule = nb_boule
        if rangee is None:
            pris = [False for _ in range(nb_boule)]
            self.rangee = []
            for _ in range(4):
                c = random.choice([i for i in range(nb_boule) if not pris[i]])
                self.rangee.append(c)
                pris[c] = True
        else:
            self.rangee = rangee

    def possede(self, x):
        return x in self.rangee
    
    def exact(self, x, i):
        return 
        
    def cherche(self, rangee):
        exact   = 0
        possede = 0
        for i in range(4):
            x = rangee[i]
            if x == self.rangee[i]:
                exact += 1
            elif x in self.rangee:
                possede += 1
        return exact, possede

if __name__ == "__main__":
    nb_boule = 8
    jeu = Mastermind()
    print(jeu.rangee)
    print()
    exact, possede = 0, 0
    while exact != 4:
        rangee = [random.randint(0, nb_boule-1) for i in range(4)]
        print(rangee)
        exact, possede = jeu.cherche(rangee)
