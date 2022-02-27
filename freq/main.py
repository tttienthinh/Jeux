import numpy as np

lexique = np.load(open("freq/lexique-5chars.npy", "rb"))
dico = {mot: float(freq) for mot, freq in lexique}
lexique = lexique[:, 0]

def filtre_vert(i, c, liste):
    return [x for x in liste if x[i]==c]

def filtre_jaune(i, c, liste):
    return [x for x in liste if (c in x) and not (x[i]==c)]

def filtre_gris(c, liste):
    return [x for x in liste if c not in x]

def compteur_freq(liste):
    return sum([dico[mot] for mot in liste])

def recursive(i, mot, liste):
    if i==5:
        return [compteur_freq(liste)]

    compteur = []
    # vert 
    compteur += recursive(i+1, mot, filtre_vert(i, mot[i], liste))
    # jaune
    compteur += recursive(i+1, mot, filtre_jaune(i, mot[i], liste))
    # gris
    compteur += recursive(i+1, mot, filtre_gris(mot[i], liste))
    
    return compteur

def entropie(freq, n):
    L = np.array(freq) / max(n, 1)
    return -(L * np.log(np.clip(L, 0.00_1/max(n, 1), 1))).sum() / np.log(2)

def nouvelle_tab(i, couleurs, mot, liste):
    if i==5:
        return liste
    elif couleurs[i] == "v": # vert
        return nouvelle_tab(i+1, couleurs, mot, filtre_vert(i, mot[i], liste))
    elif couleurs[i] == "j": # jaune
        return nouvelle_tab(i+1, couleurs, mot, filtre_jaune(i, mot[i], liste))
    else: # gris
        return nouvelle_tab(i+1, couleurs, mot, filtre_gris(mot[i], liste)) # problème heure : gggjv pour le mot rouge


def affichage(resultat):
    for (rate, _, mot) in resultat:
        if rate > 0:
            print(f"{mot} : {round(rate, 2)}")

while True:
    # Initialisation
    tab = list(lexique)
    n = compteur_freq(tab)
    resultat = [
        (5.35, None, 'vires'), (5.35, None, 'tries'), (5.36, None, 'tiser'), (5.36, None, 'rites'), 
        (5.38, None, 'raies'), (5.43, None, 'strie'), (5.52, None, 'tires'), (5.58, None, 'aires')
    ]
    while True:
        affichage(resultat[-5:])
        print(f"IL RESTE {len(tab)} MOTS ")
        # affichage tab
        compteur_tab = compteur_freq(tab) 
        affichage_tab = [(dico[mot]/compteur_tab, mot) for mot in tab]
        affichage_tab.sort()
        print("\n".join([f"  {mot} : {round(freq*100, 2)} %" for freq, mot in affichage_tab[-5:]]), end=" ...\n\n")

        mot_input = input("Entre le mot choisi : ")
        couleurs = input("Entre les couleurs : ")
        if couleurs == "end":
            print("-------------------")
            break
        elif couleurs == "lister":
            print(tab, end="\n\n")
        elif couleurs == "vvvvv":
            print("Félicitations !\n")
            input("Entrer pour rejouer")
            break
        else:
            tab = nouvelle_tab(0, couleurs, mot_input, tab)
            n = compteur_freq(tab)
            entropies = []
            for mot in lexique:
                entropies.append(entropie(recursive(0, mot, tab), n))
            resultat = [(entropies[i], (1 if lexique[i] in tab else 0), lexique[i]) for i in range(len(entropies))]
            resultat.sort()