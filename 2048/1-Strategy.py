from Game import Game
import random, time, sys

sys.setrecursionlimit(100_000)

# Aleatoire
def aleatoire():
    game = Game()
    jeux_possible, possibilite, score = game.info()
    while jeux_possible:
        x = random.choice(possibilite)
        jeux_possible, possibilite, score = game.jeux(x)
    return score

# 1 Profondeur
PONDERATION = [ 
    [1  ,   2,   4,   8],
    [16 ,  32,  64, 128],
    [256, 256, 256, 256],
    [512, 512, 512, 512]
]
PONDERATION = [[0.0031360273723379795, 0.0038036840396924454, 0.8362047496381709, 0.5005115699652146], [0.08378046404531869, 0.2821458711732301, 0.14593797463021096, 0.9637586117538086], [0.12669434687602033, 0.31450380062594985, 0.35894420863442555, 0.5769721117206498], [0.17426886386158935, 0.2859546307937846, 0.23916389252379333, 0.5818037482702322]]
PONDERATION = [[0.09312148635938844, 0.07411211347746405, 0.42315726061222536, 0.9492761739169571], [0.25093426377518724, 0.2103075407983216, 0.5283500260946518, 0.7816301208565157], [0.25734968850818785, 0.38435784403516626, 0.5458334971341687, 0.9118393006948027], [0.5760062121760149, 0.9403557092102732, 0.9321225763977898, 0.7126486689935014]]

PONDERATION = [ 
    [1  ,   2,   4,   8],
    [16 ,  32,  64, 128],
    [256, 256, 256, 256],
    [512, 512, 512, 512],
]
PONDERATION = [ 
    [1  ,   2,   4,   64],
    [2  ,   4,   8, 256],
    [4  ,  8,  256, 512],
    [8  , 256, 512, 1024],
]
def produitHadamard(grille):
    val = 0
    for i in range(4):
        for j in range(4):
            val += PONDERATION[i][j]*grille[i][j]
    return val

def prof1():
    game = Game()
    jeux_possible, possibilite, score = game.info()
    while jeux_possible:
        def eval_prof(x):
            game_x = game.variante()
            game_x.deplacement(x)
            return produitHadamard(game_x.grille)

        possibilite.sort(key=eval_prof)
        x = possibilite[0]
        jeux_possible, possibilite, score = game.jeux(x)
    return score

# 1 Profondeur Rotation
def prof1rot():
    game = Game()
    jeux_possible, possibilite, score = game.info()
    while jeux_possible:
        def eval_prof(x):
            game_x = game.variante()
            game_x.deplacement(x)
            valeurs = []
            for _ in range(2):
                game_x.retournement()
                for _ in range(4):
                    game_x.rotationD()
                    valeurs.append(produitHadamard(game_x.grille))
            return min(valeurs)

        possibilite.sort(key=eval_prof)
        x = possibilite[0]
        jeux_possible, possibilite, score = game.jeux(x)
    return score


# n Profondeur Rotation
def profnrot(n):
    game = Game()
    jeux_possible, possibilite, score = game.info()
    while jeux_possible:
        def recursion(game_x, i):
            if i == 0:
                valeurs = []
                for _ in range(2):
                    game_x.retournement()
                    for _ in range(4):
                        game_x.rotationD()
                        valeurs.append(produitHadamard(game_x.grille))
                return [min(valeurs)]
            else:
                l = []
                for y in game_x.jeux_possible()[1]:
                    game_xy = game_x.variante()
                    game_xy.deplacement(y)
                    l += recursion(game_xy, i-1)
                return l

        def eval_prof(x):
            game_x = game.variante()
            game_x.deplacement(x)
            l = recursion(game_x, n)
            if l==[]:
                return (4*4)*2048
            else:
                return sum(l)/len(l)

        possibilite.sort(key=eval_prof)
        x = possibilite[0]
        jeux_possible, possibilite, score = game.jeux(x)
    return score

inter_profnrot = (lambda n : (lambda : profnrot(n)))




# n Profondeur Rotation Plein
def profnrotplein(n):
    game = Game()
    jeux_possible, possibilite, score = game.info()
    while jeux_possible:
        def recursion(game_x, i):
            if i == 0:
                valeurs = []
                for _ in range(2):
                    game_x.retournement()
                    for _ in range(4):
                        game_x.rotationD()
                        val = produitHadamard(game_x.grille)
                        flag = True
                        for i in range(4):
                            if game_x.grille[i][0] == 0:
                                flag = False
                        if flag:
                            val -= 128
                        flag = True
                        for j in range(4):
                            if game_x.grille[0][j] == 0:
                                flag = False
                        if flag:
                            val -= 128

                        valeurs.append(val)
                return [min(valeurs)]
            else:
                l = []
                for y in game_x.jeux_possible()[1]:
                    game_xy = game_x.variante()
                    game_xy.deplacement(y)
                    l += recursion(game_xy, i-1)
                return l

        def eval_prof(x):
            game_x = game.variante()
            game_x.deplacement(x)
            l = recursion(game_x, n)
            if l==[]:
                return (4*4)*2048
            else:
                return sum(l)/len(l)

        possibilite.sort(key=eval_prof)
        x = possibilite[0]
        jeux_possible, possibilite, score = game.jeux(x)
    return score

inter_profnrotplein = (lambda n : (lambda : profnrotplein(n)))





def f():
    for i in range(4):
        pass



# Evaluation
def evalStrategies(lf, n=100):
    scores = []
    for name, s in lf:
        score = 0
        start = time.time()
        for i in range(n):
            score += s()
        scores.append((name, score/n, time.time() - start))
        print(f"{name} : Score is {score/n} in {round(time.time() - start, 2)} sec")

evalStrategies(
    [
        ("Aleatoire", aleatoire), 
        ("1 Profondeur", prof1), 
        # ("1 Profondeur Rotation", prof1rot),
        # ("2 Profondeur Rotation", inter_profnrot(2)),

        # ("3 Profondeur Rotation", inter_profnrot(3)),
        ("3 Profondeur Rotation Plein", inter_profnrotplein(3)),

    ],
    10
)
