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
s
# Installing necessary packages
sudo apt install -y git python3 python3-pip curl libsqlite3-dev openvswitch-testcontroller net-tools gnome-terminal mininet dbus-x11

# Install farpd
sudo apt install -y farpd

# Installing Honeyd - just a copy and paste of the guide
cd ~
git clone https://github.com/DataSoft/Honeyd
cd Honeyd
sudo apt install -y libevent-dev libdumbnet-dev libpcap-dev libpcre3-dev libedit-dev bison flex libtool automake make zlib1g-dev
./autogen.sh
./configure
make
sudo make install

# Installing Python3 dependencies
pip install -r requirements.txt

# create log and make it modifiable
touch honeyd.log
sudo chmod 777 honeyd.log

printf "\nInstallation finished.\n"
exit 0;
