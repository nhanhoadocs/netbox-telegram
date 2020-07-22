#!/bin/bash
SERVICES=
DATE=$(date '+%d-%m-%Y %H:%M:%S')
for SERVICE in ${SERVICES}
  do
    systemctl status $SERVICES 
    if [ $? -ne 0 ];
    then
        systemctl restart $SERVICES
    fi
done
