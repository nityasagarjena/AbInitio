#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Alex Dementsov
#                      California Institute of Technology
#                        (C) 2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

from pyre.services.TCPService import TCPService
MAXSIZE = 1024

class EchoService(TCPService):

    def __init__(self, name=None):
        super(EchoService, self).__init__(name)

    
    def onConnectionAttempt(self, selector, monitor):
        socket, address = monitor.accept()

        # How to include marshaller?
        data    = socket.recv(MAXSIZE)
        if data:
            socket.send(data)
        else:
            socket.close()

        return True



#    class Inventory(TCPService.Inventory):
#
#        import pyre.inventory
#        from pyre.services import pickler
#        marshaller = pyre.inventory.facility("marshaller", factory=pickler)
#
#
#    def _configure(self):
#        super(EchoService, self)._configure()
#
#        self.marshaller = self.inventory.marshaller



#        selector.notifyOnReadReady(socket, )
#        request = self.marshaller.receive(socket)
        #print request
#        result = self.evaluator.evaluate(self, request.command, request.args)
#        self.marshaller.send(result, socket)

#        f   = open("/tmp/request.log", "w")
#        f.write("%s" % request)
#        f.close()


        





#        if not self.validateConnection(address):
#            return True
#
#        try:
#            request = self.marshaller.receive(socket)
#        except ValueError, msg:
#            self._debug.log("bad request: %s" % msg)
#            return True
#        except self.marshaller.RequestError, msg:
#            self._info.log(msg)
#            return True
#
#        self._info.log("request from [%d@%s]: command=%r, args=%r" % (
#            address[1], address[0], request.command, request.args))
#
#        result = self.evaluator.evaluate(self, request.command, request.args)
#
#        self._debug.log("got result: %s" % result)
#
#        try:
#            self.marshaller.send(result, socket)
#        except self.marshaller.RequestError, msg:
#            self._debug.log(msg)
#
#        return True



#    def _init(self):
#        super(EchoService, self)._init()
#
#        self.selector   = self._createSelector()    # From pyre.services.Service
#        self.monitor    = self._createPortMonitor()
#        self.port       = 50010 # Listen on port




#from pyre.components.Component import Component
#
#class EchoService(Component):
##
##    from cassandra.time.Scheduler import Scheduler
##    from Session import Session
#
#
#    class Inventory(Component.Inventory):
#
#        import pyre.inventory
#
#        from pyre.units.time import minute
#        timeout = pyre.inventory.dimensional("timeout", default=10.0*minute)
#
#
##    def newSession(self, socket, address, marshaller):
##        session = self.Session(socket, address,
##                               marshaller, self.evaluator, self.scheduler,
##                               self.delegate)
##        session.registerHandlers(self.selector)
##        return session
##
#
#    def eventLoop(self):
#        self.selector.watch(self.timeout)
#
#
#    def __init__(self, name, facility=None):
#        if facility is None:
#            facility = "client"
#
#        Component.__init__(self, name, facility)
#
#        # the event loop and dispatcher
#        self.selector = None
#
#
#    def _configure(self):
#        Component._configure(self)
#        self.timeout = self.inventory.timeout.value
#        return
#
#
#    def _init(self):
#        Component._init(self)
#
#        import pyre.ipc
#        self.selector = pyre.ipc.selector()


__date__ = "$Nov 13, 2009 4:30:06 PM$"


