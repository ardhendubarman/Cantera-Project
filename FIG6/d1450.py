"""
A freely-propagating, premixed hydrogen flat flame with multicomponent
transport properties.
"""

import cantera as ct
import pickle as pkl
import numpy as np
# Simulation parameters
p = 5*ct.one_atm  # pressure [Pa]
Tin = 1450.0  # unburned gas temperature [K]
reactants = 'CH4:1, O2:2, N2:7.52'  # premixed gas composition

initial_grid = np.linspace(0.0, 0.32, 6)  # m
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
z=f.grid
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
index=np.argmax(f.X[index4])
print(index)
center = z[index]
for k in range(len(z)):
    z[k] = (z[k] - center)
#ch4=f.X[index1]
fig, (ax1, ax2, ax3) = plt.subplots(1, 3,  sharex='none', sharey=True)


ax1.set_xlim(-0.025, -0.0025)
ax1.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
ax1.plot(z,f.X[index1],dashes=[8, 4, 2, 4, 2, 4],label='CH_4')
ax1.plot(z,20*f.X[index2],'r-.',label='CH_2O')
ax1.plot(z,600*f.X[index3],label='HCO')
ax1.plot(z,f.X[index4],'k--',label='CO')
ax2.locator_params(axis='x', nbins=8)
#ax1.legend(frameon=True, handlelength = 5, fontsize=15)
#ax1.ylabel('energy equation terms [K s^{-1}]',fontsize='large')##, verticalalignment='center', horizontalalignment ='right'
ax1.set_xlabel('location [m]',fontsize='large')
ax1.locator_params(axis='x', nbins=2)

ax2.set_xlim(-0.002, 0.0005)
ax2.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
ax2.plot(z,f.X[index1],dashes=[8, 4, 2, 4, 2, 4],label='CH_4')
ax2.plot(z,20*f.X[index2],'r-.',label='CH_2O')
ax2.plot(z,600*f.X[index3],label='HCO')
ax2.plot(z,f.X[index4],'k--',label='CO')
ax2.locator_params(axis='x', nbins=4)
# ax2.legend(frameon=True, handlelength = 5, fontsize=20)
#ax2.ylabel('energy equation terms [K s^{-1}]',fontsize='large')##, verticalalignment='center', horizontalalignment ='right'
ax2.set_xlabel('location [m]',fontsize='large')

ax3.set_xlim(0.0004, 0.01)
ax3.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
ax3.plot(z,f.X[index1],dashes=[8, 4, 2, 4, 2, 4],label='CH_4')
ax3.plot(z,20*f.X[index2],'r-.',label='CH_2O')
ax3.plot(z,600*f.X[index3],label='HCO')
ax3.plot(z,f.X[index4],'k--',label='CO')
# ax3.legend(frameon=True, handlelength = 5, fontsize=20)
ax3.locator_params(axis='x', nbins=2)
#ax3.ylabel('energy equation terms [K s^{-1}]',fontsize='large')##, verticalalignment='center', horizontalalignment ='right'
ax3.set_xlabel('location [m]',fontsize='large')


ax2.set_title('1450 K', loc='right')
plt.savefig('fig8_1450k.pdf',bbox_inches='tight')
plt.show()
