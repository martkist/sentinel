import pytest
import sys
import os
import time
os.environ['SENTINEL_ENV'] = 'test'
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../../test_sentinel.conf'))
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(__file__), '../../../lib')))
import misc
import config
from models import GovernanceObject, Proposal, Superblock, Vote


# clear DB tables before each execution
def setup():
    # clear tables first...
    Vote.delete().execute()
    Proposal.delete().execute()
    Superblock.delete().execute()
    GovernanceObject.delete().execute()


def teardown():
    pass


# list of proposal govobjs to import for testing
@pytest.fixture
def go_list_proposals():
    items = [
        {u'AbsoluteYesCount': 1000,
         u'AbstainCount': 7,
         u'CollateralHash': u'acb67ec3f3566c9b94a26b70b36c1f74a010a37c0950c22d683cc50da324fdca',
         u'DataHex': u'5b5b2270726f706f73616c222c207b22656e645f65706f6368223a20323132323532303430302c20226e616d65223a20226465616e2d6d696c6c65722d35343933222c20227061796d656e745f61646472657373223a202254535466654d65577751694344774d53545752616a39777756474e6a5a466676466b222c20227061796d656e745f616d6f756e74223a2032352e37352c202273746172745f65706f6368223a20313437343236313038362c202274797065223a20312c202275726c223a2022687474703a2f2f737973636f696e2e6f7267227d5d5d',
         u'DataString': u'[["proposal", {"end_epoch": 2122520400, "name": "dean-miller-5493", "payment_address": "TFcpmdvna59VuWdhCQQYsKE4jm6tUMeuEJ", "payment_amount": 25.75, "start_epoch": 1474261086, "type": 1, "url": "http://martkist.org"}]]',
         u'Hash': u'dfd7d63979c0b62456b63d5fc5306dbec451180adee85876cbf5b28c69d1a86c',
         u'IsValidReason': u'',
         u'NoCount': 25,
         u'YesCount': 1025,
         u'fBlockchainValidity': True,
         u'fCachedDelete': False,
         u'fCachedEndorsed': False,
         u'fCachedFunding': False,
         u'fCachedValid': True},
        {u'AbsoluteYesCount': 1000,
         u'AbstainCount': 29,
         u'CollateralHash': u'3efd23283aa98c2c33f80e4d9ed6f277d195b72547b6491f43280380f6aac810',
         u'DataHex': u'5b5b2270726f706f73616c222c207b22656e645f65706f6368223a20323132323532303430302c20226e616d65223a20226665726e616e64657a2d37363235222c20227061796d656e745f61646472657373223a202254456a4d6e6842356d41507270673752344355435347514e6e4a7150654146425448222c20227061796d656e745f616d6f756e74223a2033322e30312c202273746172745f65706f6368223a20313437343236313038362c202274797065223a20312c202275726c223a2022687474703a2f2f737973636f696e2e6f7267227d5d5d',
         u'DataString': u'[["proposal", {"end_epoch": 2122520400, "name": "fernandez-7625", "payment_address": "TEjMnhB5mAPrpg7R4CUCSGQNnJqPeAFBTH", "payment_amount": 32.01, "start_epoch": 1474261086, "type": 1, "url": "http://martkist.org"}]]',
         u'Hash': u'0523445762025b2e01a2cd34f1d10f4816cf26ee1796167e5b029901e5873630',
         u'IsValidReason': u'',
         u'NoCount': 56,
         u'YesCount': 1056,
         u'fBlockchainValidity': True,
         u'fCachedDelete': False,
         u'fCachedEndorsed': False,
         u'fCachedFunding': False,
         u'fCachedValid': True},
    ]

    return items


