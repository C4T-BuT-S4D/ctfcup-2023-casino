#!/bin/bash
set -e

curdir=$(pwd)
pubtemp=$(mktemp -d)

mkdir $pubtemp/memgame
cp deploy/docker-compose.yml deploy/Dockerfile deploy/memgame.c $pubtemp/memgame/
cd $pubtemp

zip -9 -r memgame.zip memgame

cd $curdir
mv $pubtemp/memgame.zip public
rm -rf $pubtemp