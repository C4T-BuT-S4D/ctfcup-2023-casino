#!/bin/bash
set -e

curdir=$(pwd)
pubtemp=$(mktemp -d)

cp -R deploy $pubtemp/formatter
cd $pubtemp

zip -9 -r formatter.zip formatter

cd $curdir
mv $pubtemp/formatter.zip public
rm -rf $pubtemp
