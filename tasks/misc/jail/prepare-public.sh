#!/bin/bash
set -e

curdir=$(pwd)
pubtemp=$(mktemp -d)

cp -R deploy $pubtemp/jail
cd $pubtemp

zip -9 -r jail.zip jail

cd $curdir
mv $pubtemp/jail.zip public
rm -rf $pubtemp
