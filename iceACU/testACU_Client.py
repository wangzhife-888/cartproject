# -*- coding: utf-8 -*-
"""
@Time: 2023/12/12 16:24
@Author: liucong
@File: testACU_Client.py
@IDE: PyCharm
@Description: 
"""
import Ice
import sys, traceback
import shao6
import time

class SH13mClinet:
    def __init__(self):
        # try:
        #     with Ice.initialize(sys.argv) as communicator:
        #         base = communicator.stringToProxy("SimpleACU:default -h localhost -p 10001")
        #         self.rpcACU = shao6.rpcACUPrx.checkedCast(base)
        #         if not self.rpcACU:
        #             raise RuntimeError("Invalid proxy")
        #
        #         # self.rpcACU.setAzElPVA()
        # except:
        #     traceback.print_exc()
        #     status = 1
        try:
            self.communicator = Ice.initialize(sys.argv)
            base = self.communicator.stringToProxy("SimpleACU:default -h localhost -p 10005")
            self.rpcACU = shao6.rpcACUPrx.checkedCast(base)
            if not self.rpcACU:
                raise RuntimeError("Invalid proxy")

                # self.rpcACU.setAzElPVA()
        except:
            traceback.print_exc()
            status = 1

    def __del__(self):
        # Clean up
        if self.communicator:
            try:
                self.communicator.destroy()
            except:
                traceback.print_exc()
                status = 1



    def setAntPos(self, az, el):
        #  软件限位
        # if 0 < az < 360 and 5 < el < 88:
        if 90 < az < 270 and 18 < el < 85:

            self.rpcACU.setAzElPVA(azp=az, azv=0, aza=0, elp=el, elv=0, ela=0, azcir=0)
        else:
            print("软件限位，未发送指令")

    def getDetailStatus(self):
        return self.rpcACU.getStatus50ms()


if __name__ == '__main__':
    sh13m = SH13mClinet()
    # sh13m.setAntPos(az=178.5, el=84)
    while True:
        v = sh13m.getDetailStatus()
        time.sleep(0.05)
        print(v)
        print(type(v))