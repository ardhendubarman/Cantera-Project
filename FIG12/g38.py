"""
A freely-propagating, premixed hydrogen flat flame with multicomponent
transport properties.
"""

import cantera as ct
import pickle as pkl
import numpy as np
from scipy.interpolate import interp1d
# Simulation parameters
p = ct.one_atm  # pressure [Pa]
S_l=[]
#j=[0.32, 0.34, 0.38, 0.46, 0.62]
i = np.linspace(300,1500,20)  # unburned gas temperature [K]
grid=0.38
delay=[]
for Tin in i:
    reactants = 'CH4:1, O2:2, N2:7.52'  # premixed gas composition

    initial_grid = np.linspace(0.0, grid, 6)  # m
    tol_ss = [1.0e-5, 1.0e-9]  # [rtol atol] for steady-state problem
    tol_ts = [1.0e-4, 1.0e-13]  # [rtol atol] for time stepping
    loglevel = 1  # amount of diagnostic output (0 to 8)
    refine_grid = True  # 'True' to enable refinement, 'False' to disable

    # IdealGasMix object used to compute mixture properties
    gas = ct.Solution('gri30.xml')
    gas.TPX = Tin, p, reactants

    # Flame object
    f = ct.FreeFlame(gas, initial_grid)
    f.flame.set_steady_tolerances(default=tol_ss)
    f.flame.set_transient_tolerances(default=tol_ts)

    # Set properties of the upstream fuel-air mixture
    f.inlet.T = Tin
    f.inlet.X = reactants

    #f.show_solution()

    # Solve with the energy equation disabled
    f.energy_enabled = False
    f.set_max_jac_age(10, 10)
    f.set_time_step(1e-5, [2, 5, 10, 20])
    f.solve(loglevel=loglevel, refine_grid=False)
    f.save('adiabatic.xml', 'no_energy', 'solution with the energy equation disabled')

    # Solve with the energy equation enabled
    f.transport_model= 'Mix'
    f.set_refine_criteria(ratio=3, slope=0.04, curve=0.07)
    f.energy_enabled = True
    f.solve(loglevel=loglevel, refine_grid=refine_grid)
    f.save('adiabatic.xml', 'energy', 'solution with mixture-averaged transport')
    #f.show_solution()
    print('mixture-averaged flamespeed = {0:7f} m/s'.format(f.u[0]))
    S_l.append(f.u[0])

    t2=f.grid/f.u[0]
    inflxn=np.diff(f.T).argmax()
    dly=t2[inflxn]-t2[0]
    delay.append(dly)

#%%
pkl.dump(delay,open('del_'+str(grid)+'.pkl','wb'))
pkl.dump(Tin,open('temp.pkl','wb'))
import matplotlib.pyplot as plt
plt.loglog(i,delay)
f2 = interp1d(i, delay, kind='cubic')
xnew = np.linspace(300, 1000, num=41, endpoint=True)
plt.loglog(i,delay,'o', xnew,f2(xnew))
##plt.loglog(i, S_l)
    # Solve with multi-component transport properties
    # f.transport_model = 'Multi'
    # f.solve(loglevel, refine_grid)
    # f.show_solution()
    # print('multicomponent flamespeed = {0:7f} m/s'.format(f.u[0]))
    # f.save('h2_adiabatic.xml','energy_multi',
    #        'solution with multicomponent transport')

    # write the velocity, temperature, density, and mole fractions to a CSV file
##    f.write_csv('adiabatic.csv', quiet=True)

#%%
#z=[a*b for a,b in zip(f.grid,f.u)]
##z=f.grid
##z=[a*b for a,b in zip(f.grid,f.u)]
##z=f.grid/f.u[0]
##pkl.dump(z,open('data.pkl','wb'))
##pkl.dump(Tin,open('data.pkl','wb'))
##i=len(z)

##
##pkl.dump(S_l,open('vel_'+str(grid)+'.pkl','wb'))
##pkl.dump(Tin,open('temp.pkl','wb'))
