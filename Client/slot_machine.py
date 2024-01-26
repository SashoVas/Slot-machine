import pygame
from reel import Reel
import settings
import requests

class Slot_machine:
    def __init__(self,user_interface_bg,user):
        self.reels_list = []
        self.display_surface = pygame.display.get_surface()
        self.winning_lines=[]
        self.to_vizualize_winnings=False
        self.result_of_spin=0
        self.user_interface_bg=user_interface_bg
        self.user=user
        self.start_spin_sound=pygame.mixer.Sound(settings.SPIN_START_SOUND_PATH)
        self.initialize_reels()


    def initialize_reels(self):
        for i in range(5):
            width = i*(settings.IMAGE_WIDTH + settings.WIDTH_OFFSET) + settings.START_WIDTH
            height=settings.START_HEIGHT
            self.reels_list.append(Reel(width, height))


    def update(self):
        self.check_input_for_spin()
        for reel in self.reels_list:
            reel.update(self.display_surface)
        self.vizualize_winnings()


    def check_input_for_spin(self):
        keys=pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and not any([reel.is_spinning for reel in self.reels_list]):
            self.spin(100)


    def vizualize_winnings(self):
        if self.to_vizualize_winnings and not any([reel.is_spinning for reel in self.reels_list]):
            self.to_vizualize_winnings=False
            self.user.balance+=self.result_of_spin
        font=pygame.font.Font('freesansbold.ttf', 32)
        img=font.render(f"balance:{self.user.balance}",True,(255,255,255))

        self.display_surface.blit(self.user_interface_bg,(0,settings.SCREEN_HEIGHT))
        self.display_surface.blit(img,(30,settings.SCREEN_HEIGHT+30))



    def get_spin_result(self,amount):
        response=requests.post(settings.SPIN_REQUST_ENDPOINT_URL
                               ,headers={"Authorization":self.user.get_authorization_header()}
                               ,data={"cost":amount})
        
        json_data=response.json()
        return json_data["board_info"],json_data["winings_multyplier"], json_data["result"]


    def spin(self,amount):
        if self.user.balance < amount:
            return
        self.start_spin_sound.play()

        self.user.balance -= amount
        board_info,winings_multyplier, result = self.get_spin_result(amount)
        self.result_of_spin=result
        board=board_info["roll_board"]
        self.winning_lines=board_info["winning_lines"]
        self.to_vizualize_winnings=True
        for current_reel,reel in enumerate(self.reels_list):
            reel.spin(board[current_reel],current_reel*4+1)