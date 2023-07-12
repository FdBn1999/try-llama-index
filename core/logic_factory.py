from dotenv import dotenv_values

from . import logic
from . import fake_logic

config = dotenv_values()
USE_MOCK = config['USE_MOCK']

def get_logic():
    if USE_MOCK:
        return fake_logic
    else:
        return logic