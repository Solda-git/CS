import click
from chat.schatclient import SChatClient
from lib.settings import CHAT_SERVER_IP_ADDRESS, DEFAULT_PORT, BROADCAST_MODE, PEER_TO_PEER_MODE
import json
import multiprocessing
from icecream import ic

def run_echo(my_client, conn):
    print("run_echo started")
    my_client.run_in_pipe(conn)


@click.command()
#     mode of client:
#     b - duplex mode (send and receive) - to be done!!!
#     d - broadcast mode (send and receive) - by default
#     s - send mode only
# #     r - receive mode only
# @click.option('--mode', default='b')
# @click.option('--addr', default=CHAT_SERVER_IP_ADDRESS,help='Chat server IP-address')
# @click.option('--port', default=DEFAULT_PORT, help='Chat server port')
@click.option('--name', default='test1')
def run_client(
            name, 
            mode='b', 
            addr=CHAT_SERVER_IP_ADDRESS, 
            port=DEFAULT_PORT
            ):
    print(f"run_client in {mode} mode" )
    my_client = SChatClient(name, mode, addr, port)
    print(f"Client is connected to the address/port: {addr}/{port}")
    my_client.run()

# main function
if __name__ == '__main__':
    try:
        print('running Run_client.main()')
        run_client()
    except Exception as e:
        ic(e)