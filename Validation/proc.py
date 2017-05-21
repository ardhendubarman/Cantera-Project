import matplotlib
import matplotlib.pyplot as plt
import pickle as pkl
import numpy as np
import csv

x = []
y = []

with open('hermann.csv','r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        x.append(row[0])
        y.append(row[1])

x.remove(x[0])
y.remove(y[0])

plt.rc('text', usetex=True)
plt.rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
##x = pkl.load(open('phi.pkl', 'rb'))
x1=np.arange(0.6,1.60,0.05)
y1 = pkl.load(open('vel.pkl', 'rb'))
y1 = [x * 100 for x in y1]
##print(y1)
##print(x)
fig1, ax1 = plt.subplots()
ax1.scatter(x,y,marker='o',label='Heat flux method')
ax1.scatter(x1,y1,color='red',marker='x',label='Cantera')
ax1.set_xlim(0.4,1.7)
ax1.set_ylim(5,45)
ax1.set_xlabel('$\phi$',fontsize=16)
ax1.set_ylabel("$S_L(cm/s)$",fontsize=16)
##plt.title('$\phi$=1; p = 1bar', loc = "right")
plt.legend(frameon='True', loc='best')
plt.grid('on')
# plt.locator_params(axis='x', nbins=4)
plt.savefig('validation.pdf', bbox_inches='tight')
plt.show()

