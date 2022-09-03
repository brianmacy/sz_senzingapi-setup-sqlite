# docker build -t brian/sz_senzingapi-setup-sqlite .
# docker run --user $UID -it -v $PWD:/db -e SENZING_ENGINE_CONFIGURATION_JSON brian/sz_senzingapi-setup-sqlite

ARG BASE_IMAGE=senzing/senzingapi-tools
FROM ${BASE_IMAGE}

ENV REFRESHED_AT=2022-09-02

LABEL Name="brian/sz_senzingapi-setup-sqlite" \
      Maintainer="brianmacy@gmail.com" \
      Version="DEV"

COPY sz_senzingapi-setup-sqlite.py /app/
COPY create_sqlite.py /app/
COPY g2core-schema-sqlite-create.sql /app/

WORKDIR /app
RUN apt-get update \
 && apt-get -y install sqlite3 \
 && python3 create_sqlite.py \
 && apt-get -y remove sqlite3 \
 && apt-get -y autoremove

USER 1001

ENTRYPOINT ["/app/sz_senzingapi-setup-sqlite.py"]

