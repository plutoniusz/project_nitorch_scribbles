from torch._C import FloatStorageBase
from nitorch.io import savef
from nitorch.tools import qmri
import os
import zipfile
import nitorch.tools.qmri.io as qio
from matplotlib import pyplot as plt
from datetime import datetime
from pathlib import Path

# # URL to MRIs
# print("starting")
# url = 'https://owncloud.gwdg.de/index.php/s/iv2TOQwGy4FGDDZ/download?path=%2F&files=hmri_sample_dataset.zip'

# Path to downloaded zip-file
print("getting paths")
#cwd = os.getcwd()
cwd = '/data/underworld/kbas/project_nitorch_scribbles'
pth_zip = os.path.join(cwd, 'hmri_sample_dataset.zip')

mc = False

if mc:
    pth_mris = [os.path.join(cwd, '4John_Klara/mtw_mfc_3dflash_v1k_180deg_RR_0038'),
                os.path.join(cwd, '4John_Klara/pdw_mfc_3dflash_v1k_RR_0036'),
                os.path.join(cwd, '4John_Klara/t1w_mfc_3dflash_v1k_RR_0034')]
else:
    pth_mris = [os.path.join(cwd, 'MPM/mtw_mfc_3dflash_v1i_R4_0012'),
            os.path.join(cwd, 'MPM/pdw_mfc_3dflash_v1i_R4_0009'),
            os.path.join(cwd, 'MPM/t1w_mfc_3dflash_v1i_R4_0015')]

# # Path to downloaded zip-file
# print("getting paths")
# cwd = os.getcwd()
# #pth_zip = os.path.join(cwd, 'hmri_sample_dataset.zip')
# pth_mris = [os.path.join(cwd, 'slices/mtw_mfc_3dflash_v1i_R4_0012'),
#             os.path.join(cwd, 'slices/pdw_mfc_3dflash_v1i_R4_0009'),
#             os.path.join(cwd, 'slices/t1w_mfc_3dflash_v1i_R4_0015')]

# # Download file
# if not os.path.exists(pth_zip):
#     print('Downloading images...', end='')
#     wget.download(url, pth_zip)
#     print('done!')

# # Unzip file
# print("unzipping files")
# if not all([os.path.exists(p) for p in pth_mris]):
#     with zipfile.ZipFile(pth_zip, 'r') as zip_ref:
#         zip_ref.extractall(cwd)


print("preparing lists")
fmtw = []
for filename in os.listdir(str(pth_mris[0])):
    if filename.endswith(".nii"):
        # print(os.path.join(pth_mris[0], filename))
        fmtw.append(str(os.path.join(pth_mris[0], filename)))
    else:
        continue
#print(fmtw)

fpdw = []
for filename in os.listdir(str(pth_mris[1])):
    if filename.endswith(".nii"):
        #print(os.path.join(pth_mris[1], filename))
        fpdw.append(str(os.path.join(pth_mris[1], filename)))
    else:
        continue
#print(fpdw)

ft1w = []
for filename in os.listdir(str(pth_mris[2])):
    if filename.endswith(".nii"):
        #print(os.path.join(pth_mris[2], filename))
        ft1w.append(str(os.path.join(pth_mris[2], filename)))
    else:
        continue
#print(ft1w)
print("paths to additional maps")
if mc:
    b1p_ref = str(os.path.join(cwd, "4John_Klara/mfc_bloch_siegert_v1b_190deg_2ms_Classic_0011/s2021-06-23_10-18-104513-00001-00048-1.nii"))
    #b1p_ref = str(os.path.join(cwd, "4John_Klara/mfc_bloch_siegert_v1b_190deg_2ms_Classic_0011/s2021-06-23_10-18-104513-00001-00096-1.nii"))
    b1p_map = str(os.path.join(cwd, "4John_Klara/mfc_bloch_siegert_v1b_190deg_2ms_Classic_0013/s2021-06-23_10-18-104513-00001-00048-1.nii"))
else:
    b1p_map = str(os.path.join(cwd, "MPM/pdw_mfc_3dflash_v1i_R4_0009/Results/Supplementary/anon_s2018-02-28_18-26-184837-00001-00001-1_B1map.nii"))
    b1p_ref = str(os.path.join(cwd, "MPM/pdw_mfc_3dflash_v1i_R4_0009/Results/Supplementary/anon_s2018-02-28_18-26-184837-00001-00001-1_B1ref.nii"))
    mtw_b1m_map = str(os.path.join(cwd, "MPM/pdw_mfc_3dflash_v1i_R4_0009/Results/Supplementary/sensMap_HC_over_BC_division_MT.nii"))
    pdw_b1m_map = str(os.path.join(cwd, "MPM/pdw_mfc_3dflash_v1i_R4_0009/Results/Supplementary/sensMap_HC_over_BC_division_PD.nii"))
    t1w_b1m_map = str(os.path.join(cwd, "MPM/pdw_mfc_3dflash_v1i_R4_0009/Results/Supplementary/sensMap_HC_over_BC_division_T1.nii"))




