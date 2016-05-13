import pygame, sys
from pygame.locals import *
from random import choice
# Constantes
PATH 		= "sprites/"
TECLAS 		= {K_UP: (-1,0), K_DOWN: (1,0), K_w: (-1,1), K_s: (1,1)} # -1 es para arriba, 1 para abajo, segundo valor es indice jugador.

class Player(object):
	def __init__(self, numeroJugador):
		self.coords = (780*numeroJugador, 266) 						# numeroJugador puede ser 0 o 1 (player 1 y player 2)
		self.sprite = pygame.image.load(PATH+"player.jpg")
		self.direcc	= 0	# Determina si va hacia arriba o abajo (-1 arriba, 1 abajo)
		self.puntos = 0 # Score del jugador
	def mover(self):
		x, y = self.coords
		if 0 < y < 513:
			y = y+10*self.direcc

		elif y <= 0:
			y = 1
			self.direcc = 0

		elif y >= 513:
			y = 512
			self.direcc = 0

		self.coords = (x, y)

class Esfera(object):
	def __init__(self):
		self.coords = (380,280)		#Coordenada Centro
		self.sprite = pygame.image.load(PATH+"esfera.png")
		self.factorY = choice((1,-1))			# Se determina aleatoriamente hacia donde parte la esfera
		self.factorX = choice((1,-1))
		self.speed = 0			#Velocidad con la que se mueve la esfera (esta va en aumento, por eso es una variable)
	def mover(self):
		x, y = self.coords
		if y < 0:
			self.factorY = 1
		if y > 560:
			self.factorY = -1
		self.coords = (x+self.speed*self.factorX,y+self.speed*self.factorY)		#	FactorY y factorX es para que rebote donde corresponde (-1 o 1)


pygame.init() # Inicializa pygame
finJuego 							= False 
Window 								= pygame.display.set_mode((800,600))
playerOne 							= Player(0)	# Al ser 0, se ubica en X = 0
playerTwo							= Player(1) # Al ser 1, se ubica en X = 780 (ver clase para entender)
pelota								= Esfera()
listaJugadores						= [playerOne, playerTwo]	# Lista creada para permitir un manejo simultaneo de ambos jugadores.
FPS									= pygame.time.Clock()
font 								= pygame.font.Font(None, 110)
opacidad							= 251

while not finJuego:

	FPS.tick(60)
	pygame.display.set_caption("Pong | FPS: "+str(round(FPS.get_fps(), 2))) # Con esto se imprime los fps en el nombre del archivo
	tiempoJuego = pygame.time.get_ticks()

	# Opacidad va en aumento para que el score se oculte y no moleste durante la visual.
	# Se va restando de a poco para que cree el efecto "fade out", luego se reinicia cada vez que se pierde
	text1 = font.render(str(playerTwo.puntos), 1, (250,250,250))
	text2 = font.render(str(playerOne.puntos), 1, (250, 250, 250))
	Window.blit(text1, (200,100))
	Window.blit(text2, (600,100))

	if pelota.coords[0] > 760:
		playerTwo.puntos += 1
		pelota = Esfera()
	if pelota.coords[0] < 0:
		playerOne.puntos += 1
		pelota = Esfera()

	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()

		if event.type == KEYDOWN:
			# Esta condicion fue necesaria para que partiese la partida solo si es que se presiona cualquier tecla
			if pelota.speed == 0:
				pelota.speed = 5
				opacidad = 0
			# Se agruparon las 4 teclas posibles de apretar, para trabajar de forma simultanea y evitar 4 if's,
			# el diccionario esta en el formato {tecla: [direccion, jugadorAfectado]}
			for teclaPresionada in TECLAS:
				if event.key == teclaPresionada:
					indiceJugador = TECLAS[teclaPresionada][1]
					listaJugadores[indiceJugador].direcc = TECLAS[teclaPresionada][0]

		if event.type == KEYUP:
			for teclaPresionada in TECLAS:
				if event.key == teclaPresionada:
					indiceJugador = TECLAS[teclaPresionada][1]
					listaJugadores[indiceJugador].direcc = 0

	# Cada X tiempo se le va sumando velocidad a la pelota, fue necesario que solo pase cuando sea >= 5 porque
	# A veces se iniciaba solo el juego
	if not tiempoJuego%200 and pelota.speed >= 5:
		pelota.speed += 2


	posicionJugadores = []
	for jugador in listaJugadores:
		jugador.mover()
		posicionJugadores.append(Window.blit(jugador.sprite, jugador.coords)) # Actualizar posicion del jugador.

	colisiones = Window.blit(pelota.sprite, pelota.coords)
	colisiones = colisiones.collidelistall(posicionJugadores) # Crea una lista con las colisiones en el momento

	# Por ende, si la colision no esta vacia, significa que choco con alguna de las barras
	if colisiones != []:
		# Se pregunto si era igual a uno porque ahi es cuando va hacia la derecha.

		# Ademas, fue necesario reposicionar la esfera en la coordenada X para solucionar problemas 
		# de rebotes extrannos
		if pelota.factorX == 1:
			pelota.coords = (740, pelota.coords[1])	
			pelota.factorX = pelota.factorX*-1

		else:
			pelota.coords = (20, pelota.coords[1])	
			pelota.factorX = pelota.factorX*-1

	pelota.mover()
	pygame.display.update()
	Window.fill((0,0,0))