# Non blocking read on subprocess.Popen
# https://stackoverflow.com/questions/375427/a-non-blocking-read-on-a-subprocess-pipe-in-python
import click
import subprocess
import logging
import sys
import os
import threading
import time
from queue import Queue, Empty
import pytest


from deropy.commands.deploy import _deploy
from deropy.commands.generate import _generate
from deropy.commands.transpile import _transpile
from deropy.utils import get_working_directory


ON_POSIX = 'posix' in sys.builtin_module_names


@click.command('simulate')
@click.argument('simulator', type=click.Path())
@click.argument('sc_file', type=click.Path())
@click.argument('tests_file', type=click.Path())
def simulate(simulator, sc_file, tests_file):
    _simulate(simulator, sc_file, tests_file)


def check(simulator: str, sc_file: str, tests_file: str):
    if not sc_file.endswith('.py'):
        logging.error('The smart contract file must be a python file')
        return False

    if not tests_file.endswith('.py'):
        logging.error('The tests file must be a python file')
        return False

    return True


def _simulate(simulator, sc_file, tests_file):
    if not check(simulator, sc_file, tests_file):
        return

    smart_contract_name = os.path.basename(sc_file).split('.')[0].lower()
    transpile_path = os.path.join(get_working_directory(), f'{smart_contract_name}.bas')
    api_path = os.path.join(get_working_directory(), f'{smart_contract_name}_api.py')

    # Execute the DEROHE Simualtor
    # We do it into a thread because we don't want to block the main thread
    # We need to read the output from the simulator to know when it is ready to receive requests
    # Read the output from the simulator until the Listening for requests message is displayed
    print('Executing the DEROHE simulator')
    p = subprocess.Popen([simulator], stdout=subprocess.PIPE, bufsize=1, close_fds=ON_POSIX)
    q = Queue()
    t = threading.Thread(target=enqueue_output, args=(p.stdout, q))
    t.daemon = True
    t.start()
    read_until(q, 'Listening for requests')

    # Transpile the python smart-contract into a DEROHE smart-contract
    print('Transpiling the smart contract')
    _transpile(sc_file, transpile_path)

    # Deploy the smart-contract to the simulator
    print('Deploying the smart contract')
    txid = _deploy(transpile_path)
    read_until(q, "interpreting line [RETURN 0]   err:'<nil>'", 20)

    # Generate the API
    print('Generating the API')
    _generate(transpile_path, txid, 'simulator', api_path)

    # Execute the tests in the simulator
    t = threading.Thread(target=stream_output, args=(q,))
    t.daemon = True
    t.start()
    print('Executing the tests')
    os.environ['API_PATH'] = f"{api_path}"
    pytest.main([tests_file, '-vxs'])

    # Finish reading the output from the simulator
    read_until_empty(q)

    # Close the simulator
    p.terminate()
    p.wait()


def enqueue_output(out, queue):
    for line in iter(out.readline, b''):
        queue.put(line)
    out.close()


def stream_output(queue):
    while True:
        try:
            line = queue.get_nowait()
        except Empty:
            time.sleep(0.1)
            continue
        else:
            print(line.decode(), end='')


def active_waiting(msg: str, timeout: int):
    start = time.time()

    while time.time() - start < timeout:
        for char in ['|', '/', '-', '\\']:
            print(f'{msg} {char}', end='\r')
            time.sleep(0.1)
    print('')


def read_until(q, expected, timeout=20):
    while True:
        try:
            line = q.get_nowait()
        except Empty:
            time.sleep(0.1)
            continue
        else:
            print(line.decode(), end='')
            if expected in line.decode():
                break
            if timeout == 0:
                break
            timeout -= 0.1

def read_until_empty(q):
    while True:
        try:
            line = q.get_nowait()
        except Empty:
            break
        else:
            print(line.decode(), end='')