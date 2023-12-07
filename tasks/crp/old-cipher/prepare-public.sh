#!/bin/sh
set -e

curdir="$PWD"
pubtemp="$(mktemp -d)"

mkdir "$pubtemp/bad-cipher"
cp dev/cipher.py "$pubtemp/bad-cipher/"
cp dev/image.png.enc "$pubtemp/bad-cipher"

cd "$pubtemp"

zip -9 -r bad-cipher.zip bad-cipher

cd "$curdir"
mv "$pubtemp/bad-cipher.zip" public

rm -rf "$pubtemp"
