from Game import Game
import random, time



# n Profondeur Rotation
PONDERATIONS = [
    [ # 0-97
        [1  ,   16,  16,  64],
        [16  ,  16,  32, 256],
        [16 ,  32, 256, 512],
        [64 , 256, 512,1024],
    ],
    [ # 97-128
        [1  ,   8,   16,  32],
        [8  ,   16,  32,  32],
        [256, 256,  256, 512],
        [256, 256, 512, 1024],
    ],
    [ # 128-192
        [1  ,   8,  16,  64],
        [8  ,  16,  32, 256],
        [16 ,  32, 256, 512],
        [64 , 256, 512,1024],
    ],
    [ # 192-256
        [1  ,   8,   16,  32],
        [8  ,   16,  32,  32],
        [256, 256,  256, 512],
        [256, 256, 512, 1024],
    ],
    [ # 256-384
        [1  ,   8,  16,  64],
        [8  ,  16,  32, 256],
        [16 ,  32, 256, 512],
        [64 , 256, 512,1024],
    ],
    [ # 384-512
        [1  ,   32,   32,  256],
        [32 ,   64,   64, 64],
        [32, 256,  256, 512],
        [256, 256, 512, 1024],
    ],
    [ # 512-768
        [1  ,  32,  32,  64],
        [16  , 16,  32, 256],
        [16 ,  32, 256, 512],
        [64 , 256, 512,1024],
    ],
    [ # 768-2048
        [1  ,   8,   16,  32],
        [16 ,   8,  16,  32],
        [256, 256,  256, 512],
        [256, 256, 512, 1024],
    ],
]
liste = [
    range(0, 97), # 97=64+32
    range(97, 128),
    range(128, 192), # 192=128+64
    range(192, 256),
    range(256, 384), # 384=256+128
    range(384, 512),
    range(512, 768), # 768=512+256
    range(768, 2048),
]
dico = {x:i for i in range(len(liste)) for x in liste[i]}


def produitHadamard(PONDERATION, grille):
    val = 0
    maxi = max([max(PONDERATION[i]) for i in range(4)])
    for i in range(4):
        for j in range(4):
            if grille[i][j] != 0:
                val += PONDERATION[i][j]*grille[i][j]
            else:
                val -= (maxi-PONDERATION[i][j])*2
    return val

def profnrot(n):
    game = Game()
    jeux_possible, possibilite, score = game.info()
    score = 0
    while jeux_possible:
        def recursion(game_x, i):
            if i == 0:
                valeurs = []
                score_ = game_x.score()
                PONDERATION = PONDERATIONS[dico[score_]]
                for _ in range(2):
                    game_x.retournement()
                    for _ in range(4):
                        game_x.rotationD()
                        valeurs.append(produitHadamard(PONDERATION, game_x.grille))
                return [min(valeurs)]
            else:
                l = []
                valeurs = []
                score_ = game_x.score()
                PONDERATION = PONDERATIONS[dico[score_]]
                for _ in range(2):
                    game_x.retournement()
                    for _ in range(4):
                        game_x.rotationD()
                        valeurs.append(produitHadamard(PONDERATION, game_x.grille))
                val = min(valeurs)
                for y in game_x.jeux_possible()[1]:
                    game_xy = game_x.variante()
                    game_xy.deplacement(y)
                    l += recursion(game_xy, i-1)
                return [val*(i+1) + min(l+[(4*4)*2048])]

        def eval_prof(x):
            game_x = game.variante()
            game_x.deplacement(x)
            l = recursion(game_x, n)
            if l==[]:
                return (4*4)*2048
            else:
                return min(l)
                
        possibilite.sort(key=eval_prof)
        x = possibilite[0]
        game.affichage()
        print(f"Score : {score} play {x} \n")
        jeux_possible, possibilite, score = game.jeux(x)
    game.affichage()
    print(f"Score : {score}\n")
    

inter = (lambda n : (lambda : profnrot(n)))

profnrot(5)


