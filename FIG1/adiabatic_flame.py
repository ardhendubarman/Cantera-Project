"""
A freely-propagating, premixed hydrogen flat flame with multicomponent
transport properties.
"""

import cantera as ct
import pickle as pkl
import numpy as np
# Simulation parameters
pi = [ct.one_atm,2*ct.one_atm,3*ct.one_atm,4*ct.one_atm,5*ct.one_atm,6*ct.one_atm,7*ct.one_atm,8*ct.one_atm]  # pressure [Pa]
T = [400,600]  # unburned gas temperature [K]
reactants = 'CH4:1, O2:2, N2:7.52'  # premixed gas composition


initial_grid = np.linspace(0,0.03,6)  # m
tol_ss = [1.0e-5, 1.0e-13]  # [rtol atol] for steady-state problem
tol_ts = [1.0e-4, 1.0e-13]  # [rtol atol] for time stepping
loglevel = 1  # amount of diagnostic output (0 to 8)
refine_grid = True  # 'True' to enable refinement, 'False' to disable

# IdealGasMix object used to compute mixture properties
gas = ct.Solution('gri30.xml')
S_l_4=[]
S_l_6=[]
for Tin in T:
    for p in pi:
        initial_grid = np.linspace(0,0.03,6)  # m
        tol_ss = [1.0e-5, 1.0e-13]  # [rtol atol] for steady-state problem
        tol_ts = [1.0e-4, 1.0e-13]  # [rtol atol] for time stepping
        loglevel = 1  # amount of diagnostic output (0 to 8)
        refine_grid = True  # 'True' to enable refinement, 'False' to disable
        gas=ct.Solution('gri30.xml')
        gas.TPX = Tin, p, reactants

        # Flame object
        f = ct.FreeFlame(gas, initial_grid)
        f.flame.set_steady_tolerances(default=tol_ss)
        f.flame.set_transient_tolerances(default=tol_ts)

        # Set properties of the upstream fuel-air mixture
        f.inlet.T = Tin
        f.inlet.X = reactants

        f.show_solution()

        # Solve with the energy equation disabled
        f.energy_enabled = False
        f.set_max_jac_age(10, 10)
        f.set_time_step(1e-5, [2, 5, 10, 20])
        f.solve(loglevel=loglevel, refine_grid=False)
##        f.save('h2_adiabatic.xml', 'no_energy', 'solution with the energy equation disabled')

        # Solve with the energy equation enabled
        f.transport_model= 'Mix'
        f.set_refine_criteria(ratio=3, slope=0.04, curve=0.07)
        f.energy_enabled = True
        f.solve(loglevel=loglevel, refine_grid=refine_grid)
##        f.save('h2_adiabatic.xml', 'energy', 'solution with mixture-averaged transport')
        #f.show_solution()
        print('mixture-averaged flamespeed = {0:7f} m/s'.format(f.u[0]))

        # Solve with multi-component transport properties
        # f.transport_model = 'Multi'
        # f.solve(loglevel, refine_grid)
        # f.show_solution()
        # print('multicomponent flamespeed = {0:7f} m/s'.format(f.u[0]))
        # f.save('h2_adiabatic.xml','energy_multi',
        #        'solution with multicomponent transport')

        # write the velocity, temperature, density, and mole fractions to a CSV file
##        f.write_csv('h2_adiabatic.csv', quiet=True)
        v=f.u[0]
        if Tin==400:
            S_l_4.append(v)
        else:
            S_l_6.append(v)

        #%%
import matplotlib.pyplot as plt


##        z=f.grid
##        pkl.dump(z,open('data.pkl','wb'))
##        i=len(z)

#%%
# for i in range (0,10):
#     print (f.u[i])
##dTdz=[]
##for j in range (320):
##    dz=z[j+1] - z[j]
##    dTdz.append((f.T[j] - f.T[j-1])/dz)

##
##import matplotlib.pyplot as plt
##plt.plot(z[0:320],dTdz)
