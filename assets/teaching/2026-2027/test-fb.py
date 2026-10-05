import deepinv as dinv
import matplotlib.pyplot as plt

#%%% Setup

x_true = dinv.utils.load_example('cameraman.png', grayscale=True)

kernel = dinv.physics.blur.gaussian_blur(sigma=3.0)
physics = dinv.physics.Blur(filter=kernel, padding="reflect")

physics.noise_model = dinv.physics.noise.GaussianNoise(sigma=0.1)

y=physics(x_true)

#%%% Optimization functions

data_fidelity = dinv.optim.L2()
prior = dinv.optim.prior.TVPrior(n_it_max=100)
#prior = dinv.optim.prior.WaveletPrior(level=3, wv='db8', p=1)

#%%% Run algorithm

Anorm2 = physics.compute_norm(y)

n_iter = 20
stepsize = 1/Anorm2
lam = 0.1

xk = y.clone()
crit = [data_fidelity.fn(xk, y, physics) + lam * prior.fn(xk)]

for k in range(n_iter):
    xk = xk - stepsize * data_fidelity.grad(xk, y, physics)
    xk = prior.prox(xk, gamma=stepsize * lam)

    crit.append(data_fidelity.fn(xk, y, physics) + lam * prior.fn(xk))

#%%% Plots

dinv.utils.plot([x_true, y, xk], titles=["Original", "Observation", "Reconstruction"])

plt.semilogy(crit)
plt.xlabel("Iteration")
plt.ylabel("Loss value")
plt.title("Convergence of the FB algorithm")
plt.show()

# %%
