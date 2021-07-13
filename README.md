# ICSpot
A high interaction ICS honeypot that simulates a Siemens PLC and provides phisical process simulation.

With ICSpot an attacker can interact with the operations involved in the control process of the water level inside a tank.

<img src="./docs/imgs/ICSpot_schema.png" alt="ICS architecture schema" />

The figure above shows the general architecture of our honeypot and how the different components interact between each others. 

## Installation

### Requirements 
- Operating system: tested on ubuntu 18.04 and 20.04
- Python 2 for Mininet
- Python 3 for the HMI web app


### Installation process
1. Install [Honeyd](https://github.com/DataSoft/Honeyd) and all its dependencies.
1. Install farpd

`sudo apt-get install farpd`

1. Clone this repository 
1. Fix the script paths  in [honeyd.conf](./honeyd.conf) so they match the absolute path in your file system

1. Replace IP in [honeyd.conf](./honeyd.conf) with the address you've chosen: the IP address
has to be on the same network as the host interface where honeyd will listen.

1. In order to execute the program that provides the physical process simulation:
    1. install [Mininet](https://github.com/mininet/mininet) and [MiniCPS](https://github.com/scy-phy/minicps)
    1. follow the instruction in the [waterTower folder](./waterTower/README.md) to start the simulation and the HMI web application

1. Install the modified Snap7 library [libsnap7.so](https://github.com/ftrole/honeySiemens/blob/snap7/snap7/build/bin/x86_64-linux/libsnap7.so-300) in:     `/usr/lib/libsnap7.so`

1. Execute the s7comm server (you can find it [here](https://github.com/ftrole/honeySiemens/blob/snap7/snap7/examples/cpp/x86_64-linux/server) or compile it by yourself by using  `make` inside the folder of your OS.  

    `sudo ./server 127.0.0.1`

    *N.B.* it may be necessary to fix the sqlite3 db file path inside [server.cpp](./snap7/examples/cpp/server.cpp)

1. From inside the repository, run: 

    `sudo honeyd -d -p nmap-os-db -i INTERFACE -l honeyd.log -f honeyd.conf IP –disable-webserver`

    where IP is the same IP address of Honeyd configuration file and INTERFACE is the interface of the host machine

1. ICSpot is now up and running!

*N.B.* The host computer have to intercept the network traffic addressed to the honeypot, in order to allow honeyd to reply in the correct way. 
A useful tool that you can use to achieve this result is farpd:

`sudo apt install farpd`

`sudo farpd -d -i INTERFACE <IP>`

## Team
Francesco Trolese (francesco.trolese.1@studenti.unipd.it)  
Federico Turrin (turrin@math.unipd.it)


We are members of [SPRITZ Security and Privacy Research Group](https://spritz.math.unipd.it/) at University of Padua, Italy.
