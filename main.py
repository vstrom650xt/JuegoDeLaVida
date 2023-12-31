import pygame
import numpy as np
import time
import sys

pygame.init()

# Definición de la ventana
width, height = 1000, 1000
screen = pygame.display.set_mode((height, width))

# Color de fondo
bg = 25, 25, 25
screen.fill(bg)

nxC, nyC = 50, 50

dimCW = width / nxC
dimCH = height / nyC

# Estado de las células
gameState = np.zeros((nxC, nyC))
gameState[21, 21] = 1
gameState[22, 22] = 1
gameState[22, 23] = 1
gameState[21, 23] = 1
gameState[20, 23] = 1

gameState[11, 11] = 1
gameState[12, 12] = 1
gameState[12, 13] = 1
gameState[11, 13] = 1
gameState[10, 13] = 1

gameState[11, 13] = 1
gameState[12, 13] = 1
gameState[12, 33] = 1
gameState[11, 33] = 1
gameState[10, 43] = 1
# Posición inicial de las células
unitPos = [(25, 49), (26, 49), (27, 49), (26, 48)]
# Lista para almacenar las células lanzadas
launchedCells = []
# Coordenadas de la nave
shipPos = (26, 48)

pauseExec = False

# Mantiene la ventana abierta
while True:
    newGameState = np.copy(gameState)
    screen.fill(bg)
    time.sleep(0.1)
    ev = pygame.event.get()
    for event in ev:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Lanzar una nueva célula desde la posición de la nave
                launchedCells.append(list(shipPos))

            elif event.key == pygame.K_UP:
                # Mover todas las células hacia arriba
                unitPos = [(x, (y - 1) % nyC) for x, y in unitPos]
                # Mover la nave hacia arriba
                shipPos = (shipPos[0], (shipPos[1] - 1) % nyC)
            elif event.key == pygame.K_DOWN:
                # Mover todas las células hacia abajo
                unitPos = [(x, (y + 1) % nyC) for x, y in unitPos]
                # Mover la nave hacia abajo
                shipPos = (shipPos[0], (shipPos[1] + 1) % nyC)
            elif event.key == pygame.K_LEFT:
                # Mover todas las células hacia la izquierda
                unitPos = [((x - 1) % nxC, y) for x, y in unitPos]
                # Mover la nave hacia la izquierda
                shipPos = ((shipPos[0] - 1) % nxC, shipPos[1])
            elif event.key == pygame.K_RIGHT:
                # Mover todas las células hacia la derecha
                unitPos = [((x + 1) % nxC, y) for x, y in unitPos]
                # Mover la nave hacia la derecha
                shipPos = ((shipPos[0] + 1) % nxC, shipPos[1])
            elif event.key == pygame.K_RETURN:
                # Cambia el estado de las células resaltadas al presionar Enter
                for x, y in unitPos:
                    if 0 <= x < nxC and 0 <= y < nyC:
                        newGameState[x, y] = 1 - newGameState[x, y]

        mouseClick = pygame.mouse.get_pressed()
        if sum(mouseClick) > 0:
            posX, posY = pygame.mouse.get_pos()
            celX, celY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))
            if 0 <= celX < nxC and 0 <= celY < nyC:
                newGameState[celX, celY] = not mouseClick[2]

    # Mover las células lanzadas hacia arriba
    launchedCells = [(x, (y - 1) % nyC) for x, y in launchedCells]


    for y in range(0, nxC):
        for x in range(0, nyC):
            if not pauseExec:
                # Calcular el número de vecinos vivos
                n_neigh = (
                        gameState[(x - 1) % nxC, (y - 1) % nyC]
                        + gameState[(x) % nxC, (y - 1) % nyC]
                        + gameState[(x + 1) % nxC, (y - 1) % nyC]
                        + gameState[(x - 1) % nxC, (y) % nyC]
                        + gameState[(x + 1) % nxC, (y) % nyC]
                        + gameState[(x - 1) % nxC, (y + 1) % nyC]
                        + gameState[(x) % nxC, (y + 1) % nyC]
                        + gameState[(x + 1) % nxC, (y + 1) % nyC]
                )

                # Aplicar las reglas del juego de la vida de Conway
                if gameState[x, y] == 0 and n_neigh == 3:
                    newGameState[x, y] = 1
                elif gameState[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
                    newGameState[x, y] = 0

                # Dibujar el polígono correspondiente al estado de la célula
                poly = [
                    ((x) * dimCW, y * dimCH),
                    ((x + 1) * dimCW, y * dimCH),
                    ((x + 1) * dimCW, (y + 1) * dimCH),
                    ((x) * dimCW, (y + 1) * dimCH),
                ]
                if newGameState[x, y] == 0:
                    pygame.draw.polygon(screen, (128, 128, 128), poly, 1)
                else:
                    pygame.draw.polygon(screen, (255, 255, 255), poly, 0)

    # Dibujar las células lanzadas
    for x, y in launchedCells:
        if gameState[x, y] == 0 and n_neigh == 3:
            newGameState[x, y] = 1
        elif gameState[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
            newGameState[x, y] = 0
        pygame.draw.polygon(
            screen,
            (255, 0, 0),
            [
                (x * dimCW, y * dimCH),
                ((x + 1) * dimCW, y * dimCH),
                ((x + 1) * dimCW, (y + 1) * dimCH),
                (x * dimCW, (y + 1) * dimCH),
            ],
            0,
        )

    # Dibujar las células resaltadas
    for x, y in unitPos:
        pygame.draw.polygon(
            screen,
            (255, 0, 0),
            [
                (x * dimCW, y * dimCH),
                ((x + 1) * dimCW, y * dimCH),
                ((x + 1) * dimCW, (y + 1) * dimCH),
                (x * dimCW, (y + 1) * dimCH),
            ],
            1,
        )

    pygame.display.flip()
    gameState = np.copy(newGameState)
