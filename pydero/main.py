import click

from commands.generate import generate
from commands.deploy import deploy


@click.group('pydero')
@click.version_option()
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
def solwr(verbose: bool):
    """Pydero is a CLI for pydero."""
    pass

solwr.add_command(generate)
solwr.add_command(deploy)

if __name__ == '__main__':
    solwr()