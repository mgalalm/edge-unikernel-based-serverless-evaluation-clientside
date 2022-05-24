#!/bin/sh
for i in {1..10}
do 
  
    ../invoker.py 16 helloworld --concurrent --type="cd_$i"
    echo $i
done