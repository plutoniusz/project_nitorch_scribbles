from math import log
import os
from nitorch.io import savef
import nitorch.tools.qmri.io as qio
import torch
from nitorch.core.math import besseli
from nitorch.core.constants import pi
from nitorch.core.linalg import lmdiv
from nitorch.tools.qmri.relax.utils import smart_grid, smart_pull

def chi_ll(dat, pred, dof, std, model='chi'):
    """
    Calculate the log lokelihood of the observation given predicted echo

    """
    var = std**std
    rec_var = 1/var
    if model == 'chi':
        msk = torch.isfinite(pred) & torch.isfinite(dat) & (dat > 0) & (pred > 0)
        tiny = torch.tensor(1e-32)
        dat[~msk] = 0
        pred[~msk] = 0
    elif model == 'rice':
        msk = torch.isfinite(pred) & torch.isfinite(dat) & (dat > 0) & (pred > 0)
        dat[~msk] = 0
        pred[~msk] = 0
    else :
        # gaussian log-likelihood
        msk = torch.isfinite(pred) & torch.isfinite(dat) & (dat > 0) 
        dat[~msk] = 0
        pred[~msk] = 0

    if model == 'chi':
        z = (dat[msk]*pred[msk]*rec_var).clamp_min_(tiny)
        ll = ((1.-dof/2.) * pred[msk].log()
                + (dof/2.) * dat[msk].log()
                - 0.5 * rec_var * (pred[msk].square() + dat[msk].square())
                + besseli(dof/2.-1., z, 'log')
                - log(var))
        ll = torch.sum(ll, dtype=torch.double) 
    elif model =='rice':
        ll = (dat[msk] + tiny).log() - var.log() - (dat.square() + pred.square()) / (2 * var)
        ll = ll + besseli(0, dat * (pred/ var), 'log')
        ll = torch.sum(ll, dtype=torch.double)
    else :
        # gaussian log-likelihood
        res = dat.neg_().add_(pred)
        ll = (0.5 * rec_var * res.square() - 0.5*log(2.*pi*var))
        ll = torch.sum(ll, dtype=torch.double)
    return ll

# second model for comparison
second_model = 'gauss'
#echos = [0,1,2,3,4,5]
echos = [0]


# need to extract noise parameters from the maps

# # echo 5
# std = [20.68, 24.95, 17.87]
# dof = [14.65, 11.28, 18.47]

# echo 2
std = [20.74, 24.98, 17.95]
dof = [14.57, 11.27, 18.35]

cwd = os.getcwd()
# parameter estimation model
model = 'chi'
save_folder = model + '_results_leftout'

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
pth_mask = os.path.join(cwd, save_folder, mask_folder)
masks = []
for filename in os.listdir(str(pth_mask)):
    if filename.endswith("mask.nii"):
        masks.append(str(os.path.join(pth_mask, filename)))
    else:
        continue

# second model for comparison
if second_model:
    save_folder = second_model + '_results_leftout'

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

if second_model:
    save_folder = second_model + '_gauss' + '_results_leftout'

    # read predicted image
    predicted = 'predicted'
    pth_pred_sndg = os.path.join(cwd, save_folder, predicted)
    mtw_pred_sndg = []
    pdw_pred_sndg = []
    t1w_pred_sndg = []
    for filename in os.listdir(str(pth_pred_sndg)):
        if filename.endswith(".nii") and filename.startswith("flash_mtw"):
            mtw_pred_sndg.append(str(os.path.join(pth_pred_sndg, filename)))
        elif filename.endswith(".nii") and filename.startswith("flash_pdw"):
            pdw_pred_sndg.append(str(os.path.join(pth_pred_sndg, filename)))
        elif filename.endswith(".nii") and filename.startswith("flash_t1w"):
            t1w_pred_sndg.append(str(os.path.join(pth_pred_sndg, filename)))
        else:
            continue

