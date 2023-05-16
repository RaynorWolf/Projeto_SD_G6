import pygame
import client_stub
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3


class PlayerFire(pygame.sprite.DirtySprite):
    def __init__(self, number: int, pos_x: int, pos_y: int, sq_size: int, *groups):
        super().__init__(*groups)
        self.image = pygame.image.load('imagens/fogo.png')
        self._number = number
        self._direction = -1

        initial_size = self.image.get_size()
        self.sq_size = sq_size
        size_rate = sq_size / initial_size[0]
        self.new_size = (int(self.image.get_size()[0] * size_rate), int(self.image.get_size()[1] * size_rate))

        self.image = pygame.transform.scale(self.image, self.new_size)
        self.rect = pygame.rect.Rect((pos_x * sq_size, pos_y * sq_size), self.image.get_size())

    def get_size(self):
        return self.new_size

    def moveto(self, new_x: int, new_y: int):
        self.rect.x = new_x * self.sq_size
        self.rect.y = new_y * self.sq_size
        # Keep visible
        self.dirty = 1

    def update(self, game: object, stub: client_stub.StubClient):
        key = pygame.key.get_pressed()
        direcao: int = -1
        if key[pygame.K_LEFT]:
            direcao = LEFT
        if key[pygame.K_RIGHT]:
            direcao = RIGHT
        if key[pygame.K_UP]:
            direcao = UP
        if key[pygame.K_DOWN]:
            direcao = DOWN
        """
        if direcao != -1:
            new_pos = gm.execute(self._number, direcao)
            self._direction = direcao
            if new_pos != -1:
                self.moveto(new_pos[0], new_pos[1])
        """
        # Keep visible
        self.dirty = 1
