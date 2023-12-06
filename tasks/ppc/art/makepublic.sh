#!/bin/bash

set -e
set -x

rm -rf public/
mkdir -p public/ppc-art

cp dev/fake-text.png public/ppc-art/text.png
cp deploy/{Dockerfile,docker-compose.yml,task.py,requirements.txt} public/ppc-art/

cd public/

zip -r ppc-art.zip ppc-art/

