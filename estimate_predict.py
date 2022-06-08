import os
import nitorch.tools.qmri.io as qio
from nitorch.tools.qmri.param import ParameterMap
from nitorch.tools.qmri.relax import GREEQOptions
from nitorch.io import savef
from nitorch.tools.qmri.relax._mpm._greeq import greeq
from nitorch.tools.qmri.relax._mpm._predict import gre

from pathlib import Path
from datetime import datetime

# which echoes to estimate
#echos = [0, 1, 2, 3, 4, 5]
echos = [3]
second_model = 'gauss'
model = 'chi'
penalty = dict(pd=5, r1=5, mt=5, r2s=0.5)

print(f'penalty: {penalty}')

# dataset choice
# 0.6 dataset
mc = False
# 0.8 dataset
cl_list = ['112111', '115326', '116284', '128221', '130519', '133749', '170192', '176117',
 '208010', '210022', '211787', '214685', '232237', '242234', '260478', '307789', '308597',
  '324038', '330406', '346878']
cl_list = [cl_list[8]]
# hMRI dataset
cl_list = [False]

for cl in cl_list:
    if cl:
        mc = False
    # otherwise hmri toolbox dataset

    # for naming the result folders by the estimation date
    datime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    print(datime)
    print(cl)

    # paths to dataset
    print("getting paths to dataset folder")
    cwd = os.getcwd()
    if mc:
        pth_mris = [os.path.join(cwd, '4John_Klara/mtw_mfc_3dflash_v1k_180deg_RR_0038'),
                    os.path.join(cwd, '4John_Klara/pdw_mfc_3dflash_v1k_RR_0036'),
                    os.path.join(cwd, '4John_Klara/t1w_mfc_3dflash_v1k_RR_0034')]

    elif cl:
        #gen_path = "/data/underworld/01_DATA/00_ANALYSIS/02_KBAS/03_data/source/mri/"
        gen_path = "/data/underworld/kbas/03_data/source/mri/"
        path_dataset = os.path.join(gen_path, cl)
        path_scans = os.listdir(path_dataset)
        path_scans = os.path.join(path_dataset, path_scans[0])
        pth_mris = [os.path.join(path_scans, "16"), #mtw
                    os.path.join(path_scans, "13"), #pdw
                    os.path.join(path_scans, "10")] #t1w
    
    else:
        print("tutu")
        pth_mris = [os.path.join(cwd, 'MPM/mtw_mfc_3dflash_v1i_R4_0012'),
                    os.path.join(cwd, 'MPM/pdw_mfc_3dflash_v1i_R4_0009'),
                    os.path.join(cwd, 'MPM/t1w_mfc_3dflash_v1i_R4_0015')]


    # paths to field maps
    print("paths to additional maps")
    if cl:
        path_dataset = os.path.join("/data/underworld/01_DATA/00_ANALYSIS/02_KBAS/03_data/raw/", cl)
        path_pom = os.listdir(path_dataset)
        path_dataset = os.path.join(path_dataset, path_pom[0])
        path_suppl = os.path.join(path_dataset, "anat/Results/Supplementary")
        for filename in os.listdir(str(path_suppl)):
            if filename.endswith("B1map.nii"):
                b1p_map = str(os.path.join(path_suppl, filename))
            elif filename.endswith("B1ref.nii"):
                b1p_ref = str(os.path.join(path_suppl, filename))
        #b1p_map = os.path.join(path_dataset, "anat/Results/Supplementary/sMP02874-0005-00001-000001-01_B1map.nii")
        #b1p_ref = os.path.join(path_dataset, "anat/Results/Supplementary/sMP02874-0005-00001-000001-01_B1ref.nii")
        mtw_b1m_map = os.path.join(path_dataset, "anat/Results/Supplementary/sensMap_HC_over_BC_division_MT.nii")
        pdw_b1m_map = os.path.join(path_dataset, "anat/Results/Supplementary/sensMap_HC_over_BC_division_PD.nii")
        t1w_b1m_map = os.path.join(path_dataset, "anat/Results/Supplementary/sensMap_HC_over_BC_division_T1.nii")

    elif not mc:
        for filename in os.listdir(str(os.path.join(cwd, "MPM/pdw_mfc_3dflash_v1i_R4_0009/Results/Supplementary"))):
            if filename.endswith("B1map.nii"):
                b1p_map = str(os.path.join(cwd, "MPM/pdw_mfc_3dflash_v1i_R4_0009/Results/Supplementary", filename))
            elif filename.endswith("B1ref.nii"):
                b1p_ref = str(os.path.join(cwd, "MPM/pdw_mfc_3dflash_v1i_R4_0009/Results/Supplementary", filename))
        mtw_b1m_map = str(os.path.join(cwd, "MPM/pdw_mfc_3dflash_v1i_R4_0009/Results/Supplementary/sensMap_HC_over_BC_division_MT.nii"))
        pdw_b1m_map = str(os.path.join(cwd, "MPM/pdw_mfc_3dflash_v1i_R4_0009/Results/Supplementary/sensMap_HC_over_BC_division_PD.nii"))
        t1w_b1m_map = str(os.path.join(cwd, "MPM/pdw_mfc_3dflash_v1i_R4_0009/Results/Supplementary/sensMap_HC_over_BC_division_T1.nii"))

    #print(b1p_map, b1p_ref, mtw_b1m_map, pdw_b1m_map, t1w_b1m_map)

    # preparing path lists of observations 
    for echo in echos:
        print(f"left out echo: {echo}")
        print("preparing lists")
        fmtw = []
        for filename in os.listdir(str(pth_mris[0])):
            if filename.endswith(".nii"):
                fmtw.append(str(os.path.join(pth_mris[0], filename)))
            else:
                continue
        fpdw = []
        for filename in os.listdir(str(pth_mris[1])):
            if filename.endswith(".nii"):
                fpdw.append(str(os.path.join(pth_mris[1], filename)))
            else:
                continue
        ft1w = []
        for filename in os.listdir(str(pth_mris[2])):
            if filename.endswith(".nii"):
                ft1w.append(str(os.path.join(pth_mris[2], filename)))
            else:
                continue
        
        # removing one echo for each validation
        print("remove echo for validation")
        mtwlf = fmtw[echo]
        pdwlf = fpdw[echo]
        t1wlf = ft1w[echo]
        del fmtw[echo]
        del fpdw[echo]
        del ft1w[echo]

        # reading the observations and field maps
        print("reading images from paths using nitorch GradientEchoMulti")
        t1w = qio.GradientEchoMulti.from_fnames(ft1w)
        pdw = qio.GradientEchoMulti.from_fnames(fpdw)
        mtw = qio.GradientEchoMulti.from_fnames(fmtw, mt=True)
        print("precomputind field maps")
        if mc:
            transmit = None
            receive = [None]*3
        else:
            transmit = qio.PrecomputedFieldMap(b1p_map, magnitude=b1p_ref)
            receive = [qio.PrecomputedFieldMap(pdw_b1m_map,  unit='a.u'),
                        qio.PrecomputedFieldMap(t1w_b1m_map, unit='a.u'),
                        qio.PrecomputedFieldMap(mtw_b1m_map, unit='a.u')]

        if cl==False:
            cl = 'MPM'

        # options for parameter estimation
        mtw.mt = True
        opt = GREEQOptions()
        opt.recon.space = 1
        opt.backend.device = 'cuda'
        opt.preproc.register = False
        opt.optim.nb_levels = 1
        opt.verbose = 1
        opt.likelihood = model
        opt.noisemodel = 'chi'
        print(f"loglikelihood: {opt.likelihood}, noisemodel: {opt.noisemodel}")
        print("start greeq")
        opt.penalty.factor = penalty

        save_folder = 'qmri_results/' + opt.likelihood + '_results_leftout_' + datime
        folder_make = Path(save_folder).mkdir(parents=True, exist_ok=True)

        with open(save_folder + '/log_est.txt', 'a') as f:
            f.write(datime)
            f.write('\n')
            f.write(cl)
            f.write('\n')
            f.write(str(penalty))
            f.write('\n')
            f.write(model)
            f.write('\n')
            f.write(second_model)
            f.write('\n')
            f.write(str(echos))
            f.write('\n')
            f.write(save_folder)

        print (datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
        pd, r1, r2s, mt = greeq([pdw, t1w, mtw], transmit, receive, opt=opt)
        print (datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))

        #saving parameter maps
        pm_path = Path(save_folder + '/parameter_map').mkdir(parents=True, exist_ok=True)
        print(save_folder)
        savef(pd.volume, os.path.join(cwd, save_folder + '/parameter_map' +'/pd'+str(echo)+'.nii'), affine= pd.affine)
        savef(r1.volume, os.path.join(cwd, save_folder + '/parameter_map' +'/r1'+str(echo)+'.nii'), affine= r1.affine)
        savef(r2s.volume, os.path.join(cwd, save_folder + '/parameter_map' +'/r2s'+str(echo)+'.nii'), affine= r2s.affine)
        savef(mt.volume, os.path.join(cwd, save_folder + '/parameter_map' +'/mt'+str(echo)+'.nii'), affine= mt.affine)

        noise_txt = f"echo: {echo}, model: {model}, noise: {pd.noise}, std: {pd.dof}\n"

        with open(save_folder + '/noise_' + cl + '_' + datime + '.txt', 'a') as f:
            f.write(noise_txt)
            print(noise_txt)

        # paths to paramter maps
        cwd = os.getcwd()
        mtp = os.path.join(cwd, save_folder + '/parameter_map' +'/mt'+str(echo)+'.nii')
        pdp = os.path.join(cwd, save_folder + '/parameter_map' +'/pd'+str(echo)+'.nii')
        r1p = os.path.join(cwd, save_folder + '/parameter_map' +'/r1'+str(echo)+'.nii')
        r2sp = os.path.join(cwd, save_folder + '/parameter_map' +'/r2s'+str(echo)+'.nii')
        # reading the parameter maps
        if not isinstance(pdp, ParameterMap):
            pdp = ParameterMap(pdp)
        if not isinstance(r1p, ParameterMap):
            r1p = ParameterMap(r1p)
        if not isinstance(r2sp, ParameterMap):
            r2sp = ParameterMap(r2sp)
        if not isinstance(mtp, ParameterMap):
            mtp = ParameterMap(mtp)
            mtp.unit = '%'
        if not isinstance(pdp, ParameterMap):
            pdp = ParameterMap(pd.volume, affine= pd.affine)

        # calculating the predicted echo with gre for three contrasts mtw, pdw, t1w
        mtwl = qio.GradientEchoMulti(mtwlf)
        print(mtwl.te, mtwl.tr, mtwl.fa, mtw.noise, mtw.dof)
        flash = gre(pdp, r1p, r2sp,  mtp,  transmit=transmit, receive=receive[2], te=mtwl.te, tr=mtwl.tr, fa=mtwl.fa, mtpulse=True, affine=mtwl.affine, shape=mtwl.shape)
        pr_path = Path(save_folder + '/predicted').mkdir(parents=True, exist_ok=True)
        text = save_folder + '/predicted' + '/flash_mtw'+str(echo)+'.nii'
        savef(flash.volume, os.path.join(cwd, text), affine=flash.affine)

        pdwl = qio.GradientEchoMulti(pdwlf)
        print(pdwl.te, mtwl.tr, pdwl.fa, pdw.noise, pdw.dof)
        flash = gre(pdp, r1p, r2sp,  mtp,  transmit=transmit, receive=receive[0], te=pdwl.te, tr=pdwl.tr, fa=pdwl.fa, mtpulse=False, affine=pdwl.affine, shape=pdwl.shape)
        text = save_folder + '/predicted' + '/flash_pdw'+str(echo)+'.nii'
        savef(flash.volume, os.path.join(cwd, text), affine=flash.affine)

        t1wl = qio.GradientEchoMulti(t1wlf)
        print(t1wl.te, t1wl.tr, t1wl.fa, t1w.noise, t1w.dof)
        flash = gre(pdp, r1p, r2sp,  mtp,  transmit=transmit, receive=receive[1], te=t1wl.te, tr=t1wl.tr, fa=t1wl.fa, mtpulse=False, affine=t1wl.affine, shape=t1wl.shape)
        text = save_folder + '/predicted' + '/flash_t1w'+str(echo)+'.nii'
        savef(flash.volume, os.path.join(cwd, text), affine=flash.affine)

        #second model for comparison
        if second_model:

            mtw.mt = True
            opt = GREEQOptions()
            opt.recon.space = 1
            opt.backend.device = 'cuda'
            opt.preproc.register = False
            opt.optim.nb_levels = 1
            opt.verbose = 1
            opt.likelihood = second_model
            opt.noisemodel = 'chi'
            print(f"loglikelihood: {opt.likelihood}, noisemodel: {opt.noisemodel}")
            print("start greeq")
            opt.penalty.factor = penalty
            print(datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
            pd, r1, r2s, mt = greeq([pdw, t1w, mtw], transmit, receive, opt=opt)
            print(datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
            #saving parameter maps
            save_folder = 'qmri_results/' + opt.likelihood + '_results_leftout_' + datime
            folder_make = Path(save_folder).mkdir(parents=True, exist_ok=True)
            print(save_folder)


            with open(save_folder + '/log_est.txt', 'a') as f:
                f.write(datime)
                f.write('\n')
                f.write(cl)
                f.write('\n')
                f.write(str(penalty))
                f.write('\n')
                f.write(model)
                f.write('\n')
                f.write(second_model)
                f.write('\n')
                f.write(str(echos))
                f.write('\n')
                f.write(save_folder)

            pm_path = Path(save_folder + '/parameter_map').mkdir(parents=True, exist_ok=True)
            savef(pd.volume, os.path.join(cwd, save_folder + '/parameter_map' +'/pd'+str(echo)+'.nii'), affine= pd.affine)
            savef(r1.volume, os.path.join(cwd, save_folder + '/parameter_map' +'/r1'+str(echo)+'.nii'), affine= r1.affine)
            savef(r2s.volume, os.path.join(cwd, save_folder + '/parameter_map' +'/r2s'+str(echo)+'.nii'), affine= r2s.affine)
            savef(mt.volume, os.path.join(cwd, save_folder + '/parameter_map' +'/mt'+str(echo)+'.nii'), affine= mt.affine)

            noise_txt = f"echo: {echo}, model: {second_model}, noise: {pd.noise}, std: {pd.dof}\n"

            with open(save_folder + '/noise_' + cl + '_' + datime + '.txt', 'a') as f:
                f.write(noise_txt)
                print(noise_txt)

            # paths to paramter maps
            cwd = os.getcwd()
            mtp = os.path.join(cwd, save_folder + '/parameter_map' +'/mt'+str(echo)+'.nii')
            pdp = os.path.join(cwd, save_folder + '/parameter_map' +'/pd'+str(echo)+'.nii')
            r1p = os.path.join(cwd, save_folder + '/parameter_map' +'/r1'+str(echo)+'.nii')
            r2sp = os.path.join(cwd, save_folder + '/parameter_map' +'/r2s'+str(echo)+'.nii')
            # reading the parameter maps
            if not isinstance(pdp, ParameterMap):
                pdp = ParameterMap(pdp)
            if not isinstance(r1p, ParameterMap):
                r1p = ParameterMap(r1p)
            if not isinstance(r2sp, ParameterMap):
                r2sp = ParameterMap(r2sp)
            if not isinstance(mtp, ParameterMap):
                mtp = ParameterMap(mtp)
                mtp.unit = '%'

            # calculating the predicted echo with gre for three contrasts mtw, pdw, t1w
            #del mtwl
            #mtwl = qio.GradientEchoMulti(mtwlf)
            print(mtwl.te, mtwl.tr, mtwl.fa, mtw.noise, mtw.dof)
            flash = gre(pdp, r1p, r2sp,  mtp,  transmit=transmit, receive=receive[2], te=mtwl.te, tr=mtwl.tr, fa=mtwl.fa, mtpulse=True, affine=mtwl.affine, shape=mtwl.shape)
            pr_path = Path(save_folder + '/predicted').mkdir(parents=True, exist_ok=True)
            text = save_folder + '/predicted' + '/flash_mtw'+str(echo)+'.nii'
            savef(flash.volume, os.path.join(cwd, text), affine=flash.affine)

            #del pdwl
            #pdwl = qio.GradientEchoMulti(pdwlf)
            print(pdwl.te, mtwl.tr, pdwl.fa, pdw.noise, pdw.dof)
            flash = gre(pdp, r1p, r2sp,  mtp,  transmit=transmit, receive=receive[0], te=pdwl.te, tr=pdwl.tr, fa=pdwl.fa, mtpulse=False, affine=pdwl.affine, shape=pdwl.shape)
            text = save_folder + '/predicted' + '/flash_pdw'+str(echo)+'.nii'
            savef(flash.volume, os.path.join(cwd, text), affine=flash.affine)

            #del t1wl
            #t1wl = qio.GradientEchoMulti(t1wlf)
            print(t1wl.te, t1wl.tr, t1wl.fa, t1w.noise, t1w.dof)
            flash = gre(pdp, r1p, r2sp,  mtp,  transmit=transmit, receive=receive[1], te=t1wl.te, tr=t1wl.tr, fa=t1wl.fa, mtpulse=False, affine=t1wl.affine, shape=t1wl.shape)
            text = save_folder + '/predicted' + '/flash_t1w'+str(echo)+'.nii'
            savef(flash.volume, os.path.join(cwd, text), affine=flash.affine)

        #if second_model:
        if False:

            mtw.mt = True
            opt = GREEQOptions()
            opt.recon.space = 1
            opt.backend.device = 'cuda'
            opt.preproc.register = False
            opt.optim.nb_levels = 1
            opt.verbose = 1
            opt.likelihood = second_model
            opt.noisemodel = 'rice'
            print(f"loglikelihood: {opt.likelihood}, noisemodel: {opt.noisemodel}")
            print("start greeq")
            opt.penalty.factor = penalty
            pd, r1, r2s, mt = greeq([pdw, t1w, mtw], transmit, receive, opt=opt)
            #saving parameter maps
            save_folder = opt.likelihood + '_rice' + '_results_leftout_' + datime
            pm_path = Path(save_folder + '/parameter_map').mkdir(parents=True, exist_ok=True)

            savef(pd.volume, os.path.join(cwd, save_folder + '/parameter_map'+ '/pd'+str(echo)+'.nii'), affine= pd.affine)
            savef(r1.volume, os.path.join(cwd, save_folder + '/parameter_map' +'/r1'+str(echo)+'.nii'), affine= r1.affine)
            savef(r2s.volume, os.path.join(cwd, save_folder + '/parameter_map' +'/r2s'+str(echo)+'.nii'), affine= r2s.affine)
            savef(mt.volume, os.path.join(cwd, save_folder + '/parameter_map' +'/mt'+str(echo)+'.nii'), affine= mt.affine)

            # paths to paramter maps
            cwd = os.getcwd()
            mtp = os.path.join(cwd, save_folder + '/parameter_map'+'/mt'+str(echo)+'.nii')
            pdp = os.path.join(cwd, save_folder + '/parameter_map' +'/pd'+str(echo)+'.nii')
            r1p = os.path.join(cwd, save_folder + '/parameter_map' +'/r1'+str(echo)+'.nii')
            r2sp = os.path.join(cwd, save_folder + '/parameter_map' +'/r2s'+str(echo)+'.nii')
            # reading the parameter maps
            if not isinstance(pdp, ParameterMap):
                pdp = ParameterMap(pdp)
            if not isinstance(r1p, ParameterMap):
                r1p = ParameterMap(r1p)
            if not isinstance(r2sp, ParameterMap):
                r2sp = ParameterMap(r2sp)
            if not isinstance(mtp, ParameterMap):
                mtp = ParameterMap(mtp)
                mtp.unit = '%'

            # calculating the predicted echo with gre for three contrasts mtw, pdw, t1w
            mtwl = qio.GradientEchoMulti(mtwl)
            print(mtwl.te, mtwl.tr, mtwl.fa, mtw.noise, mtw.dof)
            flash = gre(pdp, r1p, r2sp,  mtp,  transmit=transmit, receive=receive[2], te=mtwl.te, tr=mtwl.tr, fa=mtwl.fa, mtpulse=True, affine=mtwl.affine, shape=mtwl.shape)
            pr_path = Path(save_folder + '/predicted').mkdir(parents=True, exist_ok=True)
            text = save_folder + '/predicted' + '/flash_mtw'+str(echo)+'.nii'
            savef(flash.volume, os.path.join(cwd, text), affine=flash.affine) #, noise = pdp.noise[2], dof = pdp.dof[2]

            pdwl = qio.GradientEchoMulti(pdwl)
            print(pdwl.te, mtwl.tr, pdwl.fa, pdw.noise, pdw.dof)
            flash = gre(pdp, r1p, r2sp,  mtp,  transmit=transmit, receive=receive[0], te=pdwl.te, tr=pdwl.tr, fa=pdwl.fa, mtpulse=False, affine=pdwl.affine, shape=pdwl.shape)
            text = save_folder + '/predicted' + '/flash_pdw'+str(echo)+'.nii'
            savef(flash.volume, os.path.join(cwd, text), affine=flash.affine)

            t1wl = qio.GradientEchoMulti(t1wl)
            print(t1wl.te, t1wl.tr, t1wl.fa, t1w.noise, t1w.dof)
            flash = gre(pdp, r1p, r2sp,  mtp,  transmit=transmit, receive=receive[1], te=t1wl.te, tr=t1wl.tr, fa=t1wl.fa, mtpulse=False, affine=t1wl.affine, shape=t1wl.shape)
            text = save_folder + '/predicted' + '/flash_t1w'+str(echo)+'.nii'
            savef(flash.volume, os.path.join(cwd, text), affine=flash.affine)