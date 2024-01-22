import pygame

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1260, 700))
        pygame.display.set_caption("Slot Machine")
        self.clock = pygame.time.Clock()
        self.bg=pygame.image.load('Client/graphics/backgrounds/bg1.png')


    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    quit()

            self.screen.blit(self.bg,(0,0))
            pygame.display.update()
            self.clock.tick(60)

if __name__ == "__main__":
    game = Game()
    game.run()