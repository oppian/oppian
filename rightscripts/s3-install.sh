#!/bin/bash -e
#
# Copyright (c) 2007-2009 RightScale, Inc, All Rights Reserved Worldwide.
#
# Parameters to retrieve the tarball with the source
# $DEPLOY_DIR  -- Installed directory


#
# Test for a reboot,  if this is a reboot just skip this script.
#
if test "$RS_REBOOT" = "true" ; then
  echo "Skip code install on reboot."
  logger -t RightScale "Skip code install on reboot."
  exit 0 # Leave with a smile ...
fi

cd $DEPLOY_DIR
chmod +x manage.py
flip -u manage.py
./manage.py syncdb --noinput

exit 0