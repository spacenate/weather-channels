# weather-channels
Download and display information about NOAA weather radio stations and their corresponding BCA BC Link channel numbers. This Python script is intended to be run in omz:software's Pythonista app, and makes use their `ui` and `console` modules, as well as Requests and BeautifulSoup 4 for fetching NOAA weather radio station data.

Station data and coverage map images are written to disk, so the after being downloaded, they may be accessed again later without an internet connection. Station data is downloaded for each state individually, when they are accessed for the first time.

### Possible improvements
- show 'downloading' feedback while downloading new state
- show indication of which states' station information has been downloaded
- allow managing downloaded station information (delete, update)

### License
MIT
