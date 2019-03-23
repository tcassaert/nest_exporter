#!/bin/bash
set -e

if [ -z $DEVICE_ID ];then
  echo "A device ID is required"
  exit 1
fi

if [ -z $SECRET ];then
  echo "A secret is required"
  exit 1
fi

if [ -z $DEVICE_TYPE ];then
  export DEVICE_TYPE=thermostat
fi

exec /opt/nest_exporter.py --type=$DEVICE_TYPE --id=$DEVICE_ID --secret=$SECRET
