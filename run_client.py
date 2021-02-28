import click
from chat.schatclient import SChatClient
from lib.settings import CHAT_SERVER_IP_ADDRESS, DEFAULT_PORT
import json


@click.command()
@click.option('--addr', default=CHAT_SERVER_IP_ADDRESS,help='Chat server IP-address')
@click.option('--port', default=DEFAULT_PORT, help='Chat server port')
def run_client(addr, port):
    print("run_client")
    my_client = SChatClient(addr, port)
    print(f"Client is connected to the address/port: {addr}/{port}")
    my_client.send_message(my_client.client_socket,my_client.make_online())
    try:
        print(my_client.parse_server_answer(my_client.get_message(my_client.client_socket)))
    except (ValueError, json.JSONDecodeError):
        print("Can't decode server message")

# main function
if __name__ == '__main__':
   run_client()
