import numpy as np

lexique = np.load(open("lexique-5chars.npy", "rb"))

def filtre_vert(i, c, liste):
    return [x for x in liste if x[i]==c]

def filtre_jaune(i, c, liste):
    return [x for x in liste if (c in x) and not (x[i]==c)]

def filtre_gris(c, liste):
    return [x for x in liste if c not in x]

def recursive(i, mot, liste):
    if i==5:
        return [len(liste)]

    compteur = []
    # vert 
    compteur += recursive(i+1, mot, filtre_vert(i, mot[i], liste))
    # jaune
    compteur += recursive(i+1, mot, filtre_jaune(i, mot[i], liste))
    # gris
    compteur += recursive(i+1, mot, filtre_gris(mot[i], liste))
    
    return compteur

def entropie(freq, n):
    L = np.array(freq) / n
    return -(L * np.log(np.clip(L, 0.00_1/n, 1))).sum() / np.log(2)

def nouvelle_tab(i, couleurs, mot, liste):
    if i==5:
        return liste
    elif couleurs[i] == "v": # vert
        return nouvelle_tab(i+1, couleurs, mot, filtre_vert(i, mot[i], liste))
    elif couleurs[i] == "j": # jaune
        return nouvelle_tab(i+1, couleurs, mot, filtre_jaune(i, mot[i], liste))
    else: # gris
        return nouvelle_tab(i+1, couleurs, mot, filtre_gris(mot[i], liste))


def affichage(resultat):
    for (rate, _, mot) in resultat:
        if rate > 0:
            print(f"{mot} : {round(rate, 2)}")

while True:
    # Initialisation
    tab = list(lexique)
    n = len(tab)
    resultat = [
        (6.16, None, 'sanie'), (6.2 , None, 'rates'), (6.21, None, 'taies'), (6.23, None, 'taire'), 
        (6.26, None, 'tares'), (6.26, None, 'aires'), (6.33, None, 'raies'), (6.33, None, 'tarie')
    ]
    while True:
        affichage(resultat[-5:])
        print(f"IL RESTE {n} MOTS ")
        if n<20:
            print(tab, end="\n\n")

        mot_input = input("Entre le mot choisi : ")
        couleurs = input("Entre les couleurs : ")
        if couleurs == "end":
            break
        elif couleurs == "lister":
            print(tab, end="\n\n")
        elif couleurs == "vvvvv":
            print("Félicitations !\n")
            input("Entrer pour rejouer")
            break
        else:
            tab = nouvelle_tab(0, couleurs, mot_input, tab)
            n = len(tab)
            entropies = []
            for mot in lexique:
                entropies.append(entropie(recursive(0, mot, tab), n))
            resultat = [(entropies[i], (1 if lexique[i] in tab else 0), lexique[i]) for i in range(len(entropies))]
            resultat.sort()