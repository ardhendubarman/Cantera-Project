import pickle as pkl
import matplotlib.pyplot as plt

plt.rc('text', usetex=True)
plt.rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})

start = False
search_string = "j_o0"
filename = 'tmp_1083.txt'

num_cols = 5
col1 = []

for i in range(num_cols):
    col1.append([])

with open(filename, 'r') as file:
    for line in file:

        if(search_string in line):
            start = True
            del col1
            col1 = []
            for i in range(num_cols):
                col1.append([])
            continue

        if(not start):
            continue

        nums = line.split()
        if(len(nums) != num_cols):
            continue
        try:
            for i in range(len(nums)):
                col1[i].append(float(nums[i]))
        except:
            pass

x_axis1 = pkl.load(open('data_1083.pkl', 'rb'))
conv1 = col1[0]
cond1 = col1[1]
chem1 = col1[2]
diff1 = col1[3]
tdiff1 = col1[4]

#%%
start = False
search_string = "j_o0"
filename = 'tmp_1113.txt'

num_cols = 5
col2 = []

for i in range(num_cols):
    col2.append([])

with open(filename, 'r') as file:
    for line in file:

        if(search_string in line):
            start = True
            del col2
            col2 = []
            for i in range(num_cols):
                col2.append([])
            continue

        if(not start):
            continue

        nums = line.split()
        if(len(nums) != num_cols):
            continue
        try:
            for i in range(len(nums)):
                col2[i].append(float(nums[i]))
        except:
            pass



x_axis2 = pkl.load(open('data_1113.pkl', 'rb'))
conv2 = col2[0]
cond2 = col2[1]
chem2 = col2[2]
diff2 = col2[3]
tdiff2 = col2[4]
#%%
start = False
search_string = "j_o0"
filename = 'tmp_1143.txt'

num_cols = 5
col3 = []

for i in range(num_cols):
    col2.append([])

with open(filename, 'r') as file:
    for line in file:

        if(search_string in line):
            start = True
            del col3
            col3 = []
            for i in range(num_cols):
                col3.append([])
            continue

        if(not start):
            continue

        nums = line.split()
        if(len(nums) != num_cols):
            continue
        try:
            for i in range(len(nums)):
                col3[i].append(float(nums[i]))
        except:
            pass

x_axis3 = pkl.load(open('data_1143.pkl', 'rb'))
conv3 = col3[0]
cond3 = col3[1]
chem3 = col3[2]
diff3 = col3[3]
tdiff3 = col3[4]

#%%
# plt.figure(figsize=(5,15))

min_y1 = min(chem1)
index1 = chem1.index(min_y1)
center1 = x_axis1[1:-1][index1]
for i in range(len(x_axis1[1:-1])):
    x_axis1[i] = (x_axis1[i] - center1)

min_y2 = min(chem2)
index2 = chem2.index(min_y2)
center2 = x_axis2[1:-1][index2]
for i in range(len(x_axis2[1:-1])):
    x_axis2[i] = (x_axis2[i] - center2)

min_y3 = min(chem3)
index3 = chem3.index(min_y3)
center3 = x_axis3[1:-1][index3]
for i in range(len(x_axis3[1:-1])):
    x_axis3[i] = (x_axis3[i] - center3)

#%%

f, (ax1, ax2, ax3) = plt.subplots(1, 3,  sharex='none', sharey=True)
ax1.ticklabel_format(style='sci', axis='x', scilimits=(0,0))

ax1.plot(x_axis1[1:-1], conv1,'k--', label='convection')
##ax1.plot(x_axis[1:-1], cond, label= 'conduction')
ax1.plot(x_axis1[1:-1], chem1,'r-.',label= 'heat realease')
ax1.plot(x_axis1[1:-1], tdiff1,'k', label= 'diffusive sum')
ax1.set_xlim(-0.0015, 0.0015)
ax1.set_ylim(-100000000, 100000000)
ax1.legend(frameon=False,handlelength = 5, fontsize=15)
ax1.locator_params(axis='x', nbins=4)
ax1.locator_params(axis='y', nbins=10)
ax1.set_title("1083K", loc='right')
ax1.set_ylabel('energy equation terms [K s^{-1}]',fontsize='large')##, verticalalignment='center', horizontalalignment ='right'
ax1.set_xlabel('location [m]',fontsize='large')
    

ax2.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
ax2.plot(x_axis2[1:-1], conv2,'k--', label='convection')
##ax1.plot(x_axis2[1:-1], cond2, label= 'conduction')
ax2.plot(x_axis2[1:-1], chem2,'r-.',label= 'heat realease')
ax2.plot(x_axis2[1:-1], tdiff2,'k', label= 'diffusive sum')
ax2.set_xlim(-0.0015, 0.0015)
ax2.locator_params(axis='y', nbins=10)
ax2.set_title("1113K", loc='right')
#plt.legend(frameon=False, handlelength = 5, fontsize=10)
ax2.set_xlabel('location [m]',fontsize='large')
ax2.locator_params(axis='x', nbins=4)

ax3.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
ax3.plot(x_axis3[1:-1], conv3,'k--', label='convection')
##ax1.plot(x_axis3[1:-1], cond3, label= 'conduction')
ax3.plot(x_axis3[1:-1], chem3,'r-.',label= 'heat realease')
ax3.plot(x_axis3[1:-1], tdiff3,'k', label= 'diffusive sum')
ax3.set_xlim(-0.0015, 0.0015)
ax3.locator_params(axis='y', nbins=10)
ax3.set_title("1143K", loc='right')
#plt.legend(frameon=False, handlelength = 5, fontsize=10)
ax3.set_xlabel('location [m]',fontsize='large')
ax3.locator_params(axis='x', nbins=4)

plt.savefig('plot1.pdf',bbox_inches='tight')
plt.show()
