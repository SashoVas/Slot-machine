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
        self.x=x
        self.y=y

        for i in range(3):
            symbol_to_spawn=random.randint(1,8)
            self.symbol_list.add(Symbol(self.y,self.x + i*(settings.IMAGE_HEIGHT+settings.HEIGHT_OFFSET), settings.IMAGE_PATHS[symbol_to_spawn]))


    def update(self, display_surface):
        self.symbol_list.draw(display_surface)
    def spin(self):
        pass

class Slot_machine:
    def __init__(self):
        self.reels_list = []
        self.display_surface=pygame.display.get_surface()
        for i in range(5):
            width = i*(settings.IMAGE_WIDTH + settings.WIDTH_OFFSET) + settings.START_WIDTH
            height=settings.START_HEIGHT
            self.reels_list.append(Reel(height, width))

    def update(self):
        for reel in self.reels_list:
            reel.update(self.display_surface)


    def spin(self):
        pass