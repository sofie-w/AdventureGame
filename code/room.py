import pygame
from pytmx.util_pygame import load_pygame
pygame.init()

from constants import TILESIZE
from tile import Tile
from enemy import Enemy

class Room():
    def __init__(self, data_url, name, player, world):
        self.data = load_pygame(data_url)
        self.world = world
        self.x = self.world.map
        self.y = 0
        self.name = name
        self.floor_group = pygame.sprite.Group()
        self.sprite_group = special_Sprite_Group()
        self.attack_weapons = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        self.doors = []
        self.player = player
        
        self.make_room()

    def make_room(self):
        #get all layers from map
        for layer in self.data.layers:
            if hasattr(layer, 'data'):
                for x, y, surf in layer.tiles():
                    pos = (x*TILESIZE, y*TILESIZE)
                    Tile(pos = pos, surf = surf, groups = [self.floor_group], type = 0, name = 0)

        #get all objects from map
        for obj in self.data.objects:
            pos = (obj.x, obj.y)
            if obj.type in ('Vegetation', 'Decor', 'Building'):
                Tile(pos, surf = obj.image, groups = [self.sprite_group], type = obj.type, name = obj.name)
            if obj.type == 'Basket':
                Tile(pos, surf = obj.image, groups = [self.sprite_group, self.attackable_sprites], type = obj.type, name = obj.name)

            if obj.type == 'Door':
                self.doors.append(obj)
            if obj.type == 'Spawner':
                Enemy(obj.name, pos, self.player, groups = [self.sprite_group, self.attackable_sprites])

    def player_attack_logic(self):
        if self.attack_weapons:
            for attack_weapon in self.attack_weapons:
                collided_sprites = pygame.sprite.spritecollide(attack_weapon, self.attackable_sprites, False)
                if collided_sprites:
                    for sprite in collided_sprites:
                        if sprite.type == 'Basket':
                            self.player.inv.append(sprite.name)
                            sprite.kill()
                        elif sprite.type == 'enemy':
                            sprite.get_damage(self.player, attack_weapon.type)



class special_Sprite_Group(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'type') and sprite.type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)