import time
from laser import Laser
import numpy as np
import matplotlib.pyplot as plt
from joblib import Parallel, delayed
from matplotlib.image import BboxImage
from matplotlib import cm

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

class FiberBundle:
    def __init__(self, r, fiber_r = 1):
        self.r = r
        self.fr = fiber_r
        self.fiber_rings = np.r_[self.fr, np.linspace(2 * self.fr, (self.r - self.fr) - (self.r - self.fr) % (2 * self.fr), int((self.r - self.fr) / (2 * self.fr)))]
        # theta position, ring radius, ring number, half
        self.fibers = self.make_bundle()
        self.centers = np.array(Parallel(n_jobs = -1, backend = "threading")(delayed(self.set_fiber_pos)(self.fr, f[0], f[1], f[2], f[3]) for i in range(len(self.fibers)) for f in self.fibers[i]))
        self.thetas = np.array([f[0] for i in range(len(self.fibers)) for f in self.fibers[i]])
        self.ring_radius = np.array([f[1] for i in range(len(self.fibers)) for f in self.fibers[i]])
        self.ring_number = np.array([int(f[2]) for i in range(len(self.fibers)) for f in self.fibers[i]])
        self.half = np.array([int(f[3]) for i in range(len(self.fibers)) for f in self.fibers[i]])
        self.count = len(self.centers)
        self.drawings = np.array(Parallel(n_jobs = -1, backend = "threading")(delayed(self.draw_fiber)(self.centers[i]) for i in range(len(self.centers))))
        return

    def set_fiber_pos(self, r, theta, ring, i, half):
        if half == 0:
            if i == 0:
                return np.array([r * np.cos(theta - np.pi / 2), r * np.sin(theta - np.pi / 2)])
            else:
                return np.array([ring * np.cos(theta - np.pi), ring * np.sin(theta - np.pi) - r])
        else:
            if i == 0:
                return np.array([r * np.cos(theta - np.pi / 2), r * np.sin(theta - np.pi / 2)])
            else:
                return np.array([ring * np.cos(theta - np.pi), ring * np.sin(theta - np.pi) + r])

    def draw_fiber(self, center = [0, 0]): 
        """
        
        draw_fiber --- draws the x, y points for the fiber to be that it can be plotted.
        
        :return: x and y arrays for the circumference of the fiber being plotted.
        
        """
        ts = np.linspace(0, 2 * np.pi, 100) # thetas for drawing the individual fiber
        return np.array([center[0] + self.fr * np.cos(ts), center[1] + self.fr * np.sin(ts)])

    def make_bundle(self):
        return np.array(Parallel(n_jobs = -1)(delayed(self.draw_ring)(ring, i) for i, ring in enumerate(self.fiber_rings)), dtype = "object").flatten()

    def draw_ring(self, ring, i):
        ts = np.append(np.linspace(0, np.pi, int(np.pi / ((2 * ring * np.arccos(1 - (self.fr ** 2) / (2 * ring ** 2))) / ring))), np.linspace(np.pi, 2 * np.pi, int(np.pi / ((2 * ring * np.arccos(1 - (self.fr ** 2) / (2 * ring ** 2))) / ring))))
        f1 = []
        Parallel(n_jobs = -1)(delayed(f1.append)([t, ring, int(i), 0]) for t in ts[:int(len(ts) / 2)])
        f2 = []
        Parallel(n_jobs = -1)(delayed(f2.append)([t, ring, int(i), 1]) for t in ts[int(len(ts) / 2):])
        return np.array(f1 + f2)

    def plot(self, fibers = True, centers = False, ax = None, figsize = (10, 10), dimensions = (1, 1), scatter_size = 1, im = [], cmap = cm.coolwarm, *args, **kwargs):
        if ax == None:
            fig, ax = plt.subplots(*dimensions, figsize = figsize)
        else:
            fig = plt.gcf()
        plt.ioff()
        for i in range(len(self.drawings)):
            if fibers:
                ax.plot(self.drawings[i][0], self.drawings[i][1], zorder = 100, *args, **kwargs)
            if centers:
                ax.scatter(*self.centers[i], s = scatter_size, zorder = 100, *args, **kwargs)
        plt.ion()
        if len(im) !=  0:
            im[np.ix_(np.where(im[:, 2] == 0)[0], [2])] = np.nan
            print(im)
            ax.add_artist(BboxImage(ax.get_window_extent, data = im[:, 2].reshape(int(np.sqrt(len(im[:, 2]))), int(np.sqrt(len(im[:, 2])))), cmap = cmap))
        ax.set_xlim(-self.r - self.r * .1, self.r + self.r * .1)
        ax.set_ylim(-self.r - self.r * .1, self.r + self.r * .1)
        ax.axline((0, self.r), (self.r, self.r))
        ax.axline((self.r, self.r), (self.r, -self.r))
        ax.axline((-self.r, -self.r), (self.r, -self.r))
        ax.axline((-self.r, -self.r), (-self.r, self.r))
        return fig, ax
    
    def sum_power(self, l):
        self.total_power = sum(Parallel(n_jobs = -1)(delayed(self.check_boundary)(l.x[i], l.y[i], l.P[i], self.centers) for i in range(len(l.x))))
        return self.total_power
            
    def check_boundary(self, x, y, p, centers):
        ind = find_nearest(np.array((x - centers[:, 0]) ** 2 + (y - centers[:, 1]) ** 2), self.fr ** 2)
        if ((x - self.centers[ind][0]) ** 2 + (y - self.centers[ind][1]) ** 2) < (self.fr ** 2):
            return p
        return 0
    # def diff_intensity(self, l):
    #     half_0 = np.where(self.half == 0)[0]
    #     l1 = l.x[np.where(l.y > 0)] ** 2 + l.y[np.where(l.y > 0)] ** 2
    #     for i in range(len(l.x[np.where(l.y > 0)])):
    #         ind = find_nearest(np.array(self.centers[:, 0] ** 2 + self.centers[:, 1] ** 2), l1[i])
    #         if (self.centers[ind][0] ** 2 + self.centers[ind][2] ** 2) > l1[i]:
                
    #     p1 = 0
    #     # for i in range(len(self.centers[half_0])):
    #     #     in_fibers = np.where((self.centers[half_0][i][0] ** 2 + self.centers[half_0][i][1] ** 2) > (l.x[np.where(l.y > 0)] ** 2 + l.y[np.where(l.y > 0)] ** 2))
    #     #     # print(in_fibers)
    #     #     p1 += sum(l.P[in_fibers])
    #     print(l1)
    #     # print(np.where(([self.centers[half_0][i][0] ** 2 + self.centers[half_0][i][1] ** 2] for i in range(len(self.centers[half_0]))) > (l.x[np.where(l.y > 0)] ** 2 + l.y[np.where(l.y > 0)] ** 2)).tolist())
    #     half_1 = np.where(self.half == 1)[0]
    #     # return np.where(l.y > 0)[0]