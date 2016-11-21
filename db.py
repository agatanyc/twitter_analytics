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
  stamps = query_tweets(acc)
  timeblocks = []
  for s in stamps:
    stamp = s[0]
    timeblocks.append(get_timeblocks(stamp))
  distribution = Counter(timeblocks)
  return dict(distribution)

def day_of_week_dist(acc):
  """For a given account check how many tweets we observed for each day of 
  week where Monday is 0 and Sunday is 6."""
  stamps = query_tweets(acc)
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

def query_tweets(acc):
  """(str) -> list,
  query the db for `created at`,`retweets` and `faves`.
  """
  cursor = conn.cursor()
  cursor.execute('SELECT created_at, retweets, faves FROM analytics_data where account =  %s;',(acc,))
  d = cursor.fetchall()
  #print get_timeblocks(d[0][0])
  #print d[0][0].weekday()
  return d

def get_faves_and_times(acc):
  """(str) -> list
  How many times each tweet was faved."""
  tweets = query_tweets(acc)
  faves = [(t[2], t[0].hour) for t in tweets]
  return faves

def get_retweets_and_times(acc):
  """(str) -> list
  How many times each tweet was retweeted."""
  tweets = query_tweets(acc)
  ret = [(t[1], t[0].hour) for t in tweets]
  return ret

"""
#----THIS BELOW WILL MOST LIKELLY GO

def get_hour(acc):
  '(str) -> list
  query the db for the time each tweet was created.'
  stamps = query_tweets(acc)
  hours = []
  for s in stamps:
    stamp = s[0]
  return hours

def get_timeblocks(s):
    '(python date object) -> int
    7 days in a week, 24 hours each divided in 6 blocks, 4 hours each. 
    We are creating `time of week` where Monday midnight is 0.'
    # get the hour of the tweet
    r = s.hour
    # get the weekday and the timeblock (Monday is range 0-5, Tuseday is 6-11 etc..)
    return r / 4 + (6 * s.weekday())
"""
if __name__ == "__main__":
    
    val1 = 'harrys'
    val2 = 'DollarShaveClub'
    print 'XXXXXX'
    
    print get_faves_and_times(val1)

