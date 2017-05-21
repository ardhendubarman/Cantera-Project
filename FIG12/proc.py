import matplotlib
from matplotlib import pyplot as plt
import pickle as pkl
import numpy as np
plt.rc('text', usetex=True)
plt.rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
##x = pkl.load(open('temp.pkl', 'rb'))
x = np.linspace(300,1500,20)
x2 = np.linspace(300, 1500, 20)
np.put(x2,11,1010)

y1 = pkl.load(open('del_0.32.pkl', 'rb'))
y2 = pkl.load(open('del_0.34.pkl', 'rb'))
y3 = pkl.load(open('del_0.38.pkl', 'rb'))
y4 = pkl.load(open('del_0.46.pkl', 'rb'))
y5 = pkl.load(open('del_0.62.pkl', 'rb'))
##y1 = [x * 100 for x in y1]
##y2 = [x * 100 for x in y2]
##y3 = [x * 100 for x in y3]
##y4 = [x * 100 for x in y4]
##y5 = [x * 100 for x in y5]

fig1, ax1 = plt.subplots()
ax1.loglog(x,y1,'k-o',label='$\Delta$X=0.32 m')
ax1.loglog(x,y2,'k-v',label='$\Delta$X=0.34 m')
ax1.loglog(x,y3,'k-d',label='$\Delta$X=0.38 m')
ax1.loglog(x2,y4,'k',label='$\Delta$X=0.46 m')
ax1.loglog(x,y5,'k-s',label='$\Delta$X=0.62 m')
ax1.set_xlim(-500,1600)
ax1.set_ylim(0.001,5)
ax1.set_xscale('log')
ax1.set_yscale('log')
ax1.set_xticks([500, 1000, 1500])
ax1.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
ax1.set_xlabel('preheating temperature [K]',fontsize=16,fontweight='bold')
ax1.set_ylabel("time from inlet to \ntemperature inflection point[s]",multialignment='center',fontsize=16)
plt.title('$\phi$=1; p = 1bar', loc = "right")
plt.legend(frameon='True', loc='best')
plt.grid('on')
# plt.locator_params(axis='x', nbins=4)
plt.savefig('fig12.pdf', bbox_inches='tight')
plt.show()

