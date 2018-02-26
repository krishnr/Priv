#!/usr/bin/env bash

docker run -d -it --rm -p 5000:5000 --name priv-server -v $PWD/src:/server/src -v $PWD/pickles:/server/pickles priv-server-image