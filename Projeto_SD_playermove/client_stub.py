import socket
import constant
import time


# Stub do lado do cliente: como comunicar com o servidor...

class StubClient:

    def __init__(self):
        self.s: socket = socket.socket()
        self.s.connect((constant.ENDERECO_SERVIDOR, constant.PORT))

    def dimension_size(self):
        msg = constant.X_MAX
        time.sleep(0.01)
        self.s.send(msg.encode(constant.CODIFICACAO_STR))
        valor = self.s.recv(constant.N_BYTES)
        x_max = int.from_bytes(valor, byteorder="big", signed=True)

        msg = constant.Y_MAX
        time.sleep(0.01)
        self.s.send(msg.encode(constant.CODIFICACAO_STR))
        valor = self.s.recv(constant.N_BYTES)
        y_max = int.from_bytes(valor, byteorder="big", signed=True)
        return x_max, y_max

    def move_player(self, number: int, direction: int) -> tuple:
        self.s.send(constant.MOVE_PLAYER.encode(constant.CODIFICACAO_STR))
        self.s.send(direction.to_bytes(constant.N_BYTES, byteorder="big", signed=True))

        # valor: bytes = self.s.recv(constante.N_BYTES)

        x: bytes = self.s.recv(constant.N_BYTES)
        y: bytes = self.s.recv(constant.N_BYTES)

        return int.from_bytes(x, byteorder="big", signed=True), int.from_bytes(y, byteorder="big", signed=True)