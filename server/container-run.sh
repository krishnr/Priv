#!/usr/bin/env bash

docker run -d -it -p 5000:5000 --name priv-server -v $PWD:/src priv-server-image