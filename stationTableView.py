# coding: utf-8
import requests
import json
from urllib import urlencode
from bs4 import BeautifulSoup
import ui
from console import quicklook

class stationTableView (ui.View):
    def __init__(self, state, *args, **kwargs):
        super(stationTableView, self).__init__(*args, **kwargs)

        table = ui.TableView()
        table.name = 'stations'
        table.delegate = stationTableViewDelegate()
        table.data_source = self.data_source = stationTableViewDataSource(state)
        table.reload_data()

        table.width = self.width
        table.height = self.height
        table.flex = 'WH'

        self.add_subview(table)

    def viewCoverageMap(self):
        @ui.in_background
        def animate():
            quicklook(self.data_source.imageName)
        animate()

    def getRowDetailsView(self, row):
        view = ui.View()
        view.background_color = 'white'
        view.name = 'Station Details'

        table = ui.TableView()
        table.width = view.width
        table.height = view.height
        table.flex = 'WH'
        data = self.data_source.stationData[row]
        table.data_source = stationDetailTableViewDataSource((
            {'title': 'Site Name', 'content': data['site']},
            {'title': 'Transmitter Name', 'content': data['transmitter']},
            {'title': 'Call Sign', 'content': data['call-sign']},
            {'title': 'Frequency', 'content': data['frequency']},
            {'title': 'Channel', 'content': data['channel']},
            {'title': 'Power', 'content': data['power']},
            {'title': 'Weather Forecast Office', 'content': data['wfo']}
        ))
        view.add_subview(table)
        return view

class stationTableViewDelegate (object):
    def tableview_did_select(self, tableview, section, row):
        if (row == 0):
            tableview.superview.viewCoverageMap()
        else:
            view = tableview.superview.getRowDetailsView(row - 1)
            tableview.navigation_view.push_view(view)

class stationTableViewDataSource (object):
    NOAA_MAPS_URL = 'http://www.nws.noaa.gov/nwr/Maps/PHP/'

    def __init__(self, state):
        self.imageName = 'map_%s.gif' % state
        self.stationData = self.getStationsCached(state)

    def getStationsCached(self, state):
        stations = self.cacheGet(state)
        if (stations is False):
            stations, imgSrc = self.getStations(state)
            # write image to file
            img = requests.get(self.NOAA_MAPS_URL + imgSrc)
            with open(self.imageName, 'wb') as f:
                f.write(img.content)
            # cache station data
            self.cacheSet(state, stations)
        return stations

    def getStations(self, state):
        requestUrl = '%s%s.php' % (self.NOAA_MAPS_URL, state)
        response = requests.get(requestUrl)
        stations, imgSrc = self.grokMarkup(response.content)
        stations = self.addChannelInfo(stations, 'BC Link')
        return (stations, imgSrc)

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

    def grokMarkup(self, markup):
        soup = BeautifulSoup(markup, 'html.parser')
        stations = []

        # grab map image src
        imgSrc = soup.select('img[alt*=Map]')[0].get('src')

        # grab stations
        for row in soup.table.find_all('tr')[1:]:
            values = row.find_all('td')
            stations.append({
                'site':        values[0].string,
                'transmitter': values[1].string,
                'call-sign':   values[2].string,
                'frequency':   values[3].string,
                'power':       values[4].string,
                'wfo':         values[5].string
            })

        return (stations, imgSrc)

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

    def tableview_number_of_rows(self, tableview, section):
        return len(self.stationData) + 1

    def tableview_cell_for_row(self, tableview, section, row):
        cell = ui.TableViewCell()

        cell.content_view.flex = 'WH'
        cell.content_view.width = tableview.width

        if (row > 0):
            index = row - 1
            callSign = ui.Label()
            callSign.text = self.stationData[index]['call-sign']
            callSign.width = 100
            callSign.height = cell.content_view.height
            callSign.x = 16
            callSign.text_color = 'gray'
            cell.content_view.add_subview(callSign)

            site = ui.Label()
            site.text = self.stationData[index]['site']
            site.width = cell.content_view.width
            site.height = cell.content_view.height
            site.x = 116
            cell.content_view.add_subview(site)

            channel = ui.Label()
            channel.text = self.stationData[index]['channel']
            channel.width = cell.content_view.width - 24
            channel.height = cell.content_view.height
            channel.flex = 'WH'
            channel.alignment = ui.ALIGN_RIGHT
            cell.content_view.add_subview(channel)

        else:
            site = ui.Label()
            site.text = 'See Coverage Map'
            site.width = cell.content_view.width
            site.height = cell.content_view.height
            site.x = 16
            cell.content_view.add_subview(site)
            cell.accessory_type = 'disclosure_indicator'

        return cell

    def tableview_can_delete(self, tableview, section, row):
        return False

    def tableview_can_move(self, tableview, section, row):
        return False

class stationDetailTableViewDataSource (object):
    def __init__(self, data):
        self.data = data

    def tableview_number_of_sections(self, tableview):
        return 6

    def tableview_number_of_rows(self, tableview, section):
        return 1

    def tableview_cell_for_row(self, tableview, section, row):
        cell = ui.TableViewCell()
        cell.text_label.text = self.data[section]['content']
        return cell

    def tableview_title_for_header(self, tableview, section):
        return self.data[section]['title']

    def tableview_can_delete(self, tableview, section, row):
        return False

    def tableview_can_move(self, tableview, section, row):
        return False
