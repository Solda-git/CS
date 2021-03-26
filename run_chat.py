from lib.settings import CHAT_SERVER_IP_ADDRESS, DEFAULT_IP_ADDRESS, DEFAULT_PORT
from chat.schatclient import SChatClient
from chat.schatserver import SChatServer
from subprocess import Popen
import click
import time
# global processes 
# processes = []

# @click.command()
# @click.option('--quantity', default=2, help='Number of clients to run')
# @click.option('--caddr', default=CHAT_SERVER_IP_ADDRESS,help='Chat server IP-address for client')
# @click.option('--saddr', default=DEFAULT_IP_ADDRESS,help='IP-address for server')
# @click.option('--port', default=DEFAULT_PORT, help='Chat server port')
# def run_chat(quantity, caddr, saddr, port):
#     global processes 
#     print('starting server  process:')
    # server_p = Popen(['python', 'run_server.py'])

#     # server_p = Popen(['python', 'run_server.py', '--addr', saddr])
#     # server_p = Popen(['python', 'run_server.py', '--addr', saddr, '--port', port])
#     # my_server = SChatServer(saddr, port)
#     # print(f'SChatServer run. Listening address: {("all addresses (by default)", saddr)[bool(saddr)]}, port: {port}')
#     # my_server.run()



#     print('starting two  clients: each in own process')
#     if quantity == 2:
#         p1 = Popen(['python3', 'run_client.py', '--mode', 'r', '--addr', caddr, '--port', port])
#         p2 = Popen(['python3', 'run_client.py', '--mode', 's', '--addr', caddr, '--port', port])
#         for p in (p1, p2):
#             processes.append(p)   

    # else:
    #     for i in range(quantity):
    #         pass
global processes
processes =[]

@click.command()
@click.option('--q', default=2)
def run_chat(q):
    global processes
    print(f'running run_chat({q})')
    args_c1 = ['python', 'run_client.py', '--mode', 'r']
    args_c2 = ['python', 'run_client.py', '--mode', 's']
    p1 = Popen(args_c1)
    processes.append(p1)
    time.sleep(0.1)
    p2 = Popen(args_c2)
    processes.append(p2)



# main function
if __name__ == '__main__':
    # global processes
    try:
        print('running main()')
        run_chat()
    finally:
        # print(f'finally: {processes}')
        # for p in processes:
        #     p.kill()
        pass
