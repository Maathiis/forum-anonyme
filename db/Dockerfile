FROM postgres:13

ENV POSTGRES_DB=forum
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=password

COPY init.sql /docker-entrypoint-initdb.d/
