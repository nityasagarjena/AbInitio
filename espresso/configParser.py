#!/usr/bin/env python

# Parses configuration file (for pw.x) and stores it in dictionary.
# It also allows to dump the dictionary to create the configuration file
# The main use case is to parse the existing configuration file, change 
# some values and save it back to the configuration file.

# Input parameters are defined in INPUT_PW.html 

"""
Stability issues:
- Parsing goes line by line. 
- Namelist starts with '&' and ends with '/' on a separate line
- Card starts with card title on a separate line and values between card titles.
- Prints both Namelists and Cards in capital 
- Would like to use ordered dictionary?
- Refactoring?  Introduce class relation: Namelist(Block), Card(Block)
1. Regex: ()
"""


import configPW

ref = {'control': configPW.namelist_control}

namelistsPW = ('control',
             'system',
             'electrons',
             'ions',
             'cell',
             'phonon')

cardsPW = ('atomic_species', 
           'atomic_positions',
           'k_points automatic',
           'cell_parameters',
           'climbing_images',
           'constraints',
           'collective_vars',
           'occupations')

import sys

# Dictionary for Quantum Espresso (QE) configuration file.
# First record in the qe['name'] refers to 'type' of the block which can be either
#  'namelist' or 'card'. E.g. qe = {'control': {'type': 'namelist', ...}}
 
class Namelist():
    """Namelist class that corresponds to Namelist in QE config file"""

    def __init__(self, name):
        # Verifies if the namelist is valid
        try:
            if name not in namelistsPW:
                raise NameError('Not valid namelist')
        except NameError:
            raise

        self.__name = name.lower() # keeps lower name
        self.params = {}

    def name(self):
        return self.__name

    def setName(self, name):
        self.__name = name.lower()

    def param(self, param):
        """Returns value of parameter 'param'"""
        if self.__paramExists(param):
            return self.params[param]

    def addParam(self, param, val):
        # Add verification?
        param = param.lower()
        self.params[param]  = val

    def editParam(self, param, val):
        """Edits parameter. If it doesn't exist, it just ignores it """
        if self.__paramExists(param):
            self.params[param] = val

    def removeParam(self, param):
        """Deletes parameter"""
        if self.__paramExists(param):
            del(self.params[param])

    def __paramExists(self, param):
        try:
            param = param.lower()
            self.params[param]
            return True
        except KeyError:    # parameter is not present
            return False 

    def toString(self, indent="    ", br="\n"):
        # Dump namelist
        s = '&%s%s' % (self.name().upper(), br)

        for p in self.params.keys():
            s += '%s%s = %s%s' % (indent, p, self.params[p], br)

        s += "/%s" % br
        return s

class Card():
    """Card class that corresponds to Card in QE config file"""
    # May be add some more convenience methods?

    def __init__(self, name):
        # Verifies if the card is valid
        try:
            if name not in cardsPW:
                raise NameError('Not valid card')
        except NameError:
            raise

        self.__name     = name.lower() # keeps lower name
        self.__lines    = []

    def name(self):
        return self.__name

    def setName(self, name):
        self.__name = name.lower()

    def line(self, num):
        """Returns value of parameter 'param'"""
        self.__checkRange(num)
        return self.__lines[num]

    def addLine(self, line):
        self.__lines.append(line)

    def removeLine(self, num):
        self.__checkRange(num)
        self.lines.pop(num)

    def removeLines(self):
        self.__lines = []

    def __checkRange(self, num):
        assert num > 0
        assert len(self.__lines) > num

    def toString(self, indent=" ", br="\n"):
        # Dump namelist
        s = '%s%s' % (self.name().upper(), br)

        for l in self.__lines:
            s += '%s%s%s' % (indent, l, br)

        return s