# list of superblock govobjs to import for testing
@pytest.fixture
def go_list_superblocks():
    items = [
        {u'AbsoluteYesCount': 1,
         u'AbstainCount': 0,
         u'CollateralHash': u'0000000000000000000000000000000000000000000000000000000000000000',
         u'DataHex': u'5b5b2274726967676572222c207b226576656e745f626c6f636b5f686569676874223a2037323639362c20227061796d656e745f616464726573736573223a202254535466654d65577751694344774d53545752616a39777756474e6a5a466676466b7c54535466654d65577751694344774d53545752616a39777756474e6a5a466676466b222c20227061796d656e745f616d6f756e7473223a202232352e37353030303030307c32352e3735303030303030222c202274797065223a20327d5d5d',
         u'DataString': u'[["trigger", {"event_block_height": 72696, "payment_addresses": "TFcpmdvna59VuWdhCQQYsKE4jm6tUMeuEJ|TFcpmdvna59VuWdhCQQYsKE4jm6tUMeuEJ", "payment_amounts": "25.75000000|25.7575000000", "type": 2}]]',
         u'Hash': u'667c4a53eb81ba14d02860fdb4779e830eb8e98306f9145f3789d347cbeb0721',
         u'IsValidReason': u'',
         u'NoCount': 0,
         u'YesCount': 1,
         u'fBlockchainValidity': True,
         u'fCachedDelete': False,
         u'fCachedEndorsed': False,
         u'fCachedFunding': False,
         u'fCachedValid': True},
        {u'AbsoluteYesCount': 1,
         u'AbstainCount': 0,
         u'CollateralHash': u'0000000000000000000000000000000000000000000000000000000000000000',
         u'DataHex': u'5b5b2274726967676572222c207b226576656e745f626c6f636b5f686569676874223a2037323639362c20227061796d656e745f616464726573736573223a202254535466654d65577751694344774d53545752616a39777756474e6a5a466676466b7c54535466654d65577751694344774d53545752616a39777756474e6a5a466676466b222c20227061796d656e745f616d6f756e7473223a202232352e37353030303030307c32352e3735303030303030222c202274797065223a20327d5d5d',
         u'DataString': u'[["trigger", {"event_block_height": 72696, "payment_addresses": "TFcpmdvna59VuWdhCQQYsKE4jm6tUMeuEJ|TFcpmdvna59VuWdhCQQYsKE4jm6tUMeuEJ", "payment_amounts": "25.75000000|25.75000000", "type": 2}]]',
         u'Hash': u'8f91ffb105739ec7d5b6c0b12000210fcfcc0837d3bb8ca6333ba93ab5fc0bdf',
         u'IsValidReason': u'',
         u'NoCount': 0,
         u'YesCount': 1,
         u'fBlockchainValidity': True,
         u'fCachedDelete': False,
         u'fCachedEndorsed': False,
         u'fCachedFunding': False,
         u'fCachedValid': True},
        {u'AbsoluteYesCount': 1,
         u'AbstainCount': 0,
         u'CollateralHash': u'0000000000000000000000000000000000000000000000000000000000000000',
         u'DataHex': u'5b5b2274726967676572222c207b226576656e745f626c6f636b5f686569676874223a2037323639362c20227061796d656e745f616464726573736573223a202254535466654d65577751694344774d53545752616a39777756474e6a5a466676466b7c54535466654d65577751694344774d53545752616a39777756474e6a5a466676466b222c20227061796d656e745f616d6f756e7473223a202232352e37353030303030307c32352e3735303030303030222c202274797065223a20327d5d5d',
         u'DataString': u'[["trigger", {"event_block_height": 72696, "payment_addresses": "TFcpmdvna59VuWdhCQQYsKE4jm6tUMeuEJ|TFcpmdvna59VuWdhCQQYsKE4jm6tUMeuEJ", "payment_amounts": "25.75000000|25.75000000", "type": 2}]]',
         u'Hash': u'bc2834f357da7504138566727c838e6ada74d079e63b6104701f4f8eb05dae36',
         u'IsValidReason': u'',
         u'NoCount': 0,
         u'YesCount': 1,
         u'fBlockchainValidity': True,
         u'fCachedDelete': False,
         u'fCachedEndorsed': False,
         u'fCachedFunding': False,
         u'fCachedValid': True},
    ]

    return items


