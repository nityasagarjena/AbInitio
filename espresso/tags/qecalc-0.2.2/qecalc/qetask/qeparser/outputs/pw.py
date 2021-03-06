#!/usr/bin/env python
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# QEcalc              by DANSE Inelastic group
#                     Nikolay Markovskiy
#                     California Institute of Technology
#                     (C) 2009  All Rights Reserved
#
# File coded by:      Nikolay Markovskiy
#
# See AUTHORS.txt for a list of people who contributed.
# See LICENSE.txt for license information.
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import string
from qe_io_dict import *
import numpy
from baseoutput import BaseOutput

class Output(BaseOutput):

    def __init__(self):
        BaseOutput.__init__(self)
        self.parsers = {
                    'total energy'       : self.getTotalEnergy,
                    'lattice parameters' : self.getLatticeParameters,
                    'fermi energy'       : self.getFermiEnergy,
                    'stress'             : self.getStress,
                    'forces'             : self.getForces,
                    'bands'              : self.getBands,
                   }

    def getTotalEnergy(self, setting):
        """
        Extract total energy value from pwscf output
        """
        #read Espresso output into memory:
        file = open(setting.get('pwOutput'))
        pwscfOut = file.readlines()
        posList =  [i for i,line in enumerate(pwscfOut) if '!    total energy' in line]
        return [([float(pwscfOut[posList[-1]].split()[4])], 'Ry')]

        #pwscfOut = read_file(setting.pwscfOutput)
        #key = find_key_from_marker_string(pwscfOut, '!', 'total energy')
        #words = string.split(pwscfOut[key])
        #return [([float(words[4])], 'Ry')]
        
    def getFermiEnergy(self, setting):
        """
        Extract Fermi energy value from pwscf output
        """
        #read Espresso output into memory:
        file = open(setting.get('pwOutput'))
        pwscfOut = file.readlines()
        posList =  [i for i,line in enumerate(pwscfOut) if 'the Fermi energy is' in line]
        return [([float(pwscfOut[posList[-1]].split()[4])], 'eV')]   

    def getLatticeParameters(self, setting):
        """
        Extract lattice parameters after pwscf geometry optimization
        Returns a list of 6 parameters: A, B, C, cos(BC), cos(AC), cos(AB)
        """
        # does not work yet
        return [(None, None)]
        from qecalc.qetask.qeparser.qelattice import QELattice
        # does not work yet
        # obtain lattice from PWSCF input file:
        lat = QELattice(setting)
        pwscfOut = read_file(setting.get('pwOutput'))
        key_a_0 = find_key_from_string(pwscfOut, 'lattice parameter (a_0)')
        a_0 = float( string.split( pwscfOut[key_a_0] )[4] )
        if lat.type == 'traditional': a_0 = a_0*0.529177249 # convert back to angstrom
        keyEnd = max( find_all_keys_from_marker_string(pwscfOut, '!', 'total energy') )
        keyCellPar = find_key_from_string_afterkey(pwscfOut, keyEnd, \
                                                  'CELL_PARAMETERS (alat)') + 1
        latticeVectors = [[float(valstr)*a_0 for valstr in string.split( pwscfOut[keyCellPar] ) ],
                         [ float(valstr)*a_0 for valstr in string.split( pwscfOut[keyCellPar+1] ) ],
                         [ float(valstr)*a_0 for valstr in string.split( pwscfOut[keyCellPar+2] ) ]]
        lat.setLatticeFromQEVectors(lat.ibrav, latticeVectors)
        return [([lat.a, lat.b, lat.c, lat.cBC ,lat.cAC , lat.cAB], None)]
        

    def getStress(self, setting):
        """
        Extract total stress in kbar after pwscf launch or geometry optimization
        """
        pwscfOut = read_file(setting.get('pwOutput'))
        key = find_last_key_from_string(pwscfOut, 'total   stress  (Ry/bohr**3)') + 1
        stress = [[float(val) for val in string.split( pwscfOut[key] )[3:] ],
                  [float(val) for val in string.split( pwscfOut[key+1] )[3:] ],
                  [float(val) for val in string.split( pwscfOut[key+2] )[3:] ]]
        return [(stress, 'Ry/bohr**3')]

    def getForces(self, setting):
        pwscfOut = read_file(setting.get('pwOutput'))
        key = find_last_key_from_string(pwscfOut, 'Forces acting on atoms (Ry/au):') + 2
        forces = []
        while 'atom' in pwscfOut[key]:
            forces.append([float(val) for val in string.split( pwscfOut[key] )[6:]])
            key = key + 1
        return [(forces, 'Ry/au')]

    def getBands(self, setting):
        """
        parses pw.x (scf or nscf) output for electronic bands.
        outputs prsed kpoints and bands as numpy arrays
        """
        kpoints = []
        bands = []
        pwscfOut = open(setting.get('pwOutput')).readlines()
        posList =  [i for i,line in enumerate(pwscfOut) \
                            if 'End of self-consistent calculation' in line or \
                            'End of band structure calculation' in line ]
        for i,line in enumerate(pwscfOut[posList[-1]:]):
            if 'band energies (ev):' in line or \
                'bands (ev):' in line:
                words = line.split('-')
                kpt = []
                for j, w in enumerate(words[1:]):
                    words[j+1] = ' -'+ words[j+1]
                kpoints.append([float(w) for w in ''.join(words).split()[2:5]])
                s = ''
                for l in pwscfOut[(posList[-1] + i + 1):]:
                    if 'band energies (ev):' not in l and \
                       'occupation numbers'  not in l and \
                       'the Fermi energy is' not in l and \
                       'highest occupied, lowest unoccupied level' not in l and \
                       'bands (ev):' not in  l:
                        s = s + l
                    else:
                        break
                bands.append([float(w) for w in s.split()])
        return [(numpy.array(kpoints), None), (numpy.array(bands), 'eV')]

if __name__ == "__main__":
    #from qecalc.qetask.qeparser import PWInput
    #from qecalc.qetask.qeparser.qestructure import QEStructure
    #setting = Setting('config.ini')
    #pwInput = PWInput(setting)
    output = Output()    
    