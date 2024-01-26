import pygame
import random
import settings
import requests

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

class Slot_machine:
    def __init__(self,user_interface_bg):
        self.reels_list = []
        self.display_surface = pygame.display.get_surface()
        self.authorization_header = 'Token 16f1d83da2c36f05275fb7ad4d1403c945eaf06a'
        self.winning_lines=[]
        self.to_vizualize_winnings=False
        self.result_of_spin=0
        self.user_interface_bg=user_interface_bg
        self.initialize_user_data()
        self.initialize_reels()


    def initialize_reels(self):
        for i in range(5):
            width = i*(settings.IMAGE_WIDTH + settings.WIDTH_OFFSET) + settings.START_WIDTH
            height=settings.START_HEIGHT
            self.reels_list.append(Reel(width, height))


    def initialize_user_data(self):
        response=requests.get(settings.USER_INFO_ENDPOINT_URL,headers={"Authorization":self.authorization_header}) 
        json_data=response.json()

        self.user_balance = json_data["balance"]
        self.user_name = json_data["username"]


    def update(self):
        self.check_input_for_spin()
        for reel in self.reels_list:
            reel.update(self.display_surface)
        self.vizualize_winnings()




    def check_input_for_spin(self):
        keys=pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and not any([reel.is_spinning for reel in self.reels_list]):
            self.spin()


    def vizualize_winnings(self):
        if self.to_vizualize_winnings and not any([reel.is_spinning for reel in self.reels_list]):
            self.to_vizualize_winnings=False
            self.user_balance+=self.result_of_spin
        font=pygame.font.Font('freesansbold.ttf', 32)
        img=font.render(f"balance:{self.user_balance}",True,(255,255,255))

        self.display_surface.blit(self.user_interface_bg,(0,settings.SCREEN_HEIGHT))
        self.display_surface.blit(img,(30,settings.SCREEN_HEIGHT+30))



    def get_spin_result(self):
        response=requests.post(settings.SPIN_REQUST_ENDPOINT_URL
                               ,headers={"Authorization":self.authorization_header}
                               ,data={"cost":100})
        
        json_data=response.json()
        return json_data["board_info"],json_data["winings_multyplier"], json_data["result"]
    

    def spin(self):
        if self.user_balance < 100:
            return
        self.user_balance -= 100
        board_info,winings_multyplier, result = self.get_spin_result()
        self.result_of_spin=result
        board=board_info["roll_board"]
        self.winning_lines=board_info["winning_lines"]
        self.to_vizualize_winnings=True
        for current_reel,reel in enumerate(self.reels_list):
            reel.spin(board[current_reel],current_reel*2+1)