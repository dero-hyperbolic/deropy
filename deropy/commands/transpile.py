import click

from deropy.dvm.parser import parse

@click.command('transpile')
@click.argument('file', type=click.Path())
def transpile(file):
    _transpile(file)

def _transpile(file):
    parse(file)