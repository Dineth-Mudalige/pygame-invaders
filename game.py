import pygame
import requests
import threading
import time
import constants
import sys

class Game:
    screen = None
    aliens = []
    rockets = []
    lost = False

    def __init__(self, width, height):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        reader_thread = threading.Thread(target=self.run_game)
        reader_thread.start()
        
    def run_game(self):
        done = False

        hero = Hero(self, self.width / 2, self.height - 20)
        generator = Generator(self)
        rocket = None
        lock = threading.Lock()
        while not done:
            if len(self.aliens) == 0:
                self.displayText("VICTORY ACHIEVED")
            self.rockets.append(Rocket(self, hero.x, hero.y))

            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_LEFT]:  # sipka doleva
                hero.x -= 6 if hero.x > 20 else 0  # leva hranice plochy
            elif pressed[pygame.K_RIGHT]:  # sipka doprava
                hero.x += 6 if hero.x < self.width - 20 else 0  # prava hranice

            with lock:
                try:
                    with open(constants.COMMAND_FILE_NAME,"r") as file:
                        command = file.read()
                        print("Read: ", command)
                        if "LEFT" in command:
                            hero.x -= 3 if hero.x > 20 else 0
                            print("Moving left")
                        elif "RIGHT" in command:
                            hero.x += 3 if hero.x < self.width - 20 else 0
                            print("Moving right")
                        else:
                            print("Staying still")
                except FileNotFoundError:
                    print("File not found")            
           
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                # if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not self.lost:
                #     self.rockets.append(Rocket(self, hero.x, hero.y))

            pygame.display.flip()
            self.clock.tick(1e5)
            self.screen.fill((0, 0, 0))

            for alien in self.aliens:
                alien.draw()
                alien.checkCollision(self)
                if (alien.y > self.height):
                    self.lost = True
                    self.displayText("YOU LOOSE")
                    

            for rocket in self.rockets:
                rocket.draw()

            if not self.lost: hero.draw()

    def displayText(self, text):
        pygame.font.init()
        font = pygame.font.SysFont('Arial', 50)
        textsurface = font.render(text, False, (44, 0, 62))
        self.screen.blit(textsurface, (110, 160))


class Alien:
    def __init__(self, game, x, y):
        self.x = x
        self.game = game
        self.y = y
        self.size = 20

    def draw(self):
        pygame.draw.rect(self.game.screen,  # renderovací plocha
                         (81, 43, 88),  # barva objektu
                         pygame.Rect(self.x, self.y, self.size, self.size))
        self.y += 0.05

    def checkCollision(self, game):
        for rocket in game.rockets:
            if (rocket.x < self.x + self.size and
                    rocket.x > self.x - self.size and
                    rocket.y < self.y + self.size and
                    rocket.y > self.y - self.size):
                game.rockets.remove(rocket)
                game.aliens.remove(self)


class Hero:
    def __init__(self, game, x, y):
        self.x = x
        self.game = game
        self.y = y

    def draw(self):
        pygame.draw.rect(self.game.screen,
                         (210, 250, 251),
                         pygame.Rect(self.x, self.y, 8, 5))


class Generator:
    def __init__(self, game):
        margin = 30  # mezera od okraju obrazovky
        width = 50  # mezera mezi alieny
        for x in range(margin, game.width - margin, width):
            for y in range(margin, int(game.height / 2), width):
                game.aliens.append(Alien(game, x, y))

        # game.aliens.append(Alien(game, 280, 50))


class Rocket:
    def __init__(self, game, x, y):
        self.x = x
        self.y = y
        self.game = game

    def draw(self):
        pygame.draw.rect(self.game.screen,  # renderovací plocha
                         (254, 52, 110),  # barva objektu
                         pygame.Rect(self.x, self.y, 2, 4))
        self.y -= 2  # poletí po herní ploše nahoru 2px/snímek

game = Game(600, 400)
