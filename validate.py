from math import log
import os
from nitorch.io import savef
import nitorch.tools.qmri.io as qio
import torch
from nitorch.core.math import besseli
from nitorch.core.constants import pi

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
        print(ll.size())
        ll = torch.sum(ll, dtype=torch.double) 
    elif model =='rice':
        ll = (dat[msk] + tiny).log() - var.log() - (dat.square() + pred.square()) / (2 * var)
        ll = ll + besseli(0, dat * (pred/ var), 'log')
        ll = torch.sum(ll, dtype=torch.double)
    else :
        # gaussian log-likelihood
        res = dat.neg_().add_(pred)
        ll = - (0.5 * dof * res.square().sum(dtype=torch.double)
            - 0.5*log(2.*pi*var))
    return ll

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

#echos = [0,1,2,3,4,5]
echos = [0]
for echo in echos:

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
    brain_mask = brain_mask.fdata()
    msk = torch.isfinite(brain_mask)
    brain_mask[~msk] = 0.

    # multiply mask by predicted image
    mtwpm = mtwp.fdata()*brain_mask
    pdwpm = pdwp.fdata()*brain_mask
    t1wpm = t1wp.fdata()*brain_mask

    # not needed really
    savef(mtwpm, os.path.join(cwd, save_folder+'/masked/mtwp'+str(echo)+'.nii'), affine = mtwp.affine)
    savef(pdwpm, os.path.join(cwd, save_folder+'/masked/pdwp'+str(echo)+'.nii'), affine = pdwp.affine)
    savef(t1wpm, os.path.join(cwd, save_folder+'/masked/t1wp'+str(echo)+'.nii'), affine = t1wp.affine)

    # multiply mask by observed image
    mtwom = mtwo.fdata()*brain_mask
    pdwom = pdwo.fdata()*brain_mask
    t1wom = t1wo.fdata()*brain_mask

    # also not needed
    savef(mtwom, os.path.join(cwd, save_folder+'/masked/mtwo'+str(echo)+'.nii'), affine = mtwo.affine)
    savef(pdwom, os.path.join(cwd, save_folder+'/masked/pdwo'+str(echo)+'.nii'), affine = pdwo.affine)
    savef(t1wom, os.path.join(cwd, save_folder+'/masked/t1wo'+str(echo)+'.nii'), affine = t1wo.affine)

    # read noise parameters
    # dof = [11, 12, 14]
    # std = [20, 17, 36]

    # echo 5
    std = [20.68, 24.95, 17.87]
    dof = [14.65, 11.28, 18.47]

    #brain_mask_size = brain_mask.sum()
    # caluclate chi lof likelihood for each contrast
    ll_mtw = chi_ll(mtwom, mtwpm, dof[0], std[0], model=model)
    ll_pdw = chi_ll(pdwom, pdwpm, dof[1], std[1], model=model)
    ll_t1w = chi_ll(t1wom, t1wpm, dof[2], std[2], model=model)

    print(ll_mtw)
    print(ll_pdw)
    print(ll_t1w)
    