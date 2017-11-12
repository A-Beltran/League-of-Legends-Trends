import re
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

def main():
    rawChampStatList1 = getStats("patch6point8.txt")
    rawChampStatList2 = getStats('patch6point9.txt')

    c1,p1,w1,b1,r1 = createProfiles(rawChampStatList1)
    c2,p2,w2,b2,r2 = createProfiles(rawChampStatList2)
    #outFile('LoLChampDataPRW.txt',c,p,w,b,r)
    roleBanGraph(c1,b1,r1,'Ban Rate by Role (Patch 6.8)')#patch6.8
    roleBanGraph(c2,b2,r2,'Ban Rate by Role (Patch 6.9)')#patch6.9
    roleWinGraph(c1,w1,r1)
    roleWinGraph(c2,w2,r2)

#challenger master
    cW,cL = getLeagueStats('challenger.txt')
    cKW,cKL = getLeagueStats('challengerKorea.txt')
    cEW,cEL = getLeagueStats('challengerEUW.txt')

    cWA,cLA = avgWL(cW,cL)
    cWAK,cLAK = avgWL(cKW,cKL)
    cWAE,cLAE = avgWL(cEW,cEL)
    print 'Wins/Losses'
    print cWA,cLA
    print cWAK,cLAK
    print cWAE,cLAE
    print 'Total Games (NA,KR,EUW)'
    naGames = games(cW,cL)
    krGames = games(cKW,cKL)
    euGames = games(cEW,cEL)
    naWins,naLosses = total(cW,cL)
    krWins,krLosses = total(cKW,cKL)
    euWins,euLosses = total(cEW,cEL)
    regionGraph(naGames,krGames,euGames,naWins,krWins,euWins,naLosses,krLosses,euLosses)
    
##    df = pd.DataFrame({ 'Total Games' : pd.Series([naGames+krGames+euGames]),
##                        'NAWins' : pd.Series([cW]),
##                        'KRWins' : pd.Series([cKW]),
##                        'EUWins' : pd.Series([cEW]),
##                         })
##    print df
##    sns.lmplot('EUWins','NAWins',df)
##    plt.sns.show
def games(wins,losses):
    win = 0
    loss = 0

    for i in wins:
        win += i
    for i in losses:
        loss += i
    return win+loss
def total(wins,losses):
    win = 0
    loss = 0

    for i in wins:
        win += i
    for i in losses:
        loss += i
    return win,loss 



def avgWL(wins,losses):
    winAvg = 0
    lossAvg = 0

    for i in wins:
        winAvg += i
    for i in losses:
        lossAvg += i
    return winAvg/len(wins),lossAvg/len(losses)        
    
def sortRoles(champions,rate,role,div):
    topLane = []
    midLane = []
    adCarry = []
    support = []
    jungler = []

    for i in range(0,len(champions)):
        if(role[i] == 'Top Lane'):
            topLane.append(float(rate[i]))
        if(role[i] == 'Middle Lane'):
            midLane.append(float(rate[i]))
        if(role[i] == 'AD Carry'):
            adCarry.append(float(rate[i]))
        if(role[i] == 'Support'):
            support.append(float(rate[i]))
        if(role[i] == 'Jungler'):
            jungler.append(float(rate[i]))
    ta = 0
    for i in topLane:
        ta+=i
    ma = 0
    for i in midLane:
        ma+=i
    aa = 0
    for i in adCarry:
        aa+=i
    sa = 0
    for i in support:
        sa+=i
    ja = 0
    for i in jungler:
        ja+=i
    return ta/div,ma/div,aa/div,sa/div,ja/div
    

def regionGraph(naTotal,krTotal,euTotal,naWins,krWins,euWins,naLosses,krLosses,euLosses):
    print 'WIN LOSS BY REGION'

        

    N = 3

    ind = np.arange(N)  # the x locations for the groups
    width = 0.35       # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, [naTotal,krTotal,euTotal], width, color='b')

    rects2 = ax.bar(ind + width, [naWins,krWins,euWins], width-0.05, color='g')
    rects3 = ax.bar(ind + width*2-0.05, [naLosses,krLosses,euLosses], width-0.05, color='r')

# add some text for labels, title and axes ticks
    ax.set_ylabel('Amount')
    ax.set_title('Playrate and Performance by Region (Challenger Tier)')
    ax.set_xticks(ind + width)
    ax.set_xticklabels(['NORTH_AMERICA','KOREA','EUROPE_WEST'])

    ax.legend((rects1[0], rects2[0],rects3[0]), ('Total', 'Wins','Losses'))
    plt.show()

