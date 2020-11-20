Built on python-craigslist module:
https://pypi.org/project/python-craigslist/

Designed to be used with a postgresql database containing a 'clscraper' db and 'listings' table. 
Alternately you can change the 'use_database' {yes|no} configuration option to output listings to
listings.txt instead. 

To test new filters and outfit this program to meet your needs, please utilize the 'testScrape.py' 
and 'test_config.ini'. 
Note: there seems to be a bug within the python-craigslist module, particularly
with the auto_* filters. They don't work- as they seem to be trying to take
each character of the filter value as the value itself, and error out. 

Pyodbc drivers:
You will need to install pyodbc on your system and determine which postgresql driver to use
based on what you have available on your system. 
> pyodbc.drivers()

For me, ubuntu used "PostgreSQL Unicode", while windows utilized "PostgreSQL ODBC Driver(ANSI)". 
This is configured within connectDb.py. 

Slack:
This program is designed to notify users via a slack channel when a new listing is detected. 
The url to the slack channel needs to be placed inside the slackURL option in config.ini. 
This function can be disabled if not desired. 

Config.ini
This config is setup to accomodate scraping for auto listings in CraigslistForSale sub-class of python-craigslist. 
This can be modified to work with any of the sub-classes. View available filters and options in the project docs. 

