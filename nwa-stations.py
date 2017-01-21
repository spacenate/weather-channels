from stationTableViewDataSource import stationTableViewDataSource
import ui

def main():
    stateList = ('CO','UT')
    setupView(stateList)
    # todo - download image of state from e.g. http://www.nws.noaa.gov/nwr/Maps/PHP/CO.php

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

        table = ui.TableView()
        table.name = '%s Stations' % state
        table.width = tableview.superview.width
        table.height = tableview.superview.height
        table.flex = 'WH'
        table.data_source = stationTableViewDataSource(table, state)

        tableview.navigation_view.push_view(table)

    def tableview_did_deselect(self, tableview, section, row):
        # Called when a row was de-selected (in multiple selection mode).
        pass

    def tableview_title_for_delete_button(self, tableview, section, row):
        # Return the title for the 'swipe-to-***' button.
        return 'Delete'



if __name__ == "__main__":
    main()
