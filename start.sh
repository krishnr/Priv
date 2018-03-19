#!/usr/bin/env bash

remove_images=0

usage()
{
    echo "Usage:
    bash start.sh [options]

    General Options:
    -r, --remove_images                 Removes Docker images and mounted volumes, then rebuilds images from scratch
    "
}


while [ "$1" != "" ]; do
    case $1 in
        -r | --remove_images )   remove_images=1
                                ;;
        -h | --help )           usage
                                exit
    esac
    shift
done

# Copy env file to server/src/util
echo "Copying environment file"
cp ./.env ./server/src/util/

# Remove any dangling images
docker rmi $( docker images -q -f dangling=true) 2> /dev/null >/dev/null

# NOTE: If any changes are made to directories other than pickles/ and src/, the image must be rebuilt
# In that case, pass in the flags -r or --remove_images

if [ "$remove_images" = "1" ]; then
    # Remove any images, running containers and volumes
    echo "Removing images"
    docker-compose down -v --rmi all
fi

# To customize running the server, make changes to server/src/prestart.sh script (i.e. adding --headless or --test)
docker-compose up -d --force-recreate

echo "Tailing server logs"
docker logs -f $(docker ps -a -q --filter name=priv_server)