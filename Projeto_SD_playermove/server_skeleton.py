import socket
import logging
from Game_mech import GameMech
import constant
import time

# Está no lado do servidor: Skeleton to user interface (permite ter informação
# de como comunicar com o cliente)


class SkeletonServer:

    def __init__(self, gm_obj: GameMech):
        self.gm = gm_obj
        self.s = socket.socket()
        self.s.bind((constant.ENDERECO_SERVIDOR, constant.PORT))
        self.s.listen()

    def process_x_max(self, s_c):
        # pedir ao gm o tamanho do jogo
        x_max = self.gm.x_max
        # enviar a mensagem com esse valor
        time.sleep(0.01)
        s_c.send(x_max.to_bytes(constant.N_BYTES, byteorder="big", signed=True))

    def process_y_max(self, s_c):
        # pedir ao gm o tamanho do jogo
        y_max = self.gm.y_max
        # enviar a mensagem com esse valor
        time.sleep(0.01)
        s_c.send(y_max.to_bytes(constant.N_BYTES, byteorder="big", signed=True))

    def process_move_player(self, s_c):
        # recebe o número do jogador e direção que quer ir
        dados_recebidos: bytes = s_c.recv(constant.N_BYTES)
        msg = int.from_bytes(dados_recebidos, byteorder="big", signed=True)
        # separa a número do jogador e a direção
        new_player_pos: tuple = self.gm.execute(0, msg)

        # manda a nova posição

        player_pos: str = str(new_player_pos[0]) + " " + str(new_player_pos[1])
        time.sleep(0.01)
        s_c.send(new_player_pos[0].to_bytes(constant.N_BYTES, byteorder="big", signed=True))
        time.sleep(0.01)
        s_c.send(new_player_pos[1].to_bytes(constant.N_BYTES, byteorder="big", signed=True))

    def run(self):
        logging.info("a escutar no porto " + str(constant.PORT))
        socket_client, address = self.s.accept()
        logging.info("o cliente com endereço " + str(address) + " ligou-se!")

        msg: str = ""
        fim = False
        while fim == False:
            dados_recebidos: bytes = socket_client.recv(constant.COMMAND_SIZE)
            msg = dados_recebidos.decode(constant.CODIFICACAO_STR)
            # print(msg)
            # logging.debug("o cliente enviou: \"" + msg + "\"")

            if msg == constant.X_MAX:
                self.process_x_max(socket_client)
            elif msg == constant.Y_MAX:
                self.process_y_max(socket_client)
            elif msg == constant.MOVE_PLAYER:
                self.process_move_player(socket_client)
            elif msg == constant.END:
                fim = True
#            if msg != constante.END:
#                msg = self.eco_obj.eco(msg)
#                socket_client.send(msg.encode(constante.CODIFICACAO_STR))

        socket_client.close()
        logging.info("o cliente com endereço o " + str(address) + " desligou-se!")

        self.s.close()


logging.basicConfig(filename=constant.NOME_FICHEIRO_LOG,
                    level=constant.NIVEL_LOG,
                    format='%(asctime)s (%(levelname)s): %(message)s')