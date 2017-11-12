from riotwatcher import RiotWatcher
from pprint import pprint
from riotwatcher import KOREA
from riotwatcher import EUROPE_WEST

w = RiotWatcher('bb7a8dae-4e14-410b-abd5-4f86308b8b0d')
def outFile(aFile,write):
    f = open(aFile,'w')
    f.write(write)
    f.close()        

#NORTH_AMERICA
challenger = w.get_challenger()
#pprint(challenger)
#KOREA
challengerKR = w.get_challenger(region=KOREA)
#pprint(challengerKR)
#EUROPE_WEST
challengerEUW = w.get_challenger(region=EUROPE_WEST)
#pprint(challengerEUW)
