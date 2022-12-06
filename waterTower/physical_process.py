"""
SWaT sub1 physical process

RawWaterTank has an inflow pipe and outflow pipe, both are modeled according
to the equation of continuity from the domain of hydraulics
(pressurized liquids) and a drain orefice modeled using the Bernoulli's
principle (for the trajectories).
"""


from minicps.devices import Tank

from utils import PUMP_FLOWRATE_IN, PUMP_FLOWRATE_OUT
from utils import TANK_SECTION
from utils import LIT_101_M, RWT_INIT_LEVEL
from utils import STATE, PP_PERIOD_SEC, PP_PERIOD_HOURS

import time
import pandas as pd


# SPHINX_SWAT_TUTORIAL TAGS(
MV001 = ('MV001', 0)
P201 = ('P201', 2)
LIT101 = ('LIT101', 1)
FIT101 = ('FIT101', 1)
FIT201 = ('FIT201', 2)
# SPHINX_SWAT_TUTORIAL TAGS)


# TODO: implement orefice drain with Bernoulli/Torricelli formula
class RawWaterTank(Tank):

    def pre_loop(self):

        # SPHINX_SWAT_TUTORIAL STATE INIT(
        self.set(MV001, 1)
        self.set(P201, 2)
        self.level = self.set(LIT101, 0.500)
        # SPHINX_SWAT_TUTORIAL STATE INIT)

    def main_loop(self):

        count = 0
        columns = ['Time', 'MV001', 'P201', 'LIT101', 'FIT101', 'FIT201']
        df = pd.DataFrame(columns=columns)
        timestamp=0
        while True: # Do not stop the flow of water 
            print("DEBUG COUNT" + str(count))

            new_level = self.level

            # compute water volume
            water_volume = self.section * new_level

            # inflows volumes
            mv001 = int(self.get(MV001))
            if mv001 == 1:
                self.set(FIT101, PUMP_FLOWRATE_IN)
                inflow = PUMP_FLOWRATE_IN * PP_PERIOD_HOURS
                print("DEBUG RawWaterTank inflow: ", inflow)
                water_volume += inflow
            else:
                self.set(FIT101, 0.00)

            # outflows volumes
            p201 = int(self.get(P201))
            if p201 == 1:
                self.set(FIT201, PUMP_FLOWRATE_OUT)
                outflow = PUMP_FLOWRATE_OUT * PP_PERIOD_HOURS
                print("DEBUG RawWaterTank outflow: ", outflow)
                water_volume -= outflow
            else:
                pass
            # compute new water_level
            new_level = water_volume / self.section

            # adjust level not to break the simulation in case of attack
            if new_level >= 1.15:
                new_level = 1.1
            if new_level <= 0.05:
                new_level = 0.1

            # level cannot be negative
            if new_level <= 0.0:
                new_level = 0.0

            # update internal and state water level
            print("DEBUG new_level: %.5f \t delta: %.5f" % (new_level, new_level - self.level))
            self.level = self.set(LIT101, new_level)

            # TODO overflow
            if new_level >= LIT_101_M['HH']:
                print('DEBUG RawWaterTank above HH count: ', count)
                break

            # TODO underflow
            elif new_level <= LIT_101_M['LL']:
                print('DEBUG RawWaterTank below LL count: ', count)
                #break

            df = df.append(pd.Series([timestamp, self.get(MV001), self.get(P201), self.get(LIT101), self.get(FIT101), self.get(FIT201)], index=df.columns), ignore_index=True)
            df.to_csv('physical_log.csv', index=False)
            count += 1
            time.sleep(PP_PERIOD_SEC)
            timestamp+=PP_PERIOD_SEC


if __name__ == '__main__':

    rwt = RawWaterTank(
        name='rwt',
        state=STATE,
        protocol=None,
        section=TANK_SECTION,
        level=RWT_INIT_LEVEL
    )