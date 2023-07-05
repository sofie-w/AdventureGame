import pygame
from constants import *
from support import import_folder
from math import sin

class Enemy(pygame.sprite.Sprite):
    def __init__(self, name, pos, player, groups):
        super().__init__(groups)
        self.type = 'enemy'
        self.player = player
        self.import_graphics(name)
        self.status = 'idle'
        self.frame_index = 0
        self.animation_speed = 0.10
        self.direction = pygame.math.Vector2()

        self.image = self.animations[self.status][self.frame_index]
        

        #movement
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-10)
        self.sprite_group = groups
        
        #stats
        self.monster_name = name
        monster_info = monster_data[self.monster_name]
        self.health = monster_info['health']
        self.exp = monster_info['exp']
        self.speed = monster_info['speed']
        self.attack_damage = monster_info['damage']
        self.resistance = monster_info['resistance']
        self.attack_radius = monster_info['attack_radius']
        self.notice_radius = monster_info['notice_radius']
        self.attack_type = monster_info['attack_type']

        #player interaction
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 400

        self.attackable = True
        self.hit_time = None
        self.hit_cooldown = 300
        

    def import_graphics(self, name):
        self.animations = {'idle': [], 'move': [], 'attack': []}
        path = f'D:\Documenten\Coderclass\Python\PyGame\AdventureGame\grafics\monsters\\{name}\\'

        for animation in self.animations.keys():
            self.animations[animation] = import_folder(path + animation)
    
    def move(self, player):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        #update new location and picture
        self.hitbox.x += self.direction.x * self.speed
        # self.collision('horizontal', player)
        self.hitbox.y += self.direction.y * self.speed
        # self.collision('vertical', player)
        self.rect.center = self.hitbox.center

    def collision(self, direction, player):
            if direction == 'horizontal':
                for obj in player.current_room.sprite_group:
                    if obj.type in ('Building', 'Decor'):
                        if obj.hitbox.colliderect(self.hitbox):
                            if self.direction.x > 0:#moving right
                                self.hitbox.right = obj.hitbox.left
                            if self.direction.x < 0: #moving left
                                self.hitbox.left = obj.hitbox.right

            if direction == 'vertical':
                for obj in player.current_room.sprite_group:
                    if obj.type in ('Building', 'Decor', 'Vegetation'):
                        if obj.hitbox.colliderect(self.hitbox):
                            if self.direction.y > 0:#moving down
                                self.hitbox.bottom = obj.hitbox.top
                            if self.direction.y < 0: #moving up
                                self.hitbox.top = obj.hitbox.bottom

    def get_player_distance_direction(self, player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()

        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2(0,0)

        return(distance, direction)

    def get_status(self, player):
        distance = self.get_player_distance_direction(player)[0]
        if distance  <= self.attack_radius and self.can_attack:
            if self.status != 'attack':
                self.frame_index = 0
            self.status = 'attack'
        elif distance <= self.notice_radius:
            self.status = 'move'
        else:
            self.status = 'idle'

    def actions(self, player):
        if self.status == 'attack':
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(self.attack_damage, self.attack_type)
        elif self.status == 'move':
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()
    
    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == 'attack':
                self.can_attack = False
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

        if not self.attackable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)
    
    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0 
        
    def cooldown(self):
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True
        if not self.attackable:
            if current_time - self.hit_time >= self.hit_cooldown:
                self.attackable = True


        

    def get_damage(self, player, attack_type):
        if self.attackable:
            self.direction = self.get_player_distance_direction(player)[1]
            if attack_type == 'weapon':
                self.health -= player.get_weapon_damage()
            else:
                pass#magic
            self.hit_time = pygame.time.get_ticks()
            self.attackable = False
    
    def check_health(self, player):
        if self.health <= 0:
            player.exp += self.exp
            self.kill()

    def push_back(self):
        if not self.attackable:
            self.direction *= -self.resistance
    
    def damage_player(self, amount, attack_type):
        if self.player.attackable:
            self.player.health -= amount
            self.player.attackable = False
            self.player.hit_time = pygame.time.get_ticks()


    def enemy_update(self, player):
        self.get_status(player)
        self.actions(player)
        self.push_back()
        self.move(player)
        self.animate()
        self.cooldown()
        self.check_health(player)


