#!/bin/sh
set -e

curdir="$PWD"
pubtemp="$(mktemp -d)"

mkdir "$pubtemp/bad_cipher"
cp dev/cipher.py "$pubtemp/bad_cipher/"
cp dev/image.png.enc "$pubtemp/bad_cipher"

cd "$pubtemp"

zip -9 -r bad_cipher.zip bad_cipher

cd "$curdir"
mv "$pubtemp/bad_cipher.zip" public

rm -rf "$pubtemp"
