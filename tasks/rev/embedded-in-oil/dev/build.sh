#!/bin/sh

set -e

curdir="$PWD"
tmpdir="$(mktemp -d)"

cd "$tmpdir"
pyinstaller -F "$curdir/embedded.py"

cd "$curdir"
mv "$tmpdir/dist/embedded" ./

rm -rf "$tmpdir"
