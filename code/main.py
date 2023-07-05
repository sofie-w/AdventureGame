import pygame, sys

from world import World
from constants import *

pygame.init()


def draw_screen(player, world):
    player.current_room.floor_group.draw(WIN)
    if player.location == 'under':
        WIN.blit(player.obj, (player.rect.x, player.rect.y))#player
    player.current_room.sprite_group.draw(WIN)
    WIN.blit(BACKGROUND_WALL, (0, HEIGHT-(TILESIZE*2)))
    world.ui.display(player)
    player.current_room.sprite_group.enemy_update(player)
    player.current_room.player_attack_logic()
     
    if player.location != 'under':
        WIN.blit(player.obj, (player.rect.x, player.rect.y))#player
    player.weapon_group.draw(WIN)   

    pygame.display.update()

def draw_dead_screen():
    text_surface = DEAD_FONT.render('GAME OVER', False, BLACK)
    text_rect = text_surface.get_rect(center = (WIDTH//2, HEIGHT//2))
    WIN.blit(text_surface, text_rect)
    pygame.display.update()



def main():    
    run = True
    clock = pygame.time.Clock()
    world = World()
    

    

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run =False
                pygame.quit()
                sys.exit()

            #key actions
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    pygame.quit()
                    sys.exit()
                else:
                    world.player.player_input(event.key, 'down')
            if event.type == pygame.KEYUP:
                world.player.player_input(event.key, 'up')
        
        
        if world.player.health < 0:
            draw_dead_screen()
        else:
            world.player.update()
            draw_screen(world.player, world)

        clock.tick(120)
    
        

if __name__ == "__main__":
    main()