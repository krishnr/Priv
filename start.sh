#!/usr/bin/env bash

# Start server container
echo "Starting server"
cd server

# Check if image exists
if [[ $(docker image inspect priv-server-image:latest 2> /dev/null >/dev/null ; echo $?) != "0" ]]; then
    # NOTE: If any changes are made to directories other than pickles/ and src/, the image must be rebuilt
    # In that case, delete the existing image using docker rmi priv-server-image, and run this script
    echo "Building server image"
    ./build-image.sh
fi

# Remove any running containers
docker rm -f $(docker ps -a -q --filter name=priv-server) 2>/dev/null

# To customize running the server, make changes to /src/prestart.sh script (i.e. adding --headless or --test)
./container-run.sh