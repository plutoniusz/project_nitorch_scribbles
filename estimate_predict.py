import os
import nitorch.tools.qmri.io as qio
from nitorch.tools.qmri.param import ParameterMap
from nitorch.tools.qmri.relax import GREEQOptions
from nitorch.io import savef
from nitorch.tools.qmri.relax import greeq
from nitorch.tools.qmri.relax._mpm._predict import gre

# paths to dataset
print("getting paths to MPM folder")
cwd = os.getcwd()
pth_mris = [os.path.join(cwd, 'MPM/mtw_mfc_3dflash_v1i_R4_0012'),
            os.path.join(cwd, 'MPM/pdw_mfc_3dflash_v1i_R4_0009'),
            os.path.join(cwd, 'MPM/t1w_mfc_3dflash_v1i_R4_0015')]
print("paths to additional maps")
b1p_map = str(os.path.join(cwd, "MPM/pdw_mfc_3dflash_v1i_R4_0009/Results/Supplementary/anon_s2018-02-28_18-26-184837-00001-00001-1_B1map.nii"))
b1p_ref = str(os.path.join(cwd, "MPM/pdw_mfc_3dflash_v1i_R4_0009/Results/Supplementary/anon_s2018-02-28_18-26-184837-00001-00001-1_B1ref.nii"))
mtw_b1m_map = str(os.path.join(cwd, "MPM/pdw_mfc_3dflash_v1i_R4_0009/Results/Supplementary/sensMap_HC_over_BC_division_MT.nii"))
pdw_b1m_map = str(os.path.join(cwd, "MPM/pdw_mfc_3dflash_v1i_R4_0009/Results/Supplementary/sensMap_HC_over_BC_division_PD.nii"))
t1w_b1m_map = str(os.path.join(cwd, "MPM/pdw_mfc_3dflash_v1i_R4_0009/Results/Supplementary/sensMap_HC_over_BC_division_T1.nii"))


echos = [0,1,2,3,4,5]
save_folder = 'gauss_results_leftout'

for echo in echos:
    # preparing path lists of observations    
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
    mtwl = fmtw[echo]
    pdwl = fpdw[echo]
    t1wl = ft1w[echo]
    del fmtw[echo]
    del fpdw[echo]
    del ft1w[echo]

    # reaging the observations and precalculating field maps
    print("reading images from paths using nitorch GradientEchoMulti")
    t1w = qio.GradientEchoMulti.from_fnames(ft1w)
    pdw = qio.GradientEchoMulti.from_fnames(fpdw)
    mtw = qio.GradientEchoMulti.from_fnames(fmtw, mt=True)
    print("precomputind field maps")
    transmit = qio.PrecomputedFieldMap(b1p_map, magnitude=b1p_ref, affine = t1w.affine)
    receive = [qio.PrecomputedFieldMap(pdw_b1m_map,  unit='a.u', affine=pdw.affine),
                qio.PrecomputedFieldMap(t1w_b1m_map, unit='a.u', affine=t1w.affine),
                qio.PrecomputedFieldMap(mtw_b1m_map, unit='a.u', affine=mtw.affine)]

    # options for parameter estimation
    mtw.mt = True
    opt = GREEQOptions()
    opt.recon.space = 1
    opt.backend.device = 'cuda'
    opt.preproc.register = False
    opt.optim.nb_levels = 1
    opt.verbose = 1
    opt.likelihood = 'gauss'
    print("start greeq")
    pd, r1, r2s, mt = greeq([pdw, t1w, mtw], transmit, receive, opt=opt)
    #saving parameter maps
    savef(pd.volume, os.path.join(cwd, save_folder+'/pd'+str(echo)+'.nii'), affine= pd.affine)
    savef(r1.volume, os.path.join(cwd, save_folder+'/r1'+str(echo)+'.nii'), affine= r1.affine)
    savef(r2s.volume, os.path.join(cwd, save_folder+'/r2s'+str(echo)+'.nii'), affine= r2s.affine)
    savef(mt.volume, os.path.join(cwd, save_folder+'/mt'+str(echo)+'.nii'), affine= mt.affine)

    # paths to paramter maps
    cwd = os.getcwd()
    mtp = os.path.join(cwd, save_folder+'/mt'+str(echo)+'.nii')
    pdp = os.path.join(cwd, save_folder+'/pd'+str(echo)+'.nii')
    r1p = os.path.join(cwd, save_folder+'/r1'+str(echo)+'.nii')
    r2sp = os.path.join(cwd, save_folder+'/r2s'+str(echo)+'.nii')
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
    mtwl = qio.GradientEchoSingle(mtwl)
    print(mtwl.te, mtwl.tr, mtwl.fa, mtw.noise, mtw.dof)
    flash = gre(pdp, r1p, r2sp,  mtp,  transmit=transmit, receive=receive[2], te=mtwl.te, tr=mtwl.tr, fa=mtwl.fa, mtpulse=True, affine=mtw.affine, shape=pdp.shape)
    text = save_folder+'/flash_mtw'+str(echo)+'.nii'
    savef(flash.volume, os.path.join(cwd, text), affine=flash.affine)

    pdwl = qio.GradientEchoSingle(pdwl)
    print(pdwl.te, mtwl.tr, pdwl.fa, pdw.noise, pdw.dof)
    flash = gre(pdp, r1p, r2sp,  mtp,  transmit=transmit, receive=receive[0], te=pdwl.te, tr=pdwl.tr, fa=pdwl.fa, mtpulse=False, affine=pdp.affine, shape=pdp.shape)
    text = save_folder+'/flash_pdw'+str(echo)+'.nii'
    savef(flash.volume, os.path.join(cwd, text), affine=flash.affine)

    t1wl = qio.GradientEchoSingle(t1wl)
    print(t1wl.te, t1wl.tr, t1wl.fa, t1w.noise, t1w.dof)
    flash = gre(pdp, r1p, r2sp,  mtp,  transmit=transmit, receive=receive[2], te=t1wl.te, tr=t1wl.tr, fa=t1wl.fa, mtpulse=False, affine=r1p.affine, shape=pdp.shape)
    text = save_folder+'/flash_t1w'+str(echo)+'.nii'
    savef(flash.volume, os.path.join(cwd, text), affine=flash.affine)
