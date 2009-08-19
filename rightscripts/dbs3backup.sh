#!/bin/bash -e
#
# Copies the file for the cron job to the postgres dumps to s3 backups
#
# DB_NAME -- Database name
# DB_BACKUP_BUCKET -- Bucket to save backup into
# CRON_JOB -- Location to cron job script (relative to DEPLOY_DIR)
# DEPLOY_DIR -- Location of release
# Ensure the S3 credentials are passed in the environment for the backup script to access the disk
# $AWS_SECRET_ACCESS_KEY -- Amazon WS credential: secret access key
# $AWS_ACCESS_KEY_ID     -- Amazon WS credential: access key


#
# Test for a reboot,  if this is a reboot just skip this script.
#
if test "$RS_REBOOT" = "true" ; then
  echo "Skip code install on reboot."
  logger -t RightScale "Skip code install on reboot."
  exit 0 # Leave with a smile ...
fi

## copy cron job to new place
CRON_FILENAME=`basename $CRON_JOB`
cp $DEPLOY_DIR$CRON_JOB /etc/cron.daily/$CRON_FILENAME

## replace vars
cronfile=/etc/cron.daily/$CRON_FILENAME

sed -i "s/%DB_NAME%/$DB_NAME/g" $cronfile
sed -i "s/%DB_BACKUP_BUCKET%/$DB_BACKUP_BUCKET/g" $cronfile
sed -i "s/%AWS_SECRET_ACCESS_KEY%/$AWS_SECRET_ACCESS_KEY/g" $cronfile
sed -i "s/%AWS_ACCESS_KEY_ID%/$AWS_ACCESS_KEY_ID/g" $cronfile

## set exec
chmod +x $cronfile

exit 0