#!/bin/bash
set -x

docker stop tlsproxy

docker build -t tlsproxy .

docker run  -p 1010:1010 -p 1010:1010/udp -d --rm --name tlsproxy tlsproxy