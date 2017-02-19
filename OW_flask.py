from plotly.offline import download_plotlyjs, init_notebook_mode, iplot, plot
from plotly.graph_objs import *
#init_notebook_mode()

import matplotlib.pyplot as plt
import numpy as np
from lxml import etree
from lxml.html import fromstring, tostring
import urllib.request

def create_allinfos(tree,category = 'competitive'): # 'quick play'
    allheroes = {}
#    xpath_onehero = '//*[@id="stats-section"]/div/div/div[@data-category-id="{0}"]/div/div/table[@class="data-table"]/tbody/tr/td' 
    xpath_onehero = '//*[@id="{}"]/section[@class="content-box u-max-width-container career-stats-section"]'
    xpath_onehero = xpath_onehero + '/div/div[@data-category-id="{}"]/div/div/table[@class="data-table"]/tbody/tr/td'
    # [@class="data-table"] is not really needed
    # each heroes has an exadecimal number associated for the data-category-id field in the xpath, 
    # "All Heroes" are treated as a single hero
    heroes_exa = { 
        "All Heroes":"0x02E00000FFFFFFFF",
        "Reaper":"0x02E0000000000002",
        "Tracer":"0x02E0000000000003",
        "Mercy":"0x02E0000000000004",
        "Hanzo":"0x02E0000000000005",
        "Torbjorn":"0x02E0000000000006",
        "Reinhardt":"0x02E0000000000007",
        "Pharah":"0x02E0000000000008",
        "Winston":"0x02E0000000000009",
        "Widowmaker":"0x02E000000000000A",
        "Bastion":"0x02E0000000000015",
        "Symmetra":"0x02E0000000000016",
        "Zenyatta":"0x02E0000000000020",
        "Genji":"0x02E0000000000029",
        "Roadhog":"0x02E0000000000040",
        "McCree":"0x02E0000000000042",
        "Junkrat":"0x02E0000000000065",
        "Zarya":"0x02E0000000000068",
        "Soldier: 76":"0x02E000000000006E",
        "Lucio":"0x02E0000000000079",
        "D.Va":"0x02E000000000007A",
        "Mei":"0x02E00000000000DD",
        "Ana":"0x02E000000000013B",
        "Sombra":"0x02E000000000012E"
    }
    for hero in heroes_exa.keys():
        temp = tree.xpath(xpath_onehero.format(category,heroes_exa[hero]))
        tempdic = {}
        for i in range(0,len(temp),2):
            tempdic[temp[i].text] = temp[i+1].text
        allheroes[hero] = tempdic        
    return allheroes

def getPlayerInfos(url,category='competitive'):
    print("obtaining {0} infos from ".format(category) + url)
    request = urllib.request.Request(url)
    rawPage = urllib.request.urlopen(request)
    read = rawPage.read()
    tree = etree.HTML(read)
    allheroes = create_allinfos(tree,category)
    return allheroes

def getAllHeroInfoName(HeroesStats, hero):
    temp = []
    for p in HeroesStats.keys():
        temp = temp + list(HeroesStats[p][hero].keys())
    temp = list(set(temp))
    return temp

def myConvToFloat(mystr):
    tobereplace = ["%",","," minutes"," minute"," hours"," hour"," seconds"," second",":"]
    for r in tobereplace:
        mystr = mystr.replace(r,"")
    return float(mystr)

def plotHeroForAllPlayersPlotly(hero,HeroesStats,FairCompare=True):
    units = ""
    allvars = getAllHeroInfoName(HeroesStats,hero)
    allvars.sort()
    data = []
    layout= Layout()
    for p in HeroesStats.keys():
        xx, yy, my_xticks = [], [], []
        pp = p[0:p.find("-")]
        for i,var in enumerate(allvars):
            if FairCompare:
                if "Average" not in var:
                    continue
            xx.append(i)
            if not var in HeroesStats[p][hero]:
                yy.append(0)
            else:
                yy.append(myConvToFloat(HeroesStats[p][hero][var]))
                if("%" in HeroesStats[p][hero][var]): units = " (%)"
                if("hour" in HeroesStats[p][hero][var]): units = " h"
                if("hours" in HeroesStats[p][hero][var]): units = " h"
                if("minute" in HeroesStats[p][hero][var]): units = " min"
                if("minutes" in HeroesStats[p][hero][var]): units = " min"
                if("seconds" in HeroesStats[p][hero][var]): units = " sec"
                if("second" in HeroesStats[p][hero][var]): units = " sec"
                else: units = ""
            my_xticks.append(var+units)
            xlabelsize = 8
            if FairCompare:
                xlabelsize = 10
            layout = Layout(
                title = hero,
                xaxis=dict(
                    title='',
                    titlefont=dict(family='Arial, sans-serif',size=18,color='lightgrey'),
                    showticklabels=True,
                    tickangle=35,
                    tickfont=dict(family='Old Standard TT, serif',size=xlabelsize,color='black'),
                ),
                yaxis=dict(
                    title='stats',
                    titlefont=dict(family='Arial, sans-serif',size=18,color='lightgrey'),
                    showticklabels=True,
                    tickangle=0,
                    tickfont=dict(family='Old Standard TT, serif',size=18,color='black'),
                    type = 'log'
                )
            ) 
        data.append(Scatter(x = my_xticks, y = yy, mode = 'markers', 
                            marker=dict(symbol="line-ew-open",size=6,line=dict(width=4)), name = pp))
        #data.append(Scatter(x = my_xticks, y = yy, mode = 'markers', name = pp))
    fig = Figure(data=data, layout=layout)
    plot(fig, filename=hero+'.html')



