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
    puntuacion = fuente.render("Puntos: " + str(puntuacion_valor), True, (255, 255, 255))
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

def regresar_al_menu():
    global vidas, nivel, jugador_X, jugador_Y, bala_Y, estado_bala
    vidas = 3
    nivel = 1
    jugador_X = 370
    jugador_Y = 523
    bala_Y = 500
    estado_bala = "reposo"
    for i in range(num_invasores):
        invasor_X[i] = random.randint(64, 737)
        invasor_Y[i] = random.randint(30, 180)
    global estado_juego
    estado_juego = "menu"

def mostrar_menu():
    pantalla.fill((0, 0, 0))
    texto_menu = fuente_menu.render("Space Invaders", True, (255, 255, 255))
    pantalla.blit(texto_menu, (ancho_pantalla // 2 - texto_menu.get_width() // 2, 100))

    texto_jugar = fuente_menu.render("1. Iniciar juego", True, (255, 255, 255))
    pantalla.blit(texto_jugar, (ancho_pantalla // 2 - texto_jugar.get_width() // 2, 200))

    texto_tienda = fuente_menu.render("2. Tienda", True, (255, 255, 255))
    pantalla.blit(texto_tienda, (ancho_pantalla // 2 - texto_tienda.get_width() // 2, 250))

    texto_instrucciones = fuente_menu.render("3. Instrucciones", True, (255, 255, 255))
    pantalla.blit(texto_instrucciones, (ancho_pantalla // 2 - texto_instrucciones.get_width() // 2, 300))

    texto_salir = fuente_menu.render("4. Salir", True, (255, 255, 255))
    pantalla.blit(texto_salir, (ancho_pantalla // 2 - texto_salir.get_width() // 2, 350))

    pygame.display.update()

def mostrar_instrucciones():
    pantalla.fill((0, 0, 0))
    instrucciones = [
        "Use las flechas izquierda y derecha para mover la nave.",
        "Presiona la barra espaciadora para disparar.",
        "Elimina a todos los invasores para ganar puntos.",
        "Ve a la tienda para canjear puntos por diferentes naves.",
        "Presiona 'M' para volver al menú principal."
    ]
y_offset = 100
for linea in instrucciones:
    texto_instruccion = fuente_instrucciones.render(linea, True, (255, 255, 255))
    pantalla.blit(texto_instruccion, (50, y_offset))
    y_offset += 40
    pygame.display.update()
mensaje_error_tienda = ""

def mostrar_tienda():
    global mensaje_error_tienda
    pantalla.fill((0, 0, 0))
    texto_tienda = fuente_menu.render("Tienda", True, (255, 255, 255))
    pantalla.blit(texto_tienda, (ancho_pantalla // 2 - texto_tienda.get_width() // 2, 100))

    texto_puntos = fuente.render(f"Puntos: {puntuacion_valor}", True, (255, 255, 255))
    pantalla.blit(texto_puntos, (50, 150))

    textos_items = [
        f"1. Nave 1 - 10 puntos",
        f"2. Nave 2 - 20 puntos",
        "Presiona 'M' para volver al menú principal."
    ]
    y_offset = 200
    for texto_item in textos_items:
        texto = fuente_instrucciones.render(texto_item, True, (255, 255, 255))
        pantalla.blit(texto, (50, y_offset))
        y_offset += 40

    if mensaje_error_tienda:
        texto_error = fuente.render(mensaje_error_tienda, True, (255, 0, 0))
        pantalla.blit(texto_error, (50, y_offset + 40))

    pygame.display.update()

def mostrar_menu_pausa():
    pantalla.fill((0, 0, 0))
    texto_pausa = fuente_menu.render("Juego Pausado", True, (255, 255, 255))
    pantalla.blit(texto_pausa, (ancho_pantalla // 2 - texto_pausa.get_width() // 2, 100))

    texto_continuar = fuente_menu.render("1. Continuar", True, (255, 255, 255))
    pantalla.blit(texto_continuar, (ancho_pantalla // 2 - texto_continuar.get_width() // 2, 200))

    texto_terminar = fuente_menu.render("2. Terminar partida", True, (255, 255, 255))
    pantalla.blit(texto_terminar, (ancho_pantalla // 2 - texto_terminar.get_width() // 2, 250))

    pygame.display.update()

estado_juego = "menu"
juego_pausado = False
corriendo = True
while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

        if estado_juego == "menu":
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1:
                    estado_juego = "juego"
                elif evento.key == pygame.K_2:
                    estado_juego = "tienda"
                elif evento.key == pygame.K_3:
                    estado_juego = "instrucciones"
                elif evento.key == pygame.K_4:
                    corriendo = False

        elif estado_juego == "instrucciones":
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_m:
                estado_juego = "menu"

        elif estado_juego == "tienda":
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_m:
                estado_juego = "menu"
                mensaje_error_tienda = ""
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1:
                    if puntuacion_valor >= 10:
                        indice_imagen_jugador = 0
                        imagen_jugador = pygame.image.load(imagenes_jugador[indice_imagen_jugador])
                        puntuacion_valor -= 10
                        mensaje_error_tienda = ""
                    else:
                        mensaje_error_tienda = "Puntos insuficientes para comprar Nave 1"
                elif evento.key == pygame.K_2:
                    if puntuacion_valor >= 20:
                        indice_imagen_jugador = 1
                        imagen_jugador = pygame.image.load(imagenes_jugador[indice_imagen_jugador])
                        puntuacion_valor -= 20
                        mensaje_error_tienda = ""
                    else:
                        mensaje_error_tienda = "Puntos insuficientes para comprar Nave 2"

        elif estado_juego == "juego":
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    jugador_Xcambio = -3
                if evento.key == pygame.K_RIGHT:
                    jugador_Xcambio = 3
                if evento.key == pygame.K_SPACE:
                    if estado_bala == "reposo":
                        bala_X = jugador_X
                        bala(bala_X, bala_Y)
                        sonido_bala = mixer.Sound('data/bullet.wav')
                        sonido_bala.play()
                if evento.key == pygame.K_p:
                    juego_pausado = True

            if evento.type == pygame.KEYUP:
                if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                    jugador_Xcambio = 0