@pytest.fixture
def superblock():
    sb = Superblock(
        event_block_height=43800,
        payment_addresses='TFcpmdvna59VuWdhCQQYsKE4jm6tUMeuEJ|TEjMnhB5mAPrpg7R4CUCSGQNnJqPeAFBTH',
        payment_amounts='5|3',
        proposal_hashes='e8a0057914a2e1964ae8a945c4723491caae2077a90a00a2aabee22b40081a87|d1ce73527d7cd6f2218f8ca893990bc7d5c6b9334791ce7973bfa22f155f826e',
    )
    return sb


def test_superblock_is_valid(superblock):
    from martkistd import MartkistDaemon
    martkistd = MartkistDaemon.from_martkist_conf(config.martkist_conf)

    orig = Superblock(**superblock.get_dict())  # make a copy

    # original as-is should be valid
    assert orig.is_valid() is True

    # mess with payment amounts
    superblock.payment_amounts = '7|yyzx'
    assert superblock.is_valid() is False

    superblock.payment_amounts = '7,|yzx'
    assert superblock.is_valid() is False

    superblock.payment_amounts = '7|8'
    assert superblock.is_valid() is True

    superblock.payment_amounts = ' 7|8'
    assert superblock.is_valid() is False

    superblock.payment_amounts = '7|8 '
    assert superblock.is_valid() is False

    superblock.payment_amounts = ' 7|8 '
    assert superblock.is_valid() is False

    # reset
    superblock = Superblock(**orig.get_dict())
    assert superblock.is_valid() is True

    # mess with payment addresses
    superblock.payment_addresses = 'TEjMnhB5mAPrpg7R4CUCSGQNnJqPeAFBTH|1234 Anywhere ST, Chicago, USA'
    assert superblock.is_valid() is False

    # leading spaces in payment addresses
    superblock.payment_addresses = ' TEjMnhB5mAPrpg7R4CUCSGQNnJqPeAFBTH'
    superblock.payment_amounts = '5.00'
    assert superblock.is_valid() is False

    # trailing spaces in payment addresses
    superblock.payment_addresses = 'TEjMnhB5mAPrpg7R4CUCSGQNnJqPeAFBTH '
    superblock.payment_amounts = '5.00'
    assert superblock.is_valid() is False

    # leading & trailing spaces in payment addresses
    superblock.payment_addresses = ' TEjMnhB5mAPrpg7R4CUCSGQNnJqPeAFBTH '
    superblock.payment_amounts = '5.00'
    assert superblock.is_valid() is False

    # single payment addr/amt is ok
    superblock.payment_addresses = 'TEjMnhB5mAPrpg7R4CUCSGQNnJqPeAFBTH'
    superblock.payment_amounts = '5.00'
    assert superblock.is_valid() is True

    # ensure number of payment addresses matches number of payments
    superblock.payment_addresses = 'TEjMnhB5mAPrpg7R4CUCSGQNnJqPeAFBTH'
    superblock.payment_amounts = '37.00|23.24'
    assert superblock.is_valid() is False

    superblock.payment_addresses = 'TFcpmdvna59VuWdhCQQYsKE4jm6tUMeuEJ|TEjMnhB5mAPrpg7R4CUCSGQNnJqPeAFBTH'
    superblock.payment_amounts = '37.00'
    assert superblock.is_valid() is False

    # ensure amounts greater than zero
    superblock.payment_addresses = 'TEjMnhB5mAPrpg7R4CUCSGQNnJqPeAFBTH'
    superblock.payment_amounts = '-37.00'
    assert superblock.is_valid() is False

    # reset
    superblock = Superblock(**orig.get_dict())
    assert superblock.is_valid() is True

    # mess with proposal hashes
    superblock.proposal_hashes = '7|yyzx'
    assert superblock.is_valid() is False

    superblock.proposal_hashes = '7,|yyzx'
    assert superblock.is_valid() is False

    superblock.proposal_hashes = '0|1'
    assert superblock.is_valid() is False

    superblock.proposal_hashes = '0000000000000000000000000000000000000000000000000000000000000000|1111111111111111111111111111111111111111111111111111111111111111'
    assert superblock.is_valid() is True

    # reset
    superblock = Superblock(**orig.get_dict())
    assert superblock.is_valid() is True


