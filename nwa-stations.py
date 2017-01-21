import requests
import json
from urllib import urlencode
from bs4 import BeautifulSoup


def main():
    stations = getStationsCached('CO')
    stations = addChannelInfo(stations, 'BC Link')

    # todo - display table of stations and channels
    # todo - prompt user for state
    # todo - download image of state from e.g. http://www.nws.noaa.gov/nwr/Maps/PHP/CO.php

def addChannelInfo(stations, device):
    device     = device.upper()
    channelMap = {
        'BC LINK': {
            '162.550': '1',
            '162.400': '2',
            '162.475': '3',
            '162.425': '4',
            '162.450': '5',
            '162.500': '6',
            '162.525': '7',
            '161.650': '8',
            '161.775': '9',
            '161.750': '10',
            '162.000': '11'
        }
    }

    if (not channelMap[device]):
        return stations

    for index, station in enumerate(stations):
        frequency = station['frequency']
        stations[index]['channel'] = channelMap[device][frequency]

    return stations

def getStationsCached(state):
    stations = cacheGet(state)
    if (stations is False):
        stations = getStations(state)
        cacheSet(state, stations)
    return stations

def getStations(state):
    baseURl = 'http://www.nws.noaa.gov/nwr/coverage/stations.php'
    query   = {'State': state}
    reqUrl  = '%s?%s' % (baseURl, urlencode(query))
    print('GET %s' % reqUrl)
    req     = requests.get(reqUrl)
    results = grokMarkup(req.content)
    return results

def grokMarkup(markup):
    soup = BeautifulSoup(markup, 'html.parser')
    map = []

    for row in soup.table.find_all('tr')[1:]:
        values = row.find_all('td')
        map.append({
            'site':        values[0].string,
            'transmitter': values[1].string,
            'call-sign':   values[2].string,
            'frequency':   values[3].string,
            'power':       values[4].string
        })

    return map

def cacheSet(key, value):
    cache = open('stations_cache_%s' % key, 'w')
    cache.truncate()
    cache.write(json.dumps(value))
    cache.close()

def cacheGet(key):
    try:
        cache = open('stations_cache_%s' % key)
    except Exception:
        return False
    value = cache.read()
    cache.close()
    if (len(value) is 0):
        return False
    return json.loads(value)

if __name__ == "__main__":
    main()
