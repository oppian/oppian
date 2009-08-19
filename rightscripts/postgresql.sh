#!/bin/bash -e
#
# Installs and configures PostgreSQL
#
# DB_ADMIN_PASS -- The pass for the database administrator
# DB_NAME -- The name of the database
# DB_USER -- The username for the database
# DB_PASS -- The password for the user for the database
#
# pkgs: postgresql postgresql-client postgresql-contrib


#
# Test for a reboot,  if this is a reboot just skip this script.
#
if test "$RS_REBOOT" = "true" ; then
  echo "Skip code install on reboot."
  logger -t RightScale "Skip install on reboot."
  exit 0 # Leave with a smile ...
fi

## reset postgres admin account
sudo -u postgres psql postgres <<EOF
ALTER USER postgres WITH PASSWORD '$DB_ADMIN_PASS';
EOF

## create user + db
sudo -u postgres psql postgres <<EOF
CREATE ROLE $DB_USER PASSWORD '$DB_PASS' NOSUPERUSER NOCREATEDB NOCREATEROLE INHERIT LOGIN;
EOF
sudo -u postgres createdb -O $DB_USER $DB_NAME
