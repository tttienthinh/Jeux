### AJOUTS :
* Tableau des meilleurs scores
* Slider sur menu principal pour config
* Monde infini
* Demander nom joueur
* Serveur

### CORRECTIONS :
* Threads IA ? -> Non, perte de performances via threads ou même via multicore (Process ou Pool, les 2 sont plus lents)
* D'abord chercher à vider le carré dans lequel l'ennemi est
* HSV -> HSB (ou HSL)
* Config custom (avec par exemple une valeur par défaut, un min, un max) -> cf. VISI201
* Vect2d : héritage de list ?
* Transformer toutes les couleurs en Color (qui hériterait de list)
* Avec les 2 idées précédentes on peut utiliser directement Vect2d et Color en parametre de fonction
* Vect2d : pouvoir le choisir constant ?

### BUGS :
* F11 fin de jeu
* Ennemis qui se chevauchent parfois
* Ennemis qui tapent les bords
* Si target dans coin alors hunter l'aura jamais et va bug dessus
* Comportement circulaire
* Resize marche mal -> la faute de pygame ?

Cf. gota.io ou agar.io

Doc : 
https://docs.python.org/3/library/enum.html <br />
https://docs.python.org/3/library/abc.html <br />
https://docs.python.org/3/library/functions.html?highlight=property#property <br />
