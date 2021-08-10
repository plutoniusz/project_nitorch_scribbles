import nitorch
from nitorch.tools import qmri
import os
import wget
import zipfile
# import torch

# URL to MRIs
url = 'https://owncloud.gwdg.de/index.php/s/iv2TOQwGy4FGDDZ/download?path=%2F&files=hmri_sample_dataset.zip'

# Path to downloaded zip-file
cwd = os.getcwd()
pth_zip = os.path.join(cwd, 'hmri_sample_dataset.zip')
pth_mris = [os.path.join(cwd, 'MPM/mtw_mfc_3dflash_v1i_R4_0012'),
            os.path.join(cwd, 'MPM/pdw_mfc_3dflash_v1i_R4_0009'),
            os.path.join(cwd, 'MPM/t1w_mfc_3dflash_v1i_R4_0015')]

# Download file
if not os.path.exists(pth_zip):
    print('Downloading images...', end='')
    wget.download(url, pth_zip)
    print('done!')

# Unzip file
if not all([os.path.exists(p) for p in pth_mris]):
    with zipfile.ZipFile(pth_zip, 'r') as zip_ref:
        zip_ref.extractall(cwd)





fmtw = [];
for filename in os.listdir(str(pth_mris[0])):
    if filename.endswith(".nii"):
        #print(os.path.join(pth_mris[0], filename))
        fmtw.append(str(os.path.join(pth_mris[0], filename)))
    else:
        continue
#print(fmtw)

fpdw = [];
for filename in os.listdir(str(pth_mris[1])):
    if filename.endswith(".nii"):
        #print(os.path.join(pth_mris[1], filename))
        fpdw.append(str(os.path.join(pth_mris[1], filename)))
    else:
        continue
#print(fpdw)

ft1w = [];
for filename in os.listdir(str(pth_mris[2])):
    if filename.endswith(".nii"):
        #print(os.path.join(pth_mris[2], filename))
        ft1w.append(str(os.path.join(pth_mris[2], filename)))
    else:
        continue
#print(ft1w)



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

pdw = qmri.io.GradientEchoMulti.from_fnames(fpdw)
t1w = qmri.io.GradientEchoMulti.from_fnames(ft1w)
mtw = qmri.io.GradientEchoMulti.from_fnames(fmtw)


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

opt = qmri.GREEQOptions()
opt.preproc.register = False # we assume everything is already registered
opt.backend.device = 'cuda' #'cuda'  # to run on gpu. Otherwise ‘cpu’
opt.recon.space = 0          # reconstruct in PDw space. By default it generates a mean space but I haven’t tested it in a while so safer to use this for now.

# opt.penalty.factor = dict(pd=5, r1=5, mt=5, r2s=0.5) # to override default reg. Default is 10 everywhere. 

# torch.cuda.empty_cache()
# 4) run the code

pd, r1, r2s, mt = qmri.greeq([pdw, t1w, mtw], transmit=None, receive=None, opt=opt) #transmit=b1p, receive=b1m, opt=opt)
