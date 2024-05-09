import click

from deropy.logger import init_logger, change_logger_level
from deropy.commands.configure import configure
from deropy.commands.generate import generate
from deropy.commands.deploy import deploy
from deropy.commands.simulate import simulate
from deropy.commands.transpile import transpile

init_logger('deropy')

@click.group('deropy')
@click.version_option()
@click.option('-v', '--verbose', count=True)
def deropy(verbose: int):
    if verbose == 1:
        change_logger_level('deropy', 'INFO')
    elif verbose > 1:
        change_logger_level('deropy', 'DEBUG')


deropy.add_command(generate)
deropy.add_command(deploy)
deropy.add_command(configure)
deropy.add_command(simulate)
deropy.add_command(transpile)

if __name__ == '__main__':
    deropy()
