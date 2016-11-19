import psycopg2
from data import get_data
from pprint import pprint as pp
from ConfigParser import SafeConfigParser
from datetime import datetime
import time
import pytz

def convert_date(s):
    """Convert Twitter's `created_at` string to python's datetime object."""
    d = datetime.strptime(s,'%a %b %d %H:%M:%S +0000 %Y').replace(tzinfo=pytz.UTC)
    return d


def populate_db(screen_names):
    """Insert data to the db."""
    config = SafeConfigParser()
    config.read('config.ini')
    user = config.get('login', 'user')
    password = config.get('login', 'password')
    
    try:
        conn = psycopg2.connect(host='localhost',
                                dbname='twitter',
                                user= user,
                                password = password)
    except:
        print "I am unable to connect to the database."
    
    cursor = conn.cursor()
    # create a table
    cursor.execute("DROP TABLE IF EXISTS ANALYTICS_DATA")
    cursor.execute("""CREATE TABLE IF NOT EXISTS ANALYTICS_DATA
           (ID               BIGINT PRIMARY KEY    NOT NULL,
           ACCOUNT           TEXT                  NOT NULL,
           TWEET             TEXT                  NOT NULL,
           CREATED_AT        TIMESTAMP                  NOT NULL,
           RETWEETS          INT                   NOT NULL,
           FAVES             INT                   NOT NULL);""")
    print "Table created successfully"
    # populate the table with data
    data = []
    for name in screen_names:
      user_data = get_data(name)
      for u in user_data:
        data.append(u)

    for row in data:
      print 'xxxxxxxxxxx'
      print 'ROW', row
      # row example [756884265451790336, u'SchickHydro', u'@DavidJMays Appreciate the love!', u'Sat Jul 23 16:10:45 +0000 2016', 1, 1]
      id = row[0]
      account = row[1]
      tweet = row[2]
      created_at = convert_date(row[3])
      retweets = row[4]
      faves = row[5]
      query = cursor.mogrify("""INSERT INTO ANALYTICS_DATA (
        ID, ACCOUNT, TWEET, CREATED_AT, RETWEETS, FAVES) VALUES (
        %s, %s,      %s,    %s,         %s,       %s)""",
        (id, account, tweet, created_at, retweets, faves))
      cursor.execute(query)

    conn.commit()
    conn.close()

if __name__ == "__main__":

    screen_names = ['harrys', 'gillette', 'dollarshaveclub', 'SchickHydro']
    print populate_db(screen_names)
