import pygame
from App import *
from Param import *

vec = pygame.math.Vector2

class Joueur:
    def __init__(self, app, pos):
        self.app = app
        self.pos_grille = pos
        self.pix_pos = self.get_pix_pos()
        self.direction = vec(0, 0) # Direction de base
        self.stored_direction = None
        self.allowed_to_move = True
        self.score_joueur = 0
        self.speed = VITESSE_JOUEUR
        self.vies = NB_VIES

    def update(self):
        #self.draw(self.app.screen)

        if self.allowed_to_move:
            self.pix_pos += self.direction*self.speed
        if self.time_to_move():
            if self.stored_direction != None :
                self.direction = self.stored_direction
            self.allowed_to_move = self.can_move()

        if self.sur_bouffe():
            self.app.bouffes.remove(vec(self.pos_grille))
            self.app.case_vides.append(vec(self.pos_grille))
            self.score_joueur += 10

        if self.sur_Gbouffe():
            self.app.Gbouffes.remove(vec(self.pos_grille))
            self.app.case_vides.append(vec(self.pos_grille))
            self.score_joueur += 50

        # Donne la position sur la grille en fonction de la position en pixels (pix_pos)
        self.pos_grille[0] = (self.pix_pos[0] - ESPACE + self.app.caseW//4)// self.app.caseW + 2
        self.pos_grille[1] = (self.pix_pos[1] - ESPACE + self.app.caseH//4)// self.app.caseH + 2

        # Si Pacman sort d'un des coté du maze, il est tp de l'autre coté
        if self.out_of_maze_right():
            self.pix_pos = vec(2*self.app.caseW, 15*self.app.caseH)

        if self.out_of_maze_left():
            self.pix_pos = vec(27*self.app.caseW, 15*self.app.caseH)

        # print(self.pos_grille) # Affiche la position de pacman sur la grille dans le terminal

    def draw(self, screen):

        if self.direction == MoveUp:
            screen.blit(imgPacmanUp, (int(self.pix_pos.x), int(self.pix_pos.y)))

        if self.direction == MoveDown:
            screen.blit(imgPacmanDown, (int(self.pix_pos.x), int(self.pix_pos.y)))

        if self.direction == MoveLeft:
            screen.blit(imgPacmanLeft, (int(self.pix_pos.x), int(self.pix_pos.y)))

        if self.direction == MoveRight:
            screen.blit(imgPacmanRight, (int(self.pix_pos.x), int(self.pix_pos.y)))

        if self.direction == vec(0, 0):
            screen.blit(imgPacmanLeft, (int(self.pix_pos.x), int(self.pix_pos.y)))
        # Affiche les vies du joueurs
        for x in range(self.vies):
            self.app.draw_texte('VIES RESTANTES :', screen, (10, WindowH - 25), TAILLE_TEXTE_ACCEUIL, BLANC, POLICE_ACCEUIL)
            screen.blit(imgPacmanLeft, (175 + 20*x, WindowH - 30))

        # Affiche la position sur la grille
        """
        pygame.draw.rect(self.app.screen, ROUGE, (self.pos_grille[0]*self.app.caseW+ESPACE//2,
                                                  self.pos_grille[1]*self.app.caseH+ESPACE//2,
                                                  self.app.caseW,
                                                  self.app.caseH), 1)
        """
    def get_pix_pos(self):
        return vec((self.pos_grille.x*self.app.caseW)+ESPACE - self.app.caseW*1.5,
                   (self.pos_grille.y*self.app.caseH)+ESPACE - self.app.caseH*1.5) # Position en pixel du joueur

    def move(self, direction):
        self.stored_direction = direction

    def time_to_move(self): # Pacman ne peut bouger que dans les cases
        if int(self.pix_pos.x) % self.app.caseW == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0):
                return True

        if int(self.pix_pos.y) % self.app.caseH == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0):
                 return True

    def can_move(self):

        for mur in self.app.murs:
            if vec(self.pos_grille + self.direction) == mur:
                return False

        for porte in self.app.porte:
            if vec(self.pos_grille + self.direction) == porte:
                return False

        return True

    def sur_bouffe(self):

        for bouffe in self.app.bouffes:
            if vec(self.pos_grille) == bouffe:
                return True
        return False

    def sur_Gbouffe(self):

        for Gbouffe in self.app.Gbouffes:
            if vec(self.pos_grille) == Gbouffe:
                return True
        return False

    def out_of_maze_right(self):
        if self.pos_grille == vec(28, 14):
            return  True

    def out_of_maze_left(self):
        if self.pos_grille == vec(0, 14):
            return  True
