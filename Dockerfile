# Byggestadium: Laster ned og pakker ut Quarto
FROM python:3.13.5-bookworm AS builder

# For å installere Quarto for ARM (f.eks. Apple silicon) i Docker-bygg
# send inn dette argumentet til byggekommandoen: --build-arg CPU=arm64.
ARG CPU=amd64
ARG QUARTO_VERSION

RUN apt-get update && apt-get install -yq --no-install-recommends \
    curl \
    jq

# Henter Quarto-versjonen hvis ikke angitt
RUN if [ -z "$QUARTO_VERSION" ]; then \
      QUARTO_VERSION=$(curl -s https://api.github.com/repos/quarto-dev/quarto-cli/releases/latest | jq -r '.tag_name' | sed -e 's/^v//'); \
    fi && \
    wget https://github.com/quarto-dev/quarto-cli/releases/download/v${QUARTO_VERSION}/quarto-${QUARTO_VERSION}-linux-${CPU}.tar.gz && \
    tar -xvzf quarto-${QUARTO_VERSION}-linux-${CPU}.tar.gz && \
    rm -rf quarto-${QUARTO_VERSION}-linux-${CPU}.tar.gz && \
    mv quarto-${QUARTO_VERSION} /quarto

# Sluttstadium: Setter opp miljøet og kjører applikasjonen
FROM python:3.13.5-slim-bookworm

# Kopierer Quarto fra builder-stadiet
COPY --from=builder /quarto /quarto
RUN ln -s /quarto/bin/quarto /usr/local/bin/quarto

# Installerer nødvendige pakker og fjerner sårbarheter
RUN apt-get update && apt-get install -yq --no-install-recommends \
      curl \
    && apt-get upgrade -y curl \
    && apt-get remove --purge -y imagemagick git-man golang golang-go libexpat1-dev \
    && apt-get -y autoremove \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Oppretter brukeren
RUN groupadd -g 1069 python && \
    useradd -r -u 1069 -g python python

WORKDIR /home/python

# Installerer Poetry og avhengigheter
RUN pip install poetry
COPY pyproject.toml .
COPY README.md .
COPY poetry.lock .
RUN poetry config virtualenvs.create false
RUN poetry install

ENV DENO_DIR=/home/python/deno
ENV XDG_CACHE_HOME=/home/python/cache
ENV XDG_DATA_HOME=/home/python/share

# Kopierer nødvendige filer
COPY publish.sh .
COPY _quarto.yml .
COPY dev.qmd .
COPY prod.qmd .
COPY /fortellinger ./fortellinger
COPY /grafer_og_visninger ./grafer_og_visninger
COPY /oppsett ./oppsett
COPY /queries ./queries

RUN chown python:python /home/python -R
USER python
CMD ["./publish.sh"]
