from craigslist import CraigslistForSale
from Logger import Logger
from configparser import ConfigParser
from connectDb import connectDb, disconnectDb
import slack
import time
import json
import requests
import pyodbc
import sys

# import config parser and configuration, object declaration
config = ConfigParser()
config.read('test_config.ini')

site = config.get('OPTIONS', 'site')
category = config.get('OPTIONS', 'category')
sortby = config.get('OPTIONS', 'sortBy')
maxresults = config.get('OPTIONS', 'maxResults')
sleeptime = config.get('OPTIONS', 'sleepTime')
slackurl = config.get('OPTIONS', 'slackURL')
maxprice = config.get('FILTERS', 'maxPrice')
minprice = config.get('FILTERS', 'minPrice')
squery = config.get('FILTERS', 'query')
sdistance = config.get('FILTERS', 'searchDistance')
szipcode = config.get('FILTERS', 'zipCode')
titlestatus = config.get('FILTERS', 'autoTitleStatus')
hasimage = config.get('FILTERS', 'hasImage')
make = config.get('FILTERS', 'make')
model = config.get('FILTERS', 'model')
minyear = config.get('FILTERS', 'minYear')
maxyear = config.get('FILTERS', 'maxYear')
minmiles = config.get('FILTERS', 'minMiles')
maxmiles = config.get('FILTERS', 'maxMiles')

clfs = CraigslistForSale(site=site, category=category, filters={'query': squery, 'max_price': int(maxprice), 'min_price': int(minprice), 'zip_code': szipcode, 'search_distance': sdistance, 'has_image': hasimage, 'make': make, 'model': model, 'min_year': minyear, 'max_year': maxyear, 'min_miles': minmiles, 'max_miles': maxmiles})

def init():
    totalListings = str(clfs.get_results_approx_count())
    Logger.writeAndPrintLine('Scraping all ' + totalListings + ' results matching criteria:\n', 0)

    results = clfs.get_results(sort_by=sortby, limit=int(maxresults))

    for r in results:
        print(r)


if __name__ == '__main__':
    init()