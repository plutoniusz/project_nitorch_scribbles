from matplotlib import pyplot as plt
import os

echos = [0,1,2,3,4,5]
#echos = [0]

# datime = "2022-05-03_20-48-37"
# likelihoods = "likelihoods_" + datime + ".txt"

# datime_list = ['2022-05-04_08-27-14', '2022-05-04_11-09-10', '2022-05-04_13-36-52', '2022-05-04_15-57-42',
#              '2022-05-04_18-17-01', '2022-05-04_20-46-55', '2022-05-04_22-56-01', '2022-05-05_01-19-49',
#              '2022-05-05_03-51-02', '2022-05-05_08-33-46', '2022-05-05_11-18-58', '2022-05-05_13-35-16',
#              '2022-05-05_15-49-07', '2022-05-05_18-13-43', '2022-05-05_20-36-01', '2022-05-06_11-30-07',
#              '2022-05-10_18-35-53', '2022-05-10_20-43-47', '2022-05-10_22-56-26']

# datime_list = ['2022-05-16_00-22-49', '2022-05-16_02-59-17', '2022-05-16_05-39-56',
#                  '2022-05-16_08-22-05', '2022-05-16_11-04-06']


# datime_list = ['2022-05-16_00-22-49', '2022-05-16_02-59-17', '2022-05-16_05-39-56',
#                   '2022-05-16_08-22-05']

#datime_list = ['2022-05-19_15-38-32', '2022-05-19_16-07-37']

#datime_list = ['2022-05-19_17-36-03', '2022-05-19_17-55-45', '2022-05-19_18-22-53']
datime_list = ['2022-05-22_20-45-15', '2022-05-22_22-25-13', '2022-05-23_01-06-32']

cl_list = ['112111', '115326', '116284', '128221', '130519',
         '133749', '170192', '176117', '208010', '210022',
         '211787', '214685', '232237', '242234', '260478',
         '308597', '324038', '330406', '346878']

#datime_now = '2022-05-13_16-08-18'
#datime_now = "2022-05-17_14-58-44"
#datime_now = "2022-05-19_22-19-23"
datime_now = "2022-05-23_14-05-29"

#lin_style = ['bs-', 'bs:','bs--', 'bs-.', 'rs-']

lin_style_chi = ['rs-', 'rs:','rs--', 'rs-.', 'r*-']
lin_style_gauss = ['bs-', 'bs:','bs--', 'bs-.', 'b*-']

plt.figure()   
for index, datime in enumerate(datime_list):
    likelihoods = "likelihoods_" + datime + datime_now + ".txt"
    path_gauss = 'qmri_results/' + 'gauss' + '_results_leftout_'+ datime
    likelihoods_gauss = os.path.join(os.getcwd(), path_gauss, likelihoods)

    path_chi = 'qmri_results/' + 'chi' + '_results_leftout_'+ datime
    likelihoods_chi = os.path.join(os.getcwd(), path_chi, likelihoods)

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


        if any(l == 'gauss' for l in line):
            if any(l == 'MT' for l in line):
                mt_gauss.append(float(line[-1]))
            if any(l == 'PD' for l in line):
                pd_gauss.append(float(line[-1]))
            if any(l == 'T1' for l in line):
                t1_gauss.append(float(line[-1]))

    #plt.yscale('log')
    # plt.plot(echos, mt_chi, 'rs' + lin_style[index], echos, mt_gauss, 'bs' + lin_style[index], echos, pd_chi, 'r^' + lin_style[index],
    #  echos, pd_gauss, 'b^' + lin_style[index], echos, t1_chi, 'r*' + lin_style[index], echos, t1_gauss, 'b*' + lin_style[index])

    #plt.plot(echos, t1_gauss, lin_style[index])

    plt.plot(echos, mt_chi, lin_style_chi[index], echos, mt_gauss, lin_style_gauss[index])

    plt.xlabel('leftout echo')
    plt.ylabel('loglikelihood')
    #plt.title('hMRI sample dataset')
    #plt.title(cl_list[index])
    plt.title(cl_list[0])
    #plt.legend(['mt_chi', 'mt_gauss', 'pd_chi', 'pd_gauss', 't1_chi', 't1_gauss'])
    #plt.legend(['/1000', '/10', 'x1', 'x10', 'x1000'])
    plt.legend(['TKH_chi', 'TKH_gauss', "TV_chi", "TV_gauss", "JTV_chi", "JTV_gauss" ])
    #plt.legend(['TKH', 'TV', "JTV"])

    plot_txt = 'likelihood_plot_' + datime + '_' + datime_now + '_' + cl_list[index]
    plot_txt = 'likelihood_plot_' + datime + '_' + datime_now + '_' + cl_list[1]
    print(plot_txt)
plot_txt = str(os.path.join(os.getcwd(), path_chi, plot_txt))

i = 0
while os.path.exists(plot_txt + "_" + str(i) + '.png'):
    i=i+1

plt.savefig(plot_txt + "_" + str(i) + '.png')

