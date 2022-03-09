#!/bin/bash

function help() {
    echo "Help"
    echo "-------------------------"
    echo "Usage: ./setup.sh [all|minimal]"
}

# Perform a system update
function update_system() {
    sudo apt update
    sudo apt dist-upgrade -y
}

function install_minimal() {
    update_system()
    sudo apt install -y neofetch htop httpie neovim
}

function install_all() {
    install_minimal()
    sudo apt install -y openjdk-17-jdk

    # Install TheFuck
    sudo apt install python3-dev python3-pip python3-setuptools
    pip3 install thefuck --user
}

if [ "$#" -ne 1 ]; then
    help()
    exit
fi

if [ "$1" -eq "help" ]; then
    help()
    exit
elif [ "$1" -eq "all" ]; then
    install_all()
elif [ "$1" -eq "minimal" ]; then
    install_minimal()
fi
