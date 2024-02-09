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
        self.win_sound=pygame.mixer.Sound(settings.WIN_SOUND_PATH)
        self.big_win_sound=pygame.mixer.Sound(settings.BIG_WIN_SOUND_PATH)
        self.omega_win_sound=pygame.mixer.Sound(settings.OMEGA_WIN_SOUND_PATH)
        self.last_win_animation_time=0
        self.winnings_multyplier=0
        self.initialize_reels()
        self.visualize_multipliyer=False
        self.is_auto_spin=False


    def is_auto_spining(self):
        return self.auto_spin


    def auto_spin(self):
        self.is_auto_spin = not self.is_auto_spin


    def initialize_reels(self):
        for i in range(5):
            width = i*(settings.IMAGE_WIDTH + settings.WIDTH_OFFSET) + settings.START_WIDTH
            height=settings.START_HEIGHT
            self.reels_list.append(Reel(width, height))

    def auto(self):
        if not any([reel.is_spinning for reel in self.reels_list]):
            self.spin(self.user.bet_amount)


    def update(self):
        if self.is_auto_spin:
            self.auto()

        for reel in self.reels_list:
            reel.update(self.display_surface)
        self.vizualize_winnings()


    def animate_winnings(self):
        if pygame.time.get_ticks() - self.last_win_animation_time > 1000 and not any([reel.is_spinning for reel in self.reels_list]):
            self.last_win_animation_time=pygame.time.get_ticks()
            for reel in self.reels_list:
                reel.remove_animations()
            if len(self.winning_lines):
                for reel_num,symbol in enumerate(self.winning_lines[-1]):
                    self.reels_list[reel_num].animate_win(symbol)
                current = self.winning_lines.pop()
                self.winning_lines.insert(0,current)


    def vizualize_winnings(self):
        if self.to_vizualize_winnings and not any([reel.is_spinning for reel in self.reels_list]):
            self.to_vizualize_winnings=False
            self.user.balance+=self.result_of_spin
            if self.result_of_spin:
                self.visualize_multipliyer=True
                if self.winnings_multyplier > settings.OMEGA_WIN_MULTIPLIER:
                    self.omega_win_sound.play()
                elif self.winnings_multyplier > settings.BIG_WIN_MULTIPLIER:
                    self.big_win_sound.play()
                else:
                    self.win_sound.play()

        self.animate_winnings()

        font=pygame.font.Font('freesansbold.ttf', 32)
        img=font.render(f"balance:{self.user.balance}",True,(255,255,255))
        
        self.display_surface.blit(self.user_interface_bg,(0,settings.SCREEN_HEIGHT))
        self.display_surface.blit(img,(30,settings.SCREEN_HEIGHT+30))
        if self.visualize_multipliyer:
            font2=pygame.font.Font('freesansbold.ttf', 50)

            img2=font2.render(f"WIN: X {self.winnings_multyplier}",True,(255,255,255))
            self.display_surface.blit(img2,(400,settings.SCREEN_HEIGHT+15))




    def get_spin_result(self,amount):
        response=requests.post(settings.SPIN_REQUST_ENDPOINT_URL
                               ,headers={"Authorization":self.user.get_authorization_header()}
                               ,data={"cost":amount})
        
        json_data=response.json()
        return json_data["board_info"],json_data["winings_multyplier"], json_data["result"]


    def spin(self,amount):
        if self.user.balance < amount:
            return
        
        if any([reel.is_spinning for reel in self.reels_list]):
            return
        
        self.visualize_multipliyer=False
        self.start_spin_sound.play()

        self.user.balance -= amount
        board_info,winings_multyplier, result = self.get_spin_result(amount)
        self.result_of_spin=result
        self.winnings_multyplier=winings_multyplier 
        board=board_info["roll_board"]
        self.winning_lines=board_info["winning_lines"]
        self.to_vizualize_winnings=True
        for current_reel,reel in enumerate(self.reels_list):
            reel.spin(board[current_reel],current_reel*4+1)