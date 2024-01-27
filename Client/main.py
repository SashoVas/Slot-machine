import pygame
import settings
from user import User
from slot_machine import Slot_machine

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


    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    quit()

            pygame.display.update()
            self.screen.blit(self.bg,(0,0))
            self.machine.update()
            self.clock.tick(settings.FPS)

if __name__ == "__main__":
    game = Game()
    game.run()