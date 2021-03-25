#!/bin/bash
output=`ps aux|grep SolarPi|grep -v "grep"`
set -- $output
pid=$2
echo $pid
if [ "$pid" == "" ]; then
    echo "SolarPi not running, excute it."
    cd /home/pi/solarpi/bin
    java -jar dist/SolarPi.jar
fi
