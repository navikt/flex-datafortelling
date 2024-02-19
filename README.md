# Datafortelling

En naisjobb for å genere en quarto-basert datafortelling.

## Installer avhengigheter

Installer avhengigheter på mac:
```shell
make macos-setup # Skrevet for MacOS
``` 
## Anbefalte instillinger

Installer avhengigheter på mac:
```shell
make recommended-settings
```

## Utvikling

Om man bare vil rendre [prod.qmd](index.qmd) til [index.html](index.html) lokalt kan man forsøke:

Logg inn og generer quarto fil: 

```shell
make render
```

## NAIS: tips og triks
For å trigge en kjøring av naisjoben kan man kjøre noe slikt: `kubectl create job --from=cronjobs/flex-datafortelling flex-testjobb-NN -n flex` NN kunne vært et tall, det viktigste er at alle adhoc jobber må ha unike navn.