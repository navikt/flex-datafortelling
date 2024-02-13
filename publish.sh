#!/bin/bash
set -e

# first_two=${NADA_TOKEN:0:2}
# curl_cmd="curl -X PUT -F index.html=@index.html \"https://${NADA_URL}/quarto/update/${QUARTO_ID}\" -H \"Authorization:Bearer not included for now\""

# json_payload=$(jq -n --arg cmd "$curl_cmd" '{"log": $cmd}')
# https://data.intern.nav.no/story/87332165-41ff-49bc-bd34-a8747cefb3db
# curl -X POST -d "$json_payload" -H 'Content-Type: application/json' http://localhost:19880/

# Assuming you have an environment variable named ENVIRONMENT
if [ "$ENVIRONMENT" == "dev" ]; then
    quarto render dev.qmd --output index.html
elif [ "$ENVIRONMENT" == "prod" ]; then
    quarto render prod.qmd --output index.html
else
    echo "assuming it is running locally"
    # quarto render dev.qmd --output dev.html
    # quarto render prod.qmd --output prod.html
    quarto render prod.qmd --output index.html
fi


#curl_cmd="curl -X PUT -F index.html=@index.html \"https://${NADA_URL}/quarto/update/${QUARTO_ID}\" -H \"Authorization:Bearer not included for now\""
#echo "request started: " $curl_cmd
#
#response=$(curl -X PUT -F index.html=@index.html \
#    "https://${NADA_URL}/quarto/update/${QUARTO_ID}" \
#    -H "Authorization:Bearer ${NADA_TOKEN}" \
#    --connect-timeout 30 \
#    --silent --show-error --write-out "HTTP_STATUS:%{http_code}" \
#    )
#
#
#http_status=$(echo "$response" | tr -d '\n' | sed -e 's/.*HTTP_STATUS://')

# date > index.html
# quarto render index.qmd
response=$(curl -X PUT -F index.html=@index.html "https://${NADA_URL}/quarto/update/${QUARTO_ID}" -H "Authorization:Bearer ${NADA_TOKEN}")

# Store the status code of the last executed command
status=$?

echo "Response: $response"
echo "HTTP Status: $http_status"

# Check if the command


