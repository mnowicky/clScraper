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
config.read('config.ini')

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

rList = []
last_insert = '0'

######################## MAIN CL REQUEST ########################

clfs = CraigslistForSale(site=site, category=category, filters={'query': squery, 'max_price': int(maxprice), 'min_price': int(minprice), 'zip_code': szipcode, 'search_distance': sdistance, 'has_image': hasimage, 'make': make, 'model': model, 'min_year': minyear, 'max_year': maxyear, 'min_miles': minmiles, 'max_miles': maxmiles})

###################### START PROGRAM ############################

def init():
    totalListings = str(clfs.get_results_approx_count())
    Logger.writeAndPrintLine('Scraping all ' + totalListings + ' results matching criteria:\n', 0)

    results = clfs.get_results(sort_by=sortby, limit=int(maxresults))

    #prepForInsert(results)
    f = open('listings.txt', 'a')
    f.write(results)
    f.close
    

    Logger.writeAndPrintLine('Starting main loop...', 0)
    Logger.writeAndPrintLine('Checking for new results every ' + str(sleeptime) + ' seconds.', 0)
    loop()


def loop():
    while True:
        Logger.writeAndPrintLine('Checking for new listings...', 0)
        results = clfs.get_results(sort_by=sortby, limit=int(maxresults))
        prepForInsert(results)
        time.sleep(int(sleeptime))


###################### PREP FOR INSERTION ######################
# This function runs at startup and upon detecting a new listing 
# to grab listing(s), parse them into lists.
################################################################

def prepForInsert(results):
    rList = [list(r.values()) for r in results]

    #print(rList)

    for l in rList:
        r_id = str(l[0])
        r_name = str(l[2])
        r_name = r_name.replace("'", "")
        r_url = str(l[3])
        r_datetime = str(l[4])
        r_updated = str(l[5])
        r_price = str(l[6])
        r_where = str(l[7])


        #insertToDatabase(r_id, r_name, r_url, r_datetime, r_updated, r_price, r_where)
        f=open('listings.txt', 'a')
        f.write(r_id, r_name, r_url, r_datetime, r_updated, r_price, r_where)
        f.close()


################### INSERT TO DATABASE ###########################
# Makes connection to database, identifies the last listing 
# inserted, compares newest listing to last listing. If new
# insert into database and notify.
##################################################################

def insertToDatabase(id, name, url, date, updated, price, where):
    global last_insert

    cnxn = connectDb()
    cursor = cnxn.cursor()
    rows = cursor.execute("SELECT post_id from listings order by tstmp desc").fetchall()
    results = [row[0] for row in rows]

    #print(results)

    try:
        if id not in results:
            Logger.writeAndPrintLine('Adding ' + id + ' to database...', 0)
            cursor.execute("insert into listings (post_id, timestamp, url, subject, price, location, tstmp) values ("+id+", '"+date+"', '"+url+"', '"+name+"', '"+price+"', '"+where+"', (current_timestamp));")
            cursor.commit()
            Logger.writeLine('done.', 0)
            last_insert = id

            Logger.writeAndPrintLine('Posting ' + id + ' to Slack...', 0)
            slacklist = [date, name, price, where, url]
            slackmsg = str(slacklist)
            postToSlack(slackmsg)
            Logger.writeLine('done.', 0)

    except:
        Logger.writeAndPrintLine('Error inserting ID ' + id + ' into database.', 0)
        pass

    cursor.close()
    disconnectDb(cnxn)


##################### POST TO SLACK ########################
# After successfully inserting to db, this function posts 
# the listing to the slack #app channel. 
############################################################

def postToSlack(message):
    post = {"text": "{0}".format(message)}

    Logger.writeLine('Posting listing to slack...', 0)
    try:
        json_data = json.dumps(post)
        print(post)

        return requests.post(slackurl,
                                data=json_data.encode('ascii'),
                                headers={'Content-Type': 'application/json'})

    except Exception as em:
        print("Exception: " + str(em))


if __name__ == '__main__':
    init()