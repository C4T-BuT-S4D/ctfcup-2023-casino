#!/bin/bash

set -e
set -x

rm -rf public/
mkdir -p public/msc-art

cp dev/fake-text.png public/msc-art/text.png
cp deploy/{Dockerfile,docker-compose.yml,task.py,requirements.txt} public/msc-art/

cd public/

zip -r msc-art.zip msc-art/
