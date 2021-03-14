import click
from chat.schatclient import SChatClient
from lib.settings import CHAT_SERVER_IP_ADDRESS, DEFAULT_PORT
import json
# from lib.routines import log


@click.command()

#     mode of client:
#     d - duplex mode (send and receive) - by default
#     s - send mode only
#     r - receive mode only
@click.option('--mode', default='d')
@click.option('--addr', default=CHAT_SERVER_IP_ADDRESS,help='Chat server IP-address')
@click.option('--port', default=DEFAULT_PORT, help='Chat server port')
def run_client(addr, port):
    print(f"run_client in {mode} mode" )
    my_client = SChatClient(mode, addr, port)
    print(f"Client is connected to the address/port: {addr}/{port}")
    # my_client.send_message(my_client.client_socket,my_client.make_online())
    my_client.run()
    # try:
    #     print(my_client.parse_server_answer(my_client.get_message(my_client.client_socket)))
    # except (ValueError, json.JSONDecodeError):
    #     print("Can't decode server message")




# main function
if __name__ == '__main__':
    run_client()
