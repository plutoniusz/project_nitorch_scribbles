import torch
import numpy as np
from matplotlib import pyplot as plt

s2 = 80 # Variance
mu = 15 # Mean
nu =  50 # degrees of freedom

s2n = 10 # Variance
mun = 30 # Mean
nun =  20 # degrees of freedom

N  = 100000 # Number of samples
noise_rate = int(N/2)
np.random.seed(6)
noise = np.random.normal(0, np.sqrt(s2n), (noise_rate, nun))+ mun/np.sqrt(nun)
signal = np.random.normal(0, np.sqrt(s2), (N-noise_rate, nu)) + mu/np.sqrt(nu)
noise=np.sqrt(np.sum(noise**2, 1))
signal=np.sqrt(np.sum(signal**2, 1))
f=np.concatenate((noise,signal), 0)
np.random.shuffle(f)

from nitorch.tools.img_statistics import estimate_noise
f=torch.from_numpy(f)
sd_noise, _, mu_noise, _= estimate_noise(f, max_iter=50000, chi=True)
print(f"vr_noise: {sd_noise**2}, sd_noise: {sd_noise}, mu_noise: {mu_noise}")  # 17.9737

