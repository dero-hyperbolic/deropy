import click

from deropy.commands.configure import configure
from deropy.commands.generate import generate
from deropy.commands.deploy import deploy
from deropy.commands.simulate import simulate


@click.group('deropy')
@click.version_option()
def deropy():
    pass


deropy.add_command(generate)
deropy.add_command(deploy)
deropy.add_command(configure)
deropy.add_command(simulate)

if __name__ == '__main__':
    deropy()
