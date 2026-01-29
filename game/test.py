import numpy as np
import pygame as pg



board = np.ndarray(shape=(4,4), dtype=int, order='C')
board.fill(0)
print(board)


pg.init() 
screen = pg.display.set_mode((800, 800))



player = pg.Rect(50, 50, 50, 50)
#screen.display.set_caption("2048 Game Board Test")
run = True
while run :
    screen.fill((0, 0, 0))
    pg.draw.rect(screen, (255, 0, 0), player)

    key = pg.key.get_pressed()
    if key[pg.K_LEFT] :
        player.move_ip(-1,0)
    if key[pg.K_RIGHT] :
        player.move_ip(1,0)
    if key[pg.K_UP] :
        player.move_ip(0,-1)
    if key[pg.K_DOWN] :
        player.move_ip(0,1)
    for event in pg.event.get() :
        if event.type == pg.QUIT :
            run = False
    pg.display.update()
pg.quit()