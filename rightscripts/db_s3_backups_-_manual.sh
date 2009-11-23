#!/bin/bash -e
#
# Does a manual backup of the db
# Note: Don't use as a boot script.
#
# $CRON_JOB -- Location to cron job script (relative to DEPLOY_DIR)
# $DB_RESTORE_FILE -- The filename to backup into
#

## run the cron script
CRON_FILENAME=`basename $CRON_JOB`
/etc/cron.daily/$CRON_FILENAME $DB_RESTORE_FILE

exit 0