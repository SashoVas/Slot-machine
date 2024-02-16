import pygame
import settings
from user import User
from slot_machine import SlotMachine
from custom_objects import Button


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT+settings.USER_INTERVACE_ADDIONAL_HEIGHT))
        pygame.display.set_caption("Slot Machine")
        self.clock = pygame.time.Clock()
        self.bg = pygame.image.load(
            settings.BACKGROUND_IMAGE_PATH).convert_alpha()
        self.user_interface_bg = pygame.image.load(
            settings.USER_INTERFACE_BACKGROUND_IMAGE_PATH).convert_alpha()
        self.user = User()
        self.machine = SlotMachine(self.user_interface_bg, self.user)

    def get_common_buttons(self, first_text, second_text):
        first_button = Button(image=pygame.image.load(settings.AUTOSPIN_BUTTON_BACKGRAOUND_PATH).convert_alpha(),
                              pos=settings.SUBMIT_BUTTON_POSITION,
                              text_input=first_text,
                              font=pygame.font.Font(settings.FONT_PATH, settings.BUTTON_FONT_SIZE), base_color="#d7fcd4", hovering_color="White")
        second_button = Button(image=pygame.image.load(settings.AUTOSPIN_BUTTON_BACKGRAOUND_PATH).convert_alpha(),
                               pos=settings.GO_BACK_BUTTON_POSITION,
                               text_input=second_text,
                               font=pygame.font.Font(settings.FONT_PATH, settings.BUTTON_FONT_SIZE), base_color="#d7fcd4", hovering_color="White")
        return first_button, second_button

    def blit_text_input(self, first_text, second_text, first_input, second_input):
        font = pygame.font.Font(
            'freesansbold.ttf', settings.TEXT_FONT_SIZE)
        username_input = font.render(
            f"{first_text}:{first_input}", True, (255, 255, 255))
        password_input = font.render(
            f"{second_text}:{second_input}", True, (255, 255, 255))
        self.screen.blit(username_input, settings.USERNAME_TEXT_POSITION)
        self.screen.blit(password_input, settings.PASSWORD_TEXT_POSITION)

    def update_buttons(self, buttons_list, mouse_pos):
        for button in buttons_list:
            button.changeColor(mouse_pos)
            button.update(self.screen)

    def handle_user_input_events(self,  username, password, username_redy, login_button, go_back_button, running, mouse_pos, submit_func):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.TEXTINPUT:
                if username_redy:
                    password += event.text
                else:
                    username += event.text
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if username_redy:
                        password = password[:-1]
                    else:
                        username = username[:-1]
                if event.key == pygame.K_RETURN:
                    if username_redy:
                        if submit_func(username, password):
                            running = False
                            self.run_menu()
                    else:
                        username_redy = True
                if event.key == pygame.K_TAB:
                    username_redy = not username_redy
            if event.type == pygame.MOUSEBUTTONDOWN:
                if login_button.checkForInput(mouse_pos):
                    if submit_func(username, password):
                        running = False
                        self.run_menu()
                if go_back_button.checkForInput(mouse_pos):
                    running = False
                    self.run_menu()
        return username, password, username_redy, running

    def run_slot_machine(self):
        running = True
        while running:

            mouse_pos = pygame.mouse.get_pos()
            auto_spin_button = Button(image=pygame.image.load(settings.AUTOSPIN_BUTTON_BACKGRAOUND_PATH).convert_alpha(),
                                      pos=(950, 650),
                                      text_input="Autospin",
                                      font=pygame.font.Font(settings.FONT_PATH, settings.BUTTON_FONT_SIZE), base_color="#d7fcd4", hovering_color="White")

            spin_button = Button(image=pygame.image.load(settings.AUTOSPIN_BUTTON_BACKGRAOUND_PATH).convert_alpha(),
                                 pos=(780, 650),
                                 text_input="Spin",
                                 font=pygame.font.Font(settings.FONT_PATH, settings.BUTTON_FONT_SIZE), base_color="#d7fcd4", hovering_color="White")
            self.update_buttons([spin_button, auto_spin_button], mouse_pos)

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
                        running = False
                        self.run_menu()

            pygame.display.update()
            self.screen.blit(self.bg, (0, 0))
            self.machine.update()
            self.clock.tick(settings.FPS)

    def run_menu(self):
        running = True
        while running:
            self.screen.fill((0, 0, 0))

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
            self.update_buttons([play_button, register_statistics_button,
                                 login_options_button, quit_button], mouse_pos)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.checkForInput(mouse_pos) and self.user.is_logged():
                        running = False
                        self.run_slot_machine()
                    if login_options_button.checkForInput(mouse_pos) and not self.user.is_logged():
                        running = False
                        self.run_login()
                    if register_statistics_button.checkForInput(mouse_pos) and not self.user.is_logged():
                        running = False
                        self.run_register()
                    if login_options_button.checkForInput(mouse_pos) and self.user.is_logged():
                        running = False
                        self.run_options()
                    if quit_button.checkForInput(mouse_pos):
                        pygame.quit()
                        quit()
                    if register_statistics_button.checkForInput(mouse_pos) and self.user.is_logged():
                        running = False
                        self.run_statistics()

            pygame.display.update()
            self.clock.tick(settings.FPS)

    def run_login(self):
        running = True
        username = ""
        password = ""
        username_redy = False
        while running:
            self.screen.fill((0, 0, 0))

            mouse_pos = pygame.mouse.get_pos()

            login_button, go_back_button = self.get_common_buttons(
                'Login', 'Go back')
            self.blit_text_input("username", "password", username, password)
            self.update_buttons([login_button, go_back_button], mouse_pos)

            username, password, username_redy, running = self.handle_user_input_events(
                username, password, username_redy, login_button, go_back_button, running, mouse_pos, self.user.login)

            pygame.display.update()
            self.clock.tick(settings.FPS)

    def run_register(self):
        running = True
        username = ""
        password = ""
        username_redy = False
        while running:
            self.screen.fill((0, 0, 0))

            mouse_pos = pygame.mouse.get_pos()
            register_button, go_back_button = self.get_common_buttons(
                'Register', 'Go back')
            self.blit_text_input("username", "password", username, password)
            self.update_buttons([register_button, go_back_button], mouse_pos)

            username, password, username_redy, running = self.handle_user_input_events(
                username, password, username_redy, register_button, go_back_button, running, mouse_pos, self.user.register)

            pygame.display.update()
            self.clock.tick(settings.FPS)

    def run_options(self):
        running = True
        bet_amount = "100"
        deposit = ""
        bet_amount_ready = False
        while running:
            self.screen.fill((0, 0, 0))

            mouse_pos = pygame.mouse.get_pos()
            submit_button, go_back_button = self.get_common_buttons(
                'Submit', 'Go back')
            self.blit_text_input("Bet amount", "Deposit", bet_amount, deposit)
            self.update_buttons([submit_button, go_back_button], mouse_pos)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.TEXTINPUT:
                    if not event.text.isdigit() and not event.text == ".":
                        continue
                    if bet_amount_ready:
                        deposit += event.text
                    else:
                        bet_amount += event.text
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        if bet_amount_ready:
                            deposit = deposit[:-1]
                        else:
                            bet_amount = bet_amount[:-1]
                    if event.key == pygame.K_RETURN:
                        if bet_amount_ready:
                            if bet_amount != '' and float(bet_amount) > 0:
                                self.user.change_bet_amount(float(bet_amount))
                            if deposit != '' and float(deposit) > 0:
                                self.user.deposit(float(deposit))
                            running = False
                            self.run_menu()
                        else:
                            bet_amount_ready = True
                    if event.key == pygame.K_TAB:
                        bet_amount_ready = not bet_amount_ready
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if submit_button.checkForInput(mouse_pos):
                        if bet_amount != '' and float(bet_amount) > 0:
                            self.user.change_bet_amount(float(bet_amount))
                        if deposit != '' and float(deposit) > 0:
                            self.user.deposit(float(deposit))
                        running = False
                        self.run_menu()
                    if go_back_button.checkForInput(mouse_pos):
                        running = False
                        self.run_menu()

            pygame.display.update()
            self.clock.tick(settings.FPS)

    def run_statistics(self):
        running = True
        statistics = self.user.get_user_statistics()
        leaderboards = self.user.get_leader_board()
        is_statistics = True
        while running:
            self.screen.fill((0, 0, 0))

            mouse_pos = pygame.mouse.get_pos()

            go_back_button = Button(image=pygame.image.load(settings.AUTOSPIN_BUTTON_BACKGRAOUND_PATH).convert_alpha(),
                                    pos=(700, 650),
                                    text_input="Go back",
                                    font=pygame.font.Font(settings.FONT_PATH, settings.BUTTON_FONT_SIZE), base_color="#d7fcd4", hovering_color="White")
            font = pygame.font.Font(
                'freesansbold.ttf', settings.TEXT_FONT_SIZE)
            statistic_screen_name = font.render(
                f"Statistics" if is_statistics else "Leaderboard by profit", True, (255, 255, 255))
            self.screen.blit(statistic_screen_name, (480, 10))

            if is_statistics:
                for current, (key, value) in enumerate(statistics.items()):
                    self.screen.blit(font.render(
                        f"{key}:{value}", True, (255, 255, 255)), (current, 40*current+50))
            else:
                for current, user in enumerate(leaderboards):
                    self.screen.blit(font.render(
                        f"{user['user__username']}:{user['profit']}", True, (255, 255, 255)), (current, 40*current+50))
            self.update_buttons([go_back_button], mouse_pos)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if go_back_button.checkForInput(mouse_pos):
                        running = False
                        self.run_menu()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_TAB:
                        is_statistics = not is_statistics

            pygame.display.update()
            self.clock.tick(settings.FPS)


if __name__ == "__main__":
    game = Game()
    game.run_menu()
