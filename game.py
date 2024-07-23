import pygame
import random
import math
import time
from pygame import mixer

pygame.init()

ancho_pantalla = 800
alto_pantalla = 600
pantalla = pygame.display.set_mode((ancho_pantalla, alto_pantalla))

pygame.display.set_caption("Bienvenido a Space Invaders")

puntuacion_valor = 0
puntuacionX = 5
puntuacionY = 5
fuente = pygame.font.Font('freesansbold.ttf', 20)

vidas = 3

nivel = 1

fuente_game_over = pygame.font.Font('freesansbold.ttf', 64)
fuente_terminado = pygame.font.Font('freesansbold.ttf', 40)
fuente_menu = pygame.font.Font('freesansbold.ttf', 32)
fuente_instrucciones = pygame.font.Font('freesansbold.ttf', 24)

mixer.music.load('data/background.wav')
mixer.music.play(-1)

imagenes_jugador = ['data/spaceship.png', 'datas/spaceship1.png', 'data/spaceship2.png']
indice_imagen_jugador = 0
imagen_jugador = pygame.image.load(imagenes_jugador[indice_imagen_jugador])
jugador_X = 370
jugador_Y = 523
jugador_Xcambio = 0

imagen_invasor = []
invasor_X = []
invasor_Y = []
invasor_Xcambio = []
invasor_Ycambio = []
num_invasores = 10
for num in range(num_invasores):
    imagen_invasor.append(pygame.image.load('data/alien.png'))
    invasor_X.append(random.randint(60, 700))
    invasor_Y.append(random.randint(30, 180))
    invasor_Xcambio.append(0.3)
    invasor_Ycambio.append(40)

imagen_bala = pygame.image.load('data/bullet.png')
bala_X = 0
bala_Y = 500
bala_Xcambio = 0
bala_Ycambio = 3
estado_bala = "reposo"

def esColision(x1, x2, y1, y2):
    distancia = math.sqrt((math.pow(x1 - x2, 2)) + (math.pow(y1 - y2, 2)))
    return distancia <= 50

def jugador(x, y):
    pantalla.blit(imagen_jugador, (x - 16, y - 10))

def invasor(x, y, i):
    pantalla.blit(imagen_invasor[i], (x, y))

def bala(x, y):
    global estado_bala
    pantalla.blit(imagen_bala, (x, y))
    estado_bala = "disparo"

def mostrar_puntuacion(x, y):
    puntuacion = fuente.render("Puntos: " + str(puntuacion_valor), True, (255, 255, 255))")
    pantalla.blit(puntuacion, (x, y))

def mostrar_vidas(x, y):
    vidas_texto = fuente.render("Vidas: " + str(vidas), True, (255, 255, 255))
    pantalla.blit(vidas_texto, (x, y))

def mostrar_nivel(x, y):
    nivel_texto = fuente.render("Nivel: " + str(nivel), True, (255, 255, 255))
    pantalla.blit(nivel_texto, (x, y))

def fin_juego():
    game_over_texto = fuente_game_over.render("GAME OVER", True, (255, 255, 255))
    pantalla.blit(game_over_texto, (190, 250))
    pygame.display.update()
    time.sleep(3)
    regresar_al_menu()

def partida_terminada():
    terminado_texto = fuente_terminado.render("Partida terminada", True,(255, 255, 255))
    pantalla.blit(terminado_texto, (190, 250))
    pygame.display.update()
    time.sleep(3)
    regresar_al_menu()
