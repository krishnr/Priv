#!/usr/bin/env bash

remove_image=0

usage()
{
    echo "Usage:
    bash start.sh [options]

    General Options:
    -r, --remove_image                 Removes Docker image and rebuilds image from scratch
    "
}


while [ "$1" != "" ]; do
    case $1 in
        -r | --remove_image )   remove_image=1
                                ;;
        -h | --help )           usage
                                exit
    esac
    shift
done

# Start server container
echo "Starting server"
cd server

# Check if image exists
if [[ $(docker image inspect priv-server-image:latest 2> /dev/null >/dev/null ; echo $?) != "0" ]]; then
    # NOTE: If any changes are made to directories other than pickles/ and src/, the image must be rebuilt
    # In that case, delete the existing image using docker rmi priv-server-image, and run this script
    echo "Building server image"
    bash build-image.sh
fi

# Remove any running containers
docker rm -f $(docker ps -a -q --filter name=priv-server) 2>/dev/null

if [ "$remove_image" = "1" ]; then
    docker rmi priv-server-image
    bash build-image.sh
fi

# To customize running the server, make changes to /src/prestart.sh script (i.e. adding --headless or --test)
bash container-run.sh

echo "Tailing logs"
docker logs -f $(docker ps -a -q --filter name=priv-server)