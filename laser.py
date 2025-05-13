import numpy as np
class Ray:
    def __init__(self, x = 0, y = 0, I = 0):
        self.x = x
        self.y = y
        self.I = I
        return
class Laser:
    def __init__(self, rays = None, res = 0, max_waist = 1, min_waist = 0, power = 100):
        self.power = power
        self.mxw = max_waist
        self.mnw = min_waist
        if rays != None:
            self.rays = np.array(rays)
            self.resolution = len(self.rays)
        else:
            self.resolution = res
            self.rays = self.make_gaussian_rays(self.resolution, self.mxw, self.mnw, self.power)
        return
    def dt(self, dy = 0):
        self.rays = self.make_gaussian_rays(self.resolution, self.mxw, self.mnw, dy)
        return None
    def insert_point(self, point = Ray()):
        return None
    def append_point(self, point = Ray()):
        self.rays = np.append(self.rays, point)
        return None
    def delete_point(self, ind = 0):
        return None
    def make_gaussian_rays(self, res, mxw, mnw, power, dy = 0):
        self.waist = np.random.rand() * (mxw - mnw) + mnw
        x, y = np.random.normal(0, self.waist / 2, size = (2, res))
        if dy != 0:
            y += dy
        r = np.linspace(-self.waist / 2, self.waist / 2, res)
        I = np.exp(-2 * r ** 2 / (self.waist ** 2)) * np.abs(np.random.normal(scale = self.waist / 2, size = res))
        P0 = 2 * power / (np.pi * self.waist ** 2)
        I = (np.random.rand() * (P0 * 1.001 - P0 * 0.999) + P0 * 0.9999) * (I / np.max(I))
        rays = np.array([])
        data = np.reshape([x, y, I], (len(x), 3))
        for i in range(len(I)):
            rays = np.append(rays, Ray(*data[i]))
        return rays