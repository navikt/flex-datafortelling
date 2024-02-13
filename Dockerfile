FROM python:3.12

RUN apt-get update && apt-get install -yq --no-install-recommends \
    curl \
    jq && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# for å installere quarto for arm (apple sillicon)
# send inn dette argumentet til byggekommandoen: --build-arg CPU=arm64
ARG CPU=amd64

# install quarto
RUN QUARTO_VERSION=$(curl https://api.github.com/repos/quarto-dev/quarto-cli/releases/latest | jq '.tag_name' | sed -e 's/[\"v]//g') && \
    wget https://github.com/quarto-dev/quarto-cli/releases/download/v${QUARTO_VERSION}/quarto-${QUARTO_VERSION}-linux-${CPU}.tar.gz && \
    tar -xvzf quarto-${QUARTO_VERSION}-linux-${CPU}.tar.gz && \
    ln -s /quarto-${QUARTO_VERSION}/bin/quarto /usr/local/bin/quarto && \
    rm -rf quarto-${QUARTO_VERSION}-linux-${CPU}.tar.gz;

RUN groupadd -g 1069 python && \
    useradd -r -u 1069 -g python python

WORKDIR /home/python


# install python related dependencies
RUN pip install poetry
RUN python3 -m pip install poetry
RUN poetry self add poetry-plugin-export
COPY pyproject.toml .
COPY poetry.lock .
RUN poetry export -f requirements.txt --output requirements.txt
RUN python -m pip install --no-cache-dir --upgrade pip wheel
RUN python -m pip install --no-cache-dir -r requirements.txt
RUN ipython kernel install --name "python3"

ENV DENO_DIR=/home/python/deno
ENV XDG_CACHE_HOME=/home/python/cache
ENV XDG_DATA_HOME=/home/python/share

COPY publish.sh .
COPY index.qmd .
COPY index.py .
RUN mkdir output

RUN chown python:python /home/python -R
USER python
# dsflsdfl
CMD ["./publish.sh"]
