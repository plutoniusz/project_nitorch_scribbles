import torch
import numpy as np
from matplotlib import pyplot as plt

s2 = 80 # Variance
mu = 15 # Mean
nu =  50 # degrees of freedom

s2n = 10 # Variance noise
mun = 30 # Mean noise
nun =  20 # degrees of freedom noise

N  = 1000000 # Number of samples
noise_rate = int(N*0.4)
np.random.seed(6)
noise = np.random.normal(0, np.sqrt(s2n), (noise_rate, nun))+ mun/np.sqrt(nun)
signal = np.random.normal(0, np.sqrt(s2), (N-noise_rate, nu)) + mu/np.sqrt(nu)
noise=np.sqrt(np.sum(noise**2, 1))
signal=np.sqrt(np.sum(signal**2, 1))
f=np.concatenate((noise,signal), 0)
np.random.shuffle(f)
#plt.hist(f)
#plt.show()


from nitorch.tools.img_statistics import estimate_noise
f=torch.from_numpy(f)
sd_noise, _, mu_noise, _= estimate_noise(f, max_iter=50000, chi=True)
print(f"mu_noise: {mu_noise}")  # 17.9737

