#!/bin/sh
for i in {1..16}
do 
    ./invoker.py $i helloworld
    sleep 10
done