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


def chi_ll(dat, pred, dof, var, model='chi', msk_calc = False, ll_save = False, contrast = False, affine = False):
    """
    Calculate the log likelihood of the observation given predicted echo

    """
    rec_var = 1./var

    if model == 'chi':
        if ll_save:
            s = dat.size()
            z = torch.zeros(s, dtype=torch.double)
            ll = torch.zeros(s, dtype=torch.double)
            z[msk_calc] = (dat[msk_calc]*pred[msk_calc]*rec_var)
            ll[msk_calc] = ((1.-dof/2.) * (pred[msk_calc].log())
                + (dof/2.) *(dat[msk_calc].log())
                - 0.5 * rec_var * (pred[msk_calc].square() + dat[msk_calc].square())
                + besseli(dof/2.-1., z[msk_calc], 'log')
                - log(var))
            savef(ll, os.path.join(cwd, save_folder+'/masked/ll_chi'+str(echo)+ contrast + '.nii'), affine = affine)
        else:
            z = (dat[msk_calc]*pred[msk_calc]*rec_var)
            ll = ((1.-dof/2.) * (pred[msk_calc].log())
                    + (dof/2.) *(dat[msk_calc].log())
                    - 0.5 * rec_var * (pred[msk_calc].square() + dat[msk_calc].square())
                    + besseli(dof/2.-1., z, 'log')
                    - log(var))
    elif model =='rice':
        ll = (dat[msk_calc]).log() - var.log() - (dat[msk_calc].square() + pred[msk_calc].square()) / (2 * var)
        ll = ll + besseli(0, dat[msk_calc] * (pred[msk_calc]/ var), 'log')
    else :
        # gaussian log-likelihood
        if ll_save:
            s = dat.size()
            res = torch.zeros(s, dtype=torch.double)
            ll = torch.zeros(s, dtype=torch.double)
            res[msk_calc] = pred[msk_calc].neg_().add_(dat[msk_calc])
            ll[msk_calc] = - (0.5 * rec_var * res[msk_calc].square() + 0.5*log(2.*pi*var))
            savef(ll, os.path.join(cwd, save_folder+'/masked/ll_gauss'+str(echo)+ contrast + '.nii'), affine = affine)
        else:
            res = pred[msk_calc].neg_().add_(dat[msk_calc])
            ll = - (0.5 * rec_var * res.square() + 0.5*log(2.*pi*var))
    ll = torch.sum(ll, dtype=torch.double) 
    return ll

##########################
##########################

ll_save = True
mask_im = True
mask_save = True
models = ["chi", "gauss"]
contrasts = ["mt", "pd", "t1"]
echos = [0,1,2,3,4,5]
echos = [0]
# estimation date
datime_list = ['2022-06-24_01-07-15']
# validation date
datime_val =  datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
# dataset choice
datasets = ['mpm',] #'mpm'/ 'cl'/ 'mc'
cwd = os.getcwd()


if datasets == ['cl']:
    cl_list = ['112111', '115326', '116284', '128221', '130519', '133749', '170192', '176117',
                '208010', '210022', '211787', '214685', '232237', '242234', '260478', '307789', '308597',
                '324038', '330406', '346878']
    datasets = cl_list[1,3,5] # chosing cl dataset indexes from the list
    cl = True
else:
    cl = False

