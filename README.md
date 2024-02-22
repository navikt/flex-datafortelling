# Datafortelling

En naisjobb for å genere en quarto-basert datafortelling.


## Opinionated setup som installerer avhengigheter på mac og konfigurerer innstillinger
Obs: Denne vil sette globale poetry instillinger for virtualenvs i projektfolderen.
```shell
make macos-opinionated-setup
```

## Installer avhengigheter

Kommandoene under er skrevet for macOS da de krever at [Homebrew](https://brew.sh/) finnes.

Installerer avhengigheter for macOS.
```shell
make macos-bootstrap
```

## Anbefalte instillinger

Konfigurerer innstillinger for Poetry.

```shell
make recommended-settings
```

Eller kjør `make` for en full oversikt over mulige kommandoer.

## Installer python avhengigheter og oprett virtualenv
Kjør så `poetry install` for å opprette et virtuelt miljø og installere avhengigheter. (Det er ofte praktisk å skru på virtualenv i prosjektfolder settingen til poetry, noe du kan gjøre før poetry install ved hjelp av `make recommended-settings`.)

```shell
poetry install
```
Om du vil aktivere virtualenv kan du kjøre `poetry shell`.
```shell
poetry shell
```


## Utvikling

Om man bare vil rendre [prod.qmd](index.qmd) til [index.html](index.html) lokalt kan man forsøke:

Generer datafortelling lokalt med:

```shell
make render
```

## Datafortelling på data.nais.io
Dev: https://data.intern.dev.nav.no/story/4eff47a7-b3aa-4777-93ff-9a18edba2415/index.html
Prod: 


## NAIS: tips og triks

For å trigge en kjøring av naisjoben kan man kjøre noe slikt: `kubectl create job --from=cronjobs/flex-datafortelling flex-testjobb-NN -n flex` NN kunne vært et tall, det viktigste er at alle adhoc jobber må ha unike navn.
