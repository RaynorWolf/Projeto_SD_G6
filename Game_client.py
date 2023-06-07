import pygame
import Player_Fire
import Player_Water
import Wall
import Button
import Oceano
import Lava
import Close_door
from Game_mech import GameMech
import client_stub


class Game(object):
    def __init__(self, stub: client_stub.StubClient, grid_size: int = 30):
        # número máximo de quadrados
        dim: tuple = stub.dimension_size()
        self.x_max = dim[0]
        self.y_max = dim[1]
        self.stub = stub

        # configuração do ecrã
        self.width, self.height = self.x_max * grid_size, self.y_max * grid_size
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("WaterGirl and FireBoy")
        self.clock = pygame.time.Clock()

        # criando grupos e Game Mechanics
        self.walls = pygame.sprite.Group()
        self.closedoor = pygame.sprite.Group()
        self.button = pygame.sprite.Group()
        self.lava = pygame.sprite.Group()
        self.oceano = pygame.sprite.Group()

        self.players = pygame.sprite.LayeredDirty()
        self._game_mechanics = GameMech(self.x_max, self.y_max)

        # Grid
        self.grid_size = grid_size

        # Create The Backgound
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill("white")
        self.screen.blit(self.background, (0, 0))
        self.draw_grid("black")
        pygame.display.update()

    # Drawing a square grid
    def draw_grid(self, colour):
        for x in range(0, self.x_max):
            pygame.draw.line(self.screen, colour, (x * self.grid_size, 0), (x * self.grid_size, self.height))
        for y in range(0, self.y_max):
            pygame.draw.line(self.screen, colour, (0, y * self.grid_size), (self.width, y * self.grid_size))

    def create_walls(self, world: dict, wall_size: int):
        # Create Wall (sprites) around world
        for key, value in world.items():
            for item in value:
                if item.__contains__("wall"):
                    Wall.Wall(key[0], key[1], wall_size, self.walls)

    def create_closedoor(self, world: dict, wall_size: int):
        # Create close_door (sprites) around world
        for key, value in world.items():
            for item in value:
                if item.__contains__("closedoor"):
                    Close_door.CloseDoor(key[0], key[1], wall_size, self.closedoor)

    def create_button(self, world: dict, wall_size: int):
        # Create button (sprites) around world
        for key, value in world.items():
            for item in value:
                if item.__contains__("button"):
                    Button.Button(key[0], key[1], wall_size, self.button)

    def create_lava(self, world: dict, wall_size: int):
        # Create lava (sprites) around world
        for key, value in world.items():
            for item in value:
                if item.__contains__("lava"):
                    Lava.Lava(key[0], key[1], wall_size, self.lava)

    def create_oceano(self, world: dict, wall_size: int):
        # Create oceano (sprites) around world
        for key, value in world.items():
            for item in value:
                if item.__contains__("oceano"):
                    Oceano.Oceano(key[0], key[1], wall_size, self.oceano)

    def set_players(self):
        self.pl = self.stub.get_players()
        nr_players = self.stub.get_nr_players()
        self.players = pygame.sprite.LayeredDirty()
        # Test
        print("Game2, Nr. of players:", nr_players)
        print("Game2, Players:", self.pl)
        for nr in range(nr_players):
            if self.pl[str(nr)]:
                # Test
                print("Game2, Player added:", nr)
                p_x, p_y = self.pl[str(nr)][1][0], self.pl[str(nr)][1][1]
                if nr == 0:
                    player = Player_Water.PlayerWater(nr, self.pl[str(nr)][0], p_x, p_y, self.grid_size, self.players)
                    self.players.add(player)
                else:
                    player = Player_Fire.PlayerFire(nr, self.pl[str(nr)][0], p_x, p_y, self.grid_size, self.players)
                    self.players.add(player)

    def run(self):
        # Create Sprites
        nome = input("Por favor, qual é o seu nome?")
        self.stub.add_player(nome)
        self.set_players()

        self.create_walls(self._game_mechanics.get_world(), self.grid_size)
        self.create_button(self._game_mechanics.get_world(), self.grid_size)
        self.create_lava(self._game_mechanics.get_world(), self.grid_size)
        self.create_oceano(self._game_mechanics.get_world(), self.grid_size)
        self.create_closedoor(self._game_mechanics.get_world(), self.grid_size)

        self.walls.draw(self.screen)
        self.closedoor.draw(self.screen)
        self.button.draw(self.screen)
        self.oceano.draw(self.screen)
        self.lava.draw(self.screen)

        end = False
        while not end:
            self.clock.tick(10)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    end = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    end = True

            self.players.update(self.stub)
            self.oceano.draw(self.screen)
            self.lava.draw(self.screen)
            pygame.display.update()

            rects = self.players.draw(self.screen)
            self.draw_grid("black")
            pygame.display.update(rects)
            self.players.clear(self.screen, self.background)
