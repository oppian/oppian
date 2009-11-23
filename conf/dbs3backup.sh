#!/bin/bash

DB_NAME=%DB_NAME%
FILENAME=$DB_NAME-db-`date +%Y%m%d%H%M`
BUCKET=%DB_BACKUP_BUCKET%
export AWS_SECRET_ACCESS_KEY=%AWS_SECRET_ACCESS_KEY%
export AWS_ACCESS_KEY_ID=%AWS_ACCESS_KEY_ID%

if [ "$1" != "" ]; then
        FILENAME=$1
fi

# dump to filename
sudo -u postgres pg_dump -Fc $DB_NAME > /tmp/$FILENAME

# save to s3
s3cmd put $BUCKET:$FILENAME /tmp/$FILENAME

echo "Saved database '$DB_NAME' to $BUCKET:$FILENAME"

# delete tmp file
rm /tmp/$FILENAME
