#!/bin/sh
set -e

docker build -t enterprise-flagchecker:latest .
docker run --rm -it -v ./vol:/vol enterprise-flagchecker:latest cp /build/task /vol