# This assumes that all the data has been co-registered
# with SPM before (there is also an option to do the
# co-registration inside the fitting function, and it
# requires a few more inputs such as magnitude images
# that go with each fieldmap)
# I guess that in a first instance, you could fit the
# data without using the transmit/receive maps to makes
# things simpler.

 

# 1) Map the weighted echoes
# fpdw = list of filenames of PDw echoes
# ft1w = list of filenames of T1w echoes
# fmtw = list of filenames of MTw echoes

# pdw = qmri.io.GradientEchoMulti.from_fnames(fpdw)
# t1w = qmri.io.GradientEchoMulti.from_fnames(ft1w)
# mtw = qmri.io.GradientEchoMulti.from_fnames(fmtw)

print("reading images from paths using nitorch GradientEchoMulti")
t1w = qio.GradientEchoMulti.from_fnames(ft1w)
pdw = qio.GradientEchoMulti.from_fnames(fpdw)
mtw = qio.GradientEchoMulti.from_fnames(fmtw, mt=True)
print("precomputind field maps")
transmit = qio.PrecomputedFieldMap(b1p_map, magnitude=b1p_ref)
if mc:
    # receive = qio.PrecomputedFieldMap(mtw_b1m_map, unit='a.u', affine=mtw.affine)
    receive = None
    transmit = None
else:
    receive = [qio.PrecomputedFieldMap(pdw_b1m_map,  unit='a.u', affine=pdw.affine),
            qio.PrecomputedFieldMap(t1w_b1m_map, unit='a.u', affine=t1w.affine),
            qio.PrecomputedFieldMap(mtw_b1m_map, unit='a.u', affine=mtw.affine)]
#receive = None

# These functions should have read the TE/TR/FA from
# the description in the header. The output objects
# have fields:

# volume : io.MappedArray or tensor       Mapped volume file
# affine : tensor                         Orientation matrix
# te : list[float]                        Echo times (in sec)
# tr : float                              Repetition time (in sec)
# ti : float                              Inversion time (in sec)
# fa : float                              Flip angle (in deg)
# mt : float or bool                      Off-resonance pulse (in hz, or bool)

# I usually ensure that the mt field is set because
# my parsing stuff sometimes fails

mtw.mt = True


# 3) Prepare the options

# opt = qmri.GREEQOptions()
# opt.preproc.register = True # we assume everything is already registered
# opt.backend.device = 'cuda' #'cuda'  # to run on gpu. Otherwise ‘cpu’
# opt.recon.space = 0          # reconstruct in PDw space. By default it generates a mean space but I haven’t tested it in a while so safer to use this for now.

# # torch.cuda.empty_cache()
# # 4) run the code

# ("calling greeq function")
# pd, r1, r2s, mt = qmri.greeq([pdw, t1w, mtw], transmit=None, receive=None, opt=opt) #transmit=b1p, receive=b1m, opt=opt)


opt = qmri.relax.GREEQOptions()
opt.penalty.factor = dict(pd=5, r1=5, mt=5, r2s=0.5) # to override default reg. Default is 10 everywhere. 
opt.recon.space = 1  # space of T1w since I provide the inputs as [pdw, t1w, mtw]
opt.backend.device = 'cpu'
opt.preproc.register = False
opt.optim.nb_levels = 1
opt.verbose = 1
opt.likelihood = 'chi'
opt.noisemodel = 'gauss'
print("start greeq")
pd, r1, r2s, mt = qmri.relax.greeq([pdw, t1w, mtw], transmit=transmit, receive=receive, opt=opt)

# 5) write results
datime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
if mc:
    save_folder = cwd + '/qmri_results/' +  str(opt.likelihood) + '_mc' + '_results' + datime
else:
    save_folder = cwd + '/qmri_results/' +  str(opt.likelihood) + '_results_' + datime
save_path = Path(save_folder).mkdir(parents=True, exist_ok=True)
savef(pd.volume, os.path.join(save_folder + '/pd.nii'), affine=pd.affine)
savef(r1.volume, os.path.join(save_folder + '/r1.nii'), affine=r1.affine)
savef(r2s.volume, os.path.join(save_folder + '/r2s.nii'), affine=r2s.affine)
savef(mt.volume, os.path.join(save_folder + '/mt.nii'), affine=mt.affine)