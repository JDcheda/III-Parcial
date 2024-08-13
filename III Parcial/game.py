import os
import pygame
import random
import math
import time
from pygame import mixer

pygame.init()

ancho_pantalla = 800
alto_pantalla = 600
pantalla = pygame.display.set_mode((ancho_pantalla, alto_pantalla))

fondo = pygame.image.load('data/fondo.png')

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

imagenes_jugador = ['data/spaceship.png', 'data/spaceship1.png', 'data/spaceship2.png']
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
num_invasores = 8
for num in range(num_invasores):
    imagen_invasor.append(pygame.image.load('data/alien.png'))
    invasor_X.append(random.randint(64, 737))
    invasor_Y.append(random.randint(30, 180))
    invasor_Xcambio.append(2)
    invasor_Ycambio.append(40)

imagen_jefe = pygame.image.load('data/ufo.png')
jefe_X = 370
jefe_Y = 50
jefe_Xcambio = 5
jefe_vida = 5

imagen_bala = pygame.image.load('data/bullet.png')
balas = [] 
bala_Ycambio = 5

def esColision(x1, x2, y1, y2):
    distancia = math.sqrt((math.pow(x1 - x2, 2)) + (math.pow(y1 - y2, 2)))
    return distancia <= 50

def jugador(x, y):
    pantalla.blit(imagen_jugador, (x - 16, y + 10))

def invasor(x, y, i):
    pantalla.blit(imagen_invasor[i], (x, y))

def dibujar_bala(x, y):
    pantalla.blit(imagen_bala, (x, y))

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
    pantalla.fill((0, 0, 0))
    game_over_texto = fuente_game_over.render("GAME OVER", True, (255, 255, 255))
    pantalla.blit(game_over_texto, (190, 250))
    pygame.display.update()
    time.sleep(3)
    regresar_al_menu(keep_puntuacion=True)

def partida_terminada():
    pantalla.fill((0, 0, 0))
    terminado_texto = fuente_terminado.render("Partida terminada", True, (255, 255, 255))
    pantalla.blit(terminado_texto, (190, 250))
    pygame.display.update()
    time.sleep(3)
    regresar_al_menu(keep_puntuacion=True) 

def regresar_al_menu(keep_puntuacion=False):
    global vidas, nivel, jugador_X, jugador_Y, balas, mensaje_error_tienda, estado_juego, juego_pausado, puntuacion_valor, jefe_vida
    if not keep_puntuacion:
        puntuacion_valor = 0
    vidas = 3
    nivel = 1
    jugador_X = 370
    jugador_Y = 523
    balas = []
    jefe_vida = 20
    mensaje_error_tienda = ""
    for i in range(num_invasores):
        invasor_X[i] = random.randint(64, 737)
        invasor_Y[i] = random.randint(30, 180)

    estado_juego = "menu"
    juego_pausado = False
    pantalla.fill((0, 0, 0))
    mostrar_menu()

def mostrar_menu():
    pantalla.blit(fondo, (0, 0))
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
    pantalla.blit(fondo, (0, 0))
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
    pantalla.blit(fondo, (0, 0))
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
        texto_error = fuente_instrucciones.render(mensaje_error_tienda, True, (255, 0, 0))
        pantalla.blit(texto_error, (50, y_offset))
    
    pygame.display.update()

estado_juego = "menu"
juego_pausado = False


