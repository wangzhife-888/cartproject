# -*- coding: utf-8 -*-
"""
@Time: 2023/12/12 16:44
@Author: liucong
@File: testACU_server.py
@IDE: PyCharm
@Description: 
"""
import signal
import sys
import Ice

Ice.loadSlice('ACU.ice')
import shao6

import ACUCMD


# Ice.loadSlice('ACU.ice')
class ACUI(shao6.rpcACU):
    def __init__(self):
        # local_addr = '127.0.0.1'
        local_addr = '192.168.100.120'
        local_port = 8090
        acu_add = '192.168.100.10'
        acu_port = 8091
        self.ACUDriver = ACUCMD.ACUDriver(local_addr, local_port, acu_add,acu_port)

    def setAzElPVA(self, azp, azv, aza, elp, elv, ela, azcir, current=None):
        self.ACUDriver.setAzElPVA(azp, azv, aza, elp, elv, ela, azcir)
        print("azp: %s, azv: %s, aza: %s, elp: %s, elv: %s, ela: %s, azcir: %s" % (azp, azv, aza, elp, elv, ela, azcir))
        return 0


    def getStatus50ms(self, current=None):

        return self.ACUDriver.getStatus_50ms()






#
# Ice.initialize returns an initialized Ice communicator,
# the communicator is destroyed once it goes out of scope.
#

with Ice.initialize(sys.argv) as communicator:
    adapter = communicator.createObjectAdapterWithEndpoints("SimpleACUAdapter", "default -h localhost -p 10005")
    adapter.add(ACUI(), Ice.stringToIdentity("SimpleACU"))
    adapter.activate()
    communicator.waitForShutdown()