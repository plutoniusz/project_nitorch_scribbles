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
echos = [0, 1]
models = ['chi', 'gauss']
penalty = dict(pd=5, r1=5, mt=5, r2s=0.5)

# dataset choice
datasets = ['mpm',] #'mpm'/ 'cl'/ 'mc'

if datasets == ['cl']:
    datasets = ['112111', '115326', '116284', '128221', '130519', '133749', '170192', '176117',
                '208010', '210022', '211787', '214685', '232237', '242234', '260478', '307789', '308597',
                '324038', '330406', '346878']
    cl = True
else:
    cl = False

# paths to the datasets
for dataset in datasets:

    # for naming the result folders by the estimation date
    datime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    print(f"date: {datime}, dataset: {dataset}")

    # paths to dataset
    print("getting paths to dataset folder")
    cwd = os.getcwd()
    if dataset == 'mc':
        pth_mris = [os.path.join(cwd, '4John_Klara/mtw_mfc_3dflash_v1k_180deg_RR_0038'),
                    os.path.join(cwd, '4John_Klara/pdw_mfc_3dflash_v1k_RR_0036'),
                    os.path.join(cwd, '4John_Klara/t1w_mfc_3dflash_v1k_RR_0034')]
    elif dataset == 'mpm':
        pth_mris = [os.path.join(cwd, 'MPM/mtw_mfc_3dflash_v1i_R4_0012'),
                    os.path.join(cwd, 'MPM/pdw_mfc_3dflash_v1i_R4_0009'),
                    os.path.join(cwd, 'MPM/t1w_mfc_3dflash_v1i_R4_0015')]
    elif cl:
        #gen_path = "/data/underworld/01_DATA/00_ANALYSIS/02_KBAS/03_data/source/mri/"
        gen_path = "/data/underworld/kbas/03_data/source/mri/"
        path_dataset = os.path.join(gen_path, dataset)
        path_scans = os.listdir(path_dataset)
        path_scans = os.path.join(path_dataset, path_scans[0])
        pth_mris = [os.path.join(path_scans, "16"), #mtw
                    os.path.join(path_scans, "13"), #pdw
                    os.path.join(path_scans, "10")] #t1w

    # paths to field maps
    print("paths to additional maps")
    if cl:
        path_dataset = os.path.join("/data/underworld/01_DATA/00_ANALYSIS/02_KBAS/03_data/raw/", dataset)
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

    elif dataset == 'mpm':
        for filename in os.listdir(str(os.path.join(cwd, "MPM/pdw_mfc_3dflash_v1i_R4_0009/Results/Supplementary"))):
            if filename.endswith("B1map.nii"):
                b1p_map = str(os.path.join(cwd, "MPM/pdw_mfc_3dflash_v1i_R4_0009/Results/Supplementary", filename))
            elif filename.endswith("B1ref.nii"):
                b1p_ref = str(os.path.join(cwd, "MPM/pdw_mfc_3dflash_v1i_R4_0009/Results/Supplementary", filename))
        mtw_b1m_map = str(os.path.join(cwd, "MPM/pdw_mfc_3dflash_v1i_R4_0009/Results/Supplementary/sensMap_HC_over_BC_division_MT.nii"))
        pdw_b1m_map = str(os.path.join(cwd, "MPM/pdw_mfc_3dflash_v1i_R4_0009/Results/Supplementary/sensMap_HC_over_BC_division_PD.nii"))
        t1w_b1m_map = str(os.path.join(cwd, "MPM/pdw_mfc_3dflash_v1i_R4_0009/Results/Supplementary/sensMap_HC_over_BC_division_T1.nii"))

    # preparing path lists of observations 
    for echo in echos:
        print(f"left out echo: {echo}")
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
        if dataset == 'mc':
            transmit = None
            receive = [None]*3
        else:
            transmit = qio.PrecomputedFieldMap(b1p_map, magnitude=b1p_ref)
            receive = [qio.PrecomputedFieldMap(pdw_b1m_map,  unit='a.u'),
                        qio.PrecomputedFieldMap(t1w_b1m_map, unit='a.u'),
                        qio.PrecomputedFieldMap(mtw_b1m_map, unit='a.u')]

        for model in models:

            # folder for saving the results of this estimation
            save_folder = 'qmri_results/' + model + '_results_leftout_' + datime
            folder_make = Path(save_folder).mkdir(parents=True, exist_ok=True)

            # logfile
            log_txt = f"date: {datime}\n dataset: {dataset}\n penalty: {penalty}\n models: {models}\n echos: {echos}\n save_folder {save_folder}\n\n"
            with open(save_folder + '/log_est.txt', 'a') as f:
                f.write(log_txt)

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
            opt.penalty.factor = penalty
            print("start greeq")
            pd, r1, r2s, mt = greeq([pdw, t1w, mtw], transmit, receive, opt=opt)

            # saving parameter maps
            pm_path = Path(save_folder + '/parameter_map').mkdir(parents=True, exist_ok=True)
            savef(pd.volume, os.path.join(cwd, save_folder + '/parameter_map' +'/pd'+str(echo)+'.nii'), affine= pd.affine)
            savef(r1.volume, os.path.join(cwd, save_folder + '/parameter_map' +'/r1'+str(echo)+'.nii'), affine= r1.affine)
            savef(r2s.volume, os.path.join(cwd, save_folder + '/parameter_map' +'/r2s'+str(echo)+'.nii'), affine= r2s.affine)
            savef(mt.volume, os.path.join(cwd, save_folder + '/parameter_map' +'/mt'+str(echo)+'.nii'), affine= mt.affine)

            # svaing noise estimates
            noise_txt = f"echo: {echo}, model: {model}, noise: {pd.noise}, dof: {pd.dof}\n"
            with open(save_folder + '/noise_' + dataset + '_' + datime + '.txt', 'a') as f:
                f.write(noise_txt)

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
            flash = gre(pdp, r1p, r2sp,  mtp,  transmit=transmit, receive=receive[2], te=mtwl.te, tr=mtwl.tr, fa=mtwl.fa, mtpulse=True, affine=mtwl.affine, shape=mtwl.shape)
            pr_path = Path(save_folder + '/predicted').mkdir(parents=True, exist_ok=True)
            text = save_folder + '/predicted' + '/flash_mtw'+str(echo)+'.nii'
            savef(flash.volume, os.path.join(cwd, text), affine=flash.affine)

            pdwl = qio.GradientEchoMulti(pdwlf)
            flash = gre(pdp, r1p, r2sp,  mtp,  transmit=transmit, receive=receive[0], te=pdwl.te, tr=pdwl.tr, fa=pdwl.fa, mtpulse=False, affine=pdwl.affine, shape=pdwl.shape)
            text = save_folder + '/predicted' + '/flash_pdw'+str(echo)+'.nii'
            savef(flash.volume, os.path.join(cwd, text), affine=flash.affine)

            t1wl = qio.GradientEchoMulti(t1wlf)
            flash = gre(pdp, r1p, r2sp,  mtp,  transmit=transmit, receive=receive[1], te=t1wl.te, tr=t1wl.tr, fa=t1wl.fa, mtpulse=False, affine=t1wl.affine, shape=t1wl.shape)
            text = save_folder + '/predicted' + '/flash_t1w'+str(echo)+'.nii'
            savef(flash.volume, os.path.join(cwd, text), affine=flash.affine)