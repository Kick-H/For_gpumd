'''----------------------------------------------------------------------------
    Copyright 2019 Xu Ke <kickhsu@gmail.com>

    This is a simple python program demonstrating the molecular dynamics of
    Argon in the ensemble using the Nose-Hoover chain and temp/rescale method.

    This is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You can find a copy of the GNU General Public License at
    <http://www.gnu.org/licenses/>.

    Acknowledgement: Zheyong Fan brucenju@gmail.com

    References:
    [1] http://blog.sciencenet.cn/blog-3102863-968600.html
    [2] http://blog.sciencenet.cn/blog-3102863-980747.html
    [3] https://github.com/brucefan1983/GPUMD (*/src/ensemble_nhc.cu)
                                              (*/doc/gpumd.pdf 3.6.5)
------------------------------------------------------------------------------'''

import time
import math
import random
import numpy as np
from behold import Behold

class CoordReader:
  # define class variable
  def __init__(self):
    self.box = []
    self.natom = 0
    self.tatom = 0
    self.atoms = []
    def natoms(self):            # A function to test.
        if len(self.atoms) == self.natom:
            return len(self.atoms)
        else:
            print (len(self.atoms), self.natom)
            raise 'Number of atom in file is not equail with number'


class Atom:
    __slots__ = ['id', 'typ', 'molecule', 'xyz', 'name', 'mass', 'sigma', 'epsilon', 
                 'velocity','NumNeighbor','NameNeighbor','force','potential']
    def __init__(self, **kwargs):
        for key in self.__slots__:
            try:
                setattr(self, key, kwargs[key])
            except KeyError:
                setattr(self, key, None)


