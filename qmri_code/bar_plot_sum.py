from matplotlib import pyplot as plt
import os
import numpy as np
import re


echos = [0,1,2,3,4,5]
datime_list = []
datime_now_list = []

for foldername in os.listdir(str('/data/underworld/kbas/project_nitorch_scribbles/qmri_results')):
            if foldername.startswith("chi_results_leftout_2023-07-15"): #or foldername.startswith("chi_results_leftout_2023-05-10"):
                datime_list.append(str(foldername[20:]))

for datime in datime_list:
    for filename in os.listdir(str('/data/underworld/kbas/project_nitorch_scribbles/qmri_results/chi_results_leftout_' + datime)):
            if filename.startswith("likelihoods_" + datime +  "_2023-07-"): #or filename.startswith("likelihoods_" + datime +  "_2023-05-25"):
                datime_now_list.append(str(filename[32:-4]))


print(datime_list)
print(datime_now_list)

cl_list = ['112111', '115326', '116284', '128221', '130519', '133749', '170192', '176117',
            '208010', '210022', '211787', '214685', '232237', '242234', '260478', '308597',
            '324038', '330406', '346878']
cl_list = cl_list[:]

cwd = '/data/underworld/kbas/project_nitorch_scribbles'

chi_mt=[]
chi_pd = []
chi_t1 = []
gs_mt = []
gs_pd = []
gs_t1 = []

dof_t1 = []
dof_pd = []
dof_mt = []
var_t1 = []
var_pd = []
var_mt = []

for index, datime in enumerate(datime_list):
    likelihoods = "likelihoods_" + datime + "_" + datime_now_list[index] + ".txt"
    noise = "noise_" + cl_list[index] + '_' + datime + ".txt"
    path_gauss = 'qmri_results/' + 'gauss' + '_results_leftout_'+ datime
    likelihoods_gauss = os.path.join(cwd, path_gauss, likelihoods)
    noise_gauss = os.path.join(cwd, path_gauss, noise)
    #print(likelihoods_gauss)

    path_chi = 'qmri_results/' + 'chi' + '_results_leftout_'+ datime
    likelihoods_chi = os.path.join(cwd, path_chi, likelihoods)
    noise_chi = os.path.join(cwd, path_chi, noise)
    #print(likelihoods_chi)

    mt_chi = []
    pd_chi = []
    t1_chi = []

    mt_gauss = []
    pd_gauss = []
    t1_gauss = []


    with open(likelihoods_gauss) as f:
        lines_gauss = f.readlines()
    with open(likelihoods_chi) as f:
        lines_chi = f.readlines()
    
    lines = lines_gauss + lines_chi

    for i in range(len(echos)*6):
        line = lines[i]
        line = line.split()
        if any(l == 'chi' for l in line):
            if any(l == 'mt' for l in line):
                mt_chi.append(float(line[-1]))
                print(float(line[-1]))
            if any(l == 'pd' for l in line):
                pd_chi.append(float(line[-1]))
            if any(l == 't1' for l in line):
                t1_chi.append(float(line[-1]))


        if any(l == 'gauss' for l in line):
            if any(l == 'mt' for l in line):
                mt_gauss.append(float(line[-1]))
            if any(l == 'pd' for l in line):
                pd_gauss.append(float(line[-1]))
            if any(l == 't1' for l in line):
                t1_gauss.append(float(line[-1]))

    chi_mt.append(sum(mt_chi))
    chi_pd.append(sum(pd_chi))
    chi_t1.append(sum(t1_chi))
    gs_mt.append(sum(mt_gauss))
    gs_pd.append(sum(pd_gauss))
    gs_t1.append(sum(t1_gauss))

    dofb_pd = 0
    dofb_t1 = 0
    dofb_mt = 0
    vara_pd = 0
    vara_t1 = 0
    vara_mt = 0

    with open(noise_chi) as f:
        lines = f.readlines()
    for i in range(len(echos)):
        line = lines[i]
        line = line.replace('[', "")
        line = line.replace(']', "")
        line = line.replace(',', "")
        split_line = line.split()
        line = re.findall(r'[+-]?[0-9]+\.?[0-9]*', line)
        vara_pd = float(line[1])+ vara_pd
        vara_t1 = float(line[2])+ vara_t1
        vara_mt = float(line[3])+ vara_mt
        dofb_pd = float(line[4])+ dofb_pd
        dofb_t1 = float(line[5])+ dofb_t1
        dofb_mt = float(line[6])+ dofb_mt
    var_pd.append(vara_pd/6)
    var_t1.append(vara_t1/6)
    var_mt.append(vara_mt/6)
    dof_pd.append(dofb_pd/6)
    dof_t1.append(dofb_t1/6)
    dof_mt.append(dofb_mt/6)

# var_pd = np.mean(np.array(var_pd))
# var_t1 = np.mean(np.array(var_t1))
# var_mt = np.mean(np.array(var_mt))
# dof_pd = np.mean(np.array(dof_pd))
# dof_t1 = np.mean(np.array(dof_t1))
# dof_mt = np.mean(np.array(dof_mt))

plt.figure()


chi_mt = np.array(chi_mt)
chi_pd = np.array(chi_pd)
chi_t1 = np.array(chi_t1)
gs_mt = np.array(gs_mt)
gs_pd = np.array(gs_pd)
gs_t1 = np.array(gs_t1)
mt_points = range(10,29)
pd_points = range(40,59)
t1_points = range(70,89)

fig, ax1 = plt.subplots()

print (chi_t1-gs_t1)
print (chi_pd - gs_pd)
print (chi_mt)
print(gs_mt)
color = 'tab:red'
ax1.set_xlabel('dataset number')
ax1.set_ylabel('ll_chi-ll_gauss', color=color)
ax1.bar(range(1, len(datime_list)+1), chi_t1- gs_t1, color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:blue'
ax2.set_ylabel('var_chi', color=color)  # we already handled the x-label with ax1
ax2.plot(range(1, len(datime_list)+1), var_mt, color=color, marker = ".")
ax2.tick_params(axis='y', labelcolor=color)
plt.xticks( ticks = range(1,20))

fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.show()
plt.savefig('t1_whole_volume6')