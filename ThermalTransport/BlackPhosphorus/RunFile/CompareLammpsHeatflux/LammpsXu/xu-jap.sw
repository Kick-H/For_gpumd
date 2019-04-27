# the torsion energy is ignored
# 2 @----@ 1
#       / \     @ 6
#      /   \   /
#   3 @     \ /
#          4 @----@ 5
# a1(armchair)=4.590A
#  a2(zigzag) =3.284A
# bot atom: 4 5 6
# Bond 1-2 2.221, bond 1-4 2.259
# Angle <213=96.001, angle <214=103.961
#
# V3=Kijk*e^[rou3ij/(rij-rmij)+rou3ik/(rik-rmik)] * (cos thetaijk - cos theta0ijk)^2
# 
#         K(eV)  theta0(degree)  rou1(A)   rou2(A)  rmin_12(A)  rmax_12(A)  rmin_13(A)  rmax_13(A)  rmin_23(A)  rmax_23(A)
# P1P1P1  1.0   0.2103     13.3143    9.2660     2.1707    -0.1045    4.3807    3045.2    4.0      0.0  0.0
# P2P2P2  1.0   0.2103     13.3143    9.2660     2.1707    -0.1045    4.3807    3045.2    4.0      0.0  0.0
# P1P2P2  1.0   0.1559     17.9602       0.0000  2.9282       0.0000  4.0936    10164.1   4.0      0.0  0.0
# P2P1P1  1.0   0.1559     17.9602       0.0000  2.9282       0.0000  4.0936    10164.1   4.0      0.0  0.0
# P1P1P2  1.0      0.0000     0.0000  11.4510      0.0000  -0.2419      0.0000    0.0000   0.0000  0.0  0.0
# P1P2P1  1.0      0.0000     0.0000  11.4510      0.0000  -0.2419      0.0000    0.0000   0.0000  0.0  0.0
# P2P1P2  1.0      0.0000     0.0000  11.4510      0.0000  -0.2419      0.0000    0.0000   0.0000  0.0  0.0
# P2P2P2  1.0      0.0000     0.0000  11.4510      0.0000  -0.2419      0.0000    0.0000   0.0000  0.0  0.0
#
# The Stillinger-Weber (SW) parameters for single-layer black phosphorus (SLBP).
# (0). Include this potential in LAMMPS input script as follows,
#	pair_style      sw
#	pair_coeff      * * bp.sw T B
# (1). SW parameters in GULP are derived analytically from the valence force field model.
# (2). Atoms in SLBP are divided into the top (T) group and the bottom (B) group.
# these entries are in LAMMPS "metal" units:
#	epsilon = eV; sigma = Angstroms
# other quantities are unitless
# element 1, element 2, element 3, 
# epsilon, sigma, a, lambda, gamma, costheta0, A, B, p, q, tol
# Created by Kick, 2018-2-4
   T   T   T   1.0   0.2103   13.3143    9.2660   2.1707   -0.1045   4.3807    3045.2   4.0   0.0   0.0
   B   B   B   1.0   0.2103   13.3143    9.2660   2.1707   -0.1045   4.3807    3045.2   4.0   0.0   0.0
   T   B   B   1.0   0.1559   17.9602    0.0000   2.9282   -0.0000   4.0936   10164.1   4.0   0.0   0.0
   B   T   T   1.0   0.1559   17.9602    0.0000   2.9282   -0.0000   4.0936   10164.1   4.0   0.0   0.0
   T   T   B   1.0   0.0000    0.0000   11.4510   0.0000   -0.2419   0.0000       0.0   0.0   0.0   0.0
   T   B   T   1.0   0.0000    0.0000   11.4510   0.0000   -0.2419   0.0000       0.0   0.0   0.0   0.0
   B   T   B   1.0   0.0000    0.0000   11.4510   0.0000   -0.2419   0.0000       0.0   0.0   0.0   0.0
   B   B   T   1.0   0.0000    0.0000   11.4510   0.0000   -0.2419   0.0000       0.0   0.0   0.0   0.0
