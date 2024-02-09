import pygame
import settings
from user import User
from slot_machine import Slot_machine
from custom_objects import Button

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT+settings.USER_INTERVACE_ADDIONAL_HEIGHT))
        pygame.display.set_caption("Slot Machine")
        self.clock = pygame.time.Clock()
        self.bg=pygame.image.load(settings.BACKGROUND_IMAGE_PATH)
        self.user_interface_bg=pygame.image.load(settings.USER_INTERFACE_BACKGROUND_IMAGE_PATH)
        self.user= User("nqkoi","nqkoi")
        #self.user.deposit(1000)
        self.machine=Slot_machine(self.user_interface_bg,self.user)


    def run_slot_machine(self):
        running=True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            #self.machine.auto_spin()
            pygame.display.update()
            self.screen.blit(self.bg,(0,0))
            self.machine.update()
            self.clock.tick(settings.FPS)
    
    def run_menu(self):
        running=True
        while running:
            MENU_MOUSE_POS = pygame.mouse.get_pos()


            play_button = Button(image=pygame.image.load(settings.BUTTON_BACKGRAOUND_PATH), pos=(540, 150), 
                                text_input="Play", font=pygame.font.Font(settings.FONT_PATH, 75), base_color="#d7fcd4", hovering_color="White")
            register_button = Button(image=pygame.image.load(settings.BUTTON_BACKGRAOUND_PATH), pos=(540, 300), 
                                text_input="Register", font=pygame.font.Font(settings.FONT_PATH, 75), base_color="#d7fcd4", hovering_color="White")
            login_button = Button(image=pygame.image.load(settings.BUTTON_BACKGRAOUND_PATH),pos=(540, 450), 
                                text_input="Login", font=pygame.font.Font(settings.FONT_PATH, 75), base_color="#d7fcd4", hovering_color="White")
            quit_button = Button(image=pygame.image.load(settings.BUTTON_BACKGRAOUND_PATH),pos=(540, 600), 
                    text_input="Quit", font=pygame.font.Font(settings.FONT_PATH, 75), base_color="#d7fcd4", hovering_color="White")

            for button in [play_button, register_button, login_button, quit_button]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.checkForInput(MENU_MOUSE_POS):
                        running=False
                        self.run_slot_machine()
                    if login_button.checkForInput(MENU_MOUSE_POS):
                        running=False
                        print("login")
                    if register_button.checkForInput(MENU_MOUSE_POS):
                        running=False
                        print("register")
                    if quit_button.checkForInput(MENU_MOUSE_POS):
                        pygame.quit()
                        quit()

            pygame.display.update()
            self.clock.tick(settings.FPS)





if __name__ == "__main__":
    game = Game()
    game.run_menu()