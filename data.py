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

def get_timeline(screen_name):
    """(str) -> list of `Status` objects
    Get the timeline data for a given user."""
    api = twitter.Api(consumer_key=API_KEY,
                      consumer_secret=API_SECRET,
                      access_token_key=TOKEN,
                      access_token_secret=TOKEN_SECRET,
                      sleep_on_rate_limit=True) # app will sleep when it hits a rate limit
    timeline = api.GetUserTimeline(screen_name=screen_name)
    return timeline

def get_data(screen_name):
    """ (str) -> list of lists
    Extract data needed for analytics."""
    timeline = get_timeline(screen_name)
    data = []
    # t is a `Status` object 
    for t in timeline:
        data.append([t.id,
                     t.user.screen_name,
                     t.text,
                     t.created_at,
                     t.retweet_count,
                     t.favorite_count])
    return data

if __name__ == '__main__':
    pp(get_data('harrys'))
