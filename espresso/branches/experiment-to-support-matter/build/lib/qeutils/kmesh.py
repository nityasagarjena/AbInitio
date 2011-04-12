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
import numpy

def kMesh(nkpt):
    """Will generate k-point mesh in crystal coordinates in [0,1] box
    Mesh is uniform. I.e. lattice symmetry is not taken into account."""
    nkx = nkpt[0]
    nky = nkpt[1]
    nkz = nkpt[2]
    j = numpy.complex(0,1)
    data = numpy.mgrid[0.0:1.0:nkx*j,0:1.0:nky*j,0:1.0:nkz*j]
    data = numpy.transpose(data.reshape(3,nkx*nky*nkz))
    return data


def kMeshCart(nkpt, recipLatticeVectors):
    """
    Will generate k-point mesh in cartesian coordinates
    Lattice symmetry is not taken into account.
    nkpt - list with kpoint dimensions (nkx,nky,nkz)
    """
    kpts = kMesh(nkpt)
    kpts_cart = numpy.zeros(kpts.shape)
    for k in range(kpts.shape[0]):
        # convert into cartesian coordinates in units of inv lattice vector a
        kpts_cart[k,:] = numpy.dot( kpts[k,:], recipLatticeVectors)
#        kpts_cart[k,:] = self.structure.lattice.recipCartesian(kpts[k,:])
#            self.structure.lattice.matter().cartesian(kpt)/ \
#                        self.structure.lattice.a

    return kpts_cart

def packBands(kpoints, Bands):
    """
    Will repack band listst, obtained  from kpoints  generated with kMesh to
    bands[iband,nkx,nky,nkz], which can be visualized for example in bandstobxsf.
    kpoints - list [nx,ny,nz]. Bands - 2d array (nkpoint, modes) of sequential
    list of points. It is assumed the points are in the following order:
    ny*nz*qz + ny*qy + qx
    """
    bands = numpy.zeros((Bands.shape[1], kpoints[0], kpoints[1], kpoints[2]))
    for iband in range(Bands.shape[1]):
        for kz in range(kpoints[2]):
            for ky in range(kpoints[1]):
                for kx in range(kpoints[0]):
                    bands[iband,kx,ky,kz] = \
                    Bands[kpoints[2]*kpoints[1]*kz + kpoints[1]*ky + kx,iband]
    return bands

#class Kpoints:
#    def _kMesh(self, nkx, nky, nkz):
#        """Will generate k-point mesh in crystal coordinates in [0,1] box
#        Mesh is uniform. I.e. lattice symmetry is not taken into account."""
#        j = numpy.complex(0,1)
#        data = numpy.mgrid[0.0:1.0:nkx*j,0:1.0:nky*j,0:1.0:nkz*j]
#        data = numpy.transpose(data.reshape(3,nkx*nky*nkz))
#        return data
#
#    def kMeshCart(self, nq1, nq2, nq3, structure):
#        """Will generate k-point mesh in cartesian coordinates
#        Lattice symmetry is not taken into account."""
#        kpts = self._kMesh(nq1, nq2, nq3)
#        kpts_cart = numpy.zeros(kpts.shape)
#        for k in range(kpts.shape[0]):
#            # convert into cartesian coordinates in units of inv lattice vector a
#            kpts_cart[k,:] = self.structure.lattice.recipCartesian(kpts[k,:])
##            self.structure.lattice.matter().cartesian(kpt)/ \
##                        self.structure.lattice.a
#
#        return kpts_cart
#
#    def recipCartesian(self, kPoint):
#        """Conversts vector on fractional coordinates in reciprocal space into
#           a vector in cartesian coordinates"""
#        recip_base = self.matter().reciprocal().base*self._a
#        return numpy.dot( kPoint, recip_base)