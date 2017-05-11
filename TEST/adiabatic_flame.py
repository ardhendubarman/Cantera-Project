"""
A freely-propagating, premixed hydrogen flat flame with multicomponent
transport properties.
"""

import cantera as ct
import pickle as pkl
import numpy as np
# Simulation parameters
p = 5*ct.one_atm  # pressure [Pa]
Tin = 600.0  # unburned gas temperature [K]
reactants = 'CH4:1, O2:2, N2:7.52'  # premixed gas composition

initial_grid = np.linspace(0.0, 0.03, 7)  # m
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
f.set_max_jac_age(20, 20)
f.set_time_step(1e-5, [2, 5, 10, 20])
f.solve(loglevel=loglevel, refine_grid=False)
f.save('adiabatic.xml', 'no_energy', 'solution with the energy equation disabled')

# Solve with the energy equation enabled
f.transport_model= 'Mix'
f.set_refine_criteria(ratio=3, slope=0.1, curve=0.3)
f.energy_enabled = True
f.solve(loglevel=loglevel, refine_grid=refine_grid)
f.save('adiabatic.xml', 'energy', 'solution with mixture-averaged transport')
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
f.write_csv('adiabatic.csv', quiet=True)


#z=[a*b for a,b in zip(f.grid,f.u)]
#z=f.grid
#pkl.dump(z,open('data.pkl','wb'))
##i=len(z)

#%%
# for i in range (0,10):
#     print (f.u[i])
##dTdz=[]
##for j in range (320):
##    dz=z[j+1] - z[j]
##    dTdz.append((f.T[j] - f.T[j-1])/dz)

##
index1=gas.species_index('CH4')
index2=gas.species_index('CH2O')
index3=gas.species_index('HCO')
index4=gas.species_index('CO')
z=f.grid 
import matplotlib.pyplot as plt
plt.rc('text', usetex=True)
plt.rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})

#ch4=f.X[index1]
index=np.argmax(f.X[index4])
print(index)
center = z[index]
for k in range(len(z)):
    z[k] = (z[k] - center)
				
				
plt.xlim(-0.0005, 0.0005)
plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
plt.plot(z,f.X[index1],dashes=[8, 4, 2, 4, 2, 4],label='CH_4')
plt.plot(z,f.X[index2],'k-.',label='CH_2O')
plt.plot(z,f.X[index3],label='HCO')
plt.plot(z,f.X[index4],'k--',label='CO')
plt.legend(frameon=False, handlelength = 5, fontsize=20)
#plt.ylabel('energy equation terms [K s^{-1}]',fontsize='large')##, verticalalignment='center', horizontalalignment ='right'
plt.xlabel('location [m]',fontsize='large')
plt.locator_params(axis='x', nbins=2)
plt.title('600 K', loc='right')
plt.savefig('plot1.pdf',bbox_inches='tight')
plt.show()
