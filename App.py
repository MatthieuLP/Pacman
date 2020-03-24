import pygame
import sys
from Param import *
from Joueur import *
from Fantome import *

pygame.init()
vec = pygame.math.Vector2


class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((WindowW, WindowH))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'start'
        self.caseW = MazeW//COLONNES
        self.caseH = MazeH//LIGNES
        self.joueur = Joueur(self, JOUEUR_START_POS)
        self.case_vides = [] # 0
        self.murs = []       # 5
        self.bouffes = []    # 1
        self.Gbouffes = []   # 8
        self.porte = []      # P
        self.f_nope = []     # N
        self.all = []        # Toutes les cases
        self.fantomes = []
        self.f_pos = []

        #self.make_fantomes()
        self.load()

    def run(self):
        while self.running:
            if self.state == 'start':
                self.start_events()
                self.start_draw()
            elif self.state == 'playing':
                self.playing_events()
                self.playing_update()
                self.playing_draw()
            elif self.state == 'Game Over':
                self.game_over_events()
                self.game_over_draw()
            elif self.state == 'Game Win':
                self.game_win_events()
                self.game_win_draw()
            else:
                self.running = False
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

############################### Fonctions d'Aide ###############################

    def draw_texte(self, mots, screen, pos, taille, couleur, police, centered=False):
        police = pygame.font.SysFont(police, taille)
        texte = police.render(mots, False, couleur)
        taille_texte = texte.get_size()
        pos = list(pos)
        if centered == True:
            pos[0] = pos[0] - taille_texte[0]//2
            pos[1] = pos[1] - taille_texte[1]//2
        screen.blit(texte, pos)

    def load(self):
        self.background = pygame.image.load('Images/maze.png')
        self.background = pygame.transform.scale(self.background, (MazeW, MazeH))

        # On crée une liste des différent objets avec leurs coodonées dans la matrice
        with open('maze.txt', 'r') as file:
            for y_idx, line in enumerate(file): # Donne un indice a chaques lignes
                for x_idx, char, in enumerate(line): # Donne un indice a chaques colonnes

                    if char == '5': # Crée une liste de murs
                        self.murs.append(vec(x_idx, y_idx))

                    elif char == '1': #Crée une liste de petites bouffes
                        self.bouffes.append(vec(x_idx, y_idx))

                    elif char == '8': #Crée une liste de GROSSES bouffes
                        self.Gbouffes.append(vec(x_idx, y_idx))

                    elif char == '0':
                        self.case_vides.append(vec(x_idx, y_idx))

                    elif char == 'E':
                        self.porte.append(vec(x_idx, y_idx))

                    elif char in ["P", "B", "I", "C"]:
                        self.f_pos.append(vec(x_idx, y_idx))

                    elif char == 'N':
                        self.f_nope.append(vec(x_idx, y_idx))

        #print(self.f_pos)

        # Pour chaques fantomes a une position on crée un fantome a cette position
        # On leur donne un numéro pour leur faire une personnalité dans "Fantome.py"
        for idx, pos in  enumerate(self.f_pos):
            self.fantomes.append(Fantome(self, pos, idx))

    def draw_grille(self): #Fonction qui affiche les murs et la grille de la matrice
        for x in range(WindowW//self.caseW):
            pygame.draw.line(self.background, GRIS, (x*self.caseW, 0), (x*self.caseW, WindowH))

        for x in range(WindowH//self.caseH):
            pygame.draw.line(self.background, GRIS, (0, x*self.caseH), (WindowW, x*self.caseH))
            """
        for mur in self.murs:
            pygame.draw.rect(self.background, ROSE, (mur.x*self.caseW, mur.y*self.caseH, self.caseW, self.caseH))
            """
    def draw_bouffe(self):
        for bouffe in self.bouffes:
            pygame.draw.circle(self.screen, JAUNE, (int(bouffe.x*self.caseW + self.caseW//2 + ESPACE//2), int(bouffe.y*self.caseH + self.caseH//2 + ESPACE//2)), 3)

        for Gbouffe in self.Gbouffes:
            pygame.draw.circle(self.screen, JAUNE, (int(Gbouffe.x*self.caseW + self.caseW//2 + ESPACE//2) , int(Gbouffe.y*self.caseH + self.caseH//2 + ESPACE//2)), 7)

    def reset(self):

        self.joueur.score_joueur = 0
        self.joueur.vies = NB_VIES

        self.bouffes = []
        self.Gbouffes = []

        # On reset la position du joueur
        self.joueur.pix_pos = vec(14.5*self.caseW, 24*self.caseH)
        self.joueur.stored_direction = None
        self.joueur.direction = vec(0, 0)

        # On reset la position des fantomes
        for fantome in self.fantomes:
            fantome.pos_grille = vec(fantome.start_pos)
            fantome.pix_pos = fantome.get_pix_pos()
            fantome.direction *= 0

        with open('maze.txt', 'r') as file:
            for y_idx, line in enumerate(file):
                for x_idx, char in enumerate(line):
                    if char == '1': #recrée une liste de petites bouffes
                        self.bouffes.append(vec(x_idx, y_idx))

                    elif char == '8': #recrée une liste de GROSSES bouffes
                        self.Gbouffes.append(vec(x_idx, y_idx))



        self.state = 'playing'

########################### Fonctions d'Introduction ###########################

    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = 'playing'

    def start_draw(self):
        self.screen.fill(NOIR)
        self.draw_texte('APPUYEZ SUR ESPACE', self.screen, [WindowW//2, WindowH//2 - 50],  TAILLE_TEXTE_ACCEUIL, ORANGE, POLICE_ACCEUIL, True)
        self.draw_texte('1 JOUEUR', self.screen, [WindowW//2, WindowH//2 + 50],  TAILLE_TEXTE_ACCEUIL, AQUA, POLICE_ACCEUIL, True)
        pygame.display.update()

############################### Fonctions de Jeu ###############################


    def playing_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP :
                self.joueur.move(MoveUp)
                #Faire tourner Pacman dans le bon sens

            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN :
                self.joueur.move(MoveDown)
                #Faire tourner Pacman dans le bon sens

            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT :
                self.joueur.move(MoveLeft)
                #Faire tourner Pacman dans le bon sens

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT :
                self.joueur.move(MoveRight)
                #Faire tourner Pacman dans le bon sens

    def playing_update(self):
        self.joueur.update()

        for fantome in self.fantomes:
            fantome.update()
            if fantome.pos_grille == self.joueur.pos_grille:
                self.enlever_vie();

        if self.bouffes == [] and self.Gbouffes == [] :
            self.state = 'Game Win'

    def playing_draw(self):
        self.screen.fill(NOIR)
        self.screen.blit(self.background, (ESPACE//2, ESPACE//2))
        self.draw_bouffe()
        #self.draw_grille()
        self.draw_texte("SCORE : " + str(self.joueur.score_joueur) , self.screen, [WindowW//2, 10], 15, BLANC, POLICE_ACCEUIL, True)
        self.joueur.draw(self.screen)

        # Faire apparaître l'écran victoire ( Quand les listes de bouffes sont vide)
        #self.bouffes = []
        #self.Gbouffes = []

        for fantome in self.fantomes:
            fantome.draw(self.screen)

        pygame.display.update()

    def enlever_vie(self):
        self.joueur.vies -= 1

        if self.joueur.vies == 0:
            self.state = 'Game Over'
        else:
            # On reset la position du joueur
            self.joueur.pix_pos = vec(14.5*self.caseW, 24*self.caseH)
            self.joueur.stored_direction = None
            self.joueur.direction = vec(0, 0)
            # On reset la position des fantomes
            for fantome in self.fantomes:
                fantome.pos_grille = vec(fantome.start_pos)
                fantome.pix_pos = fantome.get_pix_pos()
                fantome.direction *= 0

############################## Fonctions Game Over #############################

    def game_over_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.reset()

    def game_over_draw(self): # Ecran de defaite
        self.screen.fill(NOIR)
        self.draw_texte("YOU LOSE", self.screen,[WindowW//2, WindowH//2 - 50], 50, ROUGE, POLICE_ACCEUIL, True )
        self.draw_texte("APPUYEZ SUR ESPACE POUR ESSAYER D'ÊTRE MEILLEUR", self.screen,[WindowW//2, WindowH//2 + 100], TAILLE_TEXTE_ACCEUIL, BLANC, POLICE_ACCEUIL, True )
        self.draw_texte("Votre score est : " + str(self.joueur.score_joueur), self.screen,[WindowW//2, WindowH//2 + 150], TAILLE_TEXTE_ACCEUIL, BLANC, POLICE_ACCEUIL, True )
        self.draw_texte("APPUYEZ SUR ECHAP POUR RAGEQUIT", self.screen,[WindowW//2, WindowH//2 + 300], 10, BLANC, POLICE_ACCEUIL, True )
        pygame.display.update()


############################## Fonctions Game Win ##############################


    def game_win_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.reset()

    def game_win_draw(self): # Ecran de vitoire
        self.screen.fill(NOIR)
        self.draw_texte("YOU WON", self.screen,[WindowW//2, WindowH//2 - 50], 50, JAUNE, POLICE_ACCEUIL, True )
        self.draw_texte("APPUYEZ SUR ESPACE POUR RECOMMENCER", self.screen,[WindowW//2, WindowH//2 + 100], TAILLE_TEXTE_ACCEUIL, BLANC, POLICE_ACCEUIL, True )
        self.draw_texte("Votre score est : " + str(self.joueur.score_joueur), self.screen,[WindowW//2, WindowH//2 + 150], TAILLE_TEXTE_ACCEUIL, BLANC, POLICE_ACCEUIL, True )
        self.draw_texte("APPUYEZ SUR ECHAP POUR QUITTER", self.screen,[WindowW//2, WindowH//2 + 300], 10, BLANC, POLICE_ACCEUIL, True )
        pygame.display.update()
