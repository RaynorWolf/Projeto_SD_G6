import socket
import logging
import Game_mech
import constant
import client_session_management
from typing import Union
import shared


class SkeletonServer:

    def __init__(self, gm: Game_mech.GameMech):
        self.gm = gm
        self.s = socket.socket()
        self.s.bind((constant.ENDERECO_SERVIDOR, constant.PORT))
        self.s.listen()
        self.s.settimeout(constant.ACCEPT_TIMEOUT)
        self.keep_running = True
        self.shared = shared.Shared()

    def accept(self) -> Union['Socket', None]:
        """
        Nova definição do 'accept()' para providenciar um novo retorno no evento de um 'timeout'
        """
        try:
            client_connection, address = self.s.accept()
            logging.info("o cliente com endereço " + str(address) + " ligou-se!")

            return client_connection
        except socket.timeout:
            return None

    def run(self):
        logging.info("a escutar no porto " + str(constant.PORT))
        while self.keep_running:
            socket_client = self.accept()
            if socket_client is not None:
                # Add client
                # self._state.add_client(socket_client)
                client_session_management.ClientSession(socket_client, self.shared, self.gm).start()

        self.s.close()


logging.basicConfig(filename=constant.NOME_FICHEIRO_LOG,
                    level=constant.NIVEL_LOG,
                    format='%(asctime)s (%(levelname)s): %(message)s')