from cmath import nan
from math import log
import os
from nitorch.io import savef
import nitorch.tools.qmri.io as qio
import torch
from nitorch.core.math import besseli
from nitorch.core.constants import pi
from nitorch.core.linalg import lmdiv
from nitorch.tools.qmri.relax.utils import smart_grid, smart_pull
from pathlib import Path
import re
from datetime import datetime

def chi_ll(dat, pred, dof, var, model='chi'):
    """
    Calculate the log likelihood of the observation given predicted echo

    """
    rec_var = 1/var
    if model == 'chi':
        msk_check = torch.isfinite(pred) & torch.isfinite(dat) & (dat > 0) & (pred > 0)
        # tiny = torch.tensor(1e-32)
        dat[~msk_check] = 0
        pred[~msk_check] = 0
    elif model == 'rice':
        msk = torch.isfinite(pred) & torch.isfinite(dat) & (dat > 0) & (pred > 0)
        dat[~msk_check] = 0
        pred[~msk_check] = 0
    else :
        msk_check = torch.isfinite(pred) & torch.isfinite(dat) & (dat > 0) & (pred > 0)
        dat[~msk_check] = 0
        pred[~msk_check] = 0

    if model == 'chi':
        # z = (dat[msk]*pred[msk]*rec_var).clamp_min_(tiny)
        z = (dat[msk_check]*pred[msk_check]*rec_var)
        ll = ((1.-dof/2.) * (pred[msk_check].log())
                + (dof/2.) *(dat[msk_check].log())
                - 0.5 * rec_var * (pred[msk_check].square() + dat[msk_check].square())
                + besseli(dof/2.-1., z, 'log')
                - log(var))
        #ll = torch.sum(ll, dtype=torch.double) 
    elif model =='rice':
        ll = (dat[msk_check] + tiny).log() - var.log() - (dat.square() + pred.square()) / (2 * var)
        ll = ll + besseli(0, dat * (pred/ var), 'log')
        #ll = torch.sum(ll, dtype=torch.double)
    else :
        # gaussian log-likelihood
        res = pred[msk_check].neg_().add_(dat[msk_check])
        ll = - (0.5 * rec_var * res.square() + 0.5*log(2.*pi*var))
        #ll = torch.sum(ll, dtype=torch.double)
    #print(type(ll))
    print(ll.shape)
    #print(ll.size())
    #savef(ll, os.path.join(cwd, save_folder+'/ll.nii'), affine = brain_mask_affine)
    ll = torch.sum(ll, dtype=torch.double) 
    return ll

# second model for comparison
second_model = 'gauss'
echos = [0,1,2,3,4,5]
datime_now =  datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
#echos = [0]
# datime_list = ['2022-05-04_08-27-14', '2022-05-04_11-09-10', '2022-05-04_13-36-52', '2022-05-04_15-57-42',
#              '2022-05-04_18-17-01', '2022-05-04_20-46-55', '2022-05-04_22-56-01', '2022-05-05_01-19-49',
#              '2022-05-05_03-51-02', '2022-05-05_08-33-46', '2022-05-05_11-18-58', '2022-05-05_13-35-16',
#              '2022-05-05_15-49-07', '2022-05-05_18-13-43', '2022-05-05_20-36-01', '2022-05-06_11-30-07',
#              '2022-05-10_18-35-53', '2022-05-10_20-43-47', '2022-05-10_22-56-26']

datime_list = ['2022-05-24_21-29-15']

mc = False
# cl_list = ['112111', '115326', '116284', '128221', '130519',
#          '133749', '170192', '176117', '208010', '210022',
#          '211787', '214685', '232237', '242234', '260478',
#          '308597', '324038', '330406', '346878']
cl_list = [None]

