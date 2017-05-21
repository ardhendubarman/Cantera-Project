#%%
import numpy as np
import cantera as ct
import matplotlib.pyplot as plt
import pickle as pkl
A_f_s=4.76*2*28.85/16.04
CH4=1
#%%
# Simulation parameters
p = ct.one_atm
Tin = 298.0
# pressure [Pa]
# unburned gas temperature [K]
initial_grid = np.linspace(0.0, 0.03, 7)
# m
tol_ss = [1.0e-5, 1.0e-13] # [rtol atol] for steady-state problem
tol_ts = [1.0e-4, 1.0e-13] # [rtol atol] for time stepping
loglevel = 1
xch4=1
Su,Phi=[],[]
j=np.arange(0.6,1.60,0.05)
for phi in (j):
    A_f_a=A_f_s/phi
    a=(A_f_a*16.04)/(4.76*28.85)
    xo2=a
    xn2=a*3.76

    reactants = ('CH4:%s, O2:%s, N2:%s' %(xch4,xo2,xn2))

    # amount of diagnostic output (0 to 8)
    refine_grid = True
    # 'True' to enable refinement, 'False' to disable
    # IdealGasMix object used to compute mixture properties, set to the state of
    # upstream fuel-air mixture
    gas = ct.Solution('gri30.xml')
    gas.TPX = Tin, p, reactants
    # Flame object
    f = ct.FreeFlame(gas, initial_grid)
    f.flame.set_steady_tolerances(default=tol_ss)
    f.flame.set_transient_tolerances(default=tol_ts)

    #Set properties of the upstream fuel-air mixture
    f.inlet.T = Tin
    f.inlet.X = reactants
    
    # Solve with the energy equation disabled
    f.energy_enabled = False
    f.transport_model = 'Mix'
    f.set_max_jac_age(10, 10)
    f.set_time_step(1e-5, [2, 5, 10, 20])
    f.solve(loglevel=loglevel, refine_grid=False)

    # Solve with the energy equation enabled
    f.transport_model= 'Mix'
    f.set_refine_criteria(ratio=3, slope=0.04, curve=0.07)
    f.energy_enabled = True
    f.solve(loglevel=loglevel, refine_grid=refine_grid)
    #f.save('adiabatic.xml', 'energy', 'solution with mixture-averaged transport')
    #f.show_solution()
##    print('mixture-averaged flamespeed = {0:7f} m/s'.format(f.u[0]))
    Su.append(f.u[0])
    Phi.append(phi)

#%%
pkl.dump(Su,open('vel.pkl','wb'))
##pkl.dump(Phi,open('phi.pkl','wb')
