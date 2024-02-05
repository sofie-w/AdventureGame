import pygame
from constants import *

class UI:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        self.health_bar_rect = pygame.Rect(15, 670, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        
        #dictionary weapons naar list
        self.weapon_grafics = []
        for weapon in WEAPON_DATA.values():
            path = weapon['graphic']
            weapon = pygame.image.load(path)
            self.weapon_grafics.append(weapon)

        #dictionary magic naar list
        self.magic_grafics = []
        for magic in MAGIC_DATA.values():
            path = magic['graphic']
            magic = pygame.image.load(path)
            self.magic_grafics.append(magic)

        self.food_grafics = []
        for food in FOOD_DATA.values():
            path = food['graphic']
            food = pygame.image.load(path)
            self.food_grafics.append(food)

    def show_bar(self,current,max_amount,bg_rect,color):
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        #from number to pixel
        ratio = current/ max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        #draw stats bar
        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

    def show_exp(self, exp):
        text_surface = self.font.render(str(int(exp)),False, TEXT_COLOR)
        x = 20
        y = self.display_surface.get_size()[1] - TILESIZE + (text_surface.get_height()/2) + 10
        text_rect = text_surface.get_rect(bottomleft = (x,y))

        #draw exp stats
        self.display_surface.blit(text_surface, text_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(10,10), 5)

    def selection_box(self, left, top):
        bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface,UI_BG_COLOR,bg_rect)
        pygame.draw.rect(self.display_surface,UI_BORDER_COLOR,bg_rect, 3)
        return bg_rect

    def weapon_overlay(self, weapon_index):
        bg_rect = self.selection_box((WIDTH//2) - (ITEM_BOX_SIZE*(3/2)) - 10, HEIGHT - TILESIZE - (ITEM_BOX_SIZE//2))
        weapon_surf = self.weapon_grafics[weapon_index]
        weapon_rect = weapon_surf.get_rect(center = bg_rect.center)

        self.display_surface.blit(weapon_surf, weapon_rect)

    def magic_overlay(self, magic_index):
        bg_rect = self.selection_box((WIDTH//2) - (ITEM_BOX_SIZE//2), HEIGHT - TILESIZE - (ITEM_BOX_SIZE//2))
        magic_surf = self.magic_grafics[magic_index]
        magic_rect = magic_surf.get_rect(center = bg_rect.center)

        self.display_surface.blit(magic_surf, magic_rect)
    
    def food_overlay(self, food_index, player):
        bg_rect = self.selection_box((WIDTH//2) + (ITEM_BOX_SIZE//2) + 10, HEIGHT - TILESIZE - (ITEM_BOX_SIZE//2))
        food_surf = self.food_grafics[food_index]
        food_rect = food_surf.get_rect(center = bg_rect.center)

        #count amount food
        food_counter = player.inv.count(list(FOOD_DATA.keys())[food_index])
        text_surface = self.font.render(str(int(food_counter)), False, TEXT_COLOR) 
        text_rect = text_surface.get_rect(bottomright = food_rect.bottomright)

        #draw food + amount
        self.display_surface.blit(food_surf, food_rect)
        self.display_surface.blit(text_surface, text_rect)

    def explanation(self):
        #switch explantion
        text_surface1 = self.font.render('Switch wapen: q', False, TEXT_COLOR)
        text_rect1 = text_surface1.get_rect(topleft = (WIDTH*(3/4) - 150, HEIGHT - TILESIZE + 10))
        text_surface2 = self.font.render('Swicth Magic: e', False, TEXT_COLOR)
        text_rect2 = text_surface2.get_rect(topleft = (WIDTH*(3/4) - 150, HEIGHT - TILESIZE - 10))
        text_surface3 = self.font.render('Switch Food: m', False, TEXT_COLOR)
        text_rect3 = text_surface3.get_rect(topleft = (WIDTH*(3/4) - 150, HEIGHT - TILESIZE - 30))

        #use explanation
        text_surface4 = self.font.render('Use wapen: SPACE', False, TEXT_COLOR)
        text_rect4 = text_surface4.get_rect(topleft = (WIDTH*(1/4) - 80, HEIGHT - TILESIZE + 10))
        text_surface5 = self.font.render('Use Magic: CTRL', False, TEXT_COLOR)
        text_rect5 = text_surface5.get_rect(topleft = (WIDTH*(1/4) - 80, HEIGHT - TILESIZE - 10))
        text_surface6 = self.font.render('Eat Food: SHIFT', False, TEXT_COLOR)
        text_rect6 = text_surface6.get_rect(topleft = (WIDTH*(1/4) - 80, HEIGHT - TILESIZE - 30))



        self.display_surface.blit(text_surface1, text_rect1)
        self.display_surface.blit(text_surface2, text_rect2)
        self.display_surface.blit(text_surface3, text_rect3) 
        self.display_surface.blit(text_surface4, text_rect4) 
        self.display_surface.blit(text_surface5, text_rect5) 
        self.display_surface.blit(text_surface6, text_rect6)   


        

    def display(self, player):
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)

        self.show_exp(player.exp)

        self.weapon_overlay(player.weapon_index)#weapon
        self.magic_overlay(player.magic_index)#magic
        self.food_overlay(player.food_index, player)#food

        self.explanation()


        
        


