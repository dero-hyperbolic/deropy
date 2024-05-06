import click

from deropy.utils import initialise_working_directory
from deropy.dvm.parser import parse


@click.command('transpile')
@click.argument('file', type=click.Path())
@click.option('-o', '--output', type=click.Path(), help='The output path', default=None)
def transpile(file: str, output: str):
    _transpile(file, output)


def _transpile(file, output):
    initialise_working_directory()
    parse(file, output)