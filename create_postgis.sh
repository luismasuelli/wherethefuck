#!/bin/bash
docker container create -p 5432:5432 -v $HOME/DockerVolumes/wherethefuck/db --name=postgis_world \
                        -e POSTGRES_USER=postgres -e POSTGRES_PASS=my-insecure-dev-password -e POSTGRES_DBNAME=world \
                        -e POSTGRES_MULTIPLE_EXTENSIONS=postgis kartoza/postgis