class QEConfig(object):
    """Quantum Espresso configuration class. It can:
    - Parse existing configuration file
    - Add, Edit or Remove parameters from/to namelist or card
    
    """

    def __init__(self, filename=None):
        self.filename   = filename
        self.namelists  = {}
        self.cards      = {}
        self.qe         = [self.namelists, self.cards]

    def createNamelist(self, name):
        """Creates namelist and adds to QEConfig. """
        nl  = Namelist(name)
        self.namelists[name] = nl

    def addNamelist(self, namelist):
        """Adds namelist. """
        self.namelists[namelist.name()] = namelist

    def removeNamelist(self, name):
        try:
            del(self.namelists[name])
        except KeyError:    # parameter is not present
            return

    def namelist(self, name):
        # Do I need editNamelist()?
        try:
            return self.namelists[name]
        except KeyError:    # parameter is not present
            raise

    def createCard(self, name):
        """Creates card and adds to QEConfig. """
        self.cards[name] = Card(name)

    def addCard(self, card):
        """Adds card. """
        self.cards[card.name()] = card

    def removeCard(self, name):
        try:
            del(self.cards[name])
        except KeyError:    # parameter is not present
            return

    def card(self, name):
        # Do I need editNamelist()?
        try:
            return self.cards[name]
        except KeyError:    # parameter is not present
            raise

    def toString(self):
        s = ''
        for nl in self.namelists.values():
            s += nl.toString()

        for c in self.cards.values():
            s += c.toString()
        return s

    def save(self, filename="config.saved"):
        """ Saves the QEConfig to the configuration file"""

        f = open(filename, "w")
        f.write(self.toString())
        f.close()

    def parse():
        """ Parses the configuration file and stores the values in qe dictionary """

        if self.filename is not None:
            try:
                f = open(self.filename)
            except IOError:
                print "I/O error"
            except:
                print "Unexpected error:", sys.exc_info()[0]
                raise

            lines       = f.readlines()
            lines       = __clearLines(lines)
            marks       = __getMarks(lines)

            for m in marks:
                block           = __getBlock(m[0], lines[m[1]:m[2]]) # (type, slice)
                qe[block[0]]    = block[1]

            f.close()
        else:
            print "Error: You haven't specify any config file"


    def __clearLines(lines):
        """ Strips lines from white spaces, commas and empty lines"""

        cl = []     # Lines without white spaces and empty lines
        for l in lines:
            l = l.strip().strip(',') # Remove both lead and trailing whitespace, including '\n' and comma
            if l == '':
                continue

            cl.append(l)

        return cl

    def __getBlock(type, slice):
        """ Returns tuple (namelistName/cardName, parametersDictionary) """

        # Improve calls?
        if type == 'namelist':
            return getNamelist(slice)
        elif type == 'card':
            return getCard(slice)

        return

    def getNamelist(slice):
        """ Returns (namelistName, parametersDictionary)"""

        size    = len(slice)    # 8, numParams = 6
        name    = slice[0].strip('&')
        block   = {}
        block['type'] = 'namelist'

        for s in slice[1:]:
            p           = getParam(s)
            block[p[0]] = p[1]

        return (name, block)

    def getCard(slice):
        """ Returns (cardName, parametersDictionary)"""

        name    = slice[0].lower()
        block   = {}
        block['type'] = 'card'
        vals    = []
        for s in slice[1:]:
            vals.append(s)
        block['values'] = vals

        return (name, block)

        #Example return: ('atomic_species', {'type': 'card', 'values': ('Ni  26.98  Ni.pbe-nd-rrkjus.UPF', 'Other line', 'Another line')})


    def __getMarks(lines):
        """
        Determines start and end of namelist and card blocks: [type, start, end]
        E.g ['namelist', 0, 7] for CONTROL namelist
        Iterate over number of lines. Empty lines are included
        Not tested very well yet
        """
        blocklist   = []
        isNamelist  = False
        isCard      = False
        size        = len(lines)

        for i in range(size):
            l = lines[i]
            # We suppose that namelists and card do not intersect
            # Namelist part

            # Namelist end
            if l[0] == '/' and isNamelist:
                isNamelist  = False
                block.append(i)
                blocklist.append(block)

            # Namelist start
            if l[0] == '&' and not isNamelist:
                name = l[1:].lower()

                if not name in namelistsPW:
                    continue             # namelist is not recognizable

                block       = []
                isNamelist  = True
                block.append('namelist')
                block.append(i)

            # Card part
            line    = l.lower()
            # Card end
            if line in cardsPW and isCard:
                #print "End: %s, line: %d" % (line, i-1)
                isCard  = False
                block.append(i)
                blocklist.append(block)

            if i == size-1 and isCard:
                isCard  = False
                block.append(i+1)
                blocklist.append(block)

            # Card start
            if line in cardsPW and not isCard:
                #print "Start: %s, line: %d" % (line, i)
                block   = []
                isCard  = True
                block.append('card')
                block.append(i)

        return blocklist

        # Example return: [['namelist', 0, 7], ['namelist', 8, 20]]

    def getParam(s):
        """ Takes string like 'a = 2' and returns tuple ('a', 2) """

        ss = s.split('=')
        for i in range(len(ss)):
            ss[i] = ss[i].strip()

        val = ss[1]

        # Assume that there are two values only: (variable, value) pair
        assert len(ss) == 2

        return (ss[0], val)


def testCreateConfig():
    qe  = QEConfig()
    nl  = Namelist('control')
    nl.addParam('title', "'Ni'")
    nl.addParam('restart_mode', "'from_scratch'")
    print nl.toString()
    nl.editParam('title', "'Fe'")
    #nl.removeParam('title')

    qe.addNamelist(nl)
    print qe.toString()

    c = Card('atomic_species')
    c.addLine('Ni  26.98  Ni.pbe-nd-rrkjus.UPF')
    print c.toString()
    qe.addCard(c)
    print qe.toString()
    qe.save()
    """
    nl  = Namelist('system')
    nl.addParam('ibrav', 2)
    qe.addNamelist(nl)

    qe.save("testsNi.out")
    """
    """
    if filename is None:
        if len(sys.argv) != 2:
            print "Usage: configParser.py <config_file>"
            return
        else:
            filename = sys.argv[1]
    """
    """
    parse("vini/ni.scf.in")
    addNamelistParam('control', 'title', 'Ni')
    removeNamelistParam('control', 'title') #'verbosity')
    removeCard('atomic_species', )
    editNamelistParam('control', 'calculation', "'nscf'")
    editCardParam('atomic_positions', ['blah'])
    save("ni.scf.in.saved")
    """

    """
    addNamelistParam('control', 'calculation', "'scf'")
    addNamelistParam('system', 'ibrav', 2)
    save("testni.in")
    """

if __name__ == "__main__":
    testCreateConfig()
