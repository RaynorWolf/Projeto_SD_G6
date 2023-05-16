# Constantes
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3


class GameMech:
    def __init__(self, nr_max_x=20, nr_max_y=20):
        self.direcao = 0
        self.world = dict()
        self.players = dict()
        self.walls = dict()
        self.button = dict()
        self.closedoor = dict()
        self.oceano = dict()
        self.lava = dict()
        self.closedoor = dict()

        self.x_max = nr_max_x
        self.y_max = nr_max_y

        self.nr_walls = 0
        self.nr_button = 0
        self.nr_door = 0
        self.nr_closedoor = 0
        self.nr_oceano = 0
        self.nr_lava = 0

        for x in range(nr_max_x):
            for y in range(nr_max_y):
                self.world[(x, y)] = []
        # Criar paredes à volta do mundo
        for x in range(0, self.x_max):
            for y in range(0, self.y_max):
                if x in (0, self.x_max - 1) or y in (0, self.y_max - 1):
                    self.walls[self.nr_walls] = ["wall", (x, y)]
                    self.world[(x, y)].append(["obst", "wall", self.nr_walls])
                    self.nr_walls += 1

        # Desenha o mapa
        self.world[(2, 2)].append(["obst", "closedoor", self.nr_closedoor])
        self.nr_closedoor += 1
        self.world[(10, 5)].append(["obst", "closedoor", self.nr_closedoor])
        self.nr_closedoor += 1

        self.world[(1, 2)].append(["obst", "wall", self.nr_walls])
        self.nr_walls += 1
        self.world[(3, 2)].append(["obst", "wall", self.nr_walls])
        self.nr_walls += 1
        self.world[(3, 3)].append(["obst", "wall", self.nr_walls])
        self.nr_walls += 1
        self.world[(3, 4)].append(["obst", "wall", self.nr_walls])
        self.nr_walls += 1
        self.world[(2, 4)].append(["obst", "wall", self.nr_walls])
        self.nr_walls += 1
        self.world[(1, 4)].append(["obst", "wall", self.nr_walls])
        self.nr_walls += 1
        self.world[(9, 5)].append(["obst", "wall", self.nr_walls])
        self.nr_walls += 1
        self.world[(11, 5)].append(["obst", "wall", self.nr_walls])
        self.nr_walls += 1

        self.world[(5, 7)].append(["obst", "button", self.nr_button, (2, 2)])
        self.nr_button += 1
        self.world[(1, 3)].append(["obst", "button", self.nr_button, (10, 5)])
        self.nr_button += 1

        self.world[(7, 7)].append(["obst", "lava", self.nr_lava])
        self.nr_lava += 1

        self.world[(8, 8)].append(["obst", "oceano", self.nr_oceano])
        self.nr_oceano += 1

        # Criar jogador
        self.players[1] = ["fogo", (1, 1)]
        self.world[(1, 1)].append(["player", "fogo", 0])
        self.players[0] = ["agua", (1, 1)]
        self.world[(1, 1)].append(["player", "agua", 1])

    def execute(self, nr_player: int, direction: int) -> tuple:
        # if the direction is not valid, exit
        self.direcao = direction

        # check if the player exists
        player = None
        for value in self.world.values():
            for item in value:
                if "player" in item and item[2] == nr_player:
                    player = item

        # checks the current position of the player
        current_position = None
        for pos, value in self.world.items():
            if player in value:
                current_position = pos

        if self.direcao not in range(4):
            return current_position
        # if there's no player or it doesn't match the nr_player, exit
        if not current_position:
            return current_position

        # calculate the new position based on the direction
        x, y = current_position
        if self.direcao == UP:
            y -= 1
        elif self.direcao == RIGHT:
            x += 1
        elif self.direcao == DOWN:
            y += 1
        elif self.direcao == LEFT:
            x -= 1
        next_position = (x, y)

        # check if the position is reachable
        if next_position not in self.world:
            return current_position

        # check for obstacles in the way
        for item in self.world[next_position]:
            if "obst" in item:
                if item[1] == "lava" and nr_player == 1:
                    continue
                if item[1] == "oceano" and nr_player == 0:
                    continue
                if item[1] == "door":
                    continue
                if item[1] == "button":
                    num = item[3]
                    print(num)
                    self.world[num] = []
                return current_position

        # Move the player on the field
        self.world[current_position].remove(player)
        self.world[next_position].append(player)

        return next_position

    def print_world(self):
        for x in range(0, self.x_max):
            for y in range(0, self.y_max):
                print("(", x, ",", y, ")=", self.world[x, y])

    def get_world(self) -> dict:
        return self.world

    def add_wall(self, x: int, y: int):
        """
        Adiciona uma nova "parede" ao mundo
        :param x: Coordenada do eixo "X"
        :param y: Coordenada do eixo "Y"
        """
        if self.world.keys().__contains__((x, y)):
            self.nr_walls += 1
            self.world[(x, y)].append(["obst", "wall", self.nr_walls])

    def add_button(self, x: int, y: int, c_door: list):
        """
        Adiciona um novo "botão" ao mundo
        :param x: Coordenada do eixo "X"
        :param y: Coordenada do eixo "Y"
        :param c_door: Coordenada da porta associada
        """
        if self.world.keys().__contains__((x, y)):
            self.nr_button += 1
            self.world[(x, y)].append(["obst", "button", self.button, c_door])

    def add_closedoor(self, x: int, y: int):
        """
        Adiciona um novo "botão" ao mundo
        :param x: Coordenada do eixo "X"
        :param y: Coordenada do eixo "Y"
        """
        if self.world.keys().__contains__((x, y)):
            self.nr_closedoor += 1
            self.world[(x, y)].append(["obst", "close_door", self.closedoor])

    def add_oceano(self, x: int, y: int):
        """
        Adiciona um novo "botão" ao mundo
        :param x: Coordenada do eixo "X"
        :param y: Coordenada do eixo "Y"
        """
        if self.world.keys().__contains__((x, y)):
            self.nr_oceano += 1
            self.world[(x, y)].append(["obst", "oceano", self.oceano])

    def add_lava(self, x: int, y: int):
        """
        Adiciona um novo "botão" ao mundo
        :param x: Coordenada do eixo "X"
        :param y: Coordenada do eixo "Y"
        """
        if self.world.keys().__contains__((x, y)):
            self.nr_lava += 1
            self.world[(x, y)].append(["obst", "lava", self.lava])


# Test
if __name__ == '__main__':
    gm = GameMech(20, 20)
    gm.print_world()
