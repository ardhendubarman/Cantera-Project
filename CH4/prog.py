import pickle as pkl
import matplotlib.pyplot as plt

plt.rc('text', usetex=True)
plt.rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})

start = False
search_string = "j_o0"
filename = 'tmp.txt'

num_cols = 5
col = []

for i in range(num_cols):
    col.append([])

with open(filename, 'r') as file:
    for line in file:

        if(search_string in line):
            start = True
            del col
            col = []
            for i in range(num_cols):
                col.append([])
            continue

        if(not start):
            continue

        nums = line.split()
        if(len(nums) != num_cols):
            continue
        try:
            for i in range(len(nums)):
                col[i].append(float(nums[i]))
        except:
            pass


# for i in range(len(col[0])):
#     print(col[0][i], col[1][i])

x_axis = pkl.load(open('data.pkl', 'rb'))
conv = col[0]
cond = col[1]
chem = col[2]
diff = col[3]
tdiff = col[4]
#%%
plt.figure(figsize=(2.5,7.5))
min_y = min(chem)
index = chem.index(min_y)
center = x_axis[1:-1][index]
for i in range(len(x_axis[1:-1])):
    x_axis[i] = (x_axis[i] - center)
    
plt.xlim(-0.0003, 0.0003)
plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))

plt.plot(x_axis[1:-1], conv,'k--', label='convection')
##plt.plot(x_axis[1:-1], cond, label= 'conduction')
plt.plot(x_axis[1:-1], chem,'r-.',label= 'heat realease')
plt.plot(x_axis[1:-1], tdiff,'k', label= 'diffusive sum')
plt.legend(frameon=False, handlelength = 3, fontsize=12)
plt.ylabel('energy equation terms $10^8$[$K s^{-1}]$',fontsize='large')##, verticalalignment='center', horizontalalignment ='right'
plt.xlabel('location [m]',fontsize='large')
plt.locator_params(axis='x', nbins=4)
plt.title('298 K - 5 bar', loc='right')
plt.savefig('fig4.pdf',bbox_inches='tight')
plt.show()
