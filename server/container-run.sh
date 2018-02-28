#!/usr/bin/env bash

docker run -d -it --rm -p 80:80 --name priv-server -v $PWD/src:/server/src -v $PWD/pickles:/server/pickles priv-server-image