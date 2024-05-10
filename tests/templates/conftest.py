import pytest


from deropy.dvm.tester import clean_simulator


@pytest.fixture(scope='module', autouse=True)
def reset_simulation():
    print('start of the test for that file')
    yield
    print('resetting the simulation')
    clean_simulator()