#!/bin/bash
set -e

curdir=$(pwd)
pubtemp=$(mktemp -d)

mkdir $pubtemp/orders
cp deploy/build.sh deploy/docker-compose.yml deploy/Dockerfile deploy/orders.c $pubtemp/orders/
cd $pubtemp

zip -9 -r orders.zip orders

cd $curdir
mv $pubtemp/orders.zip public
rm -rf $pubtemp