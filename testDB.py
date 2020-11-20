from Logger import Logger
import pyodbc

conn_str = (
    "DRIVER={PostgreSQL Unicode};"
    "DATABASE=clScraper;"
    "UID=postgres;"
    "PWD=postgres;"
    "SERVER=localhost;"
    "PORT=5432;"
    )

def connectDb():
    print('installed ODBC drivers: ')
    print(pyodbc.drivers())
    print('Testing db connection...')
    try:
        cnxn = pyodbc.connect(conn_str)
        crsr = cnxn.cursor()
        print('success')
    except:
        Logger.writeAndPrintLine('Unable to connect to the database.', 3)


def disconnectDb(cnxn):
    cnxn.close()


if __name__ == '__main__':
    connectDb()