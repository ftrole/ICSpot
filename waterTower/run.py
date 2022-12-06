"""
waterTower run.py
"""

from mininet.net import Mininet
from mininet.cli import CLI
from minicps.mcps import MiniCPS

from topo import SwatTopo

import sys


class waterTowerCPS(MiniCPS):

    """Main container used to run the simulation."""

    def __init__(self, name, net):

        self.name = name
        self.net = net

        net.start()

        net.pingAll()

        # start devices
        plc0, plc1, plc2, s1 = self.net.get(
            'plc0', 'plc1', 'plc2', 's1')

        plc2.cmd('python2 plc2.py &')
        plc1.cmd('python2 plc1.py &')
        s1.cmd('python2 physical_process.py &')

        print("Devices started")

        
        CLI(self.net)

        net.stop()

if __name__ == "__main__":

    topo = SwatTopo()
    net = Mininet(topo=topo)

    watertower_cps = waterTowerCPS(
        name='waterTower',
        net=net)
