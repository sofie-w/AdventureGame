import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, type, name):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-24)
        self.type = type
        self.name = name
