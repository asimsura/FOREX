import argparse
import pdb

from TradeJournal.tradejournal import TradeJournal

parser = argparse.ArgumentParser(description='Script to calculate the features for Counter trades')

parser.add_argument('--ifile', required=True, help='.xlsx files with the trades')
parser.add_argument('--worksheet', required=True, help='Worksheet from --ifile that will be analyzed')
parser.add_argument('--strats', required=True, help='Strategy in --worksheet to be analyzed. It can be a single strategy '
                                                   '(i.e. counter_b1 or a comma-separated list of strategies to be '
                                                   'analysed (i.e. counter_b1,counter_b2')
parser.add_argument('--outsheet', required=True, help='Worksheet name for calculated trades')

args = parser.parse_args()

td = TradeJournal(url=args.ifile, worksheet=args.worksheet)

strats=args.strats.split(",")

trade_list = td.fetch_trades(strats=strats,run=True)

td.write_trades(trade_list, colnames=['id', 'start', 'strat', 'type', 'SMA', 'entry', 'TP', 'SL', 'SR','entry_time','outcome','pips','lasttime',
                                      'bounces','bounces_lasttime'], sheetname= args.outsheet)
#td.write_trades(trade_list, colnames=['id', 'start', 'strat', 'type', 'SMA', 'entry', 'TP', 'SL', 'SR','entry_time','outcome','pips'], sheetname= args.strat+".calc")

