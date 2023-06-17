import socket
import constant
import json


class StubClient:

    def __init__(self):
        self.s: socket = socket.socket()
        self.s.connect((constant.ENDERECO_SERVIDOR, constant.PORT))

    def get_obstacles(self) -> dict:
        msg = constant.GET_OBST
        self.s.send(msg.encode(constant.CODIFICACAO_STR))
        data: bytes = self.s.recv(constant.N_BYTES)
        dim = int.from_bytes(data, byteorder='big', signed=True)
        rec: bytes = self.s.recv(dim)
        obst = json.loads(rec)
        return obst

    def get_nr_obstacles(self):
        msg = constant.NR_OBST
        self.s.send(msg.encode(constant.CODIFICACAO_STR))
        data: bytes = self.s.recv(constant.N_BYTES)
        nr = int.from_bytes(data, byteorder='big', signed=True)
        return nr

    def get_players(self) -> dict:
        msg = constant.GET_PLAYER
        self.s.send(msg.encode(constant.CODIFICACAO_STR))
        data: bytes = self.s.recv(constant.N_BYTES)
        dim = int.from_bytes(data, byteorder='big', signed=True)
        rec: bytes = self.s.recv(dim)
        players = json.loads(rec)
        return players

    def get_nr_players(self):
        msg = constant.NR_PLAYERS
        self.s.send(msg.encode(constant.CODIFICACAO_STR))
        data: bytes = self.s.recv(constant.N_BYTES)
        nr = int.from_bytes(data, byteorder='big', signed=True)
        return nr

    def add_player(self, name: str, x: int, y: int) -> int:
        msg = constant.ADD_PLAYER
        self.s.send(msg.encode(constant.STR_COD))
        # Send the length of the name and the name
        sz = len(name)
        self.s.send(sz.to_bytes(constant.N_BYTES, byteorder="big", signed=True))
        self.s.send(name.encode(constant.STR_COD))
        self.s.send(x.to_bytes(constant.N_BYTES, byteorder="big", signed=True))
        self.s.send(y.to_bytes(constant.N_BYTES, byteorder="big", signed=True))
        rec: bytes = self.s.recv(constant.N_BYTES)
        number = int.from_bytes(rec, byteorder='big', signed=True)
        return number

    def update(self, type: str, number: int) -> tuple:
        #pass
        msg = constant.UPDATE
        #Atualizado:
        self.s.send(msg.encode(constant.STR_COD))
        self.s.send(number.to_bytes(constant.N_BYTES, byteorder="big", signed=True))
        data: bytes = self.s.recv(constant.N_BYTES)
        dim = int.from_bytes(data, byteorder='big', signed=True)
        rec: bytes = self.s.recv(dim)
        tuple = json.loads(rec)
        # Imprimir o resultado (teste)
        print("O resultado do update do jogador nr. ", number)
        return tuple

    def dimension_size(self) -> tuple:
        msg = constant.X_MAX
        self.s.send(msg.encode(constant.CODIFICACAO_STR))
        data: bytes = self.s.recv(constant.N_BYTES)
        x_max = int.from_bytes(data, byteorder='big', signed=True)
        msg = constant.Y_MAX
        self.s.send(msg.encode(constant.CODIFICACAO_STR))
        data: bytes = self.s.recv(constant.N_BYTES)
        y_max = int.from_bytes(data, byteorder='big', signed=True)
        return x_max, y_max

    # pos = gm.execute(M_UP, "player", self.number)
    def execute(self, mov: int, type: str, player: int) -> tuple:
        msg = constant.PLAYER_MOV
        self.s.send(msg.encode(constant.STR_COD))
        self.s.send(mov.to_bytes(constant.N_BYTES, byteorder="big", signed=True))
        self.s.send(player.to_bytes(constant.N_BYTES, byteorder="big", signed=True))
        data: bytes = self.s.recv(constant.N_BYTES)
        dim = int.from_bytes(data, byteorder='big', signed=True)
        rec: bytes = self.s.recv(dim)
        tuple = json.loads(rec)
        return tuple

    def start_game(self) -> None:
        """
        Pede ao servidor para começar o jogo. O servidor iniciará quando o número de jogadores for 2
        :return:
        """
        msg = constant.START_GAME
        # Test
        print("Mensagem: Eu desejo começar o jogo ...")
        self.s.send(msg.encode(constant.STR_COD))
        rec: bytes = self.s.recv(constant.N_BYTES)
        res = rec.decode(constant.STR_COD)
        # Test
        print("Começando o jogo... :", res)
        #return res
