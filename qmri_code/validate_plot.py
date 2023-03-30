from matplotlib import pyplot as plt
import os
import re

echos = [0,1,2,3,4,5]

#likelihoods_2023-01-18_00-51-57_2023-01-30_00-48-01
#likelihoods_2023-01-18_00-51-57_2023-01-30_01-12-12
#likelihoods_2023-01-18_11-28-29_2023-01-30_16-59-15
#likelihoods_2023-01-18_11-28-29_2023-01-30_17-21-57
#likelihoods_2023-01-18_13-46-13_2023-01-30_17-59-07
#likelihoods_2023-01-18_13-46-13_2023-01-30_19-09-15
#likelihoods_2023-01-18_16-03-54_2023-01-30_19-25-43
#likelihoods_2023-01-18_16-03-54_2023-01-30_19-52-47

datime_list = ['2023-02-27_21-06-41']

cl_list = ['112111', '115326', '116284', '128221', '130519',
         '133749', '170192', '176117', '208010', '210022',
         '211787', '214685', '232237', '242234', '260478',
         '308597', '324038', '330406', '346878']

cl_list = cl_list[0:1]
#cl_list = ['mpm']

datime_now = '2023-03-08_14-13-00'

cwd = cwd = '/data/underworld/kbas/project_nitorch_scribbles/'
    
for index, datime in enumerate(datime_list):
    likelihoods = "likelihoods_" + datime + '_' + datime_now + ".txt"
    path_gauss = 'qmri_results/' + 'gauss' + '_results_leftout_'+ datime
    likelihoods_gauss = os.path.join(cwd, path_gauss, likelihoods)

    path_chi = 'qmri_results/' + 'chi' + '_results_leftout_'+ datime
    likelihoods_chi = os.path.join(cwd, path_chi, likelihoods)

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
            if any(l == 'MT' for l in line):
                mt_chi.append(float(line[-1]))
            if any(l == 'PD' for l in line):
                pd_chi.append(float(line[-1]))
            if any(l == 'T1' for l in line):
                t1_chi.append(float(line[-1]))

        if any(l == 'chi' for l in line):
            if any(l == 'mt' for l in line):
                mt_chi.append(float(line[-1]))
            if any(l == 'pd' for l in line):
                pd_chi.append(float(line[-1]))
            if any(l == 't1' for l in line):
                t1_chi.append(float(line[-1]))

        if any(l == 'gauss' for l in line):
            if any(l == 'MT' for l in line):
                mt_gauss.append(float(line[-1]))
            if any(l == 'PD' for l in line):
                pd_gauss.append(float(line[-1]))
            if any(l == 'T1' for l in line):
                t1_gauss.append(float(line[-1]))
        
        if any(l == 'gauss' for l in line):
            if any(l == 'mt' for l in line):
                mt_gauss.append(float(line[-1]))
            if any(l == 'pd' for l in line):
                pd_gauss.append(float(line[-1]))
            if any(l == 't1' for l in line):
                t1_gauss.append(float(line[-1]))

    if False:
        # read noise estimates
        dof = []
        var = []
        noise_txt = 'noise_' + cl_list[index] + '_' + datime + '.txt'
        with open(os.path.join(cwd + 'qmri_results/chi_results_leftout_'+ datime,  noise_txt)) as f:
            lines = f.readlines()
        for i in range(echos[-1]+1):
            line = lines[i]
            line = line.replace('[', "")
            line = line.replace(']', "")
            line = line.replace(',', "")
            split_line = line.split()
            line = re.findall(r'[+-]?[0-9]+\.?[0-9]*', line)
            var.append(line[1:4])
            dof.append(line[4:])

    if True:
        plt.figure()
        plt.plot(echos,t1_chi, 'rs-', echos, t1_gauss, 'bs--', echos, pd_chi, 'r^-', echos, pd_gauss, 'b^--', echos,mt_chi, 'r*-', echos, mt_gauss, 'b*--')
        #plt.plot(echos, mt_chi, 'rs-', echos, mt_gauss, 'bs--', echos, pd_chi, 'r^-', echos, pd_gauss, 'b^--')
        #mt = [a-b for a, b in zip(mt_chi,mt_gauss)]
        #pd = [a-b for a, b in zip(pd_chi,pd_gauss)]
        #t1 = [a-b for a, b in zip(t1_chi,t1_gauss)]
        #plt.plot(echos, mt, 'r--', echos, pd, 'r-', echos, t1, 'r-.')
        #plt.plot(echos, pd_chi, 'r^-', echos, pd_gauss, 'b^-')
        plt.xlabel('leftout echo')
        #plt.ylabel('chi_ll - gauss_ll')
        plt.ylabel('likelihood')
        #plt.title('hMRI sample dataset')
        #plt.title(cl_list[index])
        plt.title(cl_list[0])
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
        plt.legend(['t1_chi', 't1_gauss', 'pd_chi', 'pd_gauss', 'mt_chi', 'mt_gauss'])
        #plt.legend(["mt", "pd", "t1"])

        plot_txt = 'likelihood_plot_' + datime + '_' + datime_now + '_' + cl_list[index] + '.png'
        plot_txt = str(os.path.join(cwd, path_chi, plot_txt))
        print(plot_txt)
        plt.savefig(plot_txt)
    elif False:
        var_pd = [float(d[0]) for d in var]
        var_t1 = [float(d[1]) for d in var]
        var_mt = [float(d[2]) for d in var]
        plt.figure()
        plt.plot(echos, var_pd, 'r--', echos, var_t1, 'r-', echos, var_mt, 'r-.')
        plt.xlabel('leftout echo')
        plt.ylabel('variance')
        plt.title(cl_list[0])
        plt.legend(["mt", "pd", "t1"])

        plot_txt = 'variance_plot_' + datime + '_' + cl_list[index] + '.png'
        print(plot_txt)
        plot_txt = str(os.path.join(os.getcwd(), path_chi, plot_txt))
        plt.savefig(plot_txt)
    else:
        var_pd = [float(d[0]) for d in dof]
        var_t1 = [float(d[1]) for d in dof]
        var_mt = [float(d[2]) for d in dof]
        plt.figure()
        plt.plot(echos, var_pd, 'r--', echos, var_t1, 'r-', echos, var_mt, 'r-.')
        plt.xlabel('leftout echo')
        plt.ylabel('dof')
        plt.title(cl_list[0])
        plt.legend(["mt", "pd", "t1"])

        plot_txt = 'dof_plot_' + datime + '_' + cl_list[index] + '.png'
        print(plot_txt)
        plot_txt = str(os.path.join(os.getcwd(), path_chi, plot_txt))
        plt.savefig(plot_txt)
