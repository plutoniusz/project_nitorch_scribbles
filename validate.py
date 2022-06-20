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

def chi_ll(dat, pred, dof, var, model='chi', contrast = "mt", ll_save = False):
    """
    Calculate the log likelihood of the observation given predicted echo

    """
    rec_var = 1/var
    msk_check = torch.isfinite(pred) & torch.isfinite(dat) & (dat > 0) & (pred > 0)
    dat[~msk_check] = 0
    pred[~msk_check] = 0

    if model == 'chi':
        if ll_save:
            s = dat.size()
            z = torch.zeros(s, dtype=torch.double)
            ll = torch.zeros(s, dtype=torch.double)
            z[msk_check] = (dat[msk_check]*pred[msk_check]*rec_var)
            ll[msk_check] = ((1.-dof/2.) * (pred[msk_check].log())
                + (dof/2.) *(dat[msk_check].log())
                - 0.5 * rec_var * (pred[msk_check].square() + dat[msk_check].square())
                + besseli(dof/2.-1., z[msk_check], 'log')
                - log(var))
            savef(-ll, os.path.join(cwd, save_folder+'/masked/ll_chi'+str(echo)+ contrast + '.nii'), affine = mtwp.affine)
        else:
            z = (dat[msk_check]*pred[msk_check]*rec_var)
            ll = ((1.-dof/2.) * (pred[msk_check].log())
                    + (dof/2.) *(dat[msk_check].log())
                    - 0.5 * rec_var * (pred[msk_check].square() + dat[msk_check].square())
                    + besseli(dof/2.-1., z, 'log')
                    - log(var))
    elif model =='rice':
        ll = (dat[msk_check]).log() - var.log() - (dat[msk_check].square() + pred[msk_check].square()) / (2 * var)
        ll = ll + besseli(0, dat[msk_check] * (pred[msk_check]/ var), 'log')
    else :
        # gaussian log-likelihood
        if ll_save:
            s = dat.size()
            res = torch.zeros(s, dtype=torch.double)
            ll = torch.zeros(s, dtype=torch.double)
            res[msk_check] = pred[msk_check].neg_().add_(dat[msk_check])
            ll[msk_check] = - (0.5 * rec_var * res[msk_check].square() + 0.5*log(2.*pi*var))
            savef(-ll, os.path.join(cwd, save_folder+'/masked/ll_gauss'+str(echo)+ contrast + '.nii'), affine = mtwp.affine)
        else:
            res = pred[msk_check].neg_().add_(dat[msk_check])
            ll = - (0.5 * rec_var * res.square() + 0.5*log(2.*pi*var))
    ll = torch.sum(ll, dtype=torch.double) 
    return ll

#######################################
#######################################

ll_save = True
mask_im = False
mask_save = True
models = ["chi", "gauss"]
echos = [0,1,2,3,4,5]
#echos = [0,1]
# estimation date
datime_list = ['2022-06-13_20-17-27']
# validation date
datime_val =  datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
# dataset choice
datasets = ['mpm',] #'mpm'/ 'cl'/ 'mc'

if datasets == ['cl']:
    cl_list = ['112111', '115326', '116284', '128221', '130519', '133749', '170192', '176117',
                '208010', '210022', '211787', '214685', '232237', '242234', '260478', '307789', '308597',
                '324038', '330406', '346878']
    datasets = cl_list[1,3,5] # chosing cl dataset indexes from the list
    cl = True
else:
    cl = False