ejecutando = True
while ejecutando:

  
    pantalla.fill((0, 0, 0))

    pantalla.blit(fondo, (0, 0))

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

        if evento.type == pygame.KEYDOWN:
            if estado_juego == "menu":
                if evento.key == pygame.K_1:
                    estado_juego = "jugando"
                    vidas = 3
                    puntuacion_valor = 0
                    nivel = 1
                elif evento.key == pygame.K_2:
                    estado_juego = "tienda"
                elif evento.key == pygame.K_3:
                    estado_juego = "instrucciones"
                elif evento.key == pygame.K_4:
                    ejecutando = False
            elif estado_juego == "jugando":
                if evento.key == pygame.K_LEFT:
                    jugador_Xcambio = -3
                if evento.key == pygame.K_RIGHT:
                    jugador_Xcambio = 3
                if evento.key == pygame.K_SPACE:
                    if len(balas) < 10:
                        balas.append([jugador_X, jugador_Y])
            elif estado_juego == "instrucciones":
                if evento.key == pygame.K_m:
                    regresar_al_menu()
            elif estado_juego == "tienda":
                if evento.key == pygame.K_m:
                    regresar_al_menu()
                elif evento.key == pygame.K_1:
                    if puntuacion_valor >= 10:
                        indice_imagen_jugador = 1
                        imagen_jugador = pygame.image.load(imagenes_jugador[indice_imagen_jugador])
                        puntuacion_valor -= 10
                        mensaje_error_tienda = ""
                    else:
                        mensaje_error_tienda = "No tienes suficientes puntos para comprar esta nave."
                elif evento.key == pygame.K_2:
                    if puntuacion_valor >= 20:
                        indice_imagen_jugador = 2
                        imagen_jugador = pygame.image.load(imagenes_jugador[indice_imagen_jugador])
                        puntuacion_valor -= 20
                        mensaje_error_tienda = ""
                    else:
                        mensaje_error_tienda = "No tienes suficientes puntos para comprar esta nave."

        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jugador_Xcambio = 0

    if estado_juego == "jugando":
        
        jugador_X += jugador_Xcambio
        if jugador_X <= 64:
            jugador_X = 64
        elif jugador_X >= 737:
            jugador_X = 737

        for i in range(num_invasores):
            invasor_X[i] += invasor_Xcambio[i]

            if invasor_X[i] <= 0:
                invasor_Xcambio[i] = 2 + nivel
                invasor_Y[i] += invasor_Ycambio[i]
            elif invasor_X[i] >= 736:
                invasor_Xcambio[i] = -(2 + nivel)
                invasor_Y[i] += invasor_Ycambio[i]

           
            for bala in balas:
                colision = esColision(invasor_X[i], bala[0], invasor_Y[i], bala[1])
                if colision:
                    balas.remove(bala)
                    puntuacion_valor += 1
                    invasor_X[i] = random.randint(64, 736)
                    invasor_Y[i] = random.randint(30, 200)

            invasor(invasor_X[i], invasor_Y[i], i)

        
        if nivel == 3:
            jefe_X += jefe_Xcambio
            if jefe_X <= 0 or jefe_X >= 736:
                jefe_Xcambio = -jefe_Xcambio

            for bala in balas:
                if esColision(jefe_X, bala[0], jefe_Y, bala[1]):
                    balas.remove(bala)
                    jefe_vida -= 1
                    if jefe_vida <= 0:
                        partida_terminada()

            pantalla.blit(imagen_jefe, (jefe_X, jefe_Y))

        
        for bala in balas:
            bala[1] -= bala_Ycambio
            if bala[1] <= 0:
                balas.remove(bala)
            dibujar_bala(bala[0], bala[1])

        
        for i in range(num_invasores):
            if invasor_Y[i] > 450:
                for j in range(num_invasores):
                    invasor_Y[j] = 2000
                fin_juego()
                break

        jugador(jugador_X, jugador_Y)
        mostrar_puntuacion(puntuacionX, puntuacionY)
        mostrar_vidas(puntuacionX, puntuacionY + 30)
        mostrar_nivel(puntuacionX, puntuacionY + 60)

        if puntuacion_valor >= 30 and nivel == 1:
            nivel = 2
        elif puntuacion_valor >= 60 and nivel == 2:
            nivel = 3

        pygame.display.update()

    elif estado_juego == "menu":
        mostrar_menu()
    elif estado_juego == "instrucciones":
        mostrar_instrucciones()
    elif estado_juego == "tienda":
        mostrar_tienda()

pygame.quit()
