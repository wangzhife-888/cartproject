# -*- coding: utf-8 -*-
#
# Copyright (c) ZeroC, Inc. All rights reserved.
#
#
# Ice version 3.7.10
#
# <auto-generated>
#
# Generated from file `ACU.ice'
#
# Warning: do not edit this file.
#
# </auto-generated>
#

from sys import version_info as _version_info_
import Ice, IcePy

# Start of module shao6
_M_shao6 = Ice.openModule('shao6')
__name__ = 'shao6'

if '_t_dicparam' not in _M_shao6.__dict__:
    _M_shao6._t_dicparam = IcePy.defineDictionary('::shao6::dicparam', (), IcePy._t_string, IcePy._t_string)

_M_shao6._t_rpcACU = IcePy.defineValue('::shao6::rpcACU', Ice.Value, -1, (), False, True, None, ())

if 'rpcACUPrx' not in _M_shao6.__dict__:
    _M_shao6.rpcACUPrx = Ice.createTempClass()
    class rpcACUPrx(Ice.ObjectPrx):

        def setAzElPVA(self, azp, azv, aza, elp, elv, ela, azcir, context=None):
            return _M_shao6.rpcACU._op_setAzElPVA.invoke(self, ((azp, azv, aza, elp, elv, ela, azcir), context))

        def setAzElPVAAsync(self, azp, azv, aza, elp, elv, ela, azcir, context=None):
            return _M_shao6.rpcACU._op_setAzElPVA.invokeAsync(self, ((azp, azv, aza, elp, elv, ela, azcir), context))

        def begin_setAzElPVA(self, azp, azv, aza, elp, elv, ela, azcir, _response=None, _ex=None, _sent=None, context=None):
            return _M_shao6.rpcACU._op_setAzElPVA.begin(self, ((azp, azv, aza, elp, elv, ela, azcir), _response, _ex, _sent, context))

        def end_setAzElPVA(self, _r):
            return _M_shao6.rpcACU._op_setAzElPVA.end(self, _r)

        def setFeed(self, command, angle, context=None):
            return _M_shao6.rpcACU._op_setFeed.invoke(self, ((command, angle), context))

        def setFeedAsync(self, command, angle, context=None):
            return _M_shao6.rpcACU._op_setFeed.invokeAsync(self, ((command, angle), context))

        def begin_setFeed(self, command, angle, _response=None, _ex=None, _sent=None, context=None):
            return _M_shao6.rpcACU._op_setFeed.begin(self, ((command, angle), _response, _ex, _sent, context))

        def end_setFeed(self, _r):
            return _M_shao6.rpcACU._op_setFeed.end(self, _r)

        def getStatus50ms(self, context=None):
            return _M_shao6.rpcACU._op_getStatus50ms.invoke(self, ((), context))

        def getStatus50msAsync(self, context=None):
            return _M_shao6.rpcACU._op_getStatus50ms.invokeAsync(self, ((), context))

        def begin_getStatus50ms(self, _response=None, _ex=None, _sent=None, context=None):
            return _M_shao6.rpcACU._op_getStatus50ms.begin(self, ((), _response, _ex, _sent, context))

        def end_getStatus50ms(self, _r):
            return _M_shao6.rpcACU._op_getStatus50ms.end(self, _r)

        @staticmethod
        def checkedCast(proxy, facetOrContext=None, context=None):
            return _M_shao6.rpcACUPrx.ice_checkedCast(proxy, '::shao6::rpcACU', facetOrContext, context)

        @staticmethod
        def uncheckedCast(proxy, facet=None):
            return _M_shao6.rpcACUPrx.ice_uncheckedCast(proxy, facet)

        @staticmethod
        def ice_staticId():
            return '::shao6::rpcACU'
    _M_shao6._t_rpcACUPrx = IcePy.defineProxy('::shao6::rpcACU', rpcACUPrx)

    _M_shao6.rpcACUPrx = rpcACUPrx
    del rpcACUPrx

    _M_shao6.rpcACU = Ice.createTempClass()
    class rpcACU(Ice.Object):

        def ice_ids(self, current=None):
            return ('::Ice::Object', '::shao6::rpcACU')

        def ice_id(self, current=None):
            return '::shao6::rpcACU'

        @staticmethod
        def ice_staticId():
            return '::shao6::rpcACU'

        def setAzElPVA(self, azp, azv, aza, elp, elv, ela, azcir, current=None):
            raise NotImplementedError("servant method 'setAzElPVA' not implemented")

        def setFeed(self, command, angle, current=None):
            raise NotImplementedError("servant method 'setFeed' not implemented")

        def getStatus50ms(self, current=None):
            raise NotImplementedError("servant method 'getStatus50ms' not implemented")

        def __str__(self):
            return IcePy.stringify(self, _M_shao6._t_rpcACUDisp)

        __repr__ = __str__

    _M_shao6._t_rpcACUDisp = IcePy.defineClass('::shao6::rpcACU', rpcACU, (), None, ())
    rpcACU._ice_type = _M_shao6._t_rpcACUDisp

    rpcACU._op_setAzElPVA = IcePy.Operation('setAzElPVA', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, None, (), (((), IcePy._t_double, False, 0), ((), IcePy._t_double, False, 0), ((), IcePy._t_double, False, 0), ((), IcePy._t_double, False, 0), ((), IcePy._t_double, False, 0), ((), IcePy._t_double, False, 0), ((), IcePy._t_int, False, 0)), (), ((), IcePy._t_bool, False, 0), ())
    rpcACU._op_setFeed = IcePy.Operation('setFeed', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, None, (), (((), IcePy._t_bool, False, 0), ((), IcePy._t_double, False, 0)), (), ((), IcePy._t_bool, False, 0), ())
    rpcACU._op_getStatus50ms = IcePy.Operation('getStatus50ms', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, None, (), (), (), ((), _M_shao6._t_dicparam, False, 0), ())

    _M_shao6.rpcACU = rpcACU
    del rpcACU

# End of module shao6
