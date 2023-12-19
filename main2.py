import pygame
import numpy as np
import time

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

# Posición de la célula que se moverá con las flechas
cellX, cellY = 25, 25

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
                pauseExec = not pauseExec
            elif event.key == pygame.K_UP:
                cellY = (cellY - 1) % nyC
            elif event.key == pygame.K_DOWN:
                cellY = (cellY + 1) % nyC
            elif event.key == pygame.K_LEFT:
                cellX = (cellX - 1) % nxC
            elif event.key == pygame.K_RIGHT:
                cellX = (cellX + 1) % nxC
            elif event.key == pygame.K_RETURN:
                # Cambia el estado de la célula resaltada al presionar Enter
                if 0 <= cellX < nxC and 0 <= cellY < nyC:
                    newGameState[cellX, cellY] = 1 - newGameState[cellX, cellY]

        mouseClick = pygame.mouse.get_pressed()
        if sum(mouseClick) > 0:
            posX, posY = pygame.mouse.get_pos()
            celX, celY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))
            if 0 <= celX < nxC and 0 <= celY < nyC:
                newGameState[celX, celY] = not mouseClick[2]

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

    # Dibuja la célula resaltada
    pygame.draw.polygon(
        screen,
        (255, 255, 255),
        [
            (cellX * dimCW, cellY * dimCH),
            ((cellX + 1) * dimCW, cellY * dimCH),
            ((cellX + 1) * dimCW, (cellY + 1) * dimCH),
            (cellX * dimCW, (cellY + 1) * dimCH),
        ],
        0,
    )

    pygame.display.flip()
    gameState = np.copy(newGameState)