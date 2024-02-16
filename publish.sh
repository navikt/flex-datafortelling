#!/bin/bash
set -e

# Assuming you have an environment variable named ENVIRONMENT
if [ "$ENVIRONMENT" == "dev" ]; then
    quarto render dev.qmd --output index.html
elif [ "$ENVIRONMENT" == "prod" ]; then
    quarto render prod.qmd --output index.html
else
    echo "assuming it is running locally"
    # quarto render dev.qmd --embed-resources  --output dev.html
    # quarto render prod.qmd --embed-resources --output index.html
    quarto render prod.py --output index.html
fi

response=$(curl -X PUT -F index.html=@index.html "https://${NADA_URL}/quarto/update/${QUARTO_ID}" -H "Authorization:Bearer ${NADA_TOKEN}")

# Store the status code of the last executed command
status=$?

echo "Response: $response"
echo "HTTP Status: $http_status"



