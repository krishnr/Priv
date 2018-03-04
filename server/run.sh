#!/bin/bash

### Script to run/clean/kill/debug the Priv server

debug=0
exit=0
clean=0
start=0
test=0
headless=0
quit=0

create_train_transform_sets()
{
    echo "Creating data set pickles..."
    if [ ! -d datasets ]; then
        mkdir datasets
    fi

    if [ "$headless" = "1" ]; then
        docker exec priv-server python3 src/scripts/transform.py
        docker exec priv-server python3 src/scripts/train.py
    else
        docker exec -it priv-server python3 src/scripts/transform.py
        docker exec -it priv-server python3 src/scripts/train.py
    fi
}

clean()
{
    if [ -f pickles/*.pkl ]; then
        echo "removing pickles"
        rm /pickles/*.pkl
    fi
    create_train_transform_sets
}

start()
{
    pickle_files=(pickles/*.pkl)

    if [ ! -e ${pickle_files[0]}  ]; then
        create_train_transform_sets
    fi

    echo "Starting server"

    if [ "$headless" = "1" ]; then
        echo "Running headless"
        docker exec priv-server python3 src/run.py
    else
        docker exec -it priv-server python3 src/run.py
    fi
}

usage()
{
    echo "Usage:
    ./run.sh start [options]

    General Options:
    -c, --clean                 Removes Python-generated files and rebuilds pickles
    -h, --help                  Show help
    -t, --test                  Runs NLP test scripts
    -hd, --headless             Runs as a headless PID
    "
}

test()
{
    if [ "$headless" = "1" ]; then
        docker exec priv-server python3 src/scripts/test.py
    else
        docker exec -it priv-server python3 src/scripts/test.py
    fi
}

train()
{
    create_train_transform_sets
    if [ "$headless" = "1" ]; then
        docker exec priv-server python3 src/scripts/test.py
    else
        docker exec -it priv-server python3 src/scripts/test.py
    fi
}

while [ "$1" != "" ]; do
    case $1 in
        -c | --clean )          clean=1
                                ;;
        -h | --help )           usage
                                exit
                                ;;
        -t | --test )           test=1
                                ;;
        -hd | --headless )      headless=1
                                ;;
        -q | --quit )           quit=1
                                ;;
        start )                 start=1
                                ;;
        train )                 train=1

    esac
    shift
done

### Initiate virtual environment and install Python dependencies

if [ "$clean" = "1" ]; then
    clean
fi

if [ "$test" = "1" ]; then
    test
fi

if [ "$start" = "1" ]; then
    start
fi

if [ "$train" = "1" ]; then
    train
    exit
fi

#if [ $# -eq 0 ]; then
#    echo 'No arguments found. Pass arguments: clean, test or start for more options.'
#fi

