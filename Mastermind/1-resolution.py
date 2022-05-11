from Mastermind import Mastermind
from math import log2
nb_boule = 8


def creation_liste(i=4):
    if i==0:
        return [[]]
    liste  = creation_liste(i-1)
    # return [[c]+x for c in range(nb_boule)for x in liste if not c in x ]
    return [[c]+x for c in range(nb_boule)for x in liste if not c in x ]

lexique = creation_liste()

def filtre_rouge(i, c, liste):
    return [x for x in liste if x[i]==c]

def filtre_blanc(i, c, liste):
    return [x for x in liste if (c in x) and (not x[i]==c)]

def filtre_gris(i, c, liste):
    return [x for x in liste if not (c in x)]


def creation(i, nb_blanc, nb_rouge, mot, liste, contenu, position, non_contenu):
    if i == 4:
        if nb_blanc==0 and nb_rouge==0 and liste!=[]:
            return [(liste, contenu, position, non_contenu)]
    elif liste != []:
        c = mot[i]
        liste_possible = []
        if nb_rouge>0 and ((position[i] is None) or position[i]==c) and (not non_contenu[c]):
            contenu_     = contenu.copy()
            contenu_[c]  = True
            position_    = position.copy()
            position_[i] = c
            liste_possible += creation(i+1, nb_blanc, nb_rouge-1, mot, filtre_rouge(i, mot[i], liste), contenu_, position_, non_contenu)
        if nb_blanc>0 and (position[i]!=c) and (not non_contenu[c]):
            contenu_      = contenu.copy()
            contenu_[c]   = True
            liste_possible += creation(i+1, nb_blanc-1, nb_rouge, mot, filtre_blanc(i, mot[i], liste), contenu_, position, non_contenu)
        if (position[i]!=c) and (not contenu[c]):
            non_contenu_     = non_contenu.copy()
            non_contenu_[c]  = True
            liste_possible += creation(i+1, nb_blanc, nb_rouge, mot, filtre_gris(i, mot[i], liste), contenu, position, non_contenu_)
        return liste_possible # (liste, contenu, position, non_contenu)
    return []





def possibles(reponses, liste, contenu, position, non_contenu): # (mot, nb_blanc, nb_rouge)
    if reponses==[]:
        return [(liste, contenu, position, non_contenu)]
    else:
        mot, nb_blanc, nb_rouge = reponses[0]
        liste_possible = creation(0, nb_blanc, nb_rouge, mot, liste, contenu, position, non_contenu)
        liste_possible_ = []
        for liste_, contenu_, position_, non_contenu_ in liste_possible:
            liste_possible_ += possibles(reponses[1:], liste_, contenu_, position_, non_contenu_)
        return liste_possible_


def compteur(reponses, liste, contenu, position, non_contenu):
    compteurs = []
    liste_possible = possibles(reponses, liste, contenu, position, non_contenu)
    for liste, _, _, _ in liste_possible:
        compteurs.append(len(liste))
    return sum(compteurs)
    
def compteur_total(reponse, liste, contenu, position, non_contenu):
    compteur_tt = []
    for bon in range(5):
        for nb_blanc in range(bon):
            nb_rouge = 4-nb_blanc
            compteur_tt.append(compteur([(reponse, nb_blanc, nb_rouge)], liste, contenu, position, non_contenu))
    return compteur_tt

def entropie(freqs):
    val = 0
    for freq in freqs:
        if freq == 1:
            val += 0.001
        elif freq != 0:
            val -= freq*log2(freq)
    return val


if __name__ == "__main__":
    jeu = Mastermind()
    print("Enoncé :")
    print(jeu.rangee)
    print()
    exact, possede = 0, 0
    # Inisialisation
    liste_possible = [ # (liste, contenu, position, non_contenu) = \
        (
        lexique.copy(),
        [False for _ in range(nb_boule)],
        [None for _ in range(4)],
        [False for _ in range(nb_boule)]
        )
    ]
    resultat = [(0, [i for i in range(4)])]
    j = 1
    deja = []
    while exact != 4 and j<10:
        entropie_rangee, rangee = resultat[0]
        while rangee in deja or (len(resultat) > 1 and resultat[1][0]==entropie_rangee and (not rangee in [liste[i] for liste, _, _, _ in liste_possible for i in range(len(liste))])):
            resultat = resultat[1:]
            entropie_rangee, rangee = resultat[0]

        exact, possede = jeu.cherche(rangee)
        deja.append(rangee)
        print(j)
        print(rangee)
        print(possede, exact)
        print()
        if exact != 4:
            liste_possible_ = []
            for liste, contenu, position, non_contenu in liste_possible:
                liste_possible_ += possibles([(rangee, possede, exact)], liste, contenu, position, non_contenu)
            liste_possible = liste_possible_
            # print(liste_possible)
            resultat = []
            
            for reponse in lexique:
                val_entropie = 0
                for liste, contenu, position, non_contenu in liste_possible:
                    n = len(liste)
                    compteur_tt = compteur_total(reponse, liste, contenu, position, non_contenu)
                    freqs = [x/n for x in compteur_tt]
                    val_entropie += entropie(freqs)
                resultat.append((val_entropie, reponse.copy()))
            resultat.sort(reverse=True)
        j+=1
    print()
    print(jeu.rangee)
    print(possede, exact)