import psycopg2
from data import get_data
from pprint import pprint as pp
from ConfigParser import SafeConfigParser
from datetime import datetime
import time
import pytz
from collections import Counter

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


def populate_db(screen_names):
    """ Get data and populate the `analytics_data` table. """
    
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
    data = []
    for name in screen_names:
      user_data = get_data(name)
      for u in user_data:
        data.append(u)

    for row in data:
      #print 'xxxxxxxxxxx'
      #print 'ROW', row
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


def timeblock_dist(acc):
  """ For a given account check how many tweets we observed in each of the 
  6 timeblocks (24 / 4)"""
  stamps = query_timestamps(acc)
  timeblocks = []
  for s in stamps:
    stamp = s[0]
    timeblocks.append(get_timeblocks(stamp))
  distribution = Counter(timeblocks)
  return dict(distribution)

def day_of_week_dist(acc):
  """For a given account check how many tweets we observed for each day of 
  week where Monday is 0 and Sunday is 6."""
  stamps = query_timestamps(acc)
  days = []
  for s in stamps:
    stamp = s[0]
    days.append(stamp.weekday())
  distribution = Counter(days)
  return dict(distribution)

# utility functions --------------------------------------|
    
def convert_date(s):
    """Convert Twitter's `created_at` string to python's datetime object."""
    d = datetime.strptime(s,'%a %b %d %H:%M:%S +0000 %Y').replace(tzinfo=pytz.UTC)
    return d

def query_timestamps(acc):
  cursor = conn.cursor()
  cursor.execute('SELECT created_at FROM analytics_data where account =  %s;',(acc,))
  d = cursor.fetchall()
  return d

def get_timeblocks(s):
    """24 hours divided in 6 blocks, 4 hours each."""
    # get the hour the tweet
    r = s.hour
    return r / 4

def query_retweets(acc):
  cursor = conn.cursor()
  cursor.execute('SELECT retweets FROM analytics_data where account =  %s;',(acc,))
  d = cursor.fetchall()
  r = []
  for i in d:
    r.append(i[0])
  return r

def query_faves(acc):
  cursor = conn.cursor()
  cursor.execute('SELECT faves FROM analytics_data where account =  %s;',(acc,))
  d = cursor.fetchall()
  r = []
  for i in d:
    r.append(i[0])
  return r

def query_all():
  cursor = conn.cursor()
  cursor.execute('SELECT * FROM analytics_data')
  d = cursor.fetchall()
  return d


if __name__ == "__main__":

    screen_names = ['harrys', 'Gillette', 'DollarShaveClub', 'SchickHydro']
    #populate_db(screen_names)
    
    val1 = 'harrys'
    val2 = 'DollarShaveClub'
    print screen_names
    print ' '

    for n in screen_names:
      print 'TIMEBLOCKS', timeblock_dist(n)
    print '___________________'
    for n in screen_names:
      print 'DAY_OF_WEEK', day_of_week_dist(n)

    print ' '
    print 'RETWEETS', query_retweets(val1)
    print 'FAVES', query_faves(val1)

