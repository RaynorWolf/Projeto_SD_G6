import pygame
import Player_water
import Player_Fire
import Wall
import Door
import Button
import Lava
import Oceano


class Game(object):
    def __init__(self, width: int = 640, height: int = 480):
        self.width, self.height = width, height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("WaterGirl and FireBoy")
        self.clock = pygame.time.Clock()
        # Keep sprites as a group
        self.players = pygame.sprite.Group()
        self.player_fire = Player_Fire.PlayerFire(40, 40, 20, 70, self.players)
        self.player_water = Player_water.PlayerWater(20, 20, 20, 70, self.players)
        self.players.add(self.player_fire)
        self.players.add(self.player_water)
        # New wall sprites
        wall_size = 32
        self.walls = pygame.sprite.Group()
        self.door = pygame.sprite.Group()
        self.button = pygame.sprite.Group()
        self.lava = pygame.sprite.Group()
        self.oceano = pygame.sprite.Group()

        # Build a wall around the screen's frontiers
        for x in range(0, width, wall_size):
            for y in range(0, height, wall_size):
                if x in (0, width - wall_size) or y in (0, height - wall_size):
                    w = Wall.Wall(x, y, 0, wall_size, self.walls)
                    self.walls.add(w)
        w = Wall.Wall(300, 300, 0, wall_size, self.walls)
        self.walls.add(w)
        w1 = Wall.Wall(340, 300, 0, wall_size, self.walls)
        self.walls.add(w1)

        d1 = Door.Door(320, 300, 0, wall_size, self.walls)
        self.door.add(d1)
        b1 = Button.Button(320, 240, 0, wall_size, self.walls)
        self.door.add(b1)
        o1 = Lava.Lava(120, 240, 0, wall_size, self.walls)
        self.lava.add(o1)
        o1 = Oceano.Oceano(220, 240, 0, wall_size, self.walls)
        self.oceano.add(o1)


    def run(self):
        end = False
        while not end:
            dt = self.clock.tick(10)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    end = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    end = True
            # Dividing dt by 1000 we have the time between frames in seconds
            # dt is the time between frames in milliseconds
            # same velocity of the objects in the screen, using the acc * time.
            self.players.update(dt / 1000., self)
            # self.walls.update(dt / 1000.)
            self.screen.fill((200, 200, 200))
            self.draw_grid(32)  # desenha a grid
            self.players.draw(self.screen)
            self.walls.draw(self.screen)
            pygame.display.flip()

    def draw_grid(self, grid_size):
        for x in range(self.width // grid_size):  # saber quantos quadrados cabe na width
            for y in range(self.height // grid_size):  # saber quantos quadrados cabe na height
                rect = pygame.Rect(x * grid_size, y * grid_size,  # a função rect cria os quadrados
                                   grid_size, grid_size)
                pygame.draw.rect(self.screen, "white", rect, 1,)
                # desenha os quadrados de cor branca com distancia de 1 px entre os quadrados


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    pygame.init()
    gm = Game()
    gm.run()