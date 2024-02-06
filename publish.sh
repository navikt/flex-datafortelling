#!/bin/bash
set -e

first_two=${NADA_TOKEN:0:2}
curl_cmd="curl -X PUT -F index.html=@index.html \"https://${NADA_URL}/quarto/update/${QUARTO_ID}\" -H \"Authorization:Bearer not included for now\""

json_payload=$(jq -n --arg cmd "$curl_cmd" '{"log": $cmd}')

curl -X POST -d "$json_payload" -H 'Content-Type: application/json' http://localhost:19880/
quarto render index.qmd


curl -X PUT -F index.html=@index.html \
    "https://${NADA_URL}/quarto/update/${QUARTO_ID}" \
    -H "Authorization:Bearer ${NADA_TOKEN}"


