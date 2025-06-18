#!/bin/bash
docker-compose down
find . -name '._*' -delete
find . -name '.DS_Store' -delete
docker-compose build --no-cache
docker-compose up