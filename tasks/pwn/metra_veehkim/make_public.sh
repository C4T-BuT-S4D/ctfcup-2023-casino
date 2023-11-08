#!/bin/bash
set -e

curdir=$(pwd)
pubtemp=$(mktemp -d)

mkdir $pubtemp/metra_veehkim
cp deploy/docker-compose.yml deploy/Dockerfile deploy/chall.c $pubtemp/metra_veehkim/
cd $pubtemp

zip -9 -r metra_veehkim.zip metra_veehkim

cd $curdir
mv $pubtemp/metra_veehkim.zip public
rm -rf $pubtemp