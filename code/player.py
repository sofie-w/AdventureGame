import pygame, os
from support import import_folder
from weapon import Weapon
from constants import *
from math import sin

class Player():
    def __init__(self, world):


        #player setup
        self.rect = pygame.Rect(400, 300, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.image = pygame.image.load(os.path.join('AdventureGame', 'grafics', 'characters','player', 'down', 'down_0.png'))
        self.obj = pygame.transform.scale(self.image, (PLAYER_WIDTH, PLAYER_HEIGHT))
        self.life = 3
        self.world = world
        self.current_room = None
        self.hitbox = self.rect.inflate(0, -24)

        #stats
        self.stats = {'health': 200, 'energy': 60, 'attack': 10, 'magic': 10, 'speed': 2}
        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.exp = 0
        self.speed = self.stats['speed']

        #weapon
        self.weapon_group = pygame.sprite.Group()
        self.weapon_index = 0
        self.weapon = list(WEAPON_DATA.keys())[self.weapon_index]
        self.current_attack = None

        #magic
        self.magic_index = 0
        self.magic = list(MAGIC_DATA.keys())[self.magic_index]

        #food
        self.food_index = 0
        self.food = list(FOOD_DATA.keys())[self.food_index]

        self.inv = []

        #grafics setup
        self.status = 'down'
        self.import_player_assets()
        self.frame_index = 0
        self.animation_speed = 0.10
        
        #damage cooldown
        self.attackable = True
        self.hit_time = None
        self.hit_cooldown = 200
        
        #move setup
        self.velX = 0
        self.velY = 0
        self.location = 'normal'
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None

        self.attackable = True
        

    def import_player_assets(self):
        player_path = 'D:\Documenten\Coderclass\Python\PyGame\AdventureGame\grafics\characters\\player\\'
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
                'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [],
                'right_attack': [], 'left_attack': [], 'up_attack': [], 'down_attack': []}
        
        for animation in self.animations.keys():
            full_path = player_path + animation
            self.animations[animation] = import_folder(full_path)

    def get_status(self):
        #idle_status
        if not self.right_pressed and not self.left_pressed and not self.up_pressed and not self.down_pressed:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'

        #attack_status
        if self.attacking:
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')

                else:
                    self.status = self.status + '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '')   
    
    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >+ len(animation):
            self.frame_index = 0

        #change image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center) 

        #flicker
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

    def draw(self, WIN):
        pygame.draw.rect(WIN, self.image, self.rect)
    
    def update(self):
        self.cooldowns()
        self.get_status()
        self.animate()
        self.check_movement()
        self.move()
        self.check_location()

    def check_movement(self):
        self.velX = 0
        self.velY = 0
        if not self.attacking:

            if self.left_pressed and not self.right_pressed and (self.rect.x -self.speed) > 0:
                self.velX = -self.speed
                self.status = 'left'
            if self.right_pressed and not self.left_pressed and (self.rect.x + self.speed + PLAYER_WIDTH) < WIDTH:
                self.velX = self.speed
                self.status = 'right'
            if self.up_pressed and not self.down_pressed and (self.rect.y - self.speed) > 0:
                self.velY = -self.speed
                self.status = 'up'
            if self.down_pressed and not self.up_pressed and (self.rect.y + self.speed + PLAYER_HEIGHT) < HEIGHT-128:

                self.velY = self.speed
                self.status  = 'down'
        self.obj = pygame.transform.scale(self.image, (PLAYER_WIDTH, PLAYER_HEIGHT))
    
    def check_location(self):
        for door in self.current_room.doors:
            door_rect = pygame.Rect(door.x, door.y, door.width, door.height)
            if self.rect.colliderect(door_rect):
                print(self.current_room.y, self.current_room.x)
                if door.name == 'left':
                    next_room = self.world.map[self.current_room.y][self.current_room.x-1]
                    self.hitbox.x = WIDTH - PLAYER_WIDTH - (TILESIZE//2)
                elif door.name == 'right':
                    next_room = self.world.map[self.current_room.y][self.current_room.x+1]
                    self.hitbox.x = TILESIZE//2
                elif door.name == 'up':
                    next_room = self.world.map[self.current_room.y-1][self.current_room.x]
                    self.hitbox.y = HEIGHT-128 - PLAYER_HEIGHT - (TILESIZE//2)
                elif door.name == 'down':
                    next_room = self.world.map[self.current_room.y+1][self.current_room.x]
                    self.hitbox.y = TILESIZE//2
                self.current_room = next_room 
                self.rect.center = self.hitbox.center   

    def player_input(self, key, action):
        if action == 'down':    
            #player movement
            if key == pygame.K_a:
                self.left_pressed = True
            if key == pygame.K_d:
                self.right_pressed = True
            if key == pygame.K_w:
                self.up_pressed = True
            if key == pygame.K_s:
                self.down_pressed = True

            #switch weapons
            if key == pygame.K_q:
                if self.weapon_index < len(list(WEAPON_DATA.keys())) - 1:
                    self.weapon_index += 1
                else:
                    self.weapon_index = 0
                self.weapon = list(WEAPON_DATA.keys())[self.weapon_index]

            #switch magic
            if key == pygame.K_e:
                if self.magic_index < len(list(MAGIC_DATA.keys())) - 1:
                    self.magic_index += 1
                else:
                    self.magic_index = 0
                self.magic = list(MAGIC_DATA.keys())[self.magic_index]

            #switch food
            if key == pygame.K_m:
                if self.food_index < len(list(FOOD_DATA.keys())) - 1:
                    self.food_index += 1
                else:
                    self.food_index = 0
                self.food = list(FOOD_DATA.keys())[self.food_index]

            #eat food
            if key == pygame.K_LSHIFT:
                self.eat()

            #attack input
            if key == pygame.K_SPACE and not self.attacking:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()

            #magic input
            if key == pygame.K_LCTRL and not self.attacking:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                style = list(MAGIC_DATA.keys())[self.magic_index]
                strength = list(MAGIC_DATA.values())[self.magic_index]['strength'] + self.stats['magic']
                cost = list(MAGIC_DATA.values())[self.magic_index]['cost']

                self.create_magic(style, strength, cost)

        elif action == 'up':
            #stop player movement
            if key == pygame.K_a:
                self.left_pressed = False
            if key == pygame.K_d:
                self.right_pressed = False
            if key == pygame.K_w:
                self.up_pressed = False
            if key == pygame.K_s:
                self.down_pressed = False

    def eat(self):
        if self.inv.count(self.food) > 0:
            self.inv.remove(self.food)
            self.health += list(FOOD_DATA.values())[self.food_index]['health']
            if self.health > 100:
                self.health = 100


    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown + WEAPON_DATA[self.weapon]['cooldown']:
                self.attacking = False
                self.destroy_attack()

        if not self.attackable:
            if current_time - self.hit_time >= self.hit_cooldown:
                self.attackable = True

    def create_attack(self):
        self.current_attack = Weapon(self, groups = [self.weapon_group, self.current_room.attack_weapons])

    def destroy_attack(self):

        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def create_magic(self, style, strength, cost):
        print(style)
        print(strength)
        print(cost)

    def get_weapon_damage(self):
        damage = self.stats['attack']
        weapon_damage = WEAPON_DATA[self.weapon]['damage']
        return (weapon_damage + damage)

    def move(self):
        #update new location and picture
        self.collision('horizontal')
        self.collision('vertical')
        self.rect.center = self.hitbox.center

    def collision(self, direction):
            if direction == 'horizontal':
                self.hitbox.x += self.velX
                for obj in self.current_room.sprite_group:
                    if obj.type in ('Building', 'Decor'):
                        if obj.hitbox.colliderect(self.hitbox):
                            self.hitbox.x -= self.velX

            if direction == 'vertical':
                self.hitbox.y += self.velY
                for obj in self.current_room.sprite_group:
                    if obj.type in ('Building', 'Decor', 'Vegetation'):
                        if obj.hitbox.colliderect(self.hitbox):
                            self.hitbox.y -= self.velY

                        if obj.rect.colliderect(self.rect):
                            if obj.rect.y < self.rect.y + self.obj.get_height():
                               self.location = 'under'
                            elif obj.rect.bottom > self.rect.top:
                                self.location = 'normal'