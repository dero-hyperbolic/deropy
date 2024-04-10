import click

from commands.generate import generate
from commands.deploy import deploy


@click.group('deropy')
@click.version_option()
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
def deropy(verbose: bool):
    """deropy is a CLI for deropy."""
    pass

deropy.add_command(generate)
deropy.add_command(deploy)

if __name__ == '__main__':
    deropy()