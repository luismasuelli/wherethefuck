#!/usr/bin/env bash
docker container create --hostname djcelery_wtf --name djcelery_wtf \
                        -e RABBITMQ_DEFAULT_USER=djcelery_wtf_admin \
                        -e RABBITMQ_DEFAULT_PASS=my-insecure-dev-password \
                        -p 5672:5672 rabbitmq:3
