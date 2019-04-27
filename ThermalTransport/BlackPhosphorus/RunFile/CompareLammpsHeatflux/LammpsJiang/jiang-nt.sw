# identified by experiment (Takao Y 1981 Physica B 105 580)
# 
# 2 @----@ 1
#       / \     @ 6
#      /   \   /
#   3 @     \ /
#          4 @----@ 5
# top atom: 1 2 3
# bot atom: 4 5 6
# Bond 1-2 2.224, bond 1-4 2.244, both can be assumed 2.224
# Angle <213=96.359, angle <314=102.09
# Parameters:
#
# V2=Ae^(rou/(r-rmax)) * (B/r^4-1)
#
#     A(eV) rou(A) B(A^4) rmin(A) rmax(A)
# P-P 3.626 0.809  14.287   0.0    2.79
#
# Three-body (angle-bending) SW potential parameters for SLBP used by GULP
# GULP (Gale J D 1997 J. Chem. Soc., Faraday Trans. 93 629)
# V3=Ke^[rou1/(r12-rmax12)+rou2/(r13-rmax13)] * (cos theta - cos theta0)^2
#
#            K(eV)  theta0(degree)  rou1(A)   rou2(A)  rmin_12(A)  rmax_12(A)  rmin_13(A)  rmax_13(A)  rmin_23(A)  rmax_23(A)
# Pt-Pt-Pt  35.701      96.359      0.809     0.809       0.0         2.79        0.0        2.79         0.0         3.89
# Pb-Pb-Pb  35.701      96.359      0.809     0.809       0.0         2.79        0.0        2.79         0.0         3.89
# Pt-Pt-Pb  32.006      102.094     0.809     0.809       0.0         2.79        0.0        2.79         0.0         3.89
# Pb-Pb-Pt  32.006      102.094     0.809     0.809       0.0         2.79        0.0        2.79         0.0         3.89
# The Stillinger-Weber (SW) parameters for single-layer black phosphorus (SLBP).
# (0). Include this potential in LAMMPS input script as follows,
#	pair_style      sw
#	pair_coeff      * * bp.sw T B
# (1). SW parameters in GULP are derived analytically from the valence force field model.
# (2). Atoms in SLBP are divided into the top (T) group and the bottom (B) group.
#
# these entries are in LAMMPS "metal" units:
#	epsilon = eV; sigma = Angstroms
# other quantities are unitless
#
# element 1, element 2, element 3, 
# epsilon, sigma, a, lambda, gamma, costheta0, A, B, p, q, tol
#
# Created by Kick, 2018-2-4
# B2_lmp=B_V2/rou^4=14.287/0.809^4   sigma=rou1=rou2   a=rmax/rou
# el.1, el.2, el.3, epsilon, sigma,    a,  lambda3,  gamma, costheta03,  A2,    B2,   p2, q2, tol
   T     T     T     1.000   0.809   3.449  35.701   1.000  -0.16262   3.626  33.354   4  0  0.0
   B     B     B     1.000   0.809   3.449  35.701   1.000  -0.16262   3.626  33.354   4  0  0.0
   T     B     B     1.000   0.809   3.449   0.000   1.000  -0.00000   3.626  33.354   4  0  0.0
   B     T     T     1.000   0.809   3.449   0.000   1.000  -0.00000   3.626  33.354   4  0  0.0
   T     T     B     1.000   0.809   3.449  32.006   1.000  -0.20952   0.000   0.000   0  0  0.0
   T     B     T     1.000   0.809   3.449  32.006   1.000  -0.20952   0.000   0.000   0  0  0.0
   B     B     T     1.000   0.809   3.449  32.006   1.000  -0.20952   0.000   0.000   0  0  0.0
   B     T     B     1.000   0.809   3.449  32.006   1.000  -0.20952   0.000   0.000   0  0  0.0

