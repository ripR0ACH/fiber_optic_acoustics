from laser import Laser, Ray
import numpy as np
import matplotlib.pyplot as plt
class Fiber:
    def __init__(self,  r = 1, t = 0, fr = 1, i = 0, half = 0):
        """
        
        __init__ --- initializes a single fiber instance.
        
        :param r: the radius of a single fiber.
        :param t: the theta position within a concentric ring inside of a fiber
                  bundle.
        :param fr: the radius of the current ring, where this fiber will be placed,
                   inside of the fiber bundle.
        
        :return: None.
        
        """
        self.r = r # radius of a single fiber
        self.theta = t # theta position of the fiber within the bundle
        self.fiber_ring = fr # distance of the center of the fiber from the center of the fiber bundle
        self.half = half
        self.i = i
        self.center = self.set_pos()
        self.x, self.y = self.draw_fiber()
        return
    def set_pos(self):
        if self.half == 0:
            if self.i == 0:
                return [self.r * np.cos(self.theta - np.pi / 2), self.r * np.sin(self.theta - np.pi / 2)]
            else:
                return [self.fiber_ring * np.cos(self.theta - np.pi), self.fiber_ring * np.sin(self.theta - np.pi) - self.r]
        else:
            if self.i == 0:
                return [self.r * np.cos(self.theta - np.pi / 2), self.r * np.sin(self.theta - np.pi / 2)]
            else:
                return [self.fiber_ring * np.cos(self.theta - np.pi), self.fiber_ring * np.sin(self.theta - np.pi) + self.r]
    def draw_fiber(self): 
        """
        
        draw_fiber --- draws the x, y points for the fiber to be that it can be plotted.
        
        :return: x and y arrays for the circumference of the fiber being plotted.
        
        """
        ts = np.linspace(0, 2 * np.pi, 100) # thetas for drawing the individual fiber
        return [self.center[0] + self.r * np.cos(ts), self.center[1] + self.r * np.sin(ts)]
    def intensity(self, l):
        I = 0
        for r in l.rays:
            if self.r ** 2 > (r.x - self.center[0]) ** 2 + (r.y - self.center[1]) ** 2:
                I += r.I
        return I

class FiberBundle:
    def __init__(self, r, fiber_r = 1):
        self.r = r
        self.fr = fiber_r
        self.fiber_rings = np.r_[self.fr, np.linspace(2 * self.fr, (self.r - self.fr) - (self.r - self.fr) % (2 * self.fr), int((self.r - self.fr) / (2 * self.fr)))]
        self.count, self.fibers = self.make_bundle()
        return

    def make_bundle(self):
        n = 0
        f = np.array([])
        for i, ring in enumerate(self.fiber_rings):
            ts = np.linspace(0, np.pi, int(np.pi / ((2 * ring * np.arccos(1 - self.fr ** 2 / (2 * ring ** 2))) / ring)))
            n += len(ts)
            for t in ts:
                f = np.append(f, Fiber(self.fr, t, ring, i))
            ts = np.linspace(np.pi, 2 * np.pi, int(np.pi / ((2 * ring * np.arccos(1 - self.fr ** 2 / (2 * ring ** 2))) / ring)))
            for t in ts:
                f = np.append(f, Fiber(self.fr, t, ring, i, 1))
            n += len(ts)
        return n, f
    def plot(self, centers = False, ax = None, figsize = (10, 10), *args, **kwargs):
        if ax == None:
            fig, ax = plt.subplots(1, 1, figsize = figsize)
        else:
            fig = plt.gcf()
        ax.set_xlim(-self.r - self.r * .1, self.r + self.r * .1)
        ax.set_ylim(-self.r - self.r * .1, self.r + self.r * .1)
        for f in self.fibers:
            ax.plot(f.x, f.y, *args, **kwargs)
            if centers:
                ax.scatter(f.center[0], f.center[1], s=5)
        ax.axline((0, self.r), (self.r, self.r))
        ax.axline((self.r, self.r), (self.r, -self.r))
        ax.axline((-self.r, -self.r), (self.r, -self.r))
        ax.axline((-self.r, -self.r), (-self.r, self.r))
        return fig, ax
    def sum_intensity(self, l):
        I = 0
        for f in self.fibers:
            I += f.intensity(l)
        return I
    def diff_intensity(self, l):
        half_0 = 0
        half_1 = 1
        for f in self.fibers:
            if f.half == 0:
                half_0 += f.intensity(l)
            else:
                half_1 += f.intensity(l)
        return half_0 - half_1