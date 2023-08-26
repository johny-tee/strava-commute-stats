# strava-commute-stats
# Export commute stats from Strava.com

## Usage
```
usage: monthly-commute-export.py [-h] [-m MONTH] [-y YEAR] [-M MODE] [-T TAG]

Strava commute activities reporting

options:
  -h, --help                show this help message and exit
  -m MONTH, --month MONTH   number of the month to generate the report
  -y YEAR, --year YEAR      year to generate the report
  -M MODE, --mode MODE      The way how Commute activities are marked ('C' for Strava Commute flag, 'T' for Tag in Activity name)
  -T TAG, --tag TAG         In 'T' mode this is how you input the tag value, script will search for this value in Activity name field
```
