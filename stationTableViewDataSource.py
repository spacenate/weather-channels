import requests
import json
from urllib import urlencode
from bs4 import BeautifulSoup

class stationTableViewDataSource (object):
    def __init__(self, state):
        stationData = self.getStationsCached(state)
        self.stationData = self.addChannelInfo(stationData, 'BC Link')

    def addChannelInfo(self, stations, device):
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

    def getStationsCached(self, state):
        stations = self.cacheGet(state)
        if (stations is False):
            stations = self.getStations(state)
            self.cacheSet(state, stations)
        return stations

    def getStations(self, state):
        baseURl = 'http://www.nws.noaa.gov/nwr/coverage/stations.php'
        query   = {'State': state}
        reqUrl  = '%s?%s' % (baseURl, urlencode(query))
        print('GET %s' % reqUrl)
        req     = requests.get(reqUrl)
        results = grokMarkup(req.content)
        return results

    def grokMarkup(self, markup):
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

    def cacheSet(self, key, value):
        cache = open('stations_cache_%s' % key, 'w')
        cache.truncate()
        cache.write(json.dumps(value))
        cache.close()

    def cacheGet(self, key):
        try:
            cache = open('stations_cache_%s' % key)
        except Exception:
            return False
        value = cache.read()
        cache.close()
        if (len(value) is 0):
            return False
        return json.loads(value)

    '''TableViewDataSource methods'''

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
