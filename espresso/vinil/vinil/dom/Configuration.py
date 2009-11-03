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

configElectons = """ &control
    calculation='scf'
    restart_mode='from_scratch',
    tprnfor = .true.
    prefix='ni',
    pseudo_dir = '',
    outdir=''
 /
 &system
    ibrav=2,
    celldm(1) =6.65,
    nat=  1,
    ntyp= 1,
    nspin=2,
    starting_magnetization(1)=0.5,
    degauss=0.02,
    smearing='gauss',
    occupations='smearing',
    ecutwfc =27.0
    ecutrho =300.0
 /
 &electrons
    conv_thr =  1.0d-8
    mixing_beta = 0.7
 /
ATOMIC_SPECIES
 Ni  26.98  Ni.pbe-nd-rrkjus.UPF
ATOMIC_POSITIONS
 Ni 0.00 0.00 0.00
K_POINTS AUTOMATIC
4 4 4 1 1 1"""

configPhonons = """phonons of Ni at gamma
&inputph
  tr2_ph=1.0d-16,
  prefix='ni',
  ldisp=.true.,
  nq1=2,
  nq2=2,
  nq3=2,
  amass(1)=58.6934,
  outdir='',
  fildyn='ni.dyn',
/"""

configPP = """&inputpp
   prefix='ni',
   outdir='',
   fildos='',
   Emin=5.0,
   Emax=25.0,
   DeltaE=0.1
/"""

from vinil.utils.utils import timestamp
from vinil.utils.utils import ifelse

#def timestamp():
#    import time
#    return int(time.time())


examples    = (
               {"id": 1, "simulationId": 4, "type": "PW",
               "filename": "ni.scf.in", "description": "", "timeCreated": timestamp(),
               "timeModified": timestamp(), "text": configElectons},
               {"id": 2, "simulationId": 5, "type": "PH",
                "filename": "ni.ph.in", "description": "", "timeCreated": timestamp(),
                "timeModified": timestamp(), "text": configPhonons},
               {"id": 3, "simulationId": 6, "type": "PP",
                "filename": "ni.pp.in", "description": "", "timeCreated": timestamp(),
                "timeModified": timestamp(), "text": configPP}
              )


from pyre.db.Table import Table

class Configuration(Table):

    name = "configuration"
    import pyre.db

    id = pyre.db.varchar(name="id", length=8)
    id.constraints = 'PRIMARY KEY'
    id.meta['tip'] = "the unique id"

    simulationId    = pyre.db.varchar(name="simulationId", length=8)
    #simulationId.constraints = 'REFERENCES simulation (id)'    # Important
    simulationId.meta['tip'] = "simulationId"

    type        = pyre.db.varchar(name="type", length=1024, default='')
    type.meta['tip'] = "Type of configuration. Example: PW, PP"

    # Later on can be tranformed to a separate File table
    filename    = pyre.db.varchar(name="filename", length=1024, default='')
    filename.meta['tip'] = "Filename assiciated with this configuration"

    description = pyre.db.varchar(name="description", length=1024, default='')
    description.meta['tip'] = "description"

    timeCreated = pyre.db.varchar(name="timeCreated", length=16, default='')
    timeCreated.meta['tip'] = "timeCreated"

    timeModified = pyre.db.varchar(name="timeModified", length=16, default='')
    timeModified.meta['tip'] = "timeModified"

    text = pyre.db.varchar(name="text", length=8192, default='')
    text.meta['tip'] = "text"


#    def createConfigRecord(director, params):
#        """Inserts configuration row """
#        self.id            = director.idd.token().locator
#        self.simulationId  = params['simulationId'] #self.id
#        self.type          = params[''] self.configtype
#        self.filename      = params[''] self.fname
#        self.description   = ""
#        self.timeCreated   = timestamp()
#        self.timeModified  = timestamp()
#        self.text          = self.text
#        director.clerk.insertNewRecord(c)


# For debugging
def inittable(db):
    
    def configuration(params):
        r               = Configuration()
        r.id            = params['id']
        r.simulationId  = params['simulationId']
        r.type          = params['type']
        r.filename      = params['filename']
        r.description   = params['description']
        r.timeCreated   = params['timeCreated']
        r.timeModified  = params['timeModified']
        r.text          = params['text']
        return r

    records = []
    for e in examples:
        records.append(configuration(e))

    for r in records: db.insertRow( r )
    return

def test():
    for e in examples:
        s = ""
        for v in e.keys():
            s += "%s: %s " % (v, e[v])
        print s

if __name__ == "__main__":
    test()

__date__ = "$Oct 5, 2009 8:58:32 AM$"