for index, datime in enumerate(datime_list):

    noise_txt = "noise_" + datime + ".txt"
    print(datime)

    cl = cl_list[index]
    if cl:
        mc = False
    cwd = os.getcwd()
    # parameter estimation model
    model = 'chi'

    if mc:
        save_folder = '4John_Klara/derivative/' + model + '_results_leftout_'+ datime
    else:
        save_folder = 'qmri_results/' + model + '_results_leftout_'+ datime

    # read predicted image
    predicted = 'predicted'
    pth_pred = os.path.join(cwd, save_folder, predicted)
    mtw_pred = []
    pdw_pred = []
    t1w_pred = []
    for filename in os.listdir(str(pth_pred)):
        if filename.endswith(".nii") and filename.startswith("flash_mtw"):
            mtw_pred.append(str(os.path.join(pth_pred, filename)))
        elif filename.endswith(".nii") and filename.startswith("flash_pdw"):
            pdw_pred.append(str(os.path.join(pth_pred, filename)))
        elif filename.endswith(".nii") and filename.startswith("flash_t1w"):
            t1w_pred.append(str(os.path.join(pth_pred, filename)))
        else:
            continue
    # read observed image
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
        pth_mris = [os.path.join(path_scans, "16"),
                    os.path.join(path_scans, "13"),
                    os.path.join(path_scans, "10")]

    else:
        pth_mris = [os.path.join(cwd, 'MPM/mtw_mfc_3dflash_v1i_R4_0012'),
            os.path.join(cwd, 'MPM/pdw_mfc_3dflash_v1i_R4_0009'),
            os.path.join(cwd, 'MPM/t1w_mfc_3dflash_v1i_R4_0015')]


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

    # read the brain mask
    mask_folder = 'mask'

    if mc:
        pth_mask = os.path.join(cwd, '4John_Klara/derivative')
    elif cl:
        gen_path = "/data/underworld/kbas/03_data/derivatives/"
        path_mask = os.path.join(gen_path, cl)
        path_pom = os.listdir(path_mask)
        path_pom = [d for d in path_pom if os.path.isdir(os.path.join(path_mask, d))]
        path_mask = os.path.join(path_mask, path_pom[0])
        #pth_mask = os.path.join(path_mask, "dwi/qmap-preproc-dwimask")
        pth_mask = os.path.join(path_mask, "anat/spm-qmap-preproc")
    else:
        pth_mask = os.path.join(cwd, save_folder, mask_folder)
        pth_mask = os.path.join(cwd, "MPM")

    masks = []
    for filename in os.listdir(str(pth_mask)):
        if filename.endswith("brain_mask.nii"):
            masks.append(str(os.path.join(pth_mask, filename)))
        else:
            continue

    # second model for comparison
    if second_model:
        if mc:
            save_folder = '4John_Klara/derivative/' + second_model + '_results_leftout_'+ datime
        else:
            save_folder = 'qmri_results/' + second_model + '_results_leftout_'+ datime
        

        # read predicted image
        predicted = 'predicted'
        pth_pred_snd = os.path.join(cwd, save_folder, predicted)
        mtw_pred_snd = []
        pdw_pred_snd = []
        t1w_pred_snd = []
        for filename in os.listdir(str(pth_pred_snd)):
            if filename.endswith(".nii") and filename.startswith("flash_mtw"):
                mtw_pred_snd.append(str(os.path.join(pth_pred_snd, filename)))
            elif filename.endswith(".nii") and filename.startswith("flash_pdw"):
                pdw_pred_snd.append(str(os.path.join(pth_pred_snd, filename)))
            elif filename.endswith(".nii") and filename.startswith("flash_t1w"):
                t1w_pred_snd.append(str(os.path.join(pth_pred_snd, filename)))
            else:
                continue

    # if second_model:
    #     #save_folder = second_model + '_gauss' + '_results_leftout'
    #     save_folder = '4John_Klara/derivative/' + model + '_gauss' + 'results_leftout_'+ datime

    #     # read predicted image
    #     predicted = 'predicted'
    #     pth_pred_sndg = os.path.join(cwd, save_folder, predicted)
    #     mtw_pred_sndg = []
    #     pdw_pred_sndg = []
    #     t1w_pred_sndg = []
    #     for filename in os.listdir(str(pth_pred_sndg)):
    #         if filename.endswith(".nii") and filename.startswith("flash_mtw"):
    #             mtw_pred_sndg.append(str(os.path.join(pth_pred_sndg, filename)))
    #         elif filename.endswith(".nii") and filename.startswith("flash_pdw"):
    #             pdw_pred_sndg.append(str(os.path.join(pth_pred_sndg, filename)))
    #         elif filename.endswith(".nii") and filename.startswith("flash_t1w"):
    #             t1w_pred_sndg.append(str(os.path.join(pth_pred_sndg, filename)))
    #         else:
    #             continue

    if not cl:
        cl = 'MPM'
    #read noise and dof
    if not os.path.exists(os.path.join(save_folder,  noise_txt)):
        noise_txt = 'noise_' + cl + '_' + datime + '.txt'
    with open(os.path.join(save_folder,  noise_txt)) as f:
        lines = f.readlines()

    dof_chi = []
    noise_chi = []
    
    for i in range(len(echos)):
        line = lines[i]
        line = line.replace('[', "")
        line = line.replace(']', "")
        line = line.replace(',', "")

        split_line = line.split()
        if any(l == 'chi' for l in split_line):
            line = re.findall(r'[+-]?[0-9]+\.?[0-9]*', line)
            noise_chi.append(line[1:4])
            dof_chi.append(line[4:])

        if any(l == 'gauss' for l in split_line):
            line = re.findall(r'[+-]?[0-9]+\.?[0-9]*', line)
            noise_chi.append(line[1:4])
            dof_chi.append(line[4:])
   # print(noise_chi)
   # print(dof_chi)


    for echo in echos:

        if mc:
            save_folder = '4John_Klara/derivative/' + second_model + '_results_leftout_'+ datime
        else:
            save_folder = 'qmri_results/' + model + '_results_leftout_'+ datime

        #print(save_folder)

        # read predicted image
        mtwp = qio.GradientEchoMulti(mtw_pred[echo])
        pdwp = qio.GradientEchoMulti(pdw_pred[echo])
        t1wp = qio.GradientEchoMulti(t1w_pred[echo])

        # read observed image
        mtwo = qio.GradientEchoMulti(fmtw[echo])
        pdwo = qio.GradientEchoMulti(fpdw[echo])
        t1wo = qio.GradientEchoMulti(ft1w[echo])

        # read the brain mask
        #brain_mask = qio.GradientEchoSingle(masks[echo])
        brain_mask = qio.GradientEchoSingle(masks[0])
        brain_mask_affine =brain_mask.affine
        brain_mask = brain_mask.fdata(dtype=torch.double)
        msk = torch.isfinite(brain_mask)
        size_mask= torch.sum(msk)
        brain_mask[~msk] = 0.

        mat = lmdiv(brain_mask_affine, mtwp.affine)
        grid = smart_grid(mat, mtwp.shape, brain_mask.shape)
        brain_mask_mtp = smart_pull(brain_mask, grid)
        savef(brain_mask_mtp, os.path.join(cwd, save_folder+'/mask_processed_mtp.nii'), affine = brain_mask_affine)

        mat = lmdiv(brain_mask_affine, pdwp.affine)
        grid = smart_grid(mat, pdwp.shape, brain_mask.shape)
        brain_mask_pdp = smart_pull(brain_mask, grid)
        savef(brain_mask_pdp, os.path.join(cwd, save_folder+'/mask_processed_pdp.nii'), affine = brain_mask_affine)

        mat = lmdiv(brain_mask_affine, t1wp.affine)
        grid = smart_grid(mat, t1wp.shape, brain_mask.shape)
        brain_mask_t1p = smart_pull(brain_mask, grid)
        savef(brain_mask_t1p, os.path.join(cwd, save_folder+'/mask_processed_t1p.nii'), affine = brain_mask_affine)
        print("brain mask calculated")

        # multiply mask by predicted image
        mtwpm = mtwp.fdata()*brain_mask_mtp
        pdwpm = pdwp.fdata()*brain_mask_pdp
        t1wpm = t1wp.fdata()*brain_mask_t1p

        # not needed really
        # pm_path = Path(save_folder + '/masked').mkdir(parents=True, exist_ok=True)
        # savef(mtwpm, os.path.join(cwd, save_folder+'/masked/mtwp'+str(echo)+'.nii'), affine = mtwp.affine)
        # savef(pdwpm, os.path.join(cwd, save_folder+'/masked/pdwp'+str(echo)+'.nii'), affine = pdwp.affine)
        # savef(t1wpm, os.path.join(cwd, save_folder+'/masked/t1wp'+str(echo)+'.nii'), affine = t1wp.affine)

        mat = lmdiv(brain_mask_affine, mtwo.affine)
        grid = smart_grid(mat, mtwo.shape, brain_mask.shape)
        brain_mask_mt = smart_pull(brain_mask, grid)
        savef(brain_mask_mt, os.path.join(cwd, save_folder+'/mask_processed_mt.nii'), affine = brain_mask_affine)

        mat = lmdiv(brain_mask_affine, pdwo.affine)
        grid = smart_grid(mat, pdwo.shape, brain_mask.shape)
        brain_mask_pd = smart_pull(brain_mask, grid)
        savef(brain_mask_pd, os.path.join(cwd, save_folder+'/mask_processed_pd.nii'), affine = brain_mask_affine)

        mat = lmdiv(brain_mask_affine, t1wo.affine)
        grid = smart_grid(mat, t1wo.shape, brain_mask.shape)
        brain_mask_t1 = smart_pull(brain_mask, grid)
        savef(brain_mask_t1, os.path.join(cwd, save_folder+'/mask_processed_t1.nii'), affine = brain_mask_affine)
        print("brain mask calculated")

        # multiply mask by observed image
        mtwom = mtwo.fdata()*brain_mask_mtp
        pdwom = pdwo.fdata()*brain_mask_pdp
        t1wom = t1wo.fdata()*brain_mask_t1p

        # # also not needed
        # savef(mtwom, os.path.join(cwd, save_folder+'/masked/mtwo'+str(echo)+'.nii'), affine = mtwo.affine)
        # savef(pdwom, os.path.join(cwd, save_folder+'/masked/pdwo'+str(echo)+'.nii'), affine = pdwo.affine)
        # savef(t1wom, os.path.join(cwd, save_folder+'/masked/t1wo'+str(echo)+'.nii'), affine = t1wo.affine)


        #brain_mask_size = brain_mask.sum()
    
        # caluclate chi lof likelihood for each contrast
        # ll_mtw = chi_ll(mtwom, mtwpm, dof[0], std[0], model=model)/size_mask
        # ll_pdw = chi_ll(pdwom, pdwpm, dof[1], std[1], model=model)/size_mask
        # ll_t1w = chi_ll(t1wom, t1wpm, dof[2], std[2], model=model)/size_mask

        dof = dof_chi[echo]
        std = noise_chi[echo]
        #print(mtwom.shape)

        # ll_mtw = chi_ll(mtwom, mtwpm, float(dof[0]), float(std[0]), model=model)/size_mask
        # ll_pdw = chi_ll(pdwom, pdwpm, float(dof[1]), float(std[1]), model=model)/size_mask
        # ll_t1w = chi_ll(t1wom, t1wpm, float(dof[2]), float(std[2]), model=model)/size_mask
        ll_mtw = chi_ll(mtwom, mtwpm, float(dof[0]), float(std[0]), model=model)
        ll_pdw = chi_ll(pdwom, pdwpm, float(dof[1]), float(std[1]), model=model)
        ll_t1w = chi_ll(t1wom, t1wpm, float(dof[2]), float(std[2]), model=model)

        # ll_mtw = chi_ll(mtwom, mtwpm, float(dof[0]), float(std[0]), model=second_model)/size_mask
        # ll_pdw = chi_ll(pdwom, pdwpm, float(dof[1]), float(std[1]), model=second_model)/size_mask
        # ll_t1w = chi_ll(t1wom, t1wpm, float(dof[2]), float(std[2]), model=second_model)/size_mask

        like_text = f"log likeihood MT contrast with {model} model: {ll_mtw}\nlog likeihood PD contrast with {model} model: {ll_pdw}\nlog likeihood T1 contrast with {model} model: {ll_t1w}\n"
        #print(like_text)

        with open(save_folder + '/likelihoods_' + datime + datime_now + '.txt', 'a') as f:
            f.write(like_text)

        

        # second model for comparison
        if second_model:

            if mc:
                save_folder = '4John_Klara/derivative/' + second_model + '_results_leftout_'+ datime
            else:
                save_folder = 'qmri_results/' + second_model + '_results_leftout_'+ datime

            #print(save_folder)

            # read predicted image
            mtwp_snd = qio.GradientEchoMulti(mtw_pred_snd[echo])
            pdwp_snd = qio.GradientEchoMulti(pdw_pred_snd[echo])
            t1wp_snd = qio.GradientEchoMulti(t1w_pred_snd[echo])

            mat = lmdiv(brain_mask_affine, mtwp_snd.affine)
            grid = smart_grid(mat, t1wo.shape, brain_mask.shape)
            brain_mask_mtg = smart_pull(brain_mask, grid)
            savef(brain_mask_mtg, os.path.join(cwd, save_folder+'/mask_processed_mtg.nii'), affine = brain_mask_affine)

            mat = lmdiv(brain_mask_affine, pdwp_snd.affine)
            grid = smart_grid(mat, pdwp_snd.shape, brain_mask.shape)
            brain_mask_pdg = smart_pull(brain_mask, grid)
            savef(brain_mask_pdg, os.path.join(cwd, save_folder+'/mask_processed_pdg.nii'), affine = brain_mask_affine)

            mat = lmdiv(brain_mask_affine, t1wp_snd.affine)
            grid = smart_grid(mat, t1wp_snd.shape, brain_mask.shape)
            brain_mask_t1g = smart_pull(brain_mask, grid)
            savef(brain_mask_t1g, os.path.join(cwd, save_folder+'/mask_processed_t1g.nii'), affine = brain_mask_affine)
            print("brain mask calculated")            

            # multiply mask by predicted image
            mtwpm_snd = mtwp_snd.fdata()*brain_mask_mtg
            pdwpm_snd = pdwp_snd.fdata()*brain_mask_pdg
            t1wpm_snd = t1wp_snd.fdata()*brain_mask_t1g

            # # not needed really
            # pm_path = Path(save_folder + '/masked').mkdir(parents=True, exist_ok=True)
            # savef(mtwpm_snd, os.path.join(cwd, save_folder+'/masked/mtwp'+str(echo)+'.nii'), affine = mtwp_snd.affine)
            # savef(pdwpm_snd, os.path.join(cwd, save_folder+'/masked/pdwp'+str(echo)+'.nii'), affine = pdwp_snd.affine)
            # savef(t1wpm_snd, os.path.join(cwd, save_folder+'/masked/t1wp'+str(echo)+'.nii'), affine = t1wp_snd.affine)

            # caluclate chi lof likelihood for each contrast
            # ll_mtw_snd = chi_ll(mtwom, mtwpm_snd, float(dof[0]), float(std[0]), model=second_model)/size_mask
            # ll_pdw_snd = chi_ll(pdwom, pdwpm_snd, float(dof[1]), float(std[1]), model=second_model)/size_mask
            # ll_t1w_snd = chi_ll(t1wom, t1wpm_snd, float(dof[2]), float(std[2]), model=second_model)/size_mask
            ll_mtw_snd = chi_ll(mtwom, mtwpm_snd, float(dof[0]), float(std[0]), model=second_model)
            ll_pdw_snd = chi_ll(pdwom, pdwpm_snd, float(dof[1]), float(std[1]), model=second_model)
            ll_t1w_snd = chi_ll(t1wom, t1wpm_snd, float(dof[2]), float(std[2]), model=second_model)

            # ll_mtw_snd = chi_ll(mtwom, mtwpm_snd, float(dof[0]), float(std[0]), model=model)/size_mask
            # ll_pdw_snd = chi_ll(pdwom, pdwpm_snd, float(dof[1]), float(std[1]), model=model)/size_mask
            # ll_t1w_snd = chi_ll(t1wom, t1wpm_snd, float(dof[2]), float(std[2]), model=model)/size_mask

            like_text = f"log likeihood MT contrast with {second_model} model: {ll_mtw_snd}\nlog likeihood PD contrast with {second_model} model: {ll_pdw_snd}\nlog likeihood T1 contrast with {second_model} model: {ll_t1w_snd}\n"

            with open(save_folder + '/likelihoods_' + datime + datime_now + '.txt', 'a') as f:
                f.write(like_text)
            #print(like_text)
        
            # print("chi log likelihood")
            # # caluclate chi lof likelihood for each contrast
            # ll_mtw_sndd = chi_ll(mtwom, mtwpm_snd, dof[0], std[0], model=model)
            # ll_pdw_sndd = chi_ll(pdwom, pdwpm_snd, dof[1], std[1], model=model)
            # ll_t1w_sndd = chi_ll(t1wom, t1wpm_snd, dof[2], std[2], model=model)
            # print(f"log likeihood MT contrast with {second_model} model: {ll_mtw_sndd}")
            # print(f"log likeihood PD contrast with {second_model} model: {ll_pdw_sndd}")
            # print(f"log likeihood T1 contrast with {second_model} model: {ll_t1w_sndd}")
