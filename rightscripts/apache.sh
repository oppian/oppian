#!/bin/bash -e
#
# Installs and configures apache.
#
# CONF_LOCATION -- The location to the conf file for the site
# SITE -- The name of the site
#
# pkgs: apache2-mpm-prefork libapache2-mod-macro libapache2-mod-python


#
# Test for a reboot,  if this is a reboot just skip this script.
#
if test "$RS_REBOOT" = "true" ; then
  echo "Skip code install on reboot."
  logger -t RightScale "Skip code install on reboot."
  exit 0 # Leave with a smile ...
fi

## enable macro mod
a2enmod macro

## enable rewrite mod
a2enmod rewrite

## create sym link to conf location
ln -s -f $CONF_LOCATION /etc/apache2/sites-available/$SITE

## disable default site
a2dissite default

## enable site
a2ensite $SITE

## restart apache
echo "Restarting apache..."
/etc/init.d/apache2 restart