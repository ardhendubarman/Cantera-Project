import matplotlib.pyplot as plt
plt.rc('text', usetex=True)
plt.rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
x = pkl.load(open('temp.pkl', 'rb'))
y1 = pkl.load(open('vel_0.32.pkl', 'rb'))
#y2 = pkl.load(open('vel_0.34.pkl', 'rb'))
#y3 = pkl.load(open('vel_0.38.pkl', 'rb'))
y4 = pkl.load(open('vel_0.46.pkl', 'rb'))
#y5 = pkl.load(open('vel_0.62.pkl', 'rb'))


plt.loglog(x,y1,label='$\Delta$X=0.32 m')
plt.loglog(x,y2,label='$\Delta$X=0.34 m')
plt.loglog(x,y3,label='$\Delta$X=0.38 m')
plt.loglog(x,y4,label='$\Delta$X=0.46 m')
plt.loglog(x,y5,label='$\Delta$X=0.62 m')
plt.xlabel('preheating temperature [K]')
plt.title('$\phi$=1; p = 5bar', loc = "right")
plt.legend(frameon='True', loc='Left')
plt.locator_params(axis='x', nbins=4)
plt.savefig('fig7.pdf', bbox_inches='tight')
plt.show()

