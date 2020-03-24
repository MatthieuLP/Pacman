from pygame.math import Vector2 as vec
import pygame

# Paramètres de l'écran
WindowW, WindowH =  610, 670
ESPACE = 50
MazeW, MazeH =  WindowW - ESPACE, WindowH - ESPACE
FPS = 60
ESPACE = 50

LIGNES = 30
COLONNES = 28

# Paramètres de couleur
NOIR = (0, 0, 0)
GRIS = (107, 107, 107)
BLANC = (255, 255, 255)

ORANGE = (170, 132, 58)
AQUA = (36, 133, 170)
ROUGE = (255, 0, 0)
JAUNE = (190, 194, 15)
ROSE = (255, 105, 180)


# Paramètres d'acceuil
POLICE_ACCEUIL = 'arial black'
TAILLE_TEXTE_ACCEUIL = 15

# Paramètres du joueur
JOUEUR_START_POS = vec(13.5, 23) # Position du joueur au début du jeu
VITESSE_JOUEUR = 2 # Ne pas monter trop haut ca casse tout
NB_VIES = 3

MoveUp = vec(0, -1)
MoveDown = vec(0, 1)
MoveLeft = vec(-1, 0)
MoveRight = vec(1, 0)

# Paramètres des fantomes

# Images
imgBlinkyRight = pygame.image.load('Images/Fantomes/BlinkyRight.png')
imgPinkyLeft = pygame.image.load('Images/Fantomes/PinkyLeft.png')
imgClydeUp = pygame.image.load('Images/Fantomes/ClydeUp.png')
imgInkyDown = pygame.image.load('Images/Fantomes/InkyDown.png')

imgPacmanLeft = pygame.image.load('Images/Pacman/PacMan1.png')
imgPacmanRight = pygame.transform.rotate(imgPacmanLeft, 180)
imgPacmanUp = pygame.transform.rotate(imgPacmanLeft, -90)
imgPacmanDown = pygame.transform.rotate(imgPacmanLeft, 90)
