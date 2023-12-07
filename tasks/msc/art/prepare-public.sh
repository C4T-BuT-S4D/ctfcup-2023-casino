#!/bin/bash

set -e
set -x

rm -rf public/
mkdir -p public/art

cp dev/fake-text.png public/art/text.png
cp deploy/{Dockerfile,docker-compose.yml,task.py,requirements.txt} public/art/

cd public/

zip -r art.zip art/
