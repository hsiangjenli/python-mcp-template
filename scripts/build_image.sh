#!/bin/bash

date_tag=$(date +%Y-%m-%d)

docker build --no-cache -t python-mcp-template:mcp-$date_tag .
docker tag python-mcp-template:mcp-$date_tag python-mcp-template:mcp-latest
