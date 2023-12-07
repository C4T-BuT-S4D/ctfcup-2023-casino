#!/bin/sh
set -e

curdir="$PWD"
pubtemp="$(mktemp -d)"

mkdir "$pubtemp/old-cipher"
cp dev/cipher.py "$pubtemp/old-cipher/"
cp dev/image.png.enc "$pubtemp/old-cipher"

cd "$pubtemp"

zip -9 -r old-cipher.zip old-cipher

cd "$curdir"
mv "$pubtemp/old-cipher.zip" public

rm -rf "$pubtemp"
