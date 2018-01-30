#!/bin/bash

### Script to run/clean/kill/debug the Priv server

debug=0
exit=0
clean=0
start=0

virtual_env_setup()
{
    echo "Checking if virtualenv is installed"
    if ! virtualenv --version &>/dev/null; then
        echo "No virtualenv found, installing"
        pip install virtualenv
    fi

    echo "Checking if virtual environment has been created"
    if [ ! -d virtualenv_Priv ]; then
        echo "No virtualenv directory found, creating"
        virtualenv virtualenv_Priv
    fi

    . virtualenv_Priv/bin/activate
}

create_train_transform_sets()
{
    echo "Creating data set pickles..."
    python3 scripts/transform.py
    python3 scripts/train.py
}

clean()
{
    if [ -f pickles/*.pkl ]; then
        echo "removing pickles"
        rm /pickles/*.pkl
    fi
    create_train_transform_sets
}

init()
{
    virtual_env_setup

    echo "Installing requirements..."
    pip install -r requirements.txt -q
}

start()
{
    pickle_files=(pickles/*.pkl)

    if [ ! -e ${pickle_files[0]}  ]; then
        create_train_transform_sets
    fi

    echo "Starting server"
    python3 server/__init__.py
}

usage()
{
    echo "Usage:
    ./run.sh start [options]

    General Options:
    -c, --clean                 Removes Python-generated files and rebuilds pickles
    -h, --help                  Show help
    "
}

while [ "$1" != "" ]; do
    case $1 in
        -c | --clean )          clean=1
                                ;;
        -h | --help )           usage
                                exit
                                ;;
        start )                 start=1

    esac
    shift
done

### Initiate virtual environment and install Python dependencies
init

if [ "$clean" = "1" ]; then
    clean
fi

if [ "$start" = "1" ]; then
    start
fi