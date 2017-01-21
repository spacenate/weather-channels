import requests
import json
from urllib import urlencode
from bs4 import BeautifulSoup

try:
    import ui
    import console
except:
    pass

#http://omz-software.com/pythonista/docs/ios/index.html

def main():
    stations = getStationsCached('CO')
    stations = addChannelInfo(stations, 'BC Link')

    setupView(stations)

    # todo - prompt user for state
    # todo - download image of state from e.g. http://www.nws.noaa.gov/nwr/Maps/PHP/CO.php

def setupView(stations):
    view = ui.View()

    view.name = 'Weather Stations'
    view.background_color = 'white'

    # dataSource = stationTableViewDataSource()
    # dataSource.setData(stations)

    table = ui.TableView()
    table.width = view.width
    table.height = view.height
    table.flex = 'WH'
    table.data_source = ui.ListDataSource(('CO','UT'))
    table.delegate = locationTableViewDelegate()
    view.add_subview(table)

    view.present('sheet')

def printConsole(stations):
    print('%s%s%s' % ('Sign'.ljust(8), 'Station'.ljust(18), 'Channel'))
    print('%s%s%s' % ('----'.ljust(8), '-------'.ljust(18), '-------'))
    for station in stations:
        print('%s%s%s' % (station['call-sign'].ljust(8), station['site'].ljust(18), station['channel']))

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

class locationTableViewDelegate (object):
    def tableview_did_select(self, tableview, section, row):
        # Called when a row was selected.
        @ui.in_background
        def alert():
            console.alert('Row selected', tableview.data_source.items[row])
        alert()

    def tableview_did_deselect(self, tableview, section, row):
        # Called when a row was de-selected (in multiple selection mode).
        pass

    def tableview_title_for_delete_button(self, tableview, section, row):
        # Return the title for the 'swipe-to-***' button.
        return 'Delete'

class stationTableViewDataSource (object):
    def setData(self, stations):
        self.stationData = stations

    def tableview_number_of_sections(self, tableview):
        # Return the number of sections (defaults to 1)
        return 1

    def tableview_number_of_rows(self, tableview, section):
        # Return the number of rows in the section
        return len(self.stationData)

    def tableview_cell_for_row(self, tableview, section, row):
        # Create and return a cell for the given section/row
        cell = ui.TableViewCell()

        cell.content_view.flex = 'WH'
        cell.content_view.width = tableview.width
        #cell.content_view.height = tableview.height

        callSign = ui.Label()
        callSign.text = self.stationData[row]['call-sign']
        callSign.width = 100
        callSign.height = cell.content_view.height
        callSign.x = 16
        callSign.text_color = 'gray'
        cell.content_view.add_subview(callSign)

        site = ui.Label()
        site.text = self.stationData[row]['site']
        site.width = cell.content_view.width
        site.height = cell.content_view.height
        site.x = 116
        cell.content_view.add_subview(site)

        channel = ui.Label()
        channel.text = self.stationData[row]['channel']
        channel.width = cell.content_view.width - 24
        channel.height = cell.content_view.height
        channel.flex = 'WH'
        channel.alignment = ui.ALIGN_RIGHT
        cell.content_view.add_subview(channel)
        
        return cell

    def tableview_title_for_header(self, tableview, section):
        # Return a title for the given section.
        # If this is not implemented, no section headers will be shown.
        pass

    def tableview_can_delete(self, tableview, section, row):
        # Return True if the user should be able to delete the given row.
        return False

    def tableview_can_move(self, tableview, section, row):
        # Return True if a reordering control should be shown for the given row (in editing mode).
        return False

if __name__ == "__main__":
    main()