def test_serialisable_fields():
    s1 = ['event_block_height', 'payment_addresses', 'payment_amounts', 'proposal_hashes']
    s2 = Superblock.serialisable_fields()

    s1.sort()
    s2.sort()

    assert s2 == s1


def test_deterministic_superblock_creation(go_list_proposals):
    import martkistlib
    import misc
    from martkistd import MartkistDaemon
    martkistd = MartkistDaemon.from_martkist_conf(config.martkist_conf)
    for item in go_list_proposals:
        (go, subobj) = GovernanceObject.import_gobject_from_martkistd(martkistd, item)

    max_budget = 60
    prop_list = Proposal.approved_and_ranked(proposal_quorum=1, next_superblock_max_budget=max_budget)

    # MAX_GOVERNANCE_OBJECT_DATA_SIZE defined in governance-object.h
    maxgovobjdatasize = 16 * 1024
    sb = martkistlib.create_superblock(prop_list, 72000, max_budget, misc.now(), maxgovobjdatasize)

    assert sb.event_block_height == 72000
    assert sb.payment_addresses == 'TSTfeMeWwQiCDwMSTWRaj9wwVGNjZFfvFk|TEjMnhB5mAPrpg7R4CUCSGQNnJqPeAFBTH'
    assert sb.payment_amounts == '25.75000000|32.01000000'
    assert sb.proposal_hashes == 'dfd7d63979c0b62456b63d5fc5306dbec451180adee85876cbf5b28c69d1a86c|0523445762025b2e01a2cd34f1d10f4816cf26ee1796167e5b029901e5873630'

    assert sb.hex_hash() == '1503598424dddb4aa78f0f0ffddc9371386c9692ab35f8f82065672d5d94f870'


def test_superblock_size_limit(go_list_proposals):
    import martkistlib
    import misc
    from martkistd import MartkistDaemon
    martkistd = MartkistDaemon.from_martkist_conf(config.martkist_conf)
    for item in go_list_proposals:
        (go, subobj) = GovernanceObject.import_gobject_from_martkistd(martkistd, item)

    max_budget = 60
    prop_list = Proposal.approved_and_ranked(proposal_quorum=1, next_superblock_max_budget=max_budget)

    maxgovobjdatasize = 469
    sb = martkistlib.create_superblock(prop_list, 72000, max_budget, misc.now(), maxgovobjdatasize)

    # two proposals in the list, but...
    assert len(prop_list) == 2

    # only one should have been included in the SB, because the 2nd one is over the limit
    assert sb.event_block_height == 72000
    assert sb.payment_addresses == 'TSTfeMeWwQiCDwMSTWRaj9wwVGNjZFfvFk'
    assert sb.payment_amounts == '25.75000000'
    assert sb.proposal_hashes == 'dfd7d63979c0b62456b63d5fc5306dbec451180adee85876cbf5b28c69d1a86c'

    assert sb.hex_hash() == 'c30d2f26ffbe9a3d234f301c1a8a568a29096963d4b7ac1bdc3b15479592b0d3'


def test_deterministic_superblock_selection(go_list_superblocks):
    from martkistd import MartkistDaemon
    martkistd = MartkistDaemon.from_martkist_conf(config.martkist_conf)

    for item in go_list_superblocks:
        (go, subobj) = GovernanceObject.import_gobject_from_martkistd(martkistd, item)

    # highest hash wins if same -- so just order by hash
    sb = Superblock.find_highest_deterministic('3fe3938349a350469670348adf9ebd2e8023b7ebe65ecbb87837cfa74ca8bbfa')
    assert sb.object_hash == 'bc2834f357da7504138566727c838e6ada74d079e63b6104701f4f8eb05dae36'
