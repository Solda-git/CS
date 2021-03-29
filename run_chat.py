import click
import subprocess

@click.command()
@click.option('--quantity', default=2, help='Number of clients to run')
def run_chat(quantity):
    for p in range(int(quantity)):
        subprocess.Popen(['gnome-terminal', '--', './run_clients.sh'])
        print(p)
        print(type(p))

if __name__ == '__main__':
    run_chat()