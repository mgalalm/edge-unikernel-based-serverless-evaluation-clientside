#!/bin/sh
if [ -z "$1" ]
  then
    echo "No argument supplied"
    exit 1
fi
ssh -t pi@openwhisk "bash --login -c 'deploy $1'"