class MoleculeDynamics(CoordReader):
    # Dimension, which should be 3
    # nxyz(1,3): nxyz(d) is the number of unit cells in the d-th direction
    # LatticeConstant(1,3): a(d) is the lattice constant in the d-th direction
    # r(N,3): r(i,d) is the position of atom i along the d-th direction
    def __init__(self,nxyz,LatticeConstant,r0,Mass,Dimension=3):
        super(MoleculeDynamics, self).__init__()
        self.Dimension=Dimension
        self.pbc=[0,0,0]
        self.StepTemp=0
        self.KineticEnergy=0
        for i in range(len(nxyz)):
            self.box.append([0,nxyz[i]*LatticeConstant[i]])
        for nx in range(nxyz[0]):
            for ny in range(nxyz[1]):
                for nz in range(nxyz[2]):
                    for m in range(len(r0)):
                        self.natom += 1
                        self.atoms.append(Atom(id=self.natom,typ=m+1,
                                               name='Ar',mass=Mass[self.natom-1],
                                               xyz=[(nx+r0[m][0])*LatticeConstant[0],
                                                    (ny+r0[m][1])*LatticeConstant[1],
                                                    (nz+r0[m][2])*LatticeConstant[2]]))
    # fname=fname+'.xyz'
    def OutXyz(self,fname,step):
        fname=fname+'.xyz'
        with open(fname,'a') as fxyz:
            print(self.natom,file=fxyz)
            print(step,file=fxyz)
            for atom in self.atoms:
                print(atom.name,atom.xyz[0],atom.xyz[1],atom.xyz[2],file=fxyz)
    # KB: Boltzmann's constant
    # Dimension, which is 3
    # T: temperature prescribed
    # v(N,3): v(i,d) is the velocity of atom i in the d-th direction
    def InitializeVelocity(self,KB,Temp,TestVelocity=0):
        Velocity=[[random.random()-0.5 for d in range(self.Dimension)]
                   for i in range(self.natom)]
        MomentumAverage=[0 for d in range(self.Dimension)]

        for i in range(len(Velocity)):
            for d in range(self.Dimension):
                MomentumAverage[d] += self.atoms[i].mass*Velocity[i][d]
        for d in range(self.Dimension):
            MomentumAverage[d] /= self.natom
        for i in range(len(Velocity)):
            for d in range(self.Dimension):
                Velocity[i][d] -= MomentumAverage[d]/self.atoms[i].mass

        constant = 0
        for i in range(self.natom):
            constant += self.atoms[i].mass*sum(np.power(Velocity[i],2))
        constant = math.sqrt(Temp*self.Dimension*KB*self.natom/constant)

        for i in range(len(Velocity)):
            self.atoms[i].velocity=[]
            for d in range(self.Dimension):
                self.atoms[i].velocity.append(Velocity[i][d]*constant)

        if TestVelocity:
            print('Velocity of system:',np.sum(Velocity,axis=0))
            KineticEnergy=0
            for i in range(len(Velocity)):
                KineticEnergy += 0.5*self.atoms[i].mass*sum(np.power(self.atoms[i].velocity,2))
            print('Calculate KE by sum(1/2*m*v^2)',KineticEnergy/self.natom)
            KineticEnergy=self.Dimension/2*KB*Temp
            print('Calculate KE by Dimension/2*KB*Temp',KineticEnergy)
            self.StepTemp=0
            for i in range(self.natom):
                self.StepTemp += self.atoms[i].mass*sum(np.power(self.atoms[i].velocity,2))
            self.StepTemp=self.StepTemp/self.natom/self.Dimension/KB
            print('Temp is:',self.StepTemp,KineticEnergy/self.Dimension*2/KB)
    # L(1,3): L(d) is the box length in the d-th direction
    # pbc(1,3): pbc(d)=1(0) means periodic (free) in the d-th direction
    def FindNeighbor(self,pbc,rc,TestNeighbor=0):
        rcSqure = rc**2
        self.pbc=pbc
        for i in range(self.natom-1):
            for j in range(i+1,self.natom):
                ijDistanceSqrare = FindDistance(self.pbc,self.box,
                    self.atoms[i].xyz,self.atoms[j].xyz,self.Dimension)
                if ijDistanceSqrare<rcSqure:
                    if self.atoms[i].NumNeighbor == None:
                        self.atoms[i].NumNeighbor = 1
                        self.atoms[i].NameNeighbor = [j]
                    else:
                        self.atoms[i].NumNeighbor += 1
                        self.atoms[i].NameNeighbor.append(j)
                    if self.atoms[j].NumNeighbor == None:
                        self.atoms[j].NumNeighbor = 1
                        self.atoms[j].NameNeighbor = [i]
                    else:
                        self.atoms[j].NumNeighbor += 1
                        self.atoms[j].NameNeighbor.append(i)
        if TestNeighbor:
            TestNeighbor=[[],[]]
            for i in range(self.natom):
                if self.atoms[i].NumNeighbor in TestNeighbor[0]:
                    TestNeighbor[1][TestNeighbor[0].index(self.atoms[i].NumNeighbor)] += 1
                else:
                    TestNeighbor[0].append(self.atoms[i].NumNeighbor)
                    TestNeighbor[1].append(1)
            print(TestNeighbor[0],'neighbors,',TestNeighbor[1],'this type atoms.')
    # f(N,3): f(i,d) is the total force on atom i in the d-th direction
    # U: total potential energy of the system
    def FindForce(self):
        Epsilon=1.032e-2       # in units of eV       (only for Argon)
        SIGMA=3.405            # in units of Angstrom (only for Argon)
        Sigma6=SIGMA**6
        Sigma12=Sigma6**2
        self.Potential = 0.0
        self.Force = [0,0,0]
        for i in range(self.natom):
            self.atoms[i].force=[0 for d in range(self.Dimension)]
        for i in range(self.natom-1):
            for j in self.atoms[i].NameNeighbor:
                if i > j:      # Use Newton's 3rd law to speed up
                    Dij = [0 for i in range(self.Dimension)]
                    for m in range(self.Dimension):
                        Dij[m] = self.atoms[i].xyz[m]-self.atoms[j].xyz[m]
                        Dij[m] = Dij[m]-round(Dij[m]/(self.box[m][1]-self.box[m][0])
                                 )*self.pbc[m]*(self.box[m][1]-self.box[m][0])
                    ijDistanceSqrare=sum(np.power(Dij,2))
                    Dij6=ijDistanceSqrare**3    # 2*3=6
                    Dij8=ijDistanceSqrare*Dij6  # 2+6=8
                    Dij12=Dij6**2
                    Dij14=Dij6*Dij8
                    ijForce=(Sigma6/Dij8-2.0*Sigma12/Dij14)*24.0*Epsilon
                    for d in range(self.Dimension):
                        self.atoms[i].force[d] -= ijForce*Dij[d]
                        self.atoms[j].force[d] += ijForce*Dij[d]
                    self.Potential += 4.0*Epsilon*(Sigma12/Dij12-Sigma6/Dij6)
        for i in range(self.natom):
            for d in range(self.Dimension):
                self.Force[d] += self.atoms[i].force[d]
    def VelocityVerlet(self,dt):
        for i in range(self.natom):
            for d in range(self.Dimension):
                self.atoms[i].velocity[d] += (self.atoms[i].force[d]/self.atoms[i].mass)*dt*0.5
                self.atoms[i].xyz[d] += self.atoms[i].velocity[d]*dt
                if self.atoms[i].xyz[d] > self.box[d][1]:
                    self.atoms[i].xyz[d] -= self.box[d][1]-self.box[d][0]
                elif self.atoms[i].xyz[d] < self.box[d][0]:
                    self.atoms[i].xyz[d] += self.box[d][1]-self.box[d][0]
        self.FindForce()
        for i in range(self.natom):
            for d in range(self.Dimension):
                self.atoms[i].velocity[d] += (self.atoms[i].force[d]/self.atoms[i].mass)*dt*0.5
    def TempRescale(self,KB,Temp):
        constant = 0
        Temp=Temp
        for i in range(self.natom):
            constant += self.atoms[i].mass*sum(np.power(self.atoms[i].velocity,2))
        constant = math.sqrt(Temp*self.Dimension*KB*self.natom/constant)
        self.StepTemp=0
        for i in range(self.natom):
            for d in range(self.Dimension):
                self.atoms[i].velocity[d] = self.atoms[i].velocity[d]*constant
            self.StepTemp += self.atoms[i].mass*sum(np.power(self.atoms[i].velocity,2))
        self.StepTemp=self.StepTemp/self.natom/self.Dimension/KB
        self.KineticEnergy=self.StepTemp*KB*self.Dimension/2
    def NoseHoover(self,dt,Temp,Nstep,interval=10):
        dN=self.natom*self.Dimension # number of degrees of freedom in the thermostatted system
        dt2=dt*0.5                   # half timestep
        kT=KB*Temp
        NHM=4                        # a good choice
        tau=dt*100                   # a good choice (larger tau gives looser coupling)
        velNH=[1.0,-1.0,1.0,-1.0]    # thermostat momentum Pi, good choice (but not important)
        posNH=[]                     # thermostat position Eta
        masNH=[]                     # thermostat masses   Q
        for i in range(NHM):
            posNH.append(0)          # good choice (but not important)
            masNH.append(kT*tau*tau)
        masNH[0]=dN*kT*tau*tau

        self.KineticEnergy=0
        for i in range(self.natom):
            self.KineticEnergy += self.atoms[i].mass*sum(np.power(self.atoms[i].velocity,2))

        for step in range(Nstep):
            # The invariant is not only the particle Hamiltonian
            inv = self.KineticEnergy+self.Potential
            inv += kT*dN*posNH[0]
            for m in range(1,NHM):
                inv += kT*posNH[m]
            for m in range(NHM):
                inv += 0.5*velNH[m]**2/masNH[m]

            self.StepTemp=0
            for i in range(self.natom):
                self.StepTemp += self.atoms[i].mass*sum(np.power(self.atoms[i].velocity,2))
            Ek2=self.StepTemp
            self.StepTemp=self.StepTemp/self.natom/self.Dimension/KB

            if step % interval == 0:
                print(step,self.StepTemp,self.Potential,self.KineticEnergy,inv)
                TestMD.OutXyz('Ar',step)

            # The first half of the thermostat integration
            factor, posNH, velNH, masNH = NHChain2(NHM, posNH, velNH, masNH, Ek2, kT, dN, dt2)
            for i in range(self.natom):
                for j in range(self.Dimension):
                    self.atoms[i].velocity[j] *= factor

            # The Velocity-Verlet integration
            self.VelocityVerlet(dt)

            self.StepTemp=0
            for i in range(self.natom):
                self.StepTemp += self.atoms[i].mass*sum(np.power(self.atoms[i].velocity,2))
            Ek2=self.StepTemp
            self.StepTemp=self.StepTemp/self.natom/self.Dimension/KB

            # The second half of the thermostat integration
            factor, posNH, velNH, masNH = NHChain2(NHM, posNH, velNH, masNH, Ek2, kT, dN, dt2)
            for i in range(self.natom):
                for j in range(self.Dimension):
                    self.atoms[i].velocity[j] *= factor


