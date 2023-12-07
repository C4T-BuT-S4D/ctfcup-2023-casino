#!/bin/bash
set -e

curdir=$(pwd)
pubtemp=$(mktemp -d)

mkdir $pubtemp/metra-veehkim
cp deploy/docker-compose.yml deploy/Dockerfile deploy/chall.c $pubtemp/metra-veehkim/
cd $pubtemp

zip -9 -r metra-veehkim.zip metra-veehkim

cd $curdir
mv $pubtemp/metra-veehkim.zip public
rm -rf $pubtemp
