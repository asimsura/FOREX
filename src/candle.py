'''
Created on 07 Mar 2019

@author: ernesto lowy
'''

import pdb

class Candle(object):
    """
    Constructor

    Class variables
    ---------------
    representation : str, either 'midpoint' or 'bidask'
           The candle's representation type
    time : datetime
        Candle's date and time
    volume : int
        Candle's volume
    complete : boolean
        Is the candle complete?
    formation : candle formation
        Possible values are:
    """

    def __init__(self, representation=None, time=None, volume=0, complete=True, formation=None):
        self.representation=representation
        self.time=time
        self.volume=volume
        if complete not in [True, False] : raise Exception(("complete %s is not valid. Complete should be True or False")) % complete
        self.complete=complete
        self.formation=formation


class BidAskCandle(Candle):
    '''
    Constructor

    Class variables
    ---------------
    openBid : float
              Candle's openBid value
    openAsk : float
              Candle's openAsk value
    highBid : float
              Candle's highBid value
    highAsk : float
              Candle's highAsk value
    lowBid  : float
              Candle's lowBid value
    lowAsk  : float
              Candle's lowAsk value
    closeBid : float
               Candle's lowAsk value
    closeAsk : float
               Candle's closeAsk value
    midAsk : float
             Middle of the candle. Calculated by doing
             (highAsk+lowAsk)/2
    midBid : float
              Middle of the candle. Calculated by doing
             (highBid+lowBid)/2

    Inherits from Candle
    '''

    def __init__(self, representation=None, **kwargs):
        Candle.__init__(self, representation)

        allowed_keys = ['representation', 'openBid', 'openAsk', 'highBid', 'highAsk',
                        'lowBid', 'lowAsk', 'closeBid', 'closeAsk', 'upper_wick', 'lower_wick', 'colour',
                        'perc_body', 'perc_uwick', 'perc_lwick', 'midAsk', 'midBid']

        self.__dict__.update((k, v) for k, v in kwargs.items() if k in allowed_keys)

    def set_candle_features(self):
        '''
        Set basic candle features based on price
        i.e. self.colour, upper_wick, midAsk or midBid, etc...

        Returns
        ------
        None

        '''
        if not self.openBid or not self.closeBid:
            raise Exception("Either self.openBid or self.closeBid need to be set to invoke set_candle_pattern")

        if not self.highBid or not self.lowBid:
            raise Exception("Either self.highBid or self.lowBid need to be set to invoke set_candle_pattern")

        upper = lower = 0.0
        if self.openBid < self.closeBid:
            self.colour = "green"
            upper = self.closeBid
            lower = self.openBid
        elif self.openBid > self.closeBid:
            self.colour = "red"
            upper = self.openBid
            lower = self.closeBid
        else:
            self.colour = "undefined"
            upper = self.openBid
            lower = self.closeBid

        #calculating mid*
        self.midAsk = round(abs(self.highAsk+self.lowAsk)/2,4)
        self.midBid = round(abs(self.highBid + self.lowBid)/2,4)

        self.upper_wick = self.highBid - upper
        self.lower_wick = lower - self.lowBid

    def set_candle_formation(self):
        '''
        Set candle formation

        Note: These are the conventions I will follow:

        DOJI: Body is <=10% of the total candle height

        Returns
        ------
        None

        '''
        if self.openBid is None or self.closeBid is None:
            raise Exception("Either self.openBid or self.closeBid need to be set to invoke set_candle_pattern")

        if self.highBid is None or self.lowBid is None:
            raise Exception("Either self.highBid or self.lowBid need to be set to invoke set_candle_pattern")

        if self.upper_wick is None or self.lower_wick is None:
            raise Exception("Either self.upper_wick or self.lower_wick need to be set to invoke set_candle_formation")

        height = self.highBid - self.lowBid
        body = abs(self.openBid - self.closeBid)

        perc_body = (body * 100) / height
        perc_uwick = (self.upper_wick * 100) / height
        perc_lwick = (self.lower_wick * 100) / height

        self.perc_body = perc_body
        self.perc_uwick = perc_uwick
        self.perc_lwick = perc_lwick

        if perc_body < 35 and perc_lwick > 60 and self.colour == "green":
            self.representation = "hammer"
        elif perc_body < 35 and perc_lwick > 60 and self.colour == "red":
            self.representation = "hanging_man"
        elif perc_body < 40 and perc_uwick > 55 and self.colour == "green":
            self.representation = "inverted_hammer"
        elif perc_body < 40 and perc_uwick > 55 and self.colour == "red":
            self.representation = "shooting_star"
        elif perc_body < 4 and perc_uwick > 40 and perc_lwick > 40:
            self.representation = "doji"
        elif perc_body < 4 and perc_uwick < 2 and perc_lwick > 94:
            self.representation = "dragonfly_doji"
        elif perc_body < 4 and perc_uwick > 94 and perc_lwick < 2:
            self.representation = "gravestone_doji"
        elif perc_body > 90 and self.colour == "green":
            self.representation = "green_marubozu"
        elif perc_body > 90 and self.colour == "red":
            self.representation = "red_marubozu"
        else:
            self.representation = "undefined"

    def __repr__(self):
        return "BidAskCandle"

    def __str__(self):
        out_str = ""
        for attr, value in self.__dict__.items():
            out_str += "%s:%s " % (attr, value)
        return out_str


class BiCandle:
    '''
    Constructor

    This class represents any combination of two candles

    Class variables
    ---------------

    candleA: BidAskCandle object
             First candle in the pair
    candleB: BidAskCandle object
             Second candle in the pair
    '''

    def __init__(self, candleA, candleB):
        self.candleA = candleA
        self.candleB = candleB

    def is_engulfing(self):
        '''
        Does candleB engulfs candleA?. Engulfing happens when candleB body engulfs the whole
        candleA (including the body and the wicks)

        Returns
        ------
        True or False
        '''

        if self.candleB.openBid > self.candleA.highBid and self.candleB.closeBid < self.candleA.lowBid:
            return True
        else:
            return False
