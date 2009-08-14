#!/bin/bash -e
#
# Copyright (c) 2007-2009 RightScale, Inc, All Rights Reserved Worldwide.
#
# Parameters to retrieve the tarball with the source
# $DEPLOY_DIR  -- Installed directory
# $HOSTNAME    -- Hostname of server

#
# Test for a reboot,  if this is a reboot just skip this script.
#
if test "$RS_REBOOT" = "true" ; then
  echo "Skip code install on reboot."
  logger -t RightScale "Skip code install on reboot."
  exit 0 # Leave with a smile ...
fi

## set hostname
hostname $HOSTNAME

## syncdb
cd $DEPLOY_DIR
chmod +x manage.py
flip -u manage.py
./manage.py syncdb --noinput

## chown
echo "Changing ownership to $APP_OWNER..."
chown -R $APP_OWNER $DEPLOY_DIR
if [ ! $? ]; then
  echo "Failed to change the owner."
  exit -1
fi

exit 0