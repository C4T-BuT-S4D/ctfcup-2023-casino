#!/bin/bash
set -e

curdir=$(pwd)
pubtemp=$(mktemp -d)

mkdir $pubtemp/pwn_task
cp deploy/docker-compose.yml deploy/Dockerfile deploy/pwn_task.c $pubtemp/pwn_task/
cd $pubtemp

zip -9 -r pwn_task.zip pwn_task

cd $curdir
mv $pubtemp/pwn_task.zip public
rm -rf $pubtemp