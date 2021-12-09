#!/bin/bash

export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8

cd /app/ArenaSDK_Linux_x64 && sh Arena_SDK.conf
cd /app && pip3 install -r /app/custom_requirements.txt

cd /app
python3 main_application.py &

trap "sigterm; exit" SIGTERM

function sigterm() {
    echo "Catch SIGTERM"
    echo "Try kill pid $value"
    kill "$value"
}

while [[ 1=1 ]]; do
    value=`cat deamon.pid`

    sleep 1
done