# http://blog.sciencenet.cn/blog-3102863-980747.html
def NHChain1(NHM,posNH,velNH,masNH,Ek2,kT,dN,dt2):
    dt4=dt2*0.5 ; dt8=dt4*0.5
    # update velocity of the last (M - 1) thermostat:
    G=velNH[NHM-2]**2/masNH[NHM-2]-kT
    velNH[NHM-1] += dt4*G
    # update thermostat velocities from M - 2 to 0:
    for m in range(NHM-2,-1,-1):
        tmp=math.exp(-dt8*velNH[m+1]/masNH[m+1])
        G=velNH[m-1]**2/masNH[m-1]-kT
        if m==0:
            G=Ek2-dN*kT
        velNH[m]=tmp*(tmp*velNH[m]+dt4*G)
    # update thermostat positions from M - 1 to 0:
    for m in range(NHM-1,-1,-1):
        posNH[m] += dt2*velNH[m]/masNH[m]
    # compute the scale factor 
    factor=math.exp(-dt2*velNH[0]/masNH[0])
    # update thermostat velocities from 0 to M - 2:
    for m in range(NHM-1):
        tmp=math.exp(-dt8*velNH[m+1]/masNH[m+1])
        G=velNH[m-1]**2/masNH[m-1]-kT
        if m==0:
            G=Ek2*factor**2-dN*kT
        velNH[m]=tmp*(tmp*velNH[m]+dt4*G)
    # update velocity of the last (M - 1) thermostat:
    G=velNH[NHM-2]**2/masNH[NHM-2]-kT
    velNH[NHM-1] += dt4*G
    return factor, posNH, velNH, masNH

