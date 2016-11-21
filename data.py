"""Analytics of Harry's Twitter Timeline."""
import twitter
from pprint import pprint as pp
from ConfigParser import SafeConfigParser

config = SafeConfigParser()
config.read('config.ini')
API_KEY = config.get('credentials', 'api_key' )
API_SECRET = config.get('credentials', 'api_secret')

TOKEN = config.get('credentials', 'token')
TOKEN_SECRET = config.get('credentials', 'token_secret')

api = twitter.Api(consumer_key=API_KEY,
                      consumer_secret=API_SECRET,
                      access_token_key=TOKEN,
                      access_token_secret=TOKEN_SECRET,
                      sleep_on_rate_limit=False) # app will sleep when it hits a rate limit

def get_data(screen_name):
    """ (str) -> list of lists
    Extract data needed for analytics."""
    # Get the timeline data for a given user.
    go = True
    data = []
    timeline = []
    
    # check that we keep getting data to avoid infiite loop
    # ensure we are getting as much data as Twitter api lets us
    max_id = None

    while go:
        api_call = api.GetUserTimeline(screen_name=screen_name,
                                        max_id=max_id,
                                        count=200,
                                        include_rts=False)

        timeline += api_call[1:]
        max_id = api_call[-1].id
        print max_id
        if len(api_call) < 2:
            go = False

    # t is a twitter `Status` object 
    for t in timeline:
        data.append([t.id,
                    t.user.screen_name,
                    t.text,
                    t.created_at,
                    t.retweet_count,
                    t.favorite_count])
    return data

if __name__ == '__main__':
    screen_name = 'harrys'
    get_data(screen_name)
