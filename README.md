# ICSpot
A high interaction ICS honeypot that simulates a Siemens PLC and provides physical process simulation.

With ICSpot an attacker can interact with the operations involved in the control process of the water level inside a tank.

<img src="./docs/imgs/ICSpot_schema.png" alt="ICS architecture schema" />

The figure above shows the general architecture of our Honeypot and how the different components interact with each other. 

## Installation

Installation is quite articulated, so brace yourself.

### Requirements 
- Operating system: tested on ubuntu 18.04 and 20.04. Currently, the Honeypot was tested on a *non-server* version since the HMI requires a browser to be visualized. Furthermore, some scripts in the physical process span new terminals tabs with the command `gnome-terminal`.
- Python 2 for Mininet and MiniCPS (installation included in the preconfigured script).
- Python 3 for the HMI web app (installation included in the preconfigured script).


### Installation process

1. Clone this repository: `git clone https://github.com/ftrole/ICSpot.git`
2. To install ICSpot and all its dependencies, run `sh install.sh`
3. Fix the paths in: 
    [honeyd.conf](./honeyd.conf) so they match the absolute path of the `ICSpot/scripts` folder in your file system;
    [honeyd-http-siemens.py](./scripts/honeyd-http-siemens.py) so it matches the absolute path of the `ICSpot/scripts/web-siemens` folder in your file system.

4. Pick an IP address that ICSpot will use and replace the IP filed in [honeyd.conf](./honeyd.conf) with your chosen address. Note that the IP address has to be on the *same subnet* of the listening port and should *not* be currently in use.

5. In order to execute the simulation of the physical process and the HMI run:
    
    `make watertower`

    For more info have a look at [waterTower folder](./waterTower/README.md).

6. Copy the modified Snap7 library [libsnap7.so](./snap7/build/bin/x86_64-linux/libsnap7.so) in: `/usr/lib/libsnap7.so`:
    
    ` sudo cp snap7/build/bin/x86_64-linux/libsnap7.so /usr/lib/`

    *N.B.*: By default the libsnap7.so refers to Siemens Simatic 300 PLC profile, which according to [HoneyPLC paper](https://dl.acm.org/doi/10.1145/3372297.3423356), is the one with a lower Honeyscore (thus, less likely to be flagged as Honeypot by search engines). To change the emulated PLC model, you have to rename the library of the target model present in `./snap7/build/bin/x86_64-linux/` into `libsnap7.so` and copy/overwrite it in `/usr/lib/libsnap7.so`.

7. Compile and Execute the s7comm server (you can find it [here](./snap7/examples/cpp/x86_64-linux/server) 

    Compile: `make ./snap7/examples/cpp/server.cpp`  

    Execute: `sudo ./snap7/examples/cpp/x86_64-linux/server 127.0.0.1`

    *N.B.* it may be necessary to fix the sqlite3 db file path inside [server.cpp](./snap7/examples/cpp/server.cpp)

8. From inside the repository, run: 

    `sudo honeyd -d -p nmap-os-db -i INTERFACE -l honeyd.log -f honeyd.conf IP --disable-webserver`

    where IP is the same IP address of Honeyd configuration file and INTERFACE is the interface of the listening port.

9. The host computer has to intercept the network traffic addressed to the Honeypot, to allow honeyd to reply correctly. 
A useful tool that you can use to achieve this result is farpd:

    `sudo farpd -d -i INTERFACE <IP>`

9. ICSpot is now up and running!


## Functioning check

To check the correct functioning of ICSpot you can scan the IP from outside the Host machine with Nmap (e.g., if you are hosting the Honeypot in a VM, you can launch the Nmap from your own machine).

To do this, first install Nmap: `sudo apt install nmap`.

You can use the file with `scanners.sh`. You can launch it all together or just manually pick and run them.

*N.B.* Apparently Nmap does not find the exposed port with a general scan (e.g., `nmap IP`), so you have to use specific commands, which you can find in `scanners.sh`. This is probably because the ICSpot services are different from what Nmap expects.

# To-Do List

- [ ] find an elegant way to fix the honeyd log of port 8000, which generates a packet storm. For now, the implemented solution consists in running the [clean-log.py](./clean-log.py) script on a normal log file.

- [ ] find a way to automatically write the absolute paths in the various files during the installation.

- [ ] verify the functioning of the ubuntu server. We should modify the spanning of the processes in the various terminal. They must persistently be running.

- [ ] Reduce and simplify the installation steps. 


## Team
Francesco Trolese (francesco.trolese.1@studenti.unipd.it)  
Federico Turrin (turrin@math.unipd.it)

We are members of [SPRITZ Security and Privacy Research Group](https://spritz.math.unipd.it/) at the University of Padua, Italy.

Please don't hesitate to contact us for improvement suggestions or to notify bugs.

### Reference

You can find the ICSpot paper at the [following link](https://ieeexplore.ieee.org/abstract/document/9851732).

Are you using ICSpot in your research work? Consider citing us:
```bibtex   
@inproceedings{conti2022icspot,
  title={ICSpot: A High-Interaction Honeypot for Industrial Control Systems},
  author={Conti, Mauro and Trolese, Francesco and Turrin, Federico},
  booktitle={2022 International Symposium on Networks, Computers and Communications (ISNCC)},
  pages={1--4},
  year={2022},
  organization={IEEE}
}
```
