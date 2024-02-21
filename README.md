# Datafortelling

En naisjobb for å genere en quarto-basert datafortelling.

## Installer avhengigheter

Kommandoene under er skrevet for macOS da de krever at [Homebrew](https://brew.sh/) finnes.

Setter opp miljø for å rendre datafortellingen.

```shell
make macos-setup
```

## Anbefalte instillinger

Konfigurerer innstillinger for Poetry.

```shell
make recommended-settings
```

Eller kjør `make` for en full oversikt over mulige kommandoer.

## Utvikling

Om man bare vil rendre [prod.qmd](index.qmd) til [index.html](index.html) lokalt kan man forsøke:

Generer datafortelling lokalt med:

```shell
make render
```

## NAIS: tips og triks

For å trigge en kjøring av naisjoben kan man kjøre noe slikt: `kubectl create job --from=cronjobs/flex-datafortelling flex-testjobb-NN -n flex` NN kunne vært et tall, det viktigste er at alle adhoc jobber må ha unike navn.
