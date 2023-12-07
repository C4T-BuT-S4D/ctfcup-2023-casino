#!/bin/bash

mkdir orders
chmod o+w ./orders
chmod o-r ./orders
docker compose up --build -d
