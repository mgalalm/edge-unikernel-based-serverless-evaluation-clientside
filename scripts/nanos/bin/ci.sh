#!/bin/sh
if [ -z "$1" ]
  then
    echo "No argument supplied"
    exit 1
fi
scp ../src/$1 pi@nanos:/home/pi/nanos/src && \
ssh -t pi@nanos "bash --login -c 'build $1'"