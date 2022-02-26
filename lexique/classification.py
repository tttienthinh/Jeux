# import pandas as pd
pd = None
import numpy as np
import unicodedata

df = pd.read_excel('lexique/Lexique383.xlsb', engine='pyxlsb')
tab = df['1_ortho'].to_numpy()
len(tab)

def remove_accents(mot):
    L = []
    for c in unicodedata.normalize('NFD', mot):
        if unicodedata.category(c) != 'Mn':
            L.append(c)
    return ''.join(L)


tab5 = []
for mot in tab:
    try:
        if (len(mot) == 5) and not (" " in mot) and not ("-" in mot):
            tab5.append(remove_accents(mot))
    except:
        print(mot)
len(tab5)
tab5 = np.array(tab5)
tab5 = np.unique(tab5)
len(tab5)
np.save(open("lexique-5chars.npy", "wb"), tab5) # il faut supprimer le mot "pares"
