from threading import Thread
from Game_mech import GameMech
import constant
import json
import logging
import shared


class ClientSession(Thread):
    """Mantêm a sessão com o cliente"""

    def __init__(self, socket_client: int, shr: shared.Shared, game_mech: GameMech):
        Thread.__init__(self)
        self._shared = shr
        self.socket_client = socket_client
        self.gm = game_mech

    def process_x_max(self, s_c):
        x = self.gm.x_max
        s_c.send(x.to_bytes(constant.N_BYTES, byteorder="big", signed=True))

    def process_y_max(self, s_c):
        y = self.gm.y_max
        s_c.send(y.to_bytes(constant.N_BYTES, byteorder="big", signed=True))

    def process_add_player(self, s_c):
        logging.debug("O cliente define o jogador")
        ln: bytes = s_c.recv(constant.N_BYTES)
        nm: bytes = s_c.recv(int.from_bytes(ln, byteorder='big', signed=True))
        name = nm.decode(constant.STR_COD)
        xb: bytes = s_c.recv(constant.N_BYTES)
        x = int.from_bytes(xb, byteorder='big', signed=True)
        yb: bytes = s_c.recv(constant.N_BYTES)
        y = int.from_bytes(yb, byteorder='big', signed=True)
        # Testing for player name and its position
        print("O nome do jogador:", name)
        print("Posição do jogador (x,y)=(", x, ",", y, ")")
        number = self.gm.add_player(name, x, y)
        self._shared.add_client(s_c)
        self._shared.control_nr_clients()
        s_c.send(number.to_bytes(constant.N_BYTES, byteorder="big", signed=True))

    def process_get_obst(self, s_c):
        ob = self.gm.obstacles
        msg = json.dumps(ob)
        dim = len(msg)
        s_c.send(dim.to_bytes(constant.N_BYTES, byteorder="big", signed=True))
        s_c.send(msg.encode(constant.CODIFICACAO_STR))

    def process_get_nr_obst(self, s_c):
        nr_ob = self.gm.nr_obstacles
        s_c.send(nr_ob.to_bytes(constant.N_BYTES, byteorder="big", signed=True))

    def process_get_players(self, s_c):
        pl = self.gm.players
        msg = json.dumps(pl)
        dim = len(msg)
        print("Dimensão da mensagem do 'get players':", dim)
        print("Mensagem:", msg)
        s_c.send(dim.to_bytes(constant.N_BYTES, byteorder="big", signed=True))
        s_c.send(msg.encode(constant.CODIFICACAO_STR))

    def process_get_nr_players(self, s_c):
        nr_pl = self.gm.nr_players
        s_c.send(nr_pl.to_bytes(constant.N_BYTES, byteorder="big", signed=True))

    def process_player_mov(self, s_c):
        data: bytes = s_c.recv(constant.N_BYTES)
        mov = int.from_bytes(data, byteorder='big', signed=True)
        data: bytes = s_c.recv(constant.N_BYTES)
        nr_player = int.from_bytes(data, byteorder='big', signed=True)
        pos = self.gm.execute(mov, "player", nr_player)
        msg = json.dumps(pos)
        dim = len(msg)
        s_c.send(dim.to_bytes(constant.N_BYTES, byteorder="big", signed=True))
        s_c.send(msg.encode(constant.CODIFICACAO_STR))

    def process_start_game(self, s_c):
        logging.debug("O client pretende inciar o jogo")
        self._shared._clients_control.acquire()
        logging.debug("O client vai iniciar o jogo")

        # Returning 'yes'
        value = constant.TRUE
        s_c.send(value.encode(constant.STR_COD))

    def process_update(self, s_c):
        #logging.debug("O client pede um update")
        pl: bytes = s_c.recv(constant.N_BYTES)
        number = int.from_bytes(pl, byteorder='big', signed=True)
        #Atualizar
        #pos = self.gm.get_player_pos("player", number)
        pos = self.gm.players[number][1]
        msg = json.dumps(pos)
        # Get the size of serialized data
        size = len(msg)
        s_c.send(size.to_bytes(constant.N_BYTES, byteorder="big", signed=True))
        # Test
        #  print("New position sent to client:",msg)
        s_c.send(msg.encode(constant.STR_COD))

    def dispatch_request(self, socket_client) -> bool:
        """
        :return:
        """
        lr = False
        data_rcv: bytes = socket_client.recv(constant.MSG_SIZE)
        data_str = data_rcv.decode(constant.CODIFICACAO_STR)
        # logging.debug("o cliente enviou: \"" + data_str + "\"")
        if data_str == constant.X_MAX:
            self.process_x_max(socket_client)
        elif data_str == constant.Y_MAX:
            self.process_y_max(socket_client)
        elif data_str == constant.ADD_PLAYER:
            self.process_add_player(socket_client)
        elif data_str == constant.GET_PLAYER:
            self.process_get_players(socket_client)
        elif data_str == constant.NR_PLAYERS:
            self.process_get_nr_players(socket_client)
        elif data_str == constant.GET_OBST:
            self.process_get_obst(socket_client)
        elif data_str == constant.NR_OBST:
            self.process_get_nr_obst(socket_client)
        elif data_str == constant.PLAYER_MOV:
            self.process_player_mov(socket_client)
        # Start the game....
        elif data_str == constant.START_GAME:
            self.process_start_game(socket_client)
        elif data_str == constant.UPDATE:
            self.process_update(socket_client)
        elif data_str == constant.END:
            lr = True
        return lr

    def run(self):
        """Mantêm a sessão com um cliente conforme o protocolo estabelecido"""
        # logging.debug("Client " + str(client.peer_addr) + " just connected")
        last_request = False
        while not last_request:
            last_request = self.dispatch_request(self.socket_client)
        logging.debug(
            "Client " + str(self.socket_client.peer_addr) + " disconnected")
        # Sared stuff (TODO)
        # self._shared_state.remove_client(self._client_connection)
        # self._shared_state.concurrent_clients.release()
