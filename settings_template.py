
DEBUG = $DEBUG
TEMPLATE_DEBUG = DEBUG

DATABASE_ENGINE = 'postgresql_psycopg2'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = '$DB_NAME'              # Or path to database file if using sqlite3.
DATABASE_USER = '$DB_USER'             # Not used with sqlite3.
DATABASE_PASSWORD = '$DB_PASS'         # Not used with sqlite3.
DATABASE_HOST = '$DB_HOST'             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

SITE_DOMAIN = "$SITE_DOMAIN"

# the twitter email account of the site 
TWITTER_EMAIL = "twitter@oppian.com"
TWITTER_USER  = "oppian"
# the password for the account referenced by the twitter email address above
TWITTER_PASSWORD = "deteenee52" # oppian
# the name of the agent making the requests
TWITTER_AGENT_STR = "oppian.com"

# s3 storage
AWS_STORAGE_BUCKET_NAME = 'oppian-prod-files'