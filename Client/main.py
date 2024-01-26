import pygame
import settings
from slot_machine import Slot_machine

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT+settings.USER_INTERVACE_ADDIONAL_HEIGHT))
        pygame.display.set_caption("Slot Machine")
        self.clock = pygame.time.Clock()
        self.bg=pygame.image.load(settings.BACKGROUND_IMAGE_PATH)
        self.user_interface_bg=pygame.image.load(settings.USER_INTERFACE_BACKGROUND_IMAGE_PATH)
        self.machine=Slot_machine(self.user_interface_bg)


    def run(self):
        #self.machine.spin()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    quit()

            pygame.display.update()
            self.screen.blit(self.bg,(0,0))
            #self.screen.blit(self.user_interface_bg,(0,settings.SCREEN_HEIGHT))
            self.machine.update()
            self.clock.tick(settings.FPS)

if __name__ == "__main__":
    game = Game()
    game.run()