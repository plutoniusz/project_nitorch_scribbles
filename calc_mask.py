import os
import nitorch.tools.qmri.io as qio
from nitorch.io import savef
import torch

# caluclate brain mask


cwd = os.getcwd()
save_folder = 'chi_results_leftout'

pth_mask = os.path.join(cwd, save_folder)
mtw_masks_gm = []
pdw_masks_gm = []
t1w_masks_gm = []
mtw_masks_wm = []
pdw_masks_wm = []
t1w_masks_wm = []
for filename in os.listdir(str(pth_mask)):
    if filename.endswith(".nii") and filename.startswith("c1flash_mtw"):
        mtw_masks_gm.append(str(os.path.join(pth_mask, filename)))
    elif filename.endswith(".nii") and filename.startswith("c1flash_pdw"):
        pdw_masks_gm.append(str(os.path.join(pth_mask, filename)))
    elif filename.endswith(".nii") and filename.startswith("c1flash_t1w"):
        t1w_masks_gm.append(str(os.path.join(pth_mask, filename)))
    elif filename.endswith(".nii") and filename.startswith("c2flash_mtw"):
        mtw_masks_wm.append(str(os.path.join(pth_mask, filename)))
    elif filename.endswith(".nii") and filename.startswith("c2flash_pdw"):
        pdw_masks_wm.append(str(os.path.join(pth_mask, filename)))
    elif filename.endswith(".nii") and filename.startswith("c2flash_t1w"):
        t1w_masks_wm.append(str(os.path.join(pth_mask, filename)))
    else:
        continue

# read to gradient echo multi
mtw_masks_gm = qio.GradientEchoMulti.from_fnames(mtw_masks_gm, mt=True)
pdw_masks_gm = qio.GradientEchoMulti.from_fnames(pdw_masks_gm)
t1w_masks_gm = qio.GradientEchoMulti.from_fnames(t1w_masks_gm)
mtw_masks_wm = qio.GradientEchoMulti.from_fnames(mtw_masks_wm, mt=True)
pdw_masks_wm = qio.GradientEchoMulti.from_fnames(pdw_masks_wm)
t1w_masks_wm = qio.GradientEchoMulti.from_fnames(t1w_masks_wm)

mtw_masks = []
pdw_masks = []
t1w_masks = []
# add and treshold
for echo in [0,1,2,3,4,5]:

    
    mtw_masks.append(mtw_masks_gm[echo].fdata() + mtw_masks_wm[echo].fdata())
    pdw_masks.append(pdw_masks_gm[echo].fdata() + pdw_masks_wm[echo].fdata())
    t1w_masks.append(t1w_masks_gm[echo].fdata() + t1w_masks_wm[echo].fdata())

    savef(mtw_masks[echo], os.path.join(cwd, save_folder+'/mtw'+str(echo)+'_mask.nii'), affine= mtw_masks[echo].affine)
    savef(pdw_masks[echo], os.path.join(cwd, save_folder+'/pdw'+str(echo)+'_mask.nii'), affine= pdw_masks[echo].affine)
    savef(t1w_masks[echo], os.path.join(cwd, save_folder+'/t1w'+str(echo)+'_mask.nii'), affine= t1w_masks[echo].affine)