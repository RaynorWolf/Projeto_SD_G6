import time
# Constantes
M_UP = 0
M_RIGHT = 1
M_DOWN = 2
M_LEFT = 3
TIME_STEP = 200


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
        self.obstacles = dict()

        self.x_max = nr_max_x
        self.y_max = nr_max_y

        self.nr_players = 0
        self.nr_walls = 0
        self.nr_button = 0
        self.nr_door = 0
        self.nr_closedoor = 0
        self.nr_oceano = 0
        self.nr_lava = 0
        self.nr_obstacles = 0

        for x in range(nr_max_x):
            for y in range(nr_max_y):
                self.world[(x, y)] = []
        # Criar paredes à volta do mundo
        for x in range(0, self.x_max):
            for y in range(0, self.y_max):
                if x in (0, self.x_max - 1) or y in (0, self.y_max - 1):
                    self.walls[self.nr_walls] = ["wall", (x, y)]
                    self.world[(x, y)].append(["obstacle", "wall", self.nr_walls])
                    self.nr_walls += 1

        # Desenha o mapa
        self.world[(2, 2)].append(["obstacle", "closedoor", self.nr_closedoor])
        self.nr_closedoor += 1
        self.world[(10, 5)].append(["obstacle", "closedoor", self.nr_closedoor])
        self.nr_closedoor += 1

        self.world[(1, 2)].append(["obstacle", "wall", self.nr_walls])
        self.nr_walls += 1
        self.world[(3, 2)].append(["obstacle", "wall", self.nr_walls])
        self.nr_walls += 1
        self.world[(3, 3)].append(["obstacle", "wall", self.nr_walls])
        self.nr_walls += 1
        self.world[(3, 4)].append(["obstacle", "wall", self.nr_walls])
        self.nr_walls += 1
        self.world[(2, 4)].append(["obstacle", "wall", self.nr_walls])
        self.nr_walls += 1
        self.world[(1, 4)].append(["obstacle", "wall", self.nr_walls])
        self.nr_walls += 1
        self.world[(9, 5)].append(["obstacle", "wall", self.nr_walls])
        self.nr_walls += 1
        self.world[(11, 5)].append(["obstacle", "wall", self.nr_walls])
        self.nr_walls += 1

        self.world[(5, 7)].append(
            ["obstacle", "button", self.nr_button, (2, 2)])
        self.nr_button += 1
        self.world[(1, 3)].append(
            ["obstacle", "button", self.nr_button, (10, 5)])
        self.nr_button += 1

        self.world[(7, 7)].append(["obstacle", "lava", self.nr_lava])
        self.nr_lava += 1

        self.world[(8, 8)].append(["obstacle", "oceano", self.nr_oceano])
        self.nr_oceano += 1

    def execute(self, move: int, type: str, nr_player: int) -> tuple:
        if type == "player":
            name, (pos_x, pos_y), tick = self.players[nr_player]
            new_pos_x, new_pos_y = pos_x, pos_y

            if move == M_LEFT:
                new_pos_x = pos_x - 1
            elif move == M_RIGHT:
                new_pos_x = pos_x + 1
            elif move == M_UP:
                new_pos_y = pos_y - 1
            elif move == M_DOWN:
                new_pos_y = pos_y + 1

            if self.is_obstacle('wall', new_pos_x, new_pos_y):
                new_pos_x, new_pos_y = pos_x, pos_y

            next_position = (new_pos_x, new_pos_y)

            for item in self.world[next_position]:
                if "obstacle" in item:
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
                    return pos_x, pos_y

            next_tick = int(time.time() * 1000)
            if (next_tick - tick) > TIME_STEP:
                tick = next_tick
                self.players[nr_player] = [name, (new_pos_x, new_pos_y), tick]
                self.world[(pos_x, pos_y)].remove(['player', name, nr_player, (pos_x, pos_y)])
                self.world[(new_pos_x, new_pos_y)].append(['player', name, nr_player, (new_pos_x, new_pos_y)])
            else:
                new_pos_x, new_pos_y = pos_x, pos_y

            return new_pos_x, new_pos_y

    def print_world(self):
        for x in range(0, self.x_max):
            for y in range(0, self.y_max):
                print("(", x, ",", y, ")=", self.world[x, y])

    def get_world(self) -> dict:
        return self.world

    def get_players(self) -> dict:
        return self.players

    def nr_players(self) -> int:
        return self.nr_players

    def is_obstacle(self, type, x, y) -> bool:
        """
        Test if there is an obstacle of type in x,y
        :param type:
        :param x:
        :param y:
        :return:
        """
        for e in self.world[(x, y)]:
            if e[0] == 'obstacle' and e[1] == type:
                return True
        return False

    def add_wall(self, x: int, y: int):
        """
        Adiciona uma nova "parede" ao mundo
        :param x: Coordenada do eixo "X"
        :param y: Coordenada do eixo "Y"
        """
        if self.world.keys().__contains__((x, y)):
            self.nr_walls += 1
            self.world[(x, y)].append(["obstacle", "wall", self.nr_walls])

    def add_button(self, x: int, y: int, c_door: list):
        """
        Adiciona um novo "botão" ao mundo
        :param x: Coordenada do eixo "X"
        :param y: Coordenada do eixo "Y"
        :param c_door: Coordenada da porta associada
        """
        if self.world.keys().__contains__((x, y)):
            self.nr_button += 1
            self.world[(x, y)].append(
                ["obstacle", "button", self.button, c_door])

    def add_closedoor(self, x: int, y: int):
        """
        Adiciona um novo "botão" ao mundo
        :param x: Coordenada do eixo "X"
        :param y: Coordenada do eixo "Y"
        """
        if self.world.keys().__contains__((x, y)):
            self.nr_closedoor += 1
            self.world[(x, y)].append(
                ["obstacle", "close_door", self.closedoor])

    def add_oceano(self, x: int, y: int):
        """
        Adiciona um novo "botão" ao mundo
        :param x: Coordenada do eixo "X"
        :param y: Coordenada do eixo "Y"
        """
        if self.world.keys().__contains__((x, y)):
            self.nr_oceano += 1
            self.world[(x, y)].append(["obstacle", "oceano", self.oceano])

    def add_lava(self, x: int, y: int):
        """
        Adiciona um novo "botão" ao mundo
        :param x: Coordenada do eixo "X"
        :param y: Coordenada do eixo "Y"
        """
        if self.world.keys().__contains__((x, y)):
            self.nr_lava += 1
            self.world[(x, y)].append(["obstacle", "lava", self.lava])

    def add_player(self, name, x_pos: int, y_pos: int) -> int:
        nr_player = self.nr_players
        tick = int(1000 * time.time())

        self.players[nr_player] = [name, (x_pos, y_pos), tick]
        self.world[(x_pos, y_pos)].append(
            ['player', name, nr_player, (x_pos, y_pos)])
        self.nr_players += 1
        return nr_player

    def add_obstacle(self, obstacle_type: str, x_pos: int, y_pos: int) -> bool:
        nr_obstacle = self.nr_obstacles
        self.obstacles[nr_obstacle] = [obstacle_type, (x_pos, y_pos)]
        self.world[(x_pos, y_pos)].append(
            ['obstacle', obstacle_type, nr_obstacle, (x_pos, y_pos)])
        self.nr_obstacles += 1
        return True

    def create_world(self):
        for x in range(0, self.x_max):
            for y in range(0, self.y_max):
                if x in (0, self.x_max - 1) or y in (0, self.y_max - 1):
                    self.add_obstacle("wall", x, y)
