from matplotlib import pyplot as plt
import os

echos = [0,1,2,3,4,5]

datime_list = ['2023-02-27_21-06-41', '2023-03-01_16-16-19', '2023-03-01_16-16-19', '2023-03-02_14-01-48']
datime_now_list = ['2023-02-28_17-04-45', '2023-03-01_17-00-01', '2023-03-01_17-00-01', '2023-03-02_14-47-05']
cl_list = ['112111', '115326', '116284',  '128221']

cwd = '/data/underworld/kbas/project_nitorch_scribbles'

chi_mt=[]
chi_pd = []
chi_t1 = []
gs_mt = []
gs_pd = []
gs_t1 = []

for index, datime in enumerate(datime_list):
    likelihoods = "likelihoods_" + datime + "_" + datime_now_list[index] + ".txt"
    path_gauss = 'qmri_results/' + 'gauss' + '_results_leftout_'+ datime
    likelihoods_gauss = os.path.join(cwd, path_gauss, likelihoods)
    #print(likelihoods_gauss)

    path_chi = 'qmri_results/' + 'chi' + '_results_leftout_'+ datime
    likelihoods_chi = os.path.join(cwd, path_chi, likelihoods)
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

    #print(mt_chi)
    #print(mt_gauss)
    chi_mt.append(sum(mt_chi))
    chi_pd.append(sum(pd_chi))
    chi_t1.append(sum(t1_chi))
    gs_mt.append(sum(mt_gauss))
    gs_pd.append(sum(pd_gauss))
    gs_t1.append(sum(t1_gauss))

#print(chi_mt, gs_mt)
plt.figure()

#loc_t1 = [int(a) for a in cl_list]
#loc_t1 = cl_list
#loc_pd = [str(int(a) +1) for a in cl_list]
#loc_mt = [str(int(a) +2) for a in cl_list]
#plt.plot(loc_mt, chi_mt, 'r. ', loc_mt, gs_mt, 'b. ', loc_pd, chi_pd, 'rx ', loc_pd, gs_pd, 'bx ', loc_t1, chi_t1, 'r^ ', loc_t1, gs_t1, 'b^ ')
# plt.plot(loc_mt, chi_mt, 'r. ', loc_mt, gs_mt, 'b. ')
# plt.plot(loc_pd, chi_pd, 'rx ', loc_pd, gs_pd, 'bx ')
#plt.plot(loc_t1, chi_t1, 'r^ ', loc_t1, gs_t1, 'b^ ')
#plt.bar(cl_list, chi_mt, gs_mt)
plt.plot([16,26,36,46], chi_mt, 'r. ', [16,26,36,46], gs_mt, 'bx ', [15,25,35,45], chi_pd, 'r. ', [15,25,35,45], gs_pd, 'bx ', [14,24,34,44], chi_t1, 'r. ', [14,24,34,44], gs_t1, 'bx ')
plt.xticks( ticks = [15,25,35,45], labels = cl_list)
#plt.grid()

plot_txt = 'likelihood_sum_' + '.png'
plot_txt = str(os.path.join(cwd, plot_txt))
print(plot_txt)
plt.savefig(plot_txt)