def roleWinGraph(c,w,r):
    print 'TOP WIN RATE ROLES'
    roles = ['Top Lane','Middle Lane','AD Carry','Support','Jungler']
    top,mid,adc,sup,jun = sortRoles(c,w,r,100)
    print top,mid,adc,sup,jun

    N = len(roles)
    ind = np.arange(N)  # the x locations for the groups

    width = 1.00      # the width of the bars
    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, [top,mid,adc,sup,jun], width, color='b')

    # add some text for labels, title and axes ticks
    ax.set_ylabel('Role Win Rate')
    ax.set_title('Win Rate by Role')
    ax.set_xticks(ind+0.5)
    ax.set_xticklabels([roles[i] for i in range(0,5)])

    plt.show()
    
def roleBanGraph(c,b,r,title):
    print 'TOP BAN RATE ROLES'
    roles = ['Top Lane','Middle Lane','AD Carry','Support','Jungler']
    top,mid,adc,sup,jun = sortRoles(c,b,r,5)
    N = len(roles)
    ind = np.arange(N)  # the x locations for the groups

    width = 1.00      # the width of the bars
    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, [top,mid,adc,sup,jun], width, color='r')

    # add some text for labels, title and axes ticks
    ax.set_ylabel('Cumulative Percentage')
    ax.set_title(title)
    ax.set_xticks(ind+0.5)
    ax.set_xticklabels([roles[i] for i in range(0,5)])

    plt.show()





def popularGraph(popularity,champion,winRate):
    print 'MOST POPULAR CHAMPIONS'
    indexPopular = mostStat(popularity,15)
    print indexPopular
    for i in indexPopular:
        print champion[i],winRate[i]
        

    N = len(indexPopular)
    popY = [popularity[i] for i in indexPopular]

    ind = np.arange(N)  # the x locations for the groups
    width = 0.35       # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, popY, width, color='r')

    winY = [winRate[i] for i in indexPopular]
    rects2 = ax.bar(ind + width, winY, width, color='b')

# add some text for labels, title and axes ticks
    ax.set_ylabel('Percentage')
    ax.set_title('Highest Play Rate Champions w/ Popularity')
    ax.set_xticks(ind + width)
    ax.set_xticklabels([champion[i] for i in indexPopular])

    ax.legend((rects1[0], rects2[0]), ('Popularity', 'Win Rate'))
    plt.show()

def mostStat(aList,threshold):
    index = []
    for i,j in enumerate(aList):
        if(float(j)>=threshold):
            index.append(i)
    return index

                        
def createProfiles(aList):
    champion = []
    popularity = []
    winRate = []
    banRate = []
    role = []

    for i in range(0,len(aList)):
        if(i%7==0):
            champion.append(aList[i])

        if(i%7==3):
            popularity.append(aList[i])

        if(i%7==4):
            winRate.append(aList[i])

        if(i%7==5):
            banRate.append(aList[i])

        if(i%7==6):
            role.append(aList[i])

    return champion,popularity,winRate,banRate,role
                        
def getLeagueStats(aFile):
    page = open(aFile,'r')
    data = page.read()
    rawStats = re.findall(r'wins\':\s\d+|losses\':\s\d+',data)
    cleanStats=[]
    wins = []
    losses = []
    for i in rawStats:
        c = i.find(':')
        cleanStats.append(int(i[c+2:]))

    for i in range(0,len(cleanStats)):
        if(i%2==0):
            losses.append(cleanStats[i])
        if(i%2==1):
            wins.append(cleanStats[i])
    return wins,losses
           

def getStats(aFile):
    page = open(aFile,'r')
    data = page.read()
    rawStats = re.findall(r'>\w+</|>\d+\.\d+%<|>\w+%<|>\w+ \w+</|>\w+\W+\w+</',data)
    cleanStats=[]
    for i in rawStats:
        c = i.find('>')
        cleanStats.append(i[c+1:-2])
    return cleanStats

def outFile(aFile,champion,popularity,winRate,banRate,role):
    f = open(aFile,'w')
    for i in range(0,len(champion)):
	    f.write(champion[i]
                            +', '
                            + popularity[i]
                            +', '
                            + winRate[i]
                            +', '
                            + banRate[i]
                            +', '
                            + role[i]
                            +'\n')
    f.close()        

main()
