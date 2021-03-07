import click
from chat.schatclient import SChatClient
from lib.settings import CHAT_SERVER_IP_ADDRESS, DEFAULT_PORT
import json
# from lib.routines import log


@click.command()
@click.option('--addr', default=CHAT_SERVER_IP_ADDRESS,help='Chat server IP-address')
@click.option('--port', default=DEFAULT_PORT, help='Chat server port')
def run_client(addr, port):
    print("run_client")
    my_client = SChatClient(addr, port)
    print(f"Client is connected to the address/port: {addr}/{port}")
    my_client.send_message(my_client.client_socket,my_client.make_online())
    # my_client.run()
    try:
        print(my_client.parse_server_answer(my_client.get_message(my_client.client_socket)))
    except (ValueError, json.JSONDecodeError):
        print("Can't decode server message")

# class Test():
#     @log
#     def __init__(self, mes):
#         self._message = mes
    
#     @log
#     def fn(self):
#         print(self._message)


# main function
if __name__ == '__main__':
#    t = Test('test')
#    t.fn()
    # @log
    # def test():
    #      print('test function')   


    # test()

    run_client()
