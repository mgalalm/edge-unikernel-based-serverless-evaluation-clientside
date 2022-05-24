#!/bin/sh
for i in {1..16}
do 
    ../invoker.py $i helloworld --concurrent --type=latency
    sleep 10
done