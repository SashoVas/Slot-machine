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
        self.bg=pygame.image.load(settings.BACKGROUND_IMAGE_PATH).convert_alpha()
        self.user_interface_bg=pygame.image.load(settings.USER_INTERFACE_BACKGROUND_IMAGE_PATH).convert_alpha()
        self.user= User()
        self.machine=Slot_machine(self.user_interface_bg,self.user)


    def run_slot_machine(self):
        running=True
        while running:

            mouse_pos = pygame.mouse.get_pos()
            auto_spin_button = Button(image=pygame.image.load(settings.AUTOSPIN_BUTTON_BACKGRAOUND_PATH).convert_alpha(),
                                pos=(950, 650), 
                                text_input="Autospin",
                                font=pygame.font.Font(settings.FONT_PATH, 20), base_color="#d7fcd4", hovering_color="White")
            
            spin_button = Button(image=pygame.image.load(settings.AUTOSPIN_BUTTON_BACKGRAOUND_PATH).convert_alpha(),
                                pos=(780, 650), 
                                text_input="Spin",
                                font=pygame.font.Font(settings.FONT_PATH, 20), base_color="#d7fcd4", hovering_color="White")

            for button in [spin_button, auto_spin_button]:
                button.changeColor(mouse_pos)
                button.update(self.screen)


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if spin_button.checkForInput(mouse_pos):
                        self.machine.spin(self.user.bet_amount)
                    if auto_spin_button.checkForInput(mouse_pos):
                        self.machine.auto_spin()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.machine.spin(self.user.bet_amount)
                    if event.key == pygame.K_ESCAPE:
                        running=False
                        self.run_menu()

            pygame.display.update()
            self.screen.blit(self.bg,(0,0))
            self.machine.update()
            self.clock.tick(settings.FPS)
    

    def run_menu(self):
        running=True
        while running:
            self.screen.fill((0,0,0))

            mouse_pos = pygame.mouse.get_pos()


            play_button = Button(image=pygame.image.load(settings.BUTTON_BACKGRAOUND_PATH).convert_alpha(),
                                pos=(540, 150), 
                                text_input="Play", font=pygame.font.Font(settings.FONT_PATH, 75), base_color="#d7fcd4", hovering_color="White")
            register_statistics_button = Button(image=pygame.image.load(settings.BUTTON_BACKGRAOUND_PATH).convert_alpha(),
                                pos=(540, 300), 
                                text_input="Register" if not self.user.is_logged() else "Statistics",
                                font=pygame.font.Font(settings.FONT_PATH, 75), base_color="#d7fcd4", hovering_color="White")
            login_options_button = Button(image=pygame.image.load(settings.BUTTON_BACKGRAOUND_PATH).convert_alpha(),
                                pos=(540, 450), 
                                text_input="Login" if not self.user.is_logged() else "Options",
                                font=pygame.font.Font(settings.FONT_PATH, 75), base_color="#d7fcd4", hovering_color="White")
            quit_button = Button(image=pygame.image.load(settings.BUTTON_BACKGRAOUND_PATH).convert_alpha(),
                    pos=(540, 600), 
                    text_input="Quit", font=pygame.font.Font(settings.FONT_PATH, 75), base_color="#d7fcd4", hovering_color="White")

            for button in [play_button, register_statistics_button, login_options_button, quit_button]:
                button.changeColor(mouse_pos)
                button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.checkForInput(mouse_pos) and self.user.is_logged():
                        running=False
                        self.run_slot_machine()
                    if login_options_button.checkForInput(mouse_pos) and not self.user.is_logged():
                        running=False
                        self.run_login()
                    if register_statistics_button.checkForInput(mouse_pos) and not self.user.is_logged():
                        running=False
                        self.run_register()
                    if login_options_button.checkForInput(mouse_pos) and self.user.is_logged():
                        running=False
                        self.run_options()
                    if quit_button.checkForInput(mouse_pos):
                        pygame.quit()
                        quit()
                    if register_statistics_button.checkForInput(mouse_pos) and self.user.is_logged():
                        running=False
                        self.run_statistics()

            pygame.display.update()
            self.clock.tick(settings.FPS)


    def run_login(self):
        running =True
        username=""
        password=""
        username_redy=False
        while running:
            self.screen.fill((0,0,0))

            mouse_pos = pygame.mouse.get_pos()
            
            login_button = Button(image=pygame.image.load(settings.AUTOSPIN_BUTTON_BACKGRAOUND_PATH).convert_alpha(),
                                pos=(380, 650), 
                                text_input="Login",
                                font=pygame.font.Font(settings.FONT_PATH, 20), base_color="#d7fcd4", hovering_color="White")
            go_back_button = Button(image=pygame.image.load(settings.AUTOSPIN_BUTTON_BACKGRAOUND_PATH).convert_alpha(),
                                pos=(550, 650), 
                                text_input="Go back",
                                font=pygame.font.Font(settings.FONT_PATH, 20), base_color="#d7fcd4", hovering_color="White")
            font=pygame.font.Font('freesansbold.ttf', 32)
            username_input=font.render(f"username:{username}",True,(255,255,255))
            password_input=font.render(f"password:{password}",True,(255,255,255))
            self.screen.blit(username_input,(30,200))
            self.screen.blit(password_input,(30,300))

            for button in [login_button, go_back_button]:
                button.changeColor(mouse_pos)
                button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.TEXTINPUT:
                    if username_redy:
                        password+=event.text
                    else:
                        username+=event.text
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        if username_redy:
                            password=password[:-1]
                        else:
                            username=username[:-1]
                    if event.key == pygame.K_RETURN:
                        if username_redy:
                            if self.user.login(username,password):
                                running=False
                                self.run_menu()
                        else:
                            username_redy=True
                    if event.key == pygame.K_TAB:
                        username_redy=not username_redy
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if login_button.checkForInput(mouse_pos):
                        if self.user.login(username,password):
                            running=False
                            self.run_menu()
                    if go_back_button.checkForInput(mouse_pos):
                        running=False
                        self.run_menu()

            pygame.display.update()
            self.clock.tick(settings.FPS)


    def run_register(self):
        running =True
        username=""
        password=""
        username_redy=False
        while running:
            self.screen.fill((0,0,0))

            mouse_pos = pygame.mouse.get_pos()
            
            register_button = Button(image=pygame.image.load(settings.AUTOSPIN_BUTTON_BACKGRAOUND_PATH).convert_alpha(),
                                pos=(380, 650), 
                                text_input="Register",
                                font=pygame.font.Font(settings.FONT_PATH, 20), base_color="#d7fcd4", hovering_color="White")
            go_back_button = Button(image=pygame.image.load(settings.AUTOSPIN_BUTTON_BACKGRAOUND_PATH).convert_alpha(),
                                pos=(550, 650), 
                                text_input="Go back",
                                font=pygame.font.Font(settings.FONT_PATH, 20), base_color="#d7fcd4", hovering_color="White")
            font=pygame.font.Font('freesansbold.ttf', 32)
            username_input=font.render(f"username:{username}",True,(255,255,255))
            password_input=font.render(f"password:{password}",True,(255,255,255))
            self.screen.blit(username_input,(30,200))
            self.screen.blit(password_input,(30,300))

            for button in [register_button, go_back_button]:
                button.changeColor(mouse_pos)
                button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.TEXTINPUT:
                    if username_redy:
                        password+=event.text
                    else:
                        username+=event.text
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        if username_redy:
                            password=password[:-1]
                        else:
                            username=username[:-1]
                    if event.key == pygame.K_RETURN:
                        if username_redy:
                            if self.user.register(username,password):
                                running=False
                                self.run_login()
                        else:
                            username_redy=True
                    if event.key == pygame.K_TAB:
                        username_redy=not username_redy
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if register_button.checkForInput(mouse_pos):
                        if self.user.register(username,password):
                            running=False
                            self.run_login()
                    if go_back_button.checkForInput(mouse_pos):
                        running=False
                        self.run_menu()

            pygame.display.update()
            self.clock.tick(settings.FPS)


    def run_options(self):
        running =True
        bet_amount="100"
        deposit=""
        bet_amount_ready=False
        while running:
            self.screen.fill((0,0,0))

            mouse_pos = pygame.mouse.get_pos()
            
            submit_button = Button(image=pygame.image.load(settings.AUTOSPIN_BUTTON_BACKGRAOUND_PATH).convert_alpha(),
                                pos=(380, 650), 
                                text_input="Submit",
                                font=pygame.font.Font(settings.FONT_PATH, 20), base_color="#d7fcd4", hovering_color="White")
            go_back_button = Button(image=pygame.image.load(settings.AUTOSPIN_BUTTON_BACKGRAOUND_PATH).convert_alpha(),
                                pos=(550, 650), 
                                text_input="Go back",
                                font=pygame.font.Font(settings.FONT_PATH, 20), base_color="#d7fcd4", hovering_color="White")
            font=pygame.font.Font('freesansbold.ttf', 32)
            bet_amount_input=font.render(f"Bet amount:{bet_amount}",True,(255,255,255))
            deposit_input=font.render(f"Deposit:{deposit}",True,(255,255,255))
            self.screen.blit(bet_amount_input,(30,200))
            self.screen.blit(deposit_input,(30,300))

            for button in [submit_button, go_back_button]:
                button.changeColor(mouse_pos)
                button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.TEXTINPUT:
                    if not event.text.isdigit() and not event.text==".":
                        continue
                    if bet_amount_ready:
                        deposit+=event.text
                    else:
                        bet_amount+=event.text
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        if bet_amount_ready:
                            deposit=deposit[:-1]
                        else:
                            bet_amount=bet_amount[:-1]
                    if event.key == pygame.K_RETURN:
                        if bet_amount_ready:
                            if bet_amount!='' and float(bet_amount)>0:
                                self.user.change_bet_amount(float(bet_amount))
                            if deposit != '' and float(deposit)>0:
                                self.user.deposit(float(deposit))
                            running=False
                            self.run_menu()
                        else:
                            bet_amount_ready=True
                    if event.key == pygame.K_TAB:
                        bet_amount_ready=not bet_amount_ready
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if submit_button.checkForInput(mouse_pos):
                        if bet_amount!='' and float(bet_amount)>0:
                            self.user.change_bet_amount(float(bet_amount))
                        if deposit != '' and float(deposit)>0:
                            self.user.deposit(float(deposit))
                        running=False
                        self.run_menu()
                    if go_back_button.checkForInput(mouse_pos):
                        running=False
                        self.run_menu()

            pygame.display.update()
            self.clock.tick(settings.FPS)


    def run_statistics(self):
        running =True
        statistics=self.user.get_user_statistics()
        leaderboards=self.user.get_leader_board()
        is_statistics=True
        while running:
            self.screen.fill((0,0,0))

            mouse_pos = pygame.mouse.get_pos()
            
            go_back_button = Button(image=pygame.image.load(settings.AUTOSPIN_BUTTON_BACKGRAOUND_PATH).convert_alpha(),
                                pos=(700, 650), 
                                text_input="Go back",
                                font=pygame.font.Font(settings.FONT_PATH, 20), base_color="#d7fcd4", hovering_color="White")
            font=pygame.font.Font('freesansbold.ttf', 32)
            statistic_screen_name=font.render(f"Statistics" if is_statistics else "Leaderboard",True,(255,255,255))
            self.screen.blit(statistic_screen_name,(480,10))

            if is_statistics:
                for current,(key,value) in enumerate(statistics.items()):
                    self.screen.blit(font.render(f"{key}:{value}",True,(255,255,255)),(current,40*current+50))
            else:
                for current,user in enumerate(leaderboards):
                    self.screen.blit(font.render(f"{user['user__username']}:{user['profit']}",True,(255,255,255)),(current,40*current+50))
            for button in [ go_back_button]:
                button.changeColor(mouse_pos)
                button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if go_back_button.checkForInput(mouse_pos):
                        running=False
                        self.run_menu()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_TAB:
                        is_statistics=not is_statistics

            pygame.display.update()
            self.clock.tick(settings.FPS)


if __name__ == "__main__":
    game = Game()
    game.run_menu()