for index, datime in enumerate(datime_list):
    # datasets path
    if cl:
        dataset = datasets[index]
    else:
        dataset = datasets[0]

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

    # read noise estimates
    dof = []
    var = []
    noise_txt = 'noise_' + dataset + '_' + datime + '.txt'
    with open(os.path.join('qmri_results/chi_results_leftout_'+ datime,  noise_txt)) as f:
        lines = f.readlines()
    for i in range(len(echos)):
        line = lines[i]
        line = line.replace('[', "")
        line = line.replace(']', "")
        line = line.replace(',', "")
        split_line = line.split()
        line = re.findall(r'[+-]?[0-9]+\.?[0-9]*', line)
        var.append(line[1:4])
        dof.append(line[4:])

    # read the brain mask
    if mask_im:
        mask_folder = 'mask'
        if dataset == "mc":
            pth_mask = os.path.join(cwd, '4John_Klara/derivative')
        if dataset == "mpm":
            pth_mask = os.path.join(cwd, 'qmri_results/chi_results_leftout_'+ datime, mask_folder)
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


    for contrast_number,contrast in enumerate(contrasts):
        # read observed images
        obs = []
        for filename in os.listdir(str(pth_mris[contrast_number])):
            if filename.endswith(".nii"):
                obs.append(str(os.path.join(pth_mris[contrast_number], filename)))
            else:
                continue

        for model in models:
            # folder with relevant images for the model
            save_folder = 'qmri_results/' + model + '_results_leftout_'+ datime

            # read predicted images
            predicted_folder = 'predicted'
            pth_pred = os.path.join(cwd, save_folder, predicted_folder)
            pred = []
            for filename in os.listdir(str(pth_pred)):
                if filename.endswith(".nii") and filename.startswith("flash_" + contrast):
                    pred.append(str(os.path.join(pth_pred, filename)))
                else:
                    continue
            if mask_im:
                # read the brain mask
                brain_mask = qio.GradientEchoSingle(mask)
                brain_mask_affine =brain_mask.affine
                brain_mask = brain_mask.fdata(dtype=torch.double)
                brain_mask = torch.where(brain_mask > 0.5, torch.tensor(1., dtype=torch.double), torch.tensor(0., dtype=torch.double))
                if mask_save:
                    savef(brain_mask, os.path.join(cwd, save_folder+'/mask_processed.nii'), affine = brain_mask_affine)

            for echo in echos:
                # read observed image
                observed = qio.GradientEchoMulti(obs[echo])
                # read predicted image
                predicted = qio.GradientEchoMulti(pred[echo])

                observed_affine = observed.affine
                if mask_im:
                    # resample mask on observed image
                    mat = lmdiv(brain_mask_affine, observed.affine)
                    grid = smart_grid(mat, observed.shape, brain_mask.shape)
                    brain_mask_obs = smart_pull(brain_mask, grid)
                    brain_mask_obs = torch.where(brain_mask_obs > 0.5, torch.tensor(1., dtype=torch.double), torch.tensor(0., dtype=torch.double))                

                    observed = observed.fdata(dtype=torch.double)*brain_mask_obs

                    # resample mask on predicted image
                    mat = lmdiv(brain_mask_affine, predicted.affine)
                    grid = smart_grid(mat, predicted.shape, brain_mask.shape)
                    brain_mask_pred = smart_pull(brain_mask, grid)
                    brain_mask_pred = torch.where(brain_mask_pred > 0.5, torch.tensor(1., dtype=torch.double), torch.tensor(0., dtype=torch.double))                

                    predicted_affine = predicted.affine
                    predicted = predicted.fdata(dtype=torch.double)*brain_mask_pred

                    if mask_save:
                        savef(brain_mask_obs, os.path.join(cwd, save_folder+'/mask_processed_' +  contrast + '_obs.nii'), affine = brain_mask_affine)
                        savef(brain_mask_pred, os.path.join(cwd, save_folder+'/mask_processed_' +  contrast + '_pred.nii'), affine = brain_mask_affine)
                        savef(observed, os.path.join(cwd, save_folder+'/masked/' + contrast + "_obs_mask" +str(echo)+'.nii'), affine = observed_affine)
                        savef(predicted, os.path.join(cwd, save_folder+'/masked/' + contrast + "_pred_mask" +str(echo)+'.nii'), affine = predicted_affine)
                else:
                    observed = observed.fdata(dtype=torch.double)
                    predicted = predicted.fdata(dtype=torch.double)

                if model=="chi":
                    tiny = torch.tensor(1e-32, dtype=torch.double)
                    msk_calc = torch.isfinite(observed) & torch.isfinite(predicted) & (observed > tiny) & (predicted > tiny)
                    observed[~msk_calc] = 0.
                    predicted[~msk_calc] = 0.
                # folder for saving log-likelihood maps
                pm_path = Path(save_folder + '/masked').mkdir(parents=True, exist_ok=True)
                ll = chi_ll(observed, predicted, float(dof[echo][contrast_number]), float(var[echo][contrast_number]), model=model, msk_calc = msk_calc, ll_save = ll_save, contrast = contrast, affine = observed_affine)

                # save likelihood values to the file
                like_text = f"log likeihood {contrast} contrast with {model} model: {ll}\n"
                with open(save_folder + '/likelihoods_' + datime + "_" + datime_val + '.txt', 'a') as f:
                    f.write(like_text)