cwd = os.getcwd()
for index, datime in enumerate(datime_list):
    if cl:
        dataset = datasets[index]
    else:
        dataset = datasets[0]

    # read observed image
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

    for model in models:
        save_folder = 'qmri_results/' + model + '_results_leftout_'+ datime
        # read predicted image
        predicted_folder = 'predicted'
        pth_pred = os.path.join(cwd, save_folder, predicted_folder)
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
        if model == "chi":
            pth_pred_chi = pth_pred
        if model == "gauss":
            pth_pred_gauss = pth_pred
        
        #read noise and dof
        if model == "chi":
            dof_chi = []
            noise_chi = []
            noise_txt = "noise_" + datime + ".txt"
            if not os.path.exists(os.path.join(save_folder,  noise_txt)):
                noise_txt = 'noise_' + dataset + '_' + datime + '.txt'
            with open(os.path.join(save_folder,  noise_txt)) as f:
                lines = f.readlines()
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
            # read the brain mask
            if mask_im:
                mask_folder = 'mask'
                if dataset == "mc":
                    pth_mask = os.path.join(cwd, '4John_Klara/derivative')
                if dataset == "mpm":
                    pth_mask = os.path.join(cwd, save_folder, mask_folder)
                    pth_mask = os.path.join(cwd, "MPM")
                elif cl:
                    gen_path = "/data/underworld/kbas/03_data/derivatives/"
                    path_mask = os.path.join(gen_path, dataset)
                    path_pom = os.listdir(path_mask)
                    path_pom = [d for d in path_pom if os.path.isdir(os.path.join(path_mask, d))]
                    path_mask = os.path.join(path_mask, path_pom[0])
                    #pth_mask = os.path.join(path_mask, "dwi/qmap-preproc-dwimask")
                    pth_mask = os.path.join(path_mask, "anat/spm-qmap-preproc")
                for filename in os.listdir(str(pth_mask)):
                    if filename.endswith("brain_mask.nii"):
                        mask = (str(os.path.join(pth_mask, filename)))
                    else:
                        continue
    
    for echo in echos:
        for model in models:
            save_folder = 'qmri_results/' + model + '_results_leftout_'+ datime
            if model == 'chi':
                path_pred = pth_pred_chi
            if model == "gauss":
                path_pred = pth_pred_gauss

            # read predicted image
            mtwp = qio.GradientEchoMulti(mtw_pred[echo])
            pdwp = qio.GradientEchoMulti(pdw_pred[echo])
            t1wp = qio.GradientEchoMulti(t1w_pred[echo])

            # read observed image
            mtwo = qio.GradientEchoMulti(fmtw[echo])
            pdwo = qio.GradientEchoMulti(fpdw[echo])
            t1wo = qio.GradientEchoMulti(ft1w[echo])

            if mask_im:
                # read the brain mask
                brain_mask = qio.GradientEchoSingle(mask)
                brain_mask_affine =brain_mask.affine
                brain_mask = brain_mask.fdata(dtype=torch.double)
                msk = torch.isfinite(brain_mask)
                size_mask= torch.sum(msk)

                mat = lmdiv(brain_mask_affine, mtwp.affine)
                grid = smart_grid(mat, mtwp.shape, brain_mask.shape)
                brain_mask_mtp = smart_pull(brain_mask, grid)
                brain_mask_mtp = torch.ceil(brain_mask_mtp)

                mat = lmdiv(brain_mask_affine, pdwp.affine)
                grid = smart_grid(mat, pdwp.shape, brain_mask.shape)
                brain_mask_pdp = smart_pull(brain_mask, grid)
                brain_mask_pdp = torch.ceil(brain_mask_pdp)

                mat = lmdiv(brain_mask_affine, t1wp.affine)
                grid = smart_grid(mat, t1wp.shape, brain_mask.shape)
                brain_mask_t1p = smart_pull(brain_mask, grid)
                brain_mask_t1p = torch.ceil(brain_mask_t1p)

                savef(brain_mask_mtp, os.path.join(cwd, save_folder+'/mask_processed_mtp.nii'), affine = brain_mask_affine)
                savef(brain_mask_pdp, os.path.join(cwd, save_folder+'/mask_processed_pdp.nii'), affine = brain_mask_affine)
                savef(brain_mask_t1p, os.path.join(cwd, save_folder+'/mask_processed_t1p.nii'), affine = brain_mask_affine)

                # multiply mask by predicted image
                mtwpm = mtwp.fdata()*brain_mask_mtp
                pdwpm = pdwp.fdata()*brain_mask_pdp
                t1wpm = t1wp.fdata()*brain_mask_t1p
            else:
                mtwpm = mtwp.fdata(dtype=torch.double)
                pdwpm = pdwp.fdata(dtype=torch.double)
                t1wpm = t1wp.fdata(dtype=torch.double)

            # save masked predicted images
            pm_path = Path(save_folder + '/masked').mkdir(parents=True, exist_ok=True)
            if mask_save:
                savef(mtwpm, os.path.join(cwd, save_folder+'/masked/mtwp'+str(echo)+'.nii'), affine = mtwp.affine)
                savef(pdwpm, os.path.join(cwd, save_folder+'/masked/pdwp'+str(echo)+'.nii'), affine = pdwp.affine)
                savef(t1wpm, os.path.join(cwd, save_folder+'/masked/t1wp'+str(echo)+'.nii'), affine = t1wp.affine)

            # mask observed images, same for gauss and chi
            if model =="chi":
                if mask_im:
                    mat = lmdiv(brain_mask_affine, mtwo.affine)
                    grid = smart_grid(mat, mtwo.shape, brain_mask.shape)
                    brain_mask_mt = smart_pull(brain_mask, grid)
                    brain_mask_mt = torch.ceil(brain_mask_mt)
                    savef(brain_mask_mt, os.path.join(cwd, save_folder+'/mask_processed_mt.nii'), affine = brain_mask_affine)

                    mat = lmdiv(brain_mask_affine, pdwo.affine)
                    grid = smart_grid(mat, pdwo.shape, brain_mask.shape)
                    brain_mask_pd = smart_pull(brain_mask, grid)
                    brain_mask_pd = torch.ceil(brain_mask_pd)
                    savef(brain_mask_pd, os.path.join(cwd, save_folder+'/mask_processed_pd.nii'), affine = brain_mask_affine)

                    mat = lmdiv(brain_mask_affine, t1wo.affine)
                    grid = smart_grid(mat, t1wo.shape, brain_mask.shape)
                    brain_mask_t1 = smart_pull(brain_mask, grid)
                    brain_mask_t1 = torch.ceil(brain_mask_t1)
                    savef(brain_mask_t1, os.path.join(cwd, save_folder+'/mask_processed_t1.nii'), affine = brain_mask_affine)

                    # multiply mask by observed image
                    mtwom = mtwo.fdata()*brain_mask_mt
                    pdwom = pdwo.fdata()*brain_mask_pd
                    t1wom = t1wo.fdata()*brain_mask_t1

                    if mask_save:
                        # save masked observed images
                        savef(mtwom, os.path.join(cwd, save_folder+'/masked/mtwo'+str(echo)+'.nii'), affine = mtwo.affine)
                        savef(pdwom, os.path.join(cwd, save_folder+'/masked/pdwo'+str(echo)+'.nii'), affine = pdwo.affine)
                        savef(t1wom, os.path.join(cwd, save_folder+'/masked/t1wo'+str(echo)+'.nii'), affine = t1wo.affine)
                else:
                    mtwom = mtwo.fdata(dtype=torch.double)
                    pdwom = pdwo.fdata(dtype=torch.double)
                    t1wom = t1wo.fdata(dtype=torch.double)

            dof = dof_chi[echo]
            var = noise_chi[echo]
            print(var)
            print(dof)
            ll_mtw = chi_ll(mtwom, mtwpm, float(dof[0]), float(var[0]), model=model, contrast = "mt")
            ll_pdw = chi_ll(pdwom, pdwpm, float(dof[1]), float(var[1]), model=model, contrast = "pd")
            ll_t1w = chi_ll(t1wom, t1wpm, float(dof[2]), float(var[2]), model=model, contrast = "t1")

            # save likelihood values to the file
            like_text = f"log likeihood MT contrast with {model} model: {ll_mtw}\nlog likeihood PD contrast with {model} model: {ll_pdw}\nlog likeihood T1 contrast with {model} model: {ll_t1w}\n"
            with open(save_folder + '/likelihoods_' + datime + "_" + datime_val + '.txt', 'a') as f:
                f.write(like_text)