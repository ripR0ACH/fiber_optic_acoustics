import numpy as np
class Ray:
    def __init__(self, x = 0, y = 0, I = 0):
        self.x = x
        self.y = y
        self.I = I
        return
class Laser:
    def __init__(self, rays = None):
        if rays != None:
            self.rays = np.array(rays)
        else:
            self.rays = self.make_gaussian_rays()
        return
    def insert_point(self, point = Ray()):
        return None
    def append_point(self, point = Ray()):
        self.rays = np.append(self.rays, point)
        return None
    def delete_point(self, ind = 0):
        return None
    def make_gaussian_rays(self):
        return None