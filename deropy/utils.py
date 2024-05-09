import os
import time
import shutil


simulator_host = 'http://127.0.0.1:30000'


def get_working_directory():
    return os.path.expanduser('~/.deropy')


def initialise_working_directory():
    # path = ~/.deropy
    path = os.path.expanduser('~/.deropy')

    if not os.path.exists(path):
        os.makedirs(path)


def create_sc_directory(sc_name):
    # path = ~/.deropy/sc
    path = os.path.expanduser(f'~/.deropy/{sc_name}')

    if not os.path.exists(path):
        os.makedirs(path)


def active_waiting(msg: str, timeout: int):
    start = time.time()

    while time.time() - start < timeout:
        for char in ['|', '/', '-', '\\']:
            print(f'{msg} {char}', end='\r')
            time.sleep(0.1)
    print('')