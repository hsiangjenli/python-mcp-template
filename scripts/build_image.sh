#!/bin/bash

date_tag=$(date +%Y-%m-%d)

docker build -t python-mcp-template:$date_tag .
docker tag python-mcp-template:$date_tag python-mcp-template:latest
