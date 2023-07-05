import pygame, os

WIDTH, HEIGHT = 1280, 768
TILESIZE = 64
PLAYER_WIDTH, PLAYER_HEIGHT = TILESIZE, TILESIZE
WIN = pygame.display.set_mode((WIDTH, HEIGHT))



FPS = 60

# ui 
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
UI_FONT = (os.path.join('AdventureGame', 'grafics', 'font', 'joystix.ttf'))
UI_FONT_SIZE = 18
DEAD_FONT = pygame.font.Font(UI_FONT, 60)


#images
LIFE_IMG = pygame.image.load(os.path.join('AdventureGame', 'grafics', 'characters', 'heart.png'))
DEAD_IMG = pygame.image.load(os.path.join('AdventureGame', 'grafics', 'characters', 'heart-black.png'))
BACKGROUND_WALL = pygame.image.load(os.path.join('AdventureGame', 'grafics', 'floors', 'stats_wall.png'))
# INV_IMG = pygame.image.load(os.path.join('AdventureGame', 'grafics', 'characters', 'invbox.png'))

WEAPON_DATA = {
	'sword': {'cooldown': 100, 'damage': 15,'graphic':os.path.join('AdventureGame', 'grafics', 'weapons', 'sword', 'full.png')},
	'lance': {'cooldown': 400, 'damage': 30,'graphic':os.path.join('AdventureGame', 'grafics', 'weapons', 'lance', 'full.png')},
	'axe': {'cooldown': 300, 'damage': 20, 'graphic':os.path.join('AdventureGame', 'grafics', 'weapons', 'axe', 'full.png')},
	'rapier':{'cooldown': 50, 'damage': 8, 'graphic':os.path.join('AdventureGame', 'grafics', 'weapons', 'rapier', 'full.png')},
	'sai':{'cooldown': 80, 'damage': 10, 'graphic':os.path.join('AdventureGame', 'grafics', 'weapons', 'sai', 'full.png')}}

MAGIC_DATA = {
	'flame': {'strength': 5,'cost': 20,'graphic':os.path.join('AdventureGame', 'grafics', 'particles', 'flame', 'fire.png')},
	'heal' : {'strength': 20,'cost': 10,'graphic':os.path.join('AdventureGame', 'grafics', 'particles', 'heal', 'heal.png')}}

FOOD_DATA = {
	'apple' : {'health': 5,'cost': 20,'graphic':os.path.join('AdventureGame', 'grafics', 'food', 'Apple.png')},
    'bread' : {'health': 7,'cost': 30,'graphic':os.path.join('AdventureGame', 'grafics', 'food', 'Bread.png')},
	'tea' : {'health': 10,'cost': 35,'graphic':os.path.join('AdventureGame', 'grafics', 'food', 'Tea.png')},
    'fish': {'health': 14,'cost': 50,'graphic':os.path.join('AdventureGame', 'grafics', 'food', 'Fish.png')},
	'noodles' : {'health': 18,'cost': 60,'graphic':os.path.join('AdventureGame', 'grafics', 'food', 'Noodles.png')}}


monster_data = {
	'squid': {'health': 100,'exp':50,'damage':20,'attack_type': 'slash', 'attack_sound':'../audio/attack/slash.wav', 'speed': 1.5, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 360},
	'raccoon': {'health': 300,'exp':100,'damage':40,'attack_type': 'claw',  'attack_sound':'../audio/attack/claw.wav','speed': 1, 'resistance': 3, 'attack_radius': 120, 'notice_radius': 400},
	'spirit': {'health': 100,'exp':55,'damage':8,'attack_type': 'thunder', 'attack_sound':'../audio/attack/fireball.wav', 'speed': 1.5, 'resistance': 3, 'attack_radius': 60, 'notice_radius': 350},
	'bamboo': {'health': 70,'exp':60,'damage':6,'attack_type': 'leaf_attack', 'attack_sound':'../audio/attack/slash.wav', 'speed': 1, 'resistance': 3, 'attack_radius': 50, 'notice_radius': 300}}


#colors
BLACK = (0, 0, 0)
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'

# ui colors
HEALTH_COLOR = 'red'
ENERGY_COLOR = 'green'
UI_BORDER_COLOR_ACTIVE = 'gold'