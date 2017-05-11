import pickle as pkl
import matplotlib.pyplot as plt
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
plt.plot(x_axis[1:-1], conv,'k--', label='convection')
plt.plot(x_axis[1:-1], cond, label= 'conduction')
plt.plot(x_axis[1:-1], chem,'r-.',label= 'chemical reaction')
##plt.plot(x_axis[1:-1], tdiff,'k-.' label= 'diffusion')
plt.legend()
plt.show()
