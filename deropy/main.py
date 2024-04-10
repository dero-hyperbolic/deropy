import click

from deropy.commands.generate import generate
from deropy.commands.deploy import deploy


@click.group('deropy')
@click.version_option()
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
def deropy(verbose: bool):
    """deropy is a CLI for deropy."""
    
    # if no arguments are passed, show the help message
    if not any([verbose]):
        click.echo(deropy.get_help(click.Context(deropy)))

deropy.add_command(generate)
deropy.add_command(deploy)

if __name__ == '__main__':
    deropy()