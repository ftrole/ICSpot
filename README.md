# ICSpot
A high interaction ICS honeypot that simulates a Siemens PLC and provides physical process simulation.

With ICSpot an attacker can interact with the operations involved in the control process of the water level inside a tank.

<img src="./docs/imgs/ICSpot_schema.png" alt="ICS architecture schema" />

The figure above shows the general architecture of our honeypot and how the different components interact between each others. 

## Installation

### Requirements 
- Operating system: tested on ubuntu 18.04 and 20.04. Currently the Honeypot was tested on a *non-server* version since the HMI requires a brower to be visualized. Furthermore some script in the physical process span new terminals tabs with the command `gnome-terminal`
- Python 2 for Mininet and MiniCPS (installation included in the preconfigured script).
- Python 3 for the HMI web app (installation included in the preconfigured script).


### Installation process

1. Clone this repository: `git clone https://github.com/ftrole/ICSpot.git`
2. To install ICSpot and all its dependencies run `sh install.sh`
3. Fix the script paths  in [honeyd.conf](./honeyd.conf) so they match the absolute path in your file system

4. Replace IP in [honeyd.conf](./honeyd.conf) with the address you've chosen: the IP address 
has to be on the same network as the host interface where honeyd will listen.

5. In order to execute the simulation follow the instruction in the [waterTower folder](./waterTower/README.md) to start the simulation and the HMI web application

6. Copy the modified Snap7 library [libsnap7.so](./snap7/build/bin/x86_64-linux/libsnap7.so) in: `/usr/lib/libsnap7.so`

7. Compile and Execute the s7comm server (you can find it [here](./snap7/examples/cpp/x86_64-linux/server) 

    Compile: `make .snap7/examples/cpp/server.cpp`  

    Execute: `sudo .snap7/examples/cpp/x86_64-linux/server 127.0.0.1`

    *N.B.* it may be necessary to fix the sqlite3 db file path inside [server.cpp](./snap7/examples/cpp/server.cpp)

8. From inside the repository, run: 

    `sudo honeyd -d -p nmap-os-db -i INTERFACE -l honeyd.log -f honeyd.conf IP --disable-webserver`

    where IP is the same IP address of Honeyd configuration file and INTERFACE is the interface of the host machine

9. ICSpot is now up and running!

*N.B.* The host computer have to intercept the network traffic addressed to the honeypot, in order to allow honeyd to reply in the correct way. 
A useful tool that you can use to achieve this result is farpd:

`sudo farpd -d -i INTERFACE <IP>`

## Team
Francesco Trolese (francesco.trolese.1@studenti.unipd.it)  
Federico Turrin (turrin@math.unipd.it)


We are members of [SPRITZ Security and Privacy Research Group](https://spritz.math.unipd.it/) at University of Padua, Italy.
