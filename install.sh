#!/bin/bash

cwd=$(pwd)
version=$(lsb_release -rs )

# Wrong version warning
if [ "$version" != "20.04" ] && [ "$version" != "18.04" ]
then
  printf "Warning! This installation script has only been tested on Ubuntu 20.04 LTS and 18.04 LTS and will likely not work on your Ubuntu version.\n\n"
fi

sleep 3

# Update apt
sudo apt update

# Installing necessary packages
sudo apt install -y git python2.7 python3 python3-pip curl libsqlite3-dev openvswitch-testcontroller net-tools gnome-terminal

# Install farpd
sudo apt install -y farpd

# Get python2 pip
curl https://bootstrap.pypa.io/pip/2.7/get-pip.py --output get-pip.py
sudo python2 get-pip.py
rm get-pip.py

# CPPPO Correct Version 4.3.4
sudo pip2 install cpppo==4.3.4

# Installing Honeyd - just a copy and paste of the guide
cd ~
git clone https://github.com/DataSoft/Honeyd
cd Honeyd
sudo apt install -y libevent-dev libdumbnet-dev libpcap-dev libpcre3-dev libedit-dev bison flex libtool automake make zlib1g-dev
./autogen.sh
./configure
make
sudo make install

# MiniCPSc
cd ~
git clone --depth 1 https://github.com/afmurillo/minicps.git || git -C minicps pull
cd minicps
sudo python2 -m pip install .

# Mininet from source
cd ~
git clone --depth 1 -b 2.3.1b1 https://github.com/mininet/mininet.git || git -C mininet pull
cd mininet
sudo PYTHON=python2 ./util/install.sh -fnv

# Installing Python3 dependencies
sudo pip3 install Flask-SocketIO==4.3.1
sudo pip3 install python-engineio==3.13.2
sudo pip3 install python-socketio==4.6.0
sudo pip3 install eventlet
sudo pip3 install gevent
sudo pip3 install mininet

# Installing Python2 dependencies
sudo pip2 install pandas

printf "\nInstallation finished.\n"
exit 0;