for echo in echos:

    save_folder = model + '_results_leftout'
    print(save_folder)

    # read predicted image
    mtwp = qio.GradientEchoMulti(mtw_pred[echo])
    pdwp = qio.GradientEchoMulti(pdw_pred[echo])
    t1wp = qio.GradientEchoMulti(t1w_pred[echo])

    # read observed image
    mtwo = qio.GradientEchoMulti(fmtw[echo])
    pdwo = qio.GradientEchoMulti(fpdw[echo])
    t1wo = qio.GradientEchoMulti(ft1w[echo])

    # read the brain mask
    brain_mask = qio.GradientEchoSingle(masks[echo])
    brain_mask_affine =brain_mask.affine
    brain_mask = brain_mask.fdata(dtype=torch.double)
    msk = torch.isfinite(brain_mask)
    brain_mask[~msk] = 0.
    mat = lmdiv(brain_mask_affine, mtwo.affine)
    grid = smart_grid(mat, mtwo.shape, brain_mask.shape)
    brain_mask = smart_pull(brain_mask, grid)[0]
    print("brain mask calculated")

    # multiply mask by predicted image
    mtwpm = mtwp.fdata()*brain_mask
    pdwpm = pdwp.fdata()*brain_mask
    t1wpm = t1wp.fdata()*brain_mask

    # not needed really
    # savef(mtwpm, os.path.join(cwd, save_folder+'/masked/mtwp'+str(echo)+'.nii'), affine = mtwp.affine)
    # savef(pdwpm, os.path.join(cwd, save_folder+'/masked/pdwp'+str(echo)+'.nii'), affine = pdwp.affine)
    # savef(t1wpm, os.path.join(cwd, save_folder+'/masked/t1wp'+str(echo)+'.nii'), affine = t1wp.affine)

    # multiply mask by observed image
    mtwom = mtwo.fdata()*brain_mask
    pdwom = pdwo.fdata()*brain_mask
    t1wom = t1wo.fdata()*brain_mask

    # also not needed
    # savef(mtwom, os.path.join(cwd, save_folder+'/masked/mtwo'+str(echo)+'.nii'), affine = mtwo.affine)
    # savef(pdwom, os.path.join(cwd, save_folder+'/masked/pdwo'+str(echo)+'.nii'), affine = pdwo.affine)
    # savef(t1wom, os.path.join(cwd, save_folder+'/masked/t1wo'+str(echo)+'.nii'), affine = t1wo.affine)


    #brain_mask_size = brain_mask.sum()
    # caluclate chi lof likelihood for each contrast
    ll_mtw = chi_ll(mtwom, mtwpm, dof[0], std[0], model=model)
    ll_pdw = chi_ll(pdwom, pdwpm, dof[1], std[1], model=model)
    ll_t1w = chi_ll(t1wom, t1wpm, dof[2], std[2], model=model)

    print(f"log likeihood MT contrast with {model} model: {ll_mtw}")
    print(f"log likeihood PD contrast with {model} model: {ll_pdw}")
    print(f"log likeihood T1 contrast with {model} model: {ll_t1w}")
    

    # second model for comparison
    if second_model:

        save_folder = second_model + '_results_leftout'
        print(save_folder)
        # read predicted image
        mtwp_snd = qio.GradientEchoMulti(mtw_pred_snd[echo])
        pdwp_snd = qio.GradientEchoMulti(pdw_pred_snd[echo])
        t1wp_snd = qio.GradientEchoMulti(t1w_pred_snd[echo])

        # multiply mask by predicted image
        mtwpm_snd = mtwp_snd.fdata()*brain_mask
        pdwpm_snd = pdwp_snd.fdata()*brain_mask
        t1wpm_snd = t1wp_snd.fdata()*brain_mask

        # # not needed really
        # savef(mtwpm_snd, os.path.join(cwd, save_folder+'/masked/mtwp'+str(echo)+'.nii'), affine = mtwp_snd.affine)
        # savef(pdwpm_snd, os.path.join(cwd, save_folder+'/masked/pdwp'+str(echo)+'.nii'), affine = pdwp_snd.affine)
        # savef(t1wpm_snd, os.path.join(cwd, save_folder+'/masked/t1wp'+str(echo)+'.nii'), affine = t1wp_snd.affine)

        # caluclate chi lof likelihood for each contrast
        ll_mtw_snd = chi_ll(mtwom, mtwpm_snd, dof[0], std[0], model=second_model)
        ll_pdw_snd = chi_ll(pdwom, pdwpm_snd, dof[1], std[1], model=second_model)

        ll_t1w_snd = chi_ll(t1wom, t1wpm_snd, dof[2], std[2], model=second_model)
        print(f"log likeihood MT contrast with {second_model} model: {ll_mtw_snd}")
        print(f"log likeihood PD contrast with {second_model} model: {ll_pdw_snd}")
        print(f"log likeihood T1 contrast with {second_model} model: {ll_t1w_snd}")
     
        # print("chi log likelihood")
        # # caluclate chi lof likelihood for each contrast
        # ll_mtw_sndd = chi_ll(mtwom, mtwpm_snd, dof[0], std[0], model=model)
        # ll_pdw_sndd = chi_ll(pdwom, pdwpm_snd, dof[1], std[1], model=model)
        # ll_t1w_sndd = chi_ll(t1wom, t1wpm_snd, dof[2], std[2], model=model)

        # print(f"log likeihood MT contrast with {second_model} model: {ll_mtw_sndd}")
        # print(f"log likeihood PD contrast with {second_model} model: {ll_pdw_sndd}")
        # print(f"log likeihood T1 contrast with {second_model} model: {ll_t1w_sndd}")

     # second model for comparison
    if second_model:
        
        save_folder = second_model + '_gauss' + '_results_leftout'
        print(save_folder)
        # read predicted image
        mtwp_sndg = qio.GradientEchoMulti(mtw_pred_sndg[echo])
        pdwp_sndg = qio.GradientEchoMulti(pdw_pred_sndg[echo])
        t1wp_sndg = qio.GradientEchoMulti(t1w_pred_sndg[echo])

        # multiply mask by predicted image
        mtwpm_sndg = mtwp_sndg.fdata()*brain_mask
        pdwpm_sndg = pdwp_sndg.fdata()*brain_mask
        t1wpm_sndg = t1wp_sndg.fdata()*brain_mask

        # not needed really
        # savef(mtwpm_sndg, os.path.join(cwd, save_folder+'/masked/mtwp'+str(echo)+'.nii'), affine = mtwp_sndg.affine)
        # savef(pdwpm_sndg, os.path.join(cwd, save_folder+'/masked/pdwp'+str(echo)+'.nii'), affine = pdwp_sndg.affine)
        #savef(t1wpm_sndg, os.path.join(cwd, save_folder+'/masked/t1wp'+str(echo)+'.nii'), affine = t1wp_sndg.affine)

        # caluclate chi lof likelihood for each contrast
        ll_mtw_snd = chi_ll(mtwom, mtwpm_snd, dof[0], std[0], model=second_model)
        ll_pdw_snd = chi_ll(pdwom, pdwpm_snd, dof[1], std[1], model=second_model)
        ll_t1w_snd = chi_ll(t1wom, t1wpm_snd, dof[2], std[2], model=second_model)

        print(f"log likeihood MT contrast with {second_model} model: {ll_mtw_snd}")
        print(f"log likeihood PD contrast with {second_model} model: {ll_pdw_snd}")
        print(f"log likeihood T1 contrast with {second_model} model: {ll_t1w_snd}")