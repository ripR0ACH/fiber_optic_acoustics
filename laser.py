import numpy as np
from scipy.stats import multivariate_normal
import matplotlib.pyplot as plt
from matplotlib import cm
class Laser:
    def __init__(self, x = np.array([None]), y = np.array([None]), P = np.array([None]), res = 1506, waist = 1, power = 100, chop_waist = True, chop_percent = 1, power_noise = False):
        self.power = power
        self.waist = waist
        self.resolution = res
        if x[0] != None and y[0] != None and P[0] != None:
            self.x, self.y, self.P = x, y, P
        else:
            self.xyz = self.make_gaussian_rays(self.resolution, self.power, chop_waist = chop_waist, chop_percent = chop_percent, power_noise = power_noise)
        return
    def set_power(self, power):
        self.power = power
        return power
    def get_power(self):
        return self.power
    def dt(self, dy = 0):
        self.xyz[:, 1] += dy
        self.y += dy
        return None
    def make_gaussian_rays(self, res, power, dy = 0, power_noise = False, chop_waist = True, chop_percent = 1):
        p = res
        xx, yy = np.mgrid[-(self.waist):(self.waist):(p * 1j), -(self.waist + dy):(self.waist + dy):(p * 1j)]
        mu = np.array([np.mean(xx.flat), np.mean(yy.flat)])
        sigma = np.array([self.waist / 2 * (np.random.rand() * (1.05 - 0.95) + 0.95), self.waist / 2 * (np.random.rand() * (1.05 - 0.95) + 0.95)])
        covariance = np.diag(sigma ** 2)
        xyz = np.column_stack([xx.flat, yy.flat, multivariate_normal.pdf(np.column_stack([xx.flat, yy.flat]), mean=mu, cov=covariance)])
        if power_noise:
            xyz[:, 2] *= np.abs(np.random.normal(-self.waist, self.waist, size = (len(xx.flat))))
        if chop_waist:
            xyz[np.ix_(np.where((chop_percent * (self.waist / 2)) ** 2 <= (xyz[:, 0] ** 2 + xyz[:, 1] ** 2))[0], [2])] = np.nan
        xyz[np.ix_(np.where(np.isnan(xyz[:, 2]) == False)[0], [2])] = (xyz[np.where(np.isnan(xyz[:, 2]) == False)[0]][:, 2] * (power / np.sum(xyz[np.where(np.isnan(xyz[:, 2]) == False)[0]][:, 2]))).reshape(xyz[np.ix_(np.where(np.isnan(xyz[:, 2]) == False)[0], [2])].shape)
        self.x = xyz[np.where(np.isnan(xyz[:, 2]) == False)[0]][:, 0]
        self.y = xyz[np.where(np.isnan(xyz[:, 2]) == False)[0]][:, 1]
        self.P = xyz[np.where(np.isnan(xyz[:, 2]) == False)[0]][:, 2]
        return xyz
    def plot_surface(self, ax = None, figsize = (10, 10), alpha = 1, cmap = cm.coolwarm, antialiased = False, show = False, save = False, name = "", *args, **kwargs):
        if ax == None:
            fig = plt.figure(figsize = figsize)
            ax = fig.add_subplot(111, projection='3d')
        else:
            fig = plt.gcf()
        ax.plot_surface(*[self.xyz[:, i].reshape(int(np.sqrt(len(self.xyz[:, i]))), int(np.sqrt(len(self.xyz[:, i])))) for i in range(3)], alpha = alpha, cmap = cmap, antialiased = antialiased, *args, **kwargs)
        if save and (name != ""):
            fig.savefig("")
        if show:
            plt.show()
        return fig, ax
    def imshow(self, ax = None, dimensions = (1, 1), figsize = (10, 10), cmap = cm.coolwarm, save = False, origin = "lower", extent = [],  name = "", show = False):
        if ax == None:
            fig, ax = plt.subplots(*dimensions, figsize = figsize)
        else:
            fig = plt.gcf()
        if extent != []:
            ax.imshow(self.xyz[:, 2].reshape(int(np.sqrt(len(self.xyz[:, 2]))), int(np.sqrt(len(self.xyz[:, 2])))), cmap = cmap, origin = origin, extent = extent)
        else:
            ax.imshow(self.xyz[:, 2].reshape(int(np.sqrt(len(self.xyz[:, 2]))), int(np.sqrt(len(self.xyz[:, 2])))), cmap = cmap, origin = origin, extent = [np.min(self.xyz[:, 0]), np.max(self.xyz[:, 0]), np.min(self.xyz[:, 1]), np.max(self.xyz[:, 1])])
        if save and (name != ""):
            fig.savefig("")
        if show:
            plt.show()
        return fig, ax
    def __len__(self):
        return len(self.x)