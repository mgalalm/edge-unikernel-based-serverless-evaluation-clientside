#!/bin/sh
# ./ci.sh main.go
if [ -z "$1" ]
  then
    echo "No argument supplied"
    exit 1
fi
scp ../src/$1 pi@openwhisk:/home/pi/openwhisk/src && \
ssh -t pi@openwhisk "bash --login -c 'build $1'"
