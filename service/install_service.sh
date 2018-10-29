#!/bin/bash

# Tiny script to install BOSWatch-service via systemctl
# Just a few simple steps are required to (un)register your service

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root!" 1>&2
   exit 1
fi

read -p"Do you want to install (i) or remove (r) the service? " action

if [ "$action" == "i" ]; then

    # 1 Check whether the right data are in the service-file
    
    read -p"Did you adapt the file boswatch.service (y/n)? " response
    
    if [ "$response" == "y" ]; then
        # 2 Copy the file
        cp boswatch.service /etc/systemd/system

        # 3 Enable the service and check status
        systemctl enable boswatch.service
        systemctl is-enabled boswatch.service

        # 4 fire it up
        systemctl start boswatch.service

        # 5 post the status
        systemctl status boswatch.service
    elif [ "$response" == "n" ]; then
        echo "Please adapt your personal boswatch.service-file"
        exit 1
    else
        echo "Invalid input - please try again"
        exit 1
    fi
elif [ "$action" == "r" ]; then # we want to remove the service
    # stop it...
    systemctl stop boswatch.service
    
    # disable it
    systemctl disable boswatch.service

    # and remove it
    rm /etc/systemd/system/boswatch.service
    echo "boswatch service removed"
else # error handling
    echo "Invalid input - please try again"
    exit 1
fi
