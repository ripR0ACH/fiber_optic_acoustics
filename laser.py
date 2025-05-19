import numpy as np
class Laser:
    def __init__(self, res = 0, waist = 1, power = 100):
        self.power = power
        self.waist = waist
        self.resolution = res
        self.x, self.y, self.P = self.make_gaussian_rays(self.resolution, self.waist, self.power)
        return
    def dt(self, dy = 0):
        self.rays = self.make_gaussian_rays(self.resolution, self.waist, dy)
        return None
    def make_gaussian_rays(self, res, waist, power, dy = 0):
        self.waist = waist
        x, y = np.random.normal(0, self.waist / 2, size = (2, res))
        if dy != 0:
            y += dy
        r = np.linspace(-self.waist / 2, self.waist / 2, res)
        P = np.exp(-2 * r ** 2 / (self.waist ** 2)) * np.abs(np.random.normal(scale = self.waist / 2, size = res))
        P *= power / sum(P)
        return x, y, P