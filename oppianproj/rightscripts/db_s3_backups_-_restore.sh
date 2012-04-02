#!/bin/bash -e
#
# Restores a db postgres dump file from s3
# Note: Don't use as a boot script.
#
# $DB_NAME -- Database name
# $DB_BACKUP_BUCKET -- Bucket to restore backup from
# $DB_RESTORE_FILE -- The filename in s3 to restore from
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

## get file s3
s3cmd get $DB_BACKUP_BUCKET:$DB_RESTORE_FILE /tmp/$DB_RESTORE_FILE

## dropdb and create
sudo -u postgres dropdb $DB_NAME
sudo -u postgres createdb -O $DB_USER $DB_NAME

## restore
sudo -u postgres pg_restore --dbname=$DB_NAME /tmp/$DB_RESTORE_FILE

## restart apache
/etc/init.d/apache2 restart

exit 0
