import pygame
import random
from App import *
from Param import *

vec = pygame.math.Vector2

class Fantome:

    def __init__(self, app, pos, idx):
        self.app = app
        self.pos_grille = pos
        self.start_pos = [pos.x, pos.y]
        self.pix_pos = self.get_pix_pos()
        self.idx = idx
        self.image = self.set_image()
        self.direction = vec(0, 0)
        self.personnalite = self.set_personnalite()
        self.cible = None
        self.speed = self.set_speed()
        #print(self.type_self.cible = self.set_cible()personnalite)

    def update(self):
        self.cible = self.set_cible()
        if self.cible != self.pos_grille:
            self.pix_pos += self.direction*self.speed
            if self.time_to_move():
                self.move()

        # Donne la position sur la grille en fonction de la position en pixels (pix_pos)
        self.pos_grille[0] = (self.pix_pos[0] - ESPACE + self.app.caseW//4)// self.app.caseW + 2
        self.pos_grille[1] = (self.pix_pos[1] - ESPACE + self.app.caseH//4)// self.app.caseH + 2

    def draw(self, screen):

        screen.blit(self.image, (int(self.pix_pos.x), int(self.pix_pos.y)))

    def set_cible(self):
        if self.personnalite == "Suiveur" or self.personnalite == "SuiveurLent":
            return self.app.joueur.pos_grille
        else:
            if self.app.joueur.pos_grille.x > COLONNES//2 and self.app.joueur.pos_grille.y > LIGNES//2: #Si le joueur est en bas a droire du labyrinthe
                return vec(1, 1)

            if self.app.joueur.pos_grille.x > COLONNES//2 and self.app.joueur.pos_grille.y < LIGNES//2: #Si le joueur est en haut a droire du labyrinthe
                return vec(1, LIGNES-2)

            if self.app.joueur.pos_grille.x < COLONNES//2 and self.app.joueur.pos_grille.y > LIGNES//2: #Si le joueur est en bas a gauche du labyrinthe
                return vec(COLONNES-2, 1)

            else: #Si le joueur est en haut a gauche du labyrinthe
                return vec(COLONNES-2, LIGNES-2)

    def set_speed(self): #Donne une vitesse au fantomes en foction de leur humeur
        if self.personnalite in ["Suiveur"]:
            speed = 2
        elif self.personnalite in ["SuiveurLent"]:
            speed = 1
        elif self.personnalite in ["Effrayé"]:
            speed = 2
        elif self.personnalite in ["Random"]:
            speed = 2
        return speed

    def time_to_move(self):
        if int(self.pix_pos.x) % self.app.caseW == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0):
                return True

        if int(self.pix_pos.y) % self.app.caseH == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0):
                 return True
        return False

    def move(self):
        if self.personnalite == 'Suiveur':
            self.direction = self.get_path_direction(self.cible)

        if self.personnalite == 'SuiveurLent':
            self.direction = self.get_path_direction(self.cible)

        if self.personnalite == 'Random':
            self.direction = self.get_random_direction()

        if self.personnalite == 'Effrayé':
            self.direction = self.get_path_direction(self.cible)

    def get_path_direction(self, cible):
        next_case = self.find_next_case_in_path(cible)

        x_dir = next_case[0] - self.pos_grille[0]
        y_dir = next_case[1] - self.pos_grille[1]

        return vec(x_dir, y_dir)

    def find_next_case_in_path(self, cible):
        path = self.BFS([int(self.pos_grille.x), int(self.pos_grille.y)],[int(cible.x), int(cible.y)])

        return path[1]

    def BFS(self, start, cible): # Algo de parcours en largeur pour obtenir le plus_court_chemin d'un point de départ à une cible

    # On définit les murs dans lesquels les fantomes ne doivent pas passer
        grille = [[0 for x in range(28)] for x in range(30)]
        for case in self.app.murs:
            if case.x < 28 and case.y < 30:
                grille[int(case.y)][int(case.x)] = 1 # On donne au cases qui sont des murs la valeur 1

        for case in self.app.f_nope:
            if case.x < 28 and case.y < 30:
                grille[int(case.y)][int(case.x)] = 1

    # On crée trois listes
        queue = [start] # La queue
        chemin = [] # Liste des cases par lesquelles passer pour atteindre la cible
        visited = [] # Liste des cases sur lesquelles on est déja allé pour atteindre la cible
        while queue:
            actuel = queue[0]
            queue.remove(queue[0])# On enlève la case sur laquelle on se trouve de la queue pour ne pas la reprendre dans le chemin
            visited.append(actuel) # On ajoute la case dans les cases visitées pour ne pas y retourner
            if actuel == cible: # Si on atteind la cible on arrête de chercher
                break
            else:
                voisins = [[0, -1], [1, 0], [0, 1], [-1, 0]] # Haut, Droite, Gauche, Bas
                for voisin in voisins:
                    if voisin[0]+actuel[0] >= 0 and voisin[0]+actuel[0] < len(grille[0]): # On vérifie si notre prochain déplacement n'est pas en dehors de l'arène
                        if voisin[1]+actuel[1] >= 0 and voisin[1]+actuel[1] < len(grille):
                            next_case = [voisin[0] + actuel[0], voisin[1] + actuel[1]]
                            if next_case not in visited: # On vérifie que la prochaine case on est suceptible d'aller n'a pas déja été visitée
                                if grille[next_case[1]][next_case[0]] != 1: # On vérifie que cette case n'est pas un mur
                                    queue.append(next_case) # on met dans la queue la prochaine case dans lauelle on va aller
                                    chemin.append({"Actuel": actuel, "Next case": next_case}) #On crée un dictionnaire avec nottre case actuelle et la prochaine case
        plus_court_chemin = [cible]

        while cible != start: # Tant qu'on est pas sur la cible ( pacman)
            for pas in chemin: # pour tout les pas dans le chemin ( 1 pas = un case)
                if pas["Next case"] == cible: #si le pas est notre cible alors la cible devient notre prochain pas
                    cible = pas["Actuel"]
                    plus_court_chemin.insert(0, pas["Actuel"])


        return plus_court_chemin # On renvoie le chemin par lequel le fantome doit passer pour ateindre pacman le plus rapidement possible

    def get_random_direction(self):
        while True:
            number = random.randint(0, 3)
            if number == 0: # Aller vers la droite
                x_dir = 1
                y_dir = 0

            elif number == 1: # Aller vers le bas
                x_dir = 0
                y_dir = 1

            elif number == 2: # Aller vers la gauche
                x_dir = -1
                y_dir = 0

            else: # Aller vers le haut
                x_dir = 0
                y_dir = -1

            next_pos = vec(self.pos_grille.x + x_dir, self.pos_grille.y + y_dir)
            if next_pos not in self.app.murs:
                break

        return vec(x_dir, y_dir)


    def get_pix_pos(self):
        return vec((self.pos_grille.x*self.app.caseW)+ESPACE - self.app.caseW*1.5,
                   (self.pos_grille.y*self.app.caseH)+ESPACE - self.app.caseH*1.5) # Position en pixel d'un fantome

    def set_image(self):#On donne une tête a chaques fantomes indexé
        if self.idx == 0:
            return imgPinkyLeft
        if self.idx == 1:
            return imgBlinkyRight
        if self.idx == 2:
            return imgInkyDown
        if self.idx == 3:
            return imgClydeUp


#On donne une personnalié a une index qui faire reference a un fantome
#Deux fantomes suivront pacman
#Un fantome aura peur de PacMan
#Un fantome ferra des mouvement aléatoire
    def set_personnalite(self):
        if self.idx == 0:
            return "SuiveurLent"
        elif self.idx == 1:
            return "Suiveur"
        elif self.idx == 2:
            return "Random"
        else:
            return "Effrayé"
