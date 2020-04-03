import pytest
import sys
import os
import re
os.environ['SENTINEL_ENV'] = 'test'
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import config

from martkistd import MartkistDaemon
from martkist_config import MartkistConfig


def test_martkistd():
    config_text = MartkistConfig.slurp_config_file(config.martkist_conf)
    network = 'mainnet'
    is_testnet = False
    genesis_hash = u'00000a7f5622e1499ea8649f89c033973b9d5f4b96715ba21858af6234c7cc32'
    for line in config_text.split("\n"):
        if line.startswith('testnet=1'):
            network = 'testnet'
            is_testnet = True
            genesis_hash = u'00000a7f5622e1499ea8649f89c033973b9d5f4b96715ba21858af6234c7cc32'

    creds = MartkistConfig.get_rpc_creds(config_text, network)
    martkistd = MartkistDaemon(**creds)
    assert martkistd.rpc_command is not None

    assert hasattr(martkistd, 'rpc_connection')

    # Martkist testnet block 0 hash == 00000bafbc94add76cb75e2ec92894837288a481e5c005f6563d91623bf8bc2c
    # test commands without arguments
    info = martkistd.rpc_command('getinfo')
    info_keys = [
        'blocks',
        'connections',
        'difficulty',
        'errors',
        'protocolversion',
        'proxy',
        'testnet',
        'timeoffset',
        'version',
    ]
    for key in info_keys:
        assert key in info
    assert info['testnet'] is is_testnet

    # test commands with args
    assert martkistd.rpc_command('getblockhash', 0) == genesis_hash
