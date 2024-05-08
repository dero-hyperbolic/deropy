import os
import click
import logging

from deropy.utils import initialise_working_directory


@click.command('configure')
def configure():
    _install_autocomplete()


def _configure():
    _install_autocomplete()


def _install_autocomplete():
    initialise_working_directory()

    bashrc_path = os.path.join(os.path.expanduser('~'), '.bashrc')
    if os.path.isfile(bashrc_path):
        logging.info('Installing bash autocomplete')
        cmd_str = '~/.deropy/deropy_complete.bash'
        rc_file = os.path.join(os.path.expanduser('~'), '.bashrc')

        if _check_exist_in_file(cmd_str, rc_file):
            return

        os.system('_DEROPY_COMPLETE=bash_source deropy > ~/.deropy/deropy_complete.bash')
        os.system(f'echo ". {cmd_str}" >> {rc_file}')

    zshrc_path = os.path.join(os.path.expanduser('~'), '.zshrc')
    if os.path.isfile(zshrc_path):
        logging.info('Installing zsh autocomplete')
        cmd_str = '~/.deropy/deropy_complete.zsh'
        rc_file = os.path.join(os.path.expanduser('~'), '.zshrc')

        if _check_exist_in_file(cmd_str, rc_file):
            return

        os.system(f'_DEROPY_COMPLETE=zsh_source deropy > {cmd_str}')
        os.system(f'echo ". {cmd_str}" >> ~/.zshrc')


def _check_exist_in_file(sentence: str, filepath: str):
    with open(filepath, 'r') as file:
        return any(sentence in line for line in file.readlines())
