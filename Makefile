.PHONY: $(shell sed -n -e '/^$$/ { n ; /^[^ .\#][^ ]*:/ { s/:.*$$// ; p ; } ; }' $(MAKEFILE_LIST))

root_dir := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

help:
	@echo "$$(grep -hE '^\S+:.*##' $(MAKEFILE_LIST) | sed -e 's/:.*##\s*/:/' -e 's/^\(.\+\):\(.*\)/\\x1b[36m\1\\x1b[m:\2/' | column -c2 -t -s :)"

macos-bootstrap: ## Installer avhengigheter for macOS.
	@python3.12 --version || { echo 'python3.12 is not installed, you will need it to install it' && read; }
	@pipx --version || { brew install pipx && pipx ensurepath; }
	@poetry --version || pipx install poetry
	@quarto --version || brew install quarto
	@gcloud --version || brew install --cask google-cloud-sdk

update: macos-bootstrap ## Oppdaterer avhengigheter.
	poetry update

login: ## Sjekker om man er autentisert mot gcloud og logger inn hvis ikke.
	@gcloud auth print-identity-token >/dev/null 2>&1 || gcloud auth login --update-adc

macos-setup: macos-bootstrap login ## Setter opp miljø for å rendre datafortellingen.

recommended-settings: ## Konfigurer poetry med virtualenvs.in-project true
	poetry --version && poetry config virtualenvs.in-project true

render: login ## Rendrer datafortelling til index.html og åpner den i nettleser.
	poetry run quarto render prod.qmd -o index.html
	open index.html

preview: login ## Rendrer Quarto datafortelling til lokal webserver ved å lytte på endringer i index.qmd.
	rm -rf .quarto && poetry run quarto preview prod.qmd -o index.html

preview_no_execute: login  ## Samme som preview, men kjører ikke Python-koden.
	poetry run quarto preview prod.qmd -o index.html --no-execute

format: ## Formater koden med Black
	poetry run black .