# Players = ['Ale-1244', 'Frenci-1486', 'Sam-1619', 'kiukki-2350', 'Alby-2701', "ziGno-2418"]
# heroes_name=["Reaper", "Tracer", "Mercy", "Hanzo", "Torbjorn", "Reinhardt", "Pharah",
#              "Winston", "Widowmaker", "Bastion", "Symmetra", "Zenyatta", "Genji", "Roadhog", 
#              "McCree", "Junkrat", "Zarya", "Soldier: 76", "Lucio", "D.Va", "Mei", 'Ana', 'Sombra']
# heroes_name.sort()
# heroes_name_2 = ["All Heroes"] + heroes_name

# HeroesStatsQuickPlay = {}
# HeroesStatsCompetitive = {}
# for p in Players:
#     HeroesStatsQuickPlay[p] = getPlayerInfos(prefix + p,'quickplay')
#     HeroesStatsCompetitive[p] = getPlayerInfos(prefix + p,'competitive')


### start to code the flask app
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask import request

import json
import plotly


name = 'OW_stats_compare'
app = Flask(name)
app.debug = True
app.config['key'] = 'secret'
socketio = SocketIO(app)

def get_players_stats(players):
    # players = app_state['players'].split(",")
    players = players.split(",")
    HeroesStatsQuickPlay = {}
    HeroesStatsCompetitive = {}
    prefix = "https://playoverwatch.com/en-gb/career/pc/eu/"
    for p in players:
        p=p.strip()
        try:
            HeroesStatsQuickPlay[p] = getPlayerInfos(prefix + p,'quickplay')
            HeroesStatsCompetitive[p] = getPlayerInfos(prefix + p,'competitive')
        except urllib.error.HTTPError:
            print("Players {0} not found".format(p))
    return HeroesStatsQuickPlay, HeroesStatsCompetitive

# HeroesStats = {"quickplay":{}, "competitive":{}}

@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        players_choosen = request.form.get('players', None)
        global HeroesStatsQuickPlay
        global HeroesStatsCompetitive
        HeroesStatsQuickPlay, HeroesStatsCompetitive = get_players_stats(players_choosen)
    return render_template('layouts/layout_single_column_and_controls.html', app_name=name)

@socketio.on('replot')
def replot(app_state):
    HeroesStats = {}
    if app_state['mode'] == 'competitive':
        HeroesStats = HeroesStatsCompetitive
    elif app_state['mode'] == 'quickplay':
        HeroesStats = HeroesStatsQuickPlay
    hero = app_state['hero']
    units = ""
    allvars = getAllHeroInfoName(HeroesStats,hero)
    allvars.sort()
    data = []
    traces = []
    for ii,p in enumerate(HeroesStats.keys()):
        pp = p[0:p.find("-")]
        xx, yy, my_xticks = [], [], []
        for i,var in enumerate(allvars):
            xx.append(i)
            if not var in HeroesStats[p][hero]:
                yy.append(0)
            else:
                yy.append(myConvToFloat(HeroesStats[p][hero][var]))
                if("%" in HeroesStats[p][hero][var]): units = " (%)"
                if("hour" in HeroesStats[p][hero][var]): units = " h"
                if("hours" in HeroesStats[p][hero][var]): units = " h"
                if("minute" in HeroesStats[p][hero][var]): units = " min"
                if("minutes" in HeroesStats[p][hero][var]): units = " min"
                if("seconds" in HeroesStats[p][hero][var]): units = " sec"
                if("second" in HeroesStats[p][hero][var]): units = " sec"
                else: units = ""
            my_xticks.append(var+units)

        traces.append(Scatter({'x':my_xticks, 'y':yy, 'mode':'markers', 'name':pp,
                              'marker':{'symbol':"line-ew-open",'size':6,'line':{'width':4}}}
        ))
    fig = {
        'layout':{
            'title':hero,
            'xaxis':{
                'title':'',
                'titlefont':{'family':'Arial, sans-serif',
                             'size':18,'color':'lightgrey'},
                'showticklabels':True,
                'tickangle':35,
                'tickfont':{'family':'Old Standard TT, serif',
                            'size':8,'color':'black'},
            },
            'yaxis':{
                'title':'stats',
                'titlefont':{'family':'Arial, sans-serif','size':18,'color':'lightgrey'},
                'showticklabels':True,
                'tickangle':0,
                'tickfont':{'family':'Old Standard TT, serif','size':18,'color':'black'},
                'type':'log'
            }
        },
        'data': traces
    }
         
    messages = [{'id': 'Scatter',
                 'task': 'newPlot',
                 'data': fig['data'],
                 'layout': fig['layout'] }]

    emit('postMessage', json.dumps(messages, cls=plotly.utils.PlotlyJSONEncoder))
    


if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=5000)
