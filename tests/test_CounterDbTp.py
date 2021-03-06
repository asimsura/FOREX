from Pattern.counter_dbtp import CounterDbTp

import pytest
import pdb

@pytest.fixture
def ctdbptp_object():
    '''Returns CounterDbTp object'''

    c = CounterDbTp(
                    id='GBP_AUD 21FEB2019H12',
                    start='2019-02-21 22:00:00',
                    trend_i='2018-12-11 22:00:00',
                    pair='GBP_AUD',
                    timeframe='H12',
                    entry=1.83198,
                    SL=1.84637,
                    TP=1.81196,
                    SR=1.84218,
                    type='short')

    return c

@pytest.fixture
def ctdbptp_object_notrendi():
    '''Returns CounterDbTp object without the 'trend_i' initialised'''

    c = CounterDbTp(
                    id='GBP_AUD 21FEB2019H12',
                    start='2019-02-21 22:00:00',
                    pair='GBP_AUD',
                    timeframe='H12',
                    SL=1.84637,
                    SR=1.84218,
                    entry=1.83198,
                    RR=1.5,
                    type='short')

    return c


def test_init_feats(ctdbptp_object):

    ctdbptp_object.init_feats()
"""
def test_calc_itrend(ctdbptp_object_notrendi):

    ctdbptp_object_notrendi.calc_itrend()

def test_set_1stbounce(ctdbptp_object):

    ctdbptp_object.set_1stbounce()

def test_set_2ndbounce(ctdbptp_object):

    ctdbptp_object.set_2ndbounce()

def test_init_trend_feats(ctdbptp_object_notrendi):

    ctdbptp_object_notrendi.init_trend_feats()

def test_set_diff(ctdbptp_object):

    self.get_bounces(plot=True)
    ctdbptp_object.set_1stbounce()
    ctdbptp_object.set_2ndbounce()
    ctdbptp_object.set_diff()

    assert ctdbptp_object.diff==8.643089131783825

def test_set_valley(ctdbptp_object):

    ctdbptp_object.set_1stbounce()
    ctdbptp_object.set_2ndbounce()
    ctdbptp_object.set_valley()

    assert ctdbptp_object.valley==38
"""

