"""
A freely-propagating, premixed hydrogen flat flame with multicomponent
transport properties.
"""

import cantera as ct
import pickle as pkl

# Simulation parameters
p = 5*ct.one_atm  # pressure [Pa]
Tin = 600.0  # unburned gas temperature [K]
reactants = 'CH4:1, O2:2, N2:7.52'  # premixed gas composition

initial_grid = [0.0, 0.001, 0.01, 0.02, 0.029, 0.03]  # m
tol_ss = [1.0e-5, 1.0e-13]  # [rtol atol] for steady-state problem
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
f.save('CH4_600.xml', 'no_energy', 'solution with the energy equation disabled')

# Solve with the energy equation enabled
f.transport_model= 'Mix'
f.set_refine_criteria(ratio=3, slope=0.04, curve=0.07)
f.energy_enabled = True
f.solve(loglevel=loglevel, refine_grid=refine_grid)
f.save('CH4_600.xml', 'energy', 'solution with mixture-averaged transport')
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
f.write_csv('CH4_600.csv', quiet=True)

#%%
z=f.grid/f.u[0]
pkl.dump(z,open('data_600.pkl','wb'))
i=len(z)

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
