
DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASE_ENGINE = 'postgresql_psycopg2'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'oppian'              # Or path to database file if using sqlite3.
DATABASE_USER = 'oppian'             # Not used with sqlite3.
DATABASE_PASSWORD = 'ceelness22'         # Not used with sqlite3.
DATABASE_HOST = 'localhost'             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# the twitter email account of the site 
TWITTER_EMAIL = "twitter@oppian.com"
TWITTER_USER  = "oppian"
# the password for the account referenced by the twitter email address above
TWITTER_PASSWORD = "deteenee52" # oppian
# the name of the agent making the requests
TWITTER_AGENT_STR = "oppian.com"
# how often to check the tweet status

# s3 storage
AWS_STORAGE_BUCKET_NAME = 'oppian-prod-files'