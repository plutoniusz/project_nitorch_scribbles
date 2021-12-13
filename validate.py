import os
from nitorch.io import savef
import nitorch.tools.qmri.io as qio
import torch
from nitorch.tools.qmri.param import ParameterMap
from nitorch.core.math import besseli_ratio, besseli

def chi_ll(dat, pred, dof, std, chi=True):
    #std = std.sqrt()
    if chi:
        msk = torch.isfinite(pred) & torch.isfinite(dat) & (dat > 0) & (pred > 0)
        tiny = torch.tensor(1e-32)
        dat[~msk] = 0
        pred[~msk] = 0
    else:
        msk = torch.isfinite(pred) & torch.isfinite(dat) & (dat > 0) 
        dat[~msk] = 0
        pred[~msk] = 0


    if chi:
        z = (dat[msk]*pred[msk]*std).clamp_min_(tiny)
        critn = ((dof/2.-1.) * pred[msk].log()
                - (dof/2.) * dat[msk].log()
                + 0.5 * std * (pred[msk].square() + dat[msk].square())
                - besseli(dof/2.-1., z, 'log'))
        crit = torch.sum(critn, dtype=torch.double)

        z = besseli_ratio(dof/2.-1., z, N=2, K=4)
        res = torch.zeros(dat.shape) # unsure
        res[msk] = z.mul_(dat[msk]).neg_().add_(pred[msk])     
        del z       
    else:
        # gaussian log-likelihood
        res = dat.neg_().add_(pred)
        crit = 0.5 * dof * res.square().sum(dtype=torch.double)
    
    return crit

cwd = os.getcwd()
save_folder = 'chi_results_leftout'

# read predicted image
pth_pred = os.path.join(cwd, save_folder)
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
pth_mask = os.path.join(cwd, save_folder)
mtw_masks = []
pdw_masks = []
t1w_masks = []
for filename in os.listdir(str(pth_mask)):
    if filename.endswith("mask.nii") and filename.startswith("mtw"):
        mtw_masks.append(str(os.path.join(pth_mask, filename)))
    elif filename.endswith("mask.nii") and filename.startswith("pdw"):
        pdw_masks.append(str(os.path.join(pth_mask, filename)))
    elif filename.endswith("mask.nii") and filename.startswith("t1w"):
        t1w_masks.append(str(os.path.join(pth_mask, filename)))
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
    mtwm = qio.GradientEchoSingle(mtw_masks[echo])
    pdwm = qio.GradientEchoSingle(pdw_masks[echo])
    t1wm = qio.GradientEchoSingle(t1w_masks[echo])

    # multiply mask by predicted image
    mtwp = mtwp.fdata()*mtwm.fdata()
    pdwp = pdwp.fdata()*pdwm.fdata()
    t1wp = t1wp.fdata()*t1wm.fdata()

    # multiply mask by observed image
    mtwo = mtwo.fdata()*mtwm.fdata()
    pdwo = pdwo.fdata()*pdwm.fdata()
    t1wo = t1wo.fdata()*t1wm.fdata()

    print(mtwm.fdata())
    print(pdwm.fdata())
    print(t1wm.fdata())

    # read noise parameters
    dof = [11, 12, 14]
    std = [20, 17, 36]
    print(std)
    print(dof)


    # caluclate chi lof likelihood for each contrast
    ll_mtw = chi_ll(mtwo, mtwp, dof[0], std[0], chi=True)/mtwm.fdata().sum()
    ll_pdw = chi_ll(pdwo, pdwp, dof[1], std[1], chi=True)/pdwm.fdata().sum()
    ll_t1w = chi_ll(t1wo, t1wp, dof[2], std[2], chi=True)/t1wm.fdata().sum()

    print(ll_mtw)
    print(ll_pdw)
    print(ll_t1w)
    