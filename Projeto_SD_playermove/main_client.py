import pygame
from client_stub import StubClient
from Game_client import Game


def main():
    pygame.init()
    stub = StubClient()
    ui = Game(stub)
    ui.run()


main()
