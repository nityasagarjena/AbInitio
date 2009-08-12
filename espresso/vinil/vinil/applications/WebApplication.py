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

from luban.applications.WebApplication import WebApplication as Base

class WebApplication(Base):

    class Inventory(Base.Inventory):

        import opal.inventory
        import pyre.inventory

        # components
        actor = opal.inventory.actor(default='greet')
        actor.meta['tip'] = "the component that defines the application behavior"

#        import pyre.idd
#        idd = pyre.inventory.facility('idd-session', factory=pyre.idd.session, args=['idd-session'])
#        idd.meta['tip'] = "access to the token server"

#        from vinil.components import clerk
#        clerk = pyre.inventory.facility(name="clerk", factory=clerk)
#        clerk.meta['tip'] = "the component that retrieves data from the various database tables"

#        from vinil.components.DummyClerk import Clerk
#        #import vinil.components
#        clerk = pyre.inventory.facility('clerk', factory=Clerk)

#        debug = pyre.inventory.bool(name="debug", default=True)
#        debug.meta['tip'] = "suppress some html output for debugging purposes"

        imagepath       = pyre.inventory.str(name='imagepath', default = 'images' )
        javascriptpath  = pyre.inventory.str(name='javascriptpath', default = 'javascripts' )

    def __init__(self, name):
        Base.__init__(self, name)

#        # access to the token server
#        self.idd = None

        # access to the data retriever
#        self.clerk = None

#        # debugging mode
#        self.debug = False


    def main(self, *args, **kwds):
        actor = self.actor

        # If no actor is provided e.g.: example.com/main.cgi
        if actor is None:
            self.actor = self.retrieveActor('greet')

        try:
            page = self.actor.perform(self, routine=self.inventory.routine, debug=self.debug)

            if isinstance(page, basestring):
                print page
            else:
                self.render(page)
        except:
            self.plainBugReport()

    def retrievePage(self, name):
        page = super(WebApplication, self).retrievePage(name)
        if page:
            return page
        raise RuntimeError, "Unable to load page %s" % name

    def redirect(self, actor, routine, **kwds):
        self.inventory.routine = routine
        self.actor = self.retrieveActor(actor)

        if self.actor is not None:
            self.configureComponent(self.actor)
            for k,v in kwds.iteritems():
                setattr(self.actor.inventory, k, v)

        try:
            self.main()
        except:
            raise RuntimeError, "redirect to actor %r, routine %r, with kwds %r failed" % (
                actor, routine, kwds)
        return

    def plainBugReport(self):
        print '<pre>'
        import traceback
        traceback.print_exc()
        print '</pre>'
        return

    def render(self, page=None):
        self.weaver.resetRenderer()
        self.weaver.weave(document=page, stream=self.stream)
        return

    def _defaults(self):
        super(WebApplication, self)._defaults()
        from luban.components.weaver.web import weaver
        self.inventory.weaver = weaver()
        return

    def _configure(self):
        super(WebApplication, self)._configure()

#        self.idd = self.inventory.idd
#        self.clerk = self.inventory.clerk
#        self.debug = self.inventory.debug
#        print self.clerk
        self.clerk.director = self

        return

    def _init(self):
        super(WebApplication, self)._init()
        
    """
    def _getPrivateDepositoryLocations(self):

        import os
        odbroot = os.path.abspath('../content')
        config = os.path.abspath('../config')

        depos = []
        depos.append(config)

        for entry in os.listdir(odbroot):
            path = os.path.join(odbroot, entry)
            if os.path.isdir(path): depos.append(path)
            continue

        return depos
    """
    
    def _getPrivateDepositoryLocations(self):
        from os.path import join
        root = '..'
        content = join(root, 'content')
        config = join(root, 'config')

        return [config, content]

if __name__=='__main__':
    w = WebApplication(name = 'test')
    print w


__date__ = "$Aug 5, 2009 4:23:32 PM$"


