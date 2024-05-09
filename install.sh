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

# Installing Python3 dependencies
# packages requiring sudo space due to mininet
sudo pip install cpppo==4.3.4
sudo pip install pymodbus
sudo pip install pandas
sudo pip install Flask-SocketIO==4.3.1
sudo pip install python-engineio==3.13.2
sudo pip install python-socketio==4.6.0
sudo pip install flask==1.1.2
sudo pip install jinja2==2.11.2
sudo pip install MarkupSafe==1.1.1
sudo pip install Werkzeug==1.0.1
sudo pip install itsdangerous==1.1.0

#all other packages
pip install -r requirements.txt

# create log and make it modifiable
touch honeyd.log
sudo chmod 777 honeyd.log

# Installing Honeyd - just a copy and paste of the guide
cd ~
git clone https://github.com/DataSoft/Honeyd
cd Honeyd
sudo apt install -y libevent-dev libdumbnet-dev libpcap-dev libpcre3-dev libedit-dev bison flex libtool automake make zlib1g-dev
./autogen.sh
./configure
make
sudo make install

printf "\nInstallation finished.\n"
exit 0;
