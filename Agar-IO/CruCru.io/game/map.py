"""Terrain de jeu"""

import time
import random
import math

if __name__ == "__main__":
    import sys
    sys.path.append("..")

from view.display import Display
from view.camera import Camera

from util.vector import Vect2d
from util.color import Color

from entity.cell import Cell
from entity.player import Player
from entity.enemy import Enemy
from entity.bush import Bush
from entity.creature import Creature

import config

class Map:
    """Terrain de jeu

    Attributs:
        size (Vect2d): taille de la map
        grid_size (Vect2d): taille de la grille des cellules
        grid (list of list of list of Cell): grille, tableau tridimensionnel

        game_finished (bool): jeu fini ou non

        bushes (list of Bush): buissons

        start_time (float): temps de début de jeu
        creatures (dict of list of Creature): créatures dans le jeu
                                              chaque clé du dictionnaire est
                                              l'id de la famille
        player_id (int): id du joueur
        focused_creature_id (int): id de la créature centrée par la caméra
        MAX_SPLIT (int): nombre maximal de créatures par famille
        CREATURES_MAX_SIZE (int): nombre total de familles de créatures

        player_infos (dict): score et temps du joueur
        all_usernames (list): liste de tous les noms d'utilisateur possibles

        all_cells (list of Cell): liste de toutes les cellules
        MAX_CELLS (int): nombre maximal de cellules
        NB_CELL_PER_SECOND (int): nombre de cellules par secondes
        DELTA_T_NEW_CELL (float): temps entre le spawn de deux cellules
        ref_time (float): temps depuis le dernier spawn de cellule
    """

    @classmethod
    def init(cls, width: int, height: int) -> None:
        """Initialisation de la map

        Args:
            width (int): largeur de la map
            height (int): hauteur de la map
        """

        Creature.notifyMapNewCreature = cls.createCreatureFromParent

        cls.size = Vect2d(width, height)

        cls.MAX_CELLS = config.MAX_CELLS
        cls.NB_CELL_PER_SECOND = config.NB_CELL_PER_SECOND
        cls.DELTA_T_NEW_CELL = config.DELTA_T_NEW_CELL
        cls.MAX_SPLIT = config.MAX_SPLIT

        cls.grid_size = Vect2d(config.GRID_WIDTH, config.GRID_HEIGHT)

        cls.CREATURES_MAX_SIZE = config.NB_ENEMIES+1

        try:
            f = open("./data/usernames.txt", 'r')
        except FileNotFoundError:
            print("Pas de fichier usernames.txt")
            cls.all_usernames = None
        else:
            cls.all_usernames = []

            line = f.readline()

            while line != "":
                line = line.replace('\n', '')
                line = line.replace('\r', '')

                cls.all_usernames.append(line)
                line = f.readline()

            f.close()
        cls.reset()

    @classmethod
    def reset(cls) -> None:
        """Réinitialise la map"""

        cls.start_time = time.time()

        cls.game_finished = False

        cls.player_infos = {}

        cls.all_cells = []

        cls.ref_time = -1*cls.DELTA_T_NEW_CELL

        cls.grid = [[[] for y in range(cls.grid_size.y)] for x in range(cls.grid_size.x)]

        cls.creatures = {}

        cls.player_id = cls.generateId()
        cls.focused_creature_id = cls.player_id

        player = Player(Vect2d(cls.size.x/2, cls.size.y/2),
                        "Player",
                        Color.randomColor(),
                        cls.player_id)

        cls.creatures[cls.player_id] = [player]
        # Création du joueur

        cls.bushes = []

        for i in range(config.NB_BUSHES):
            cls.createBush()

    @classmethod
    def generateId(cls) -> int:
        """Génère un nouvel id
        On pourrait aussi générer un id incrémentiel, mais ici c'est booon ça va

        Returns:
            int: id
        """

        return random.randrange(10**64)

    @classmethod
    def createBush(cls) -> None:
        """Crée un buisson qui ne soit pas en collision avec un autre buisson"""

        ok = False
        timeout = 0

        while not ok and timeout < 1000:
            ok = True

            pos = Vect2d(random.randrange(Bush.RADIUS*2, cls.size.x-Bush.RADIUS*2),
                         random.randrange(Bush.RADIUS*2, cls.size.x-Bush.RADIUS*2))

            for bush in cls.bushes:
                if Vect2d.dist(pos, bush.pos) < Bush.RADIUS*4:
                    ok = False

            timeout += 1

        if ok:
            cls.bushes.append(Bush(pos))

    @classmethod
    def createCreatureFromParent(cls, parent: Creature, is_player: bool, override_limit: bool) -> None:
        """Crée une nouvelle créature en fonction du parent pour le split

        Args:
            parent (Creature): créature parente
            is_player (bool): joueur ou ennemi ?
            override_limit (bool): si la limite de split doit être prise
                                   en compte ou non
        """

        if len(cls.creatures[parent.creature_id]) < cls.MAX_SPLIT or override_limit:
            parent.score //= 2
            parent.inertia = 0.25

            if is_player:
                creature = Player(parent.pos.copy(), parent.name, parent.color, parent.creature_id)
            else:
                creature = Enemy(parent.pos.copy(), parent.name, parent.color, parent.creature_id)

            creature.family.extend(parent.family)
            parent.family = creature.family

            creature.score = parent.score
            creature.radius = 1
            creature.img = parent.img

            creature.speed = parent.speed.copy()
            creature.split_speed = 2

            cls.creatures[parent.creature_id].append(creature)

    @classmethod
    def createEnemy(cls) -> None:
        """Crée un nouvel ennemi en évitant le spawn-kill, apparition sur une
        autre créature"""

        ok = False
        timed_out = False
        compt = 0

        while not ok and not timed_out:
            ok = True

            pos = Vect2d(random.randrange(Creature.BASE_RADIUS*2, cls.size.x-Creature.BASE_RADIUS*2),
                         random.randrange(Creature.BASE_RADIUS*2, cls.size.y-Creature.BASE_RADIUS*2))

            for k in cls.creatures.keys():
                creatures_list = cls.creatures[k]

                for creature in creatures_list:
                    if Vect2d.dist(pos, creature.pos) < (Creature.BASE_RADIUS + creature.radius)*2:
                        ok = False

            if compt == 10:
                timed_out = True

            compt += 1

        if not timed_out:
            enemy_id = cls.generateId()

            if cls.all_usernames is None:
                size = random.randint(3, 5)
                name = cls.generateNewName(size)
            else:
                name = cls.all_usernames[random.randrange(len(cls.all_usernames))]

            enemy = Enemy(pos, name, Color.randomColor(), enemy_id)

            cls.creatures[enemy_id] = [enemy]

    @staticmethod
    def generateNewName(size: int) -> str:
        """Génère un nouveau nom
        Fonction utilisée si le fichier usernames.txt n'existe pas

        Args:
            size (int): nombre de syllabes du nom voulu

        Returns:
            name (str): nom généré
        """

        consonants = ('b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'z')
        vowels = ('a', 'e', 'i', 'o', 'u', 'y', 'ai', 'ei', 'eu', 'ey', 'ie', 'io', 'oi', 'ou', 'oy', 'ya', 'ye', 'yi', 'yo', 'yu')

        name = ""

        for i in range(size):
            name += consonants[random.randrange(len(consonants))]
            name += vowels[random.randrange(len(vowels))]

        return name

    @classmethod
    def setMousePos(cls, mouse_pos: Vect2d) -> None:
        """Applique la nouvelle position de la souris

        Args:
            mouse_pos (Vect2d): nouvelle position
        """

        for player in cls.creatures[cls.player_id]:
            player.mouse_pos = mouse_pos - Vect2d(Display.size.x/2, Display.size.y/2)
            player.mouse_pos += Camera.pos - player.pos + Vect2d(Display.size.x/2, Display.size.y/2)

    @classmethod
    def updateStats(cls) -> None:
        """Met à jour les statistiques du jeu"""

        for k in cls.creatures.keys():
            creatures_list = cls.creatures[k]

            if k == cls.player_id:
                score_player = 0

                for creature in creatures_list:
                    score_player += creature.score

                cls.player_infos["score"] = score_player
                cls.player_infos["time"] = int(1000*(time.time() - cls.start_time))/1000

            for creature in creatures_list:
                if creature.radius*2 >= min(cls.size.toTuple()):
                    cls.game_finished = True

    @classmethod
    def handleBushSplit(cls) -> None:
        """Gère le split lié aux buissons"""

        for k in cls.creatures.keys():
            creatures_list = cls.creatures[k]

            for creature in creatures_list:
                if creature.radius > Bush.RADIUS:
                    for bush in cls.bushes:
                        if Vect2d.dist(bush.pos, creature.pos) < creature.radius:
                            bush.hit()
                            creature.split(is_player=(creature.creature_id == cls.player_id),
                                           override_limit=True)

    @classmethod
    def updateEnemies(cls) -> None:
        """Met à jour les ennemis"""

        creatures_info = {}

        for k in cls.creatures.keys():
            creatures_list = cls.creatures[k]

            creatures_info[k] = []

            for creature in creatures_list:
                creatures_info[k].append((creature.pos.copy(), creature.radius, creature.score))

        for k in cls.creatures.keys():
            enemy_list = cls.creatures[k]

            if k != cls.player_id:
                for enemy in enemy_list:
                    enemy.setMapCell(cls.getCellPosMap())

                    other_creatures_infos = []

                    for k2 in creatures_info.keys():
                        if k != k2:
                            for elem in creatures_info[k2]:
                                other_creatures_infos.append(elem)

                    enemy.setCreaturesInfo(other_creatures_infos)
                    enemy.update(cls.size)

    @classmethod
    def update(cls) -> None:
        """Mise à jour générale de la map"""

        if len(cls.creatures) < cls.CREATURES_MAX_SIZE:
            cls.createEnemy()

        for bush in cls.bushes:
            bush.update()

        cls.handleBushSplit()

        Creature.map_size = Map.size

        if cls.isPlayerAlive():
            for player in cls.creatures[cls.player_id]:
                player.update(cls.size)

        cls.updateEnemies()

        cls.updateStats()

        for k in cls.creatures.keys():
            creatures_list = cls.creatures[k]

            for creature in creatures_list:
                cls.detectCellHitbox(creature)

        cls.detectEnemyHitbox()

        cls.garbageCollect()

        for i in range(cls.NB_CELL_PER_SECOND):
            cls.createNewCell()

    @classmethod
    def garbageCollect(cls) -> None:
        """Purge les créatures mortes"""

        for i in range(len(cls.bushes)):
            if not cls.bushes[i].is_alive:
                del cls.bushes[i]

        focused_killer_id = None

        for k in cls.creatures.keys():
            for i in range(len(cls.creatures[k])-1, -1, -1):
                if not cls.creatures[k][i].is_alive:
                    if k == cls.focused_creature_id:
                        focused_killer_id = cls.creatures[k][i].killer_id

                    del cls.creatures[k][i]

        for k in list(cls.creatures.keys()):
            if len(cls.creatures[k]) == 0:
                if k == cls.focused_creature_id:
                    cls.focused_creature_id = focused_killer_id

                del cls.creatures[k]

    @classmethod
    def getFocusedPos(cls) -> Vect2d:
        """Retourne la position de focus, pour la caméra

        Returns:
            pos (Vect2d): position
        """

        pos = Vect2d(0, 0)

        for creature in cls.creatures[cls.focused_creature_id]:
            pos += creature.pos

        pos /= len(cls.creatures[cls.focused_creature_id])

        return pos

    @classmethod
    def getFocusedRadius(cls) -> float:
        """Retourne le rayon de la créature focusée, pour le zoom"""

        radius = 0

        for creature in cls.creatures[cls.focused_creature_id]:
            radius += creature.radius

        radius /= len(cls.creatures[cls.focused_creature_id])

        return radius

    @classmethod
    def isPlayerAlive(cls) -> bool:
        """Joueur vivant ou non ?"""

        try:
            is_alive = cls.creatures[cls.player_id][0].is_alive
        except KeyError:
            is_alive = False

        return is_alive

    @classmethod
    def detectEnemyHitbox(cls) -> None:
        """Gère la hitbox des créatures"""

        for k1 in cls.creatures.keys():
            for k2 in cls.creatures.keys():
                enemy_list_1 = cls.creatures[k1]
                enemy_list_2 = cls.creatures[k2]

                for enemy_1 in enemy_list_1:
                    for enemy_2 in enemy_list_2:
                        if enemy_1 is not enemy_2 and enemy_1.is_alive and enemy_2.is_alive:
                            dist = Vect2d.dist(enemy_1.pos, enemy_2.pos)

                            if k1 == k2 :
                                t1 = time.time() - enemy_1.invincibility_family_time
                                t2 = time.time() - enemy_2.invincibility_family_time

                                if t1 > Creature.SPLIT_TIME and t2 > Creature.SPLIT_TIME:
                                    if dist <= max(enemy_1.radius, enemy_2.radius):
                                        enemy_1.kill(enemy_2.score)
                                        enemy_2.killed(k1)

                                        family_tmp = []

                                        for creature in enemy_1.family:
                                            if creature is not enemy_2:
                                                family_tmp.append(creature)

                                        enemy_1.family = family_tmp
                            else:
                                if Creature.canEat(enemy_1.radius, enemy_2.radius):
                                    if dist <= max(enemy_1.radius, enemy_2.radius):
                                        enemy_1.kill(enemy_2.score)
                                        enemy_2.killed(k1)

    @classmethod
    def getCellPosMap(cls):
        res = [[None for i in range(cls.grid_size.y)] for j in range(cls.grid_size.x)]

        for x in range(cls.grid_size.x):
            for y in range(cls.grid_size.y):
                content = []

                for cell in cls.grid[x][y]:
                    content.append(cell.pos.copy())

                res[x][y] = tuple(content)
        return res

    @classmethod
    def createNewCell(cls) -> None:
        if time.time() - cls.ref_time > cls.DELTA_T_NEW_CELL:
            cls.ref_time = time.time()

            x = random.randrange(Cell.BASE_RADIUS, cls.size.x-Cell.BASE_RADIUS)
            y = random.randrange(Cell.BASE_RADIUS, cls.size.y-Cell.BASE_RADIUS)
            cell = Cell(Vect2d(x, y))

            ok = True

            for k in cls.creatures.keys():
                enemy_list = cls.creatures[k]

                for enemy in enemy_list:
                    if Vect2d.dist(enemy.pos, cell.pos) < cell.radius + enemy.radius:
                        ok = False

            x = int(cell.pos.x / cls.size.x * cls.grid_size.x)
            y = int(cell.pos.y / cls.size.y * cls.grid_size.y)

            if ok:
                cls.all_cells.append(cell)
                cls.grid[x][y].append(cell)

            if len(cls.all_cells) >= cls.MAX_CELLS:
                cls.deleteCell(0)

    @classmethod
    def display(cls):
        """Affichage de la map"""

        w = cls.size.x
        h = cls.size.y

        for x in range(1, cls.grid_size.x):
            # Lignes entre la grille
            Display.drawLine(Vect2d(x*w/cls.grid_size.x, 0),
                             Vect2d(x*w/cls.grid_size.x, h),
                             color=Color.DARK_GRAY,
                             base_pos=Camera.pos)

        for y in range(1, cls.grid_size.y):
            Display.drawLine(Vect2d(0, y*h/cls.grid_size.y),
                             Vect2d(w, y*h/cls.grid_size.y),
                             color=Color.DARK_GRAY,
                             base_pos=Camera.pos)

        Display.drawLine(Vect2d(0, 0), Vect2d(w, 0), color=Color.RED, base_pos=Camera.pos)
        Display.drawLine(Vect2d(w, 0), Vect2d(w, h), color=Color.RED, base_pos=Camera.pos)
        Display.drawLine(Vect2d(w, h), Vect2d(0, h), color=Color.RED, base_pos=Camera.pos)
        Display.drawLine(Vect2d(0, h), Vect2d(0, 0), color=Color.RED, base_pos=Camera.pos)

        cls.displayCell()

        for k in cls.creatures.keys():
            enemy_list = cls.creatures[k]

            if k != cls.player_id:
                for enemy in enemy_list:
                    enemy.display()

        if cls.isPlayerAlive():
            for player in cls.creatures[cls.player_id]:
                player.display()

        for i in range(len(cls.bushes)):
            cls.bushes[i].display()

        x = Display.size.x/2
        y = Display.size.y/2
        r = min(x, y)/50

        Display.drawLine(Vect2d(x-r, y-r), Vect2d(x+r, y+r), color=Color.RED)
        Display.drawLine(Vect2d(x-r, y+r), Vect2d(x+r, y-r), color=Color.RED)

        Camera.setPos(cls.getFocusedPos())

        r = cls.getFocusedRadius() - Creature.BASE_RADIUS
        r = abs(r)
        r = r**0.1
        z = math.exp(-r+1)
        Display.zoom(z)

    @classmethod
    def displayCell(cls) -> None:
        for i in range(len(cls.all_cells)):
            cls.all_cells[i].display()

    @classmethod
    def splitPlayer(cls):
        if cls.isPlayerAlive():
            player_list = cls.creatures[cls.player_id]
            player_list_tmp = []

            for player in player_list:
                player_list_tmp.append(player)

            for player in player_list_tmp:
                player.split(is_player=True)

    @classmethod
    def detectCellHitbox(cls, creature: Creature) -> None:
        for i in range(len(cls.all_cells)-1, -1, -1):
            cell_i = cls.all_cells[i]

            if Vect2d.distSq(creature.pos, cell_i.pos) < (creature.radius+cell_i.radius)**2:
                creature.score += cell_i.score
                cls.deleteCell(i)

    @classmethod
    def deleteCell(cls, index: int):
        """Supprime une cellule

        Args:
            index (int): index de cls.all_cells de la cellule à supprimer,
                         supprimée aussi dans cls.grid
        """

        cell = cls.all_cells[index]

        x = int(cell.pos.x/cls.size.x * cls.grid_size.x)
        y = int(cell.pos.y/cls.size.y * cls.grid_size.y)

        for i in range(len(cls.grid[x][y])-1, -1, -1):
            if cell == cls.grid[x][y][i]:
                del cls.grid[x][y][i]

        del cls.all_cells[index]
