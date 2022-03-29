#!/usr/bin/env bash
runners=$(cat docker-compose.yml | yq '.services | keys' | grep "\-runner" | sed 's/- //g')
for r in ${runners}; do
    ports_line=$(cat docker-compose.yml | yq ".services.${r}.ports")
    port=$(echo $ports_line | sed -E "s/- [0-9]+://g")
    echo "${r} algorithm schemas:"
    curl -s http://localhost:${port}/schemas | jq .
    echo
done
