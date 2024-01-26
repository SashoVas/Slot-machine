import pygame
import random
import settings

class Symbol(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Reel:
    def __init__(self, x, y):
        self.symbol_list = pygame.sprite.Group()
        self.animation_sprites = pygame.sprite.Group()
        self.x=x
        self.y=y
        self.is_spinning=False
        self.is_board_full=False
        self.reel_end_sound=pygame.mixer.Sound(settings.SPIN_END_SOUND_PATH)
        for i in range(3):
            symbol_to_spawn=random.randint(1,8)
            self.symbol_list.add(Symbol(self.x,self.y + i*(settings.IMAGE_HEIGHT+settings.HEIGHT_OFFSET), settings.IMAGE_PATHS[symbol_to_spawn]))

    def update(self, display_surface):
        self.animate()
        self.symbol_list.draw(display_surface)

    def re_center_symbols(self):
        for current, symbol in enumerate( self.symbol_list):
            symbol.rect.y = self.y + current*(settings.IMAGE_HEIGHT+settings.HEIGHT_OFFSET)

    def generate_new_symbol_in_animation(self):
        if not self.is_board_full and self.symbol_list.sprites()[-1].rect.y+195 >= settings.SCREEN_HEIGHT:
            self.is_board_full=True
            if len(self.animation_sprites):
                sprite_list=self.symbol_list.sprites()
                sprite_list.insert(0,self.animation_sprites.sprites()[-1])
                self.animation_sprites.remove(self.animation_sprites.sprites()[-1])
                self.symbol_list = pygame.sprite.Group()
                self.symbol_list.add(sprite_list)

        if self.symbol_list.sprites()[-1].rect.y >= settings.SCREEN_HEIGHT:
            self.symbol_list.sprites()[-1].kill()
            self.is_board_full=False

    def animate(self):
        if not self.is_spinning:
            return

        if not len(self.animation_sprites) and len( self.symbol_list)==3:
            self.reel_end_sound.play()
            self.is_spinning=False
            self.re_center_symbols()

            return
        
        for symbol in self.symbol_list:
            symbol.rect.y += settings.SPIN_SPEED

        self.generate_new_symbol_in_animation()
                
    
    def spin(self, symbol_list,additional_symbols):
        if self.is_spinning:
            return
        
        self.is_spinning=True
        for symbol in symbol_list:
            self.animation_sprites.add(Symbol(self.x,settings.ANIMATION_SYMBOL_SPAWN_HEIGHT,settings.IMAGE_PATHS[symbol]))
        
        for i in range(additional_symbols):
            symbol_to_spawn=random.randint(1,8)
            self.animation_sprites.add(Symbol(self.x,settings.ANIMATION_SYMBOL_SPAWN_HEIGHT, settings.IMAGE_PATHS[symbol_to_spawn]))