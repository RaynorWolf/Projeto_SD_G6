from threading import Thread
from Game_mech import GameMech
import constant
import json
import logging


class ClientSession(Thread):
    """Maintains a session with the client"""

    def __init__(self, socket_client: int,  game_mech: GameMech):
        """
        Constructs a thread to hold a session with the client
        :param shared_state: The server's state shared by threads
        :param client_socket: The client's socket
        """
        Thread.__init__(self)
        # self._shared = shr
        self.socket_client = socket_client
        self.gm = game_mech

    def process_x_max(self,s_c):
        x = self.gm.x_max
        s_c.send(x.to_bytes(constant.N_BYTES,byteorder= "big", signed=True))

    def process_y_max(self,s_c):
        y = self.gm.y_max
        s_c.send(y.to_bytes(constant.N_BYTES,byteorder= "big", signed=True))

    def process_add_player(self, s_c):
        data_rcv: bytes = s_c.recv(constant.MSG_SIZE)
        name = data_rcv.decode(constant.CODIFICACAO_STR)
        number = self.gm.add_player(name,1,1)
        s_c.send(number.to_bytes(constant.N_BYTES,byteorder= "big", signed=True))

    def process_get_obst(self, s_c):
        ob = self.gm.obstacles
        msg = json.dumps(ob)
        dim = len(msg)
        s_c.send(dim.to_bytes(constant.N_BYTES,byteorder= "big", signed=True))
        s_c.send(msg.encode(constant.CODIFICACAO_STR))

    def process_get_nr_obst(self, s_c):
        nr_ob = self.gm.nr_obstacles
        s_c.send(nr_ob.to_bytes(constant.N_BYTES,byteorder= "big", signed=True))

    def process_get_players(self, s_c):
        pl = self.gm.players
        msg = json.dumps(pl)
        dim = len(msg)
        s_c.send(dim.to_bytes(constant.N_BYTES,byteorder= "big", signed=True))
        s_c.send(msg.encode(constant.CODIFICACAO_STR))

    def process_get_nr_players(self, s_c):
        nr_pl = self.gm.nr_players
        s_c.send(nr_pl.to_bytes(constant.N_BYTES,byteorder= "big", signed=True))

    def process_player_mov(self, s_c):
        data: bytes = s_c.recv(constant.N_BYTES)
        mov = int.from_bytes(data, byteorder='big', signed=True)
        data: bytes = s_c.recv(constant.N_BYTES)
        nr_player = int.from_bytes(data, byteorder='big', signed=True)
        pos = self.gm.execute(mov,"player",nr_player)
        msg = json.dumps(pos)
        dim = len(msg)
        s_c.send(dim.to_bytes(constant.N_BYTES,byteorder= "big", signed=True))
        s_c.send(msg.encode(constant.CODIFICACAO_STR))

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
        elif data_str == constant.MOVE_PLAYER:
            self.process_player_mov(socket_client)
        elif data_str == constant.END:
            lr = True
        return lr

    def run(self):
        """Maintains a session with the client, following the established protocol"""
        #logging.debug("Client " + str(client.peer_addr) + " just connected")
        last_request = False
        while not last_request:
            last_request = self.dispatch_request(self.socket_client)
        logging.debug("Client " + str(self.socket_client.peer_addr) + " disconnected")
        # Sared stuff (TODO)
        #self._shared_state.remove_client(self._client_connection)
        #self._shared_state.concurrent_clients.release()
