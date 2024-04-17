import click

from deropy.commands.configure import configure
from deropy.commands.generate import generate
from deropy.commands.deploy import deploy
from deropy.commands.transpile import transpile


@click.group('deropy')
@click.version_option()
def deropy():
    pass

deropy.add_command(generate)
deropy.add_command(deploy)
deropy.add_command(transpile)
deropy.add_command(configure)

if __name__ == '__main__':
    deropy()