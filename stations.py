# coding: utf-8
from stationTableView import stationTableView
import ui

STATES = {
    'Alabama': 'AL',
    'Montana': 'MT',
    'Alaska': 'AK',
    'Nebraska': 'NE',
    'Arizona': 'AZ',
    'Nevada': 'NV',
    'Arkansas': 'AR',
    'New Hampshire': 'NH',
    'California': 'CA',
    'New Jersey': 'NJ',
    'Colorado': 'CO',
    'New Mexico': 'NM',
    'Connecticut': 'CT',
    'New York': 'NY',
    'Delaware': 'DE',
    'North Carolina': 'NC',
    'Florida': 'FL',
    'North Dakota': 'ND',
    'Georgia': 'GA',
    'Ohio': 'OH',
    'Hawaii': 'HI',
    'Oklahoma': 'OK',
    'Idaho': 'ID',
    'Oregon': 'OR',
    'Illinois': 'IL',
    'Pennsylvania': 'PA',
    'Indiana': 'IN',
    'Rhode Island': 'RI',
    'Iowa': 'IA',
    'South Carolina': 'SC',
    'Kansas': 'KS',
    'South Dakota': 'SD',
    'Kentucky': 'KY',
    'Tennessee': 'TN',
    'Louisiana': 'LA',
    'Texas': 'TX',
    'Maine': 'ME',
    'Utah': 'UT',
    'Maryland': 'MD',
    'Vermont': 'VT',
    'Massachusetts': 'MA',
    'Virginia': 'VA',
    'Michigan': 'MI',
    'Washington': 'WA',
    'Minnesota': 'MN',
    'West Virginia': 'WV',
    'Mississippi': 'MS',
    'Wisconsin': 'WI',
    'Missouri': 'MO',
    'Wyoming': 'WY'
}

def main():
    setupView(sorted(STATES.iterkeys()))

def setupView(states):
    view = ui.View()
    view.name = 'Weather Stations'
    view.background_color = 'white'

    table = ui.TableView()
    table.width = view.width
    table.height = view.height
    table.flex = 'WH'
    table.data_source = ui.ListDataSource(states)
    table.delegate = locationTableViewDelegate()
    view.add_subview(table)

    nav = ui.NavigationView(view)
    nav.present('sheet')

class locationTableViewDelegate (object):
    def tableview_did_select(self, tableview, section, row):
        # Called when a row was selected.
        state = tableview.data_source.items[row]
        abbr = STATES[state]

        table = stationTableView(abbr)
        table.name = state
        table.width = tableview.superview.width
        table.height = tableview.superview.height
        table.flex = 'WH'

        tableview.navigation_view.push_view(table)

if __name__ == "__main__":
    main()
