#!/bin/bash -e
#
# Downloads and unpacks the app
#
# $APPLICATION_CODE_BUCKET  -- Bucket where the tarball resides
# $APPLICATION_CODE_PACKAGE -- S3 Key of the tarball  (gzipped)
# $DEPLOY_DIR				-- The dir to deploy into
#
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

echo "Checking whether APPLICATION_CODE_BUCKET and APPLICATION_CODE_PACKAGE are set..."
if [ -z "$APPLICATION_CODE_BUCKET" -a -z "$APPLICATION_CODE_PACKAGE" ]; then 
  echo "Bucket and prefix not defined..."
  echo "skipping the retrieval of the application"
  exit -1
fi

## Find out about the old deploy directory
if [ -e $DEPLOY_DIR ]; then
  echo "Removing existing deploy directory..."
  rm -rf $DEPLOY_DIR
fi

## Create deploy dir
echo "Creating deploy directory..."
mkdir -p $DEPLOY_DIR

## Retrieve the code from S3 and unpack it
echo "Downloading $APPLICATION_CODE_PACKAGE from S3:$APPLICATION_CODE_BUCKET..."
s3cmd get $APPLICATION_CODE_BUCKET:$APPLICATION_CODE_PACKAGE /tmp/$APPLICATION_CODE_PACKAGE 

## Prepare dir
echo "Prepare to deploy..."
chmod 775 $DEPLOY_DIR

## Unpacking...
echo "Unpacking web application..."
echo "Extracting $APPLICATION_CODE_PACKAGE in $DEPLOY_DIR..."
tar -xzf /tmp/$APPLICATION_CODE_PACKAGE -C $DEPLOY_DIR
if [ ! $? ]; then
  echo "Failed to extract sources."
  exit -1
fi

exit 0