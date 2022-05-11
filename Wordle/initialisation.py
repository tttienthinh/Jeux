import numpy as np

"""
Il n'est pas utile de recalculer à chaque fois les premières propositions qui sont universelles à la langue utilisé, ici le français

Calculons le une fois pour toute
"""
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

# Initialisation
tab = list(lexique)
n = len(tab)
entropies = []
for mot in lexique:
    entropies.append(entropie(recursive(0, mot, tab), n))
resultat = [(entropies[i], (1 if lexique[i] in tab else 0), lexique[i]) for i in range(len(entropies))]
resultat.sort()
print([(round(r, 2), x) for r, _, x in resultat[-8:]])