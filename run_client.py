import click
from chat.schatclient import SChatClient
from lib.settings import CHAT_SERVER_IP_ADDRESS, DEFAULT_PORT, BROADCAST_MODE, PEER_TO_PEER_MODE
import json
import multiprocessing

def run_echo(my_client, conn):
    print("run_echo started")
    my_client.run_in_pipe(conn)



@click.command()
#     mode of client:
#     d - duplex mode (send and receive) - by default
#     s - send mode only
#     r - receive mode only
@click.option('--mode', default='d')
@click.option('--addr', default=CHAT_SERVER_IP_ADDRESS,help='Chat server IP-address')
@click.option('--port', default=DEFAULT_PORT, help='Chat server port')
def run_client(mode, addr, port):
    print(f"run_client in {mode} mode" )
    if mode != PEER_TO_PEER_MODE:
        my_client = SChatClient(mode, addr, port)
        print(f"Client is connected to the address/port: {addr}/{port}")
        my_client.run()
    else: #lesson 8: peer-to-peer mode runs 2 client in different processes

        my_client = SChatClient(BROADCAST_MODE, addr, port)  # main client
        echo_client = SChatClient(mode, addr, port)         # echo client 
        parent_conn, child_conn = multiprocessing.Pipe()
        
        client_proc = multiprocessing.Process(target=run_echo, args=(echo_client, child_conn))
        client_proc.start()
        my_client.run(parent_conn)
        client_proc.join()
        child_conn.close() 
        parent_conn.close()






# main function
if __name__ == '__main__':
    run_client()
