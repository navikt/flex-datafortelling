.PHONY: $(shell sed -n -e '/^$$/ { n ; /^[^ .\#][^ ]*:/ { s/:.*$$// ; p ; } ; }' $(MAKEFILE_LIST))

root_dir := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

help:
	@echo "$$(grep -hE '^\S+:.*##' $(MAKEFILE_LIST) | sed -e 's/:.*##\s*/:/' -e 's/^\(.\+\):\(.*\)/\\x1b[36m\1\\x1b[m:\2/' | column -c2 -t -s :)"

recommended-settings:
	poetry --version && poetry config virtualenvs.in-project true

macos-bootstrap: # Setter opp miljø for quarto-rendring
	python3.12 --version || echo 'python3.12 is not installed, press any key' && read
	poetry --version || brew install pipx
	poetry --version || pipx ensurepath
	poetry --version || pipx install poetry
	quarto --version || brew install quarto
	gcloud --version || brew install --cask google-cloud-sdk


login: # Sjekker om man er autentisert mot gcloud og logger inn hvis ikke
	gcloud auth print-identity-token >/dev/null 2>&1 || gcloud auth login --update-adc # Reduserer antall ganger man har glemt å logge på

 env: # Slipper feilmelding fordi .env-fil mangler
	cat	 .env || cp env.example .env

setup: macos-bootstrap ## Setter opp miljø for å rendre datafortellingen


render: login ## Rendrer quarto datafortelling til index.html og åpner i nettleser
	poetry run quarto render index.qmd
	open index.html

preview: login  ## Rendrer quarto datafortelling til lokal webserver ved å lytte på endringer i index.qmd
	rm -rf .quarto && poetry run quarto preview index.qmd

preview_no_execute: login  ## Samme som preview, men kjører ikke python-koden
	poetry run quarto preview index.qmd --no-execute
