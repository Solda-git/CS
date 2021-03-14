import click
from chat.schatserver import SChatServer
from lib.settings import DEFAULT_IP_ADDRESS, DEFAULT_PORT

@click.command()
# @click.option('--mode', default='broadcast')
@click.option('--addr', default=DEFAULT_IP_ADDRESS, help='IP address listening by server')
@click.option('--port', default=DEFAULT_PORT, help='Listening port')
def run_server(addr, port):
    my_server = SChatServer(addr, port)
    print(f'SChatServer run. Listening address: {("all addresses (by default)", addr)[bool(addr)]}, port: {port}')
    my_server.run()


if __name__ == '__main__':
    
    run_server()
  