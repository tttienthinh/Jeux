import pandas as pd
import numpy as np
import unicodedata

df = pd.read_excel('lexique/Lexique383.xlsb', engine='pyxlsb')
tab = df[['1_ortho', '7_freqlemfilms2']].to_numpy()
len(tab)

def remove_accents(mot):
    L = []
    for c in unicodedata.normalize('NFD', mot):
        if unicodedata.category(c) != 'Mn':
            L.append(c)
    return ''.join(L)

# lexique sans fréquence
lexique_5chars = []
for mot, f in tab:
    try:
        if (len(mot) == 5) and not (" " in mot) and not ("-" in mot):
            lexique_5chars.append(remove_accents(mot))
    except:
        print(mot)
lexique_5chars = np.array(lexique_5chars)
lexique_5chars = np.unique(lexique_5chars)
len(lexique_5chars)
np.save(open("lexique-5chars.npy", "wb"), lexique_5chars) # il faut supprimer le mot "pares"


# lexique avec fréquence
lexique_5chars_freq = []
for mot, f in tab:
    try:
        if (len(mot) == 5) and not (" " in mot) and not ("-" in mot):
            lexique_5chars_freq.append((remove_accents(mot), f))
    except:
        print(mot)
lexique_5chars_freq = np.array(lexique_5chars_freq)
dico = {}
for mot, freq in lexique_5chars_freq:
    freq = float(freq)
    if mot not in dico.keys():
        dico[mot] = freq
    else:
        dico[mot] += freq
lexique_5chars_freq = np.array(sorted([[mot, dico[mot]] for mot in dico.keys()]))
len(lexique_5chars_freq)
np.save(open("freq/lexique-5chars.npy", "wb"), lexique_5chars_freq)