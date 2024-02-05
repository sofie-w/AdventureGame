import pygame
from room import Room
from ui import UI
from player import Player
from constants import *

class World():
    def __init__(self):
        #get tmx files for maps
        self.map = []
        
        self.ui = UI()
        self.player = Player(self)
        
        
        self.create_rooms()
        

        
    def create_rooms(self):
        #get tmx files for maps
        room1 = Room("D:\Documenten\Coderclass\Python\Pygame\AdventureGame\data\\tmx\\room1.tmx", 1, self.player, self)
        room2 = Room("D:\Documenten\Coderclass\Python\Pygame\AdventureGame\data\\tmx\\room2.tmx", 2, self.player, self)
        room3 = Room("D:\Documenten\Coderclass\Python\Pygame\AdventureGame\data\\tmx\\room3.tmx", 3, self.player, self)
        room4 = Room("D:\Documenten\Coderclass\Python\Pygame\AdventureGame\data\\tmx\\room4.tmx", 4, self.player, self)
        room5 = Room("D:\Documenten\Coderclass\Python\Pygame\AdventureGame\data\\tmx\\room5.tmx", 5, self.player, self)
        room6 = Room("D:\Documenten\Coderclass\Python\Pygame\AdventureGame\data\\tmx\\room6.tmx", 6, self.player, self)

        self.map = [
            [room1, room2, room5],
            [room3, room4, room6]]
        
        room1.y, room1.x = 0, 0
        room2.y, room2.x = 0, 1
        room3.y, room3.x = 1, 0
        room4.y, room4.x = 1, 1
        room5.y, room5.x = 0, 2
        room6.y, room6.x = 1, 2
        
        self.player.current_room = self.map[0][1]
        

    
class YSort(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

    def custom_draw(self):
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            WIN.blit(sprite.image, sprite.rect)
            


        