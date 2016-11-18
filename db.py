# postgresql tutorial
import psycopg2
from data import get_data
from pprint import pprint as pp
from ConfigParser import SafeConfigParser

# screen_names = ['harys', 'gillette', 'dollarshaveclub', 'SchickHydro']
def populate_db(screen_names):
    
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
           CREATED_AT        TEXT                  NOT NULL,
           RETWEETS          INT                   NOT NULL,
           FAVES             INT                   NOT NULL);""")
    print "Table created successfully"
    # populate the table with data
    data = []
    for name in screen_names:
      user_data = get_data(name)
      for u in user_data:
        data.append(u)
    pp(data)

    for row in data:
      print 'xxxxxxxxxxx'
      print 'ROW', row
      # row example [u'harrys',  u'@nascar_freak Appreciate you. #\U0001f44a', u'Thu Nov 17 16:04:30 +0000 2016', 0, 0]
      id = row[0]
      account = row[1]
      tweet = row[2]
      created_at = row[3]
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

    screen_names = ['harys', 'gillette', 'dollarshaveclub', 'SchickHydro']
    populate_db(screen_names)
