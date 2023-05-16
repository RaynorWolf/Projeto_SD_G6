import pygame
import client_stub

M_UP = 0
M_RIGHT = 1
M_DOWN = 2
M_LEFT = 3


class PlayerWater(pygame.sprite.DirtySprite):
    def __init__(self, number: int, pos_x: int, pos_y: int, sq_size: int, *groups):
        super().__init__(*groups)
        self.image = pygame.image.load('imagens/agua.png')
        self._number = number
        self._direction = -1

        initial_size = self.image.get_size()
        self.sq_size = sq_size
        size_rate = sq_size / initial_size[0]
        self.new_size = (int(self.image.get_size()[0] * size_rate), int(self.image.get_size()[1] * size_rate))

        self.image = pygame.transform.scale(self.image, self.new_size)
        self.rect = pygame.rect.Rect((pos_x * sq_size, pos_y * sq_size), self.image.get_size())

        # Create an instance of StubClient
        self.stub_client = client_stub.StubClient()

    def get_size(self):
        return self.new_size

    def moveto(self, new_x: int, new_y: int):
        self.rect.x = new_x * self.sq_size
        self.rect.y = new_y * self.sq_size
        # Keep visible
        self.dirty = 1

    def update(self, stub: client_stub.StubClient):
        #        last = self.rect.copy()
        # print("Updating player ", self.name, " with the number ", self.number)
        key = pygame.key.get_pressed()
        new_player_pos = ()
        if key[pygame.K_LEFT]:
            new_player_pos = stub.move_player(self._number, M_LEFT)
        if key[pygame.K_RIGHT]:
            new_player_pos = stub.move_player(self._number, M_RIGHT)
        if key[pygame.K_UP]:
            new_player_pos = stub.move_player(self._number, M_UP)
        if key[pygame.K_DOWN]:
            new_player_pos = stub.move_player(self._number, M_DOWN)

        if new_player_pos:
            self.moveto(new_player_pos[0], new_player_pos[1])
        # Keep visible
        self.dirty = 1
