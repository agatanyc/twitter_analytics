Analytics of Harry's tweets and its competitors.

DEPENDENCIES:
1. pyhton
2. PostgreSQ L9.6.1
3. Twitter (python library)
4. plotly

5. To create your config file use ConfigParser.
You will need config.ini file with following format:

[credentials]          # credentials for Twitter API
api_key = 'your_key'
api_secret = 'your_secret'
token = 'your_token'
token_secret = 'your_secret'
[login]               # login to postgresql
user='your_user'
password = 'your_password'

