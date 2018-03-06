#!/usr/bin/env bash

docker run -d -it --rm -p 80:80 --name priv-server -v $PWD/src:/app/src -v $PWD/pickles:/app/pickles priv-server-image