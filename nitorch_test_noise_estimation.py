from nitorch.tools.img_statistics import estimate_noise
import os
import nitorch.tools.qmri.io as qio

cwd = os.getcwd()
p = os.path.join(cwd, "MPM/t1w_mfc_3dflash_v1i_R4_0015")
#t1w = str(os.path.join(p, 'anon_s2018-02-28_18-26-190921-00001-00224-1.nii'))

t1w = []
for filename in os.listdir(str(p)):
    if filename.endswith(".nii"):
        # print(os.path.join(pth_mris[0], filename))
        t1w.append(str(os.path.join(p, filename)))
    else:
        continue

t1w = qio.GradientEchoMulti.from_fnames(t1w)

for e in t1w:
    print("NEW ECHO")
    sd_noise, _, mu_noise, _= estimate_noise(e.fdata(), chi=True)
    print(f"vr_noise: {sd_noise**2}, sd_noise: {sd_noise}, mu_noise: {mu_noise}")  # 17.9737