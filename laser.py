import numpy as np
from scipy.stats import multivariate_normal
import matplotlib.pyplot as plt
from matplotlib import cm
class Laser:
    def __init__(self, x = np.array([None]), y = np.array([None]), P = np.array([None]), res = 1506, waist = 1, power = 100, chop_waist = True):
        self.power = power
        self.waist = waist
        self.resolution = res
        if x[0] != None and y[0] != None and P[0] != None:
            self.x, self.y, self.P = x, y, P
        else:
            self.xyz, self.x, self.y, self.P = self.make_gaussian_rays(self.resolution, self.waist, self.power, chop_waist = chop_waist)
        return
    def dt(self, dy = 0):
        self.rays = self.make_gaussian_rays(self.resolution, self.waist, dy)
        return None
    def make_gaussian_rays(self, res, waist, power, dy = 0, power_noise = False, chop_waist = True):
        # self.waist = waist
        # x, y = np.random.normal(0, self.waist / 2, size = (2, res))
        # if dy != 0:
        #     y += dy
        # r = np.linspace(-self.waist / 2, self.waist / 2, res)
        # P = np.exp(-2 * r ** 2 / (self.waist ** 2)) * np.abs(np.random.normal(scale = self.waist / 2, size = res))
        # P *= power / sum(P)
        # return x, y, P
        self.waist = waist
        p = res
        waist = 1
        xx, yy = np.mgrid[-(waist):(waist):(p * 1j), -(waist):(waist):(p * 1j)]
        mu = np.array([np.mean(xx.flat), np.mean(yy.flat)])
        sigma = np.array([waist / 2 * (np.random.rand() * (1 - 0.9) + 0.9), waist / 2 * (np.random.rand() * (1 - 0.9) + 0.9)])
        covariance = np.diag(sigma ** 2)
        xyz = np.column_stack([xx.flat, yy.flat, multivariate_normal.pdf(np.column_stack([xx.flat, yy.flat]), mean=mu, cov=covariance)])
        if power_noise:
            xyz[:, 2] *= (np.random.normal(-waist, waist, size = (len(xx.flat))))
        if chop_waist:
            xyz[np.ix_(np.where((1.5 * (waist / 2)) ** 2 <= (xyz[:, 0] ** 2 + xyz[:, 1] ** 2))[0], [2])] = 0
        xyz[:, 2] *= power / np.sum(xyz[:, 2])
        return xyz, xyz[:, 0], xyz[:, 1], xyz[:, 2]
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
        return ax
    def imshow(self, ax = None, dimensions = (1, 1), figsize = (10, 10), cmap = cm.coolwarm, save = False, origin = "lower", name = "", show = False):
        if ax == None:
            fig, ax = plt.subplots(*dimensions, figsize = figsize)
        else:
            fig = plt.gcf()
        plt.imshow(self.xyz[:, 2].reshape(int(np.sqrt(len(self.xyz[:, 2]))), int(np.sqrt(len(self.xyz[:, 2])))), cmap = cm.coolwarm, origin = origin)
        if save and (name != ""):
            fig.savefig("")
        if show:
            plt.show()
        return ax