# The Nose-Hover thermostat integrator
# https://github.com/brucefan1983/GPUMD (*/src/ensemble_nhc.cu)
def NHChain2(NHM,posNH,velNH,masNH,Ek2,kT,dN,dt2):
    # These constants are taken from Tuckerman's book
    w=[0.784513610477560,
       0.235573213359357,
      -1.17767998417887,
       1.31518632068391,
      -1.17767998417887,
       0.235573213359357,
       0.784513610477560]
    n_respa=4
    for n1 in range(len(w)):
        dt2=dt2*w[n1]/n_respa ; dt4=dt2*0.5 ; dt8=dt4*0.5 ; factor=1.0 # to be accumulated
        for n2 in range(n_respa):
            # update velocity of the last (M - 1) thermostat:
            G=velNH[NHM-2]**2/masNH[NHM-2]-kT
            velNH[NHM-1] += dt4*G
            # update thermostat velocities from M - 2 to 0:
            for m in range(NHM-2,-1,-1):
                tmp=math.exp(-dt8*velNH[m+1]/masNH[m+1])
                G=velNH[m-1]**2/masNH[m-1]-kT
                if m==0:
                    G=Ek2-dN*kT
                velNH[m]=tmp*(tmp*velNH[m]+dt4*G)
            # update thermostat positions from M - 1 to 0:
            for m in range(NHM-1,-1,-1):
                posNH[m] += dt2*velNH[m]/masNH[m]
            # compute the scale factor 
            factor_local=math.exp(-dt2*velNH[0]/masNH[0])
            Ek2 *= factor_local**2
            factor *= factor_local
            # update thermostat velocities from 0 to M - 2:
            for m in range(NHM-1):
                tmp=math.exp(-dt8*velNH[m+1]/masNH[m+1])
                G=velNH[m-1]**2/masNH[m-1]-kT
                if m==0:
                    G=Ek2*factor**2-dN*kT
                velNH[m]=tmp*(tmp*velNH[m]+dt4*G)
            # update velocity of the last (M - 1) thermostat:
            G=velNH[NHM-2]**2/masNH[NHM-2]-kT
            velNH[NHM-1] += dt4*G
            return factor, posNH, velNH, masNH


def FindDistance(pbc,box,xyz1,xyz2,Dim):
    Dij=[0 for i in range(Dim)]
    for i in range(Dim):
        Dij[i] = xyz1[i]-xyz2[i]
        Dij[i] = Dij[i] - round(Dij[i]/(box[i][1]-box[i][0]))*pbc[i]*(box[i][1]-box[i][0])
    return sum(np.power(Dij,2))


def main():
    # My unit system: energy-eV; length-Angstrom; mass-atomic mass unit
    global KB
    KB=8.625e-5;      # Boltzmann's constant in my unit system  
    r0=[[0.0,0.0,0.0],
        [0.0,0.5,0.5],
        [0.5,0.0,0.5],
        [0.5,0.5,0.0]]
    nxyz=[4,4,4]
    Temp=80           # K
    LatticeConstant=[5.45,5.45,5.45]
    Mass=[40.0 for i in range(nxyz[0]*nxyz[1]*nxyz[2]*len(r0))]
    TestMD=MoleculeDynamics(nxyz,LatticeConstant,r0,Mass)
    TestMD.OutXyz('Ar',0)
    TestMD.InitializeVelocity(KB,Temp,TestVelocity=1)
    pbc=[1,1,1]
    rc=10
    TestMD.FindNeighbor(pbc,rc,TestNeighbor=1)
    TestMD.FindForce()
    dt=1
    NumStep=100000
    sample_interval=10
    # Test.NVT
    print('# STEP TEMP PE KE TE')
    TestMD.NoseHoover(dt,Temp,NumStep,interval=sample_interval)
    # Test.NVE+Temp/Rescale
#    for step in range(NumStep):
#        #TestMD.VelocityVerlet(dt)
#        #TestMD.TempRescale(KB,Temp)
#        if step % sample_interval == 0:
#            TEMP=TestMD.StepTemp
#            PE=TestMD.Potential
#            KE=TestMD.KineticEnergy
#            TE=TestMD.Potential+TestMD.KineticEnergy
#            Fxyz=TestMD.Force
#            TestMD.OutXyz('Ar',step)
#            print('{0:5d} {1:9.4f} {2:12.6g} {3:12.6g} {4:12.6g}'
#                  .format(step,TEMP,PE,KE,TE))

if __name__ == '__main__':
    clock_start = time.clock()
    main()
    clock_end = time.clock()
    print ('Running time of this program:',clock_end-clock_start)
