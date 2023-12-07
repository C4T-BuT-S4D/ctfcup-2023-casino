#!/bin/bash
set -e

curdir=$(pwd)
pubtemp=$(mktemp -d)

mkdir $pubtemp/enterprise-flagchecker
cp dev/vol/task $pubtemp/enterprise-flagchecker
cd $pubtemp

zip -9 -r enterprise-flagchecker.zip enterprise-flagchecker

cd $curdir
mv $pubtemp/enterprise-flagchecker.zip public
rm -rf $pubtemp
