import numpy as np
import matplotlib.pyplot as plt
class Fiber:
    def __init__(self,  r = 1, t = 0, fr = 1):
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
        
        # This section defines the center of the fiber inside of the fiber bundle
        # this is useful information for later when I need to draw the fibers
        # or maybe not, I'll find out once I finish drafting.
        # Since the fiber bundle will be axisymmetric, I need to define two separate
        # halves of the bundle. Therefore the center of the first fiber is at the radius
        # of the fiber and on the 0 y position.
        # For the other half, the first fiber is at the opposite side of the x-axis,
        # i.e. at x = r and y = 2r. 
        # if self.theta == 0:
        #     self.center = [self.fiber_ring, 0] # the first fiber.
        # elif self.theta < np.pi:
        #     self.center = [self.fiber_ring * np.cos(self.theta), self.fiber_ring * np.sin(self.theta)] 
        #     # the rest of the fibers in the top half 
        #     # are drawn in arcs defined by concentric rings, fiber_ring.
        #     # therefore, depending on the ring and the angle theta, the fiber is set.
        # elif self.theta == np.pi:
        #     self.center = [-self.fiber_ring, 0] # the first fiber on the other side of x-axis.
        # else:
        #     self.center = [self.fiber_ring * np.cos(self.theta), 2 * self.r - (self.fiber_ring * np.cos(self.theta))]
        #     # same as above, the fibers are drawn in concentric rings defined by
        #     # by theta and the fiber_ring.
        self.center = [(self.r + self.fiber_ring) * np.cos(self.theta), (self.r + self.fiber_ring) * np.sin(self.theta)]
        self.x, self.y = self.draw_fiber()
        return
    
    def draw_fiber(self): 
        """
        
        draw_fiber --- draws the x, y points for the fiber to be that it can be plotted.
        
        :return: x and y arrays for the circumference of the fiber being plotted.
        
        """
        r = self.r # radius of the fiber to be drawn
        t = self.theta # theta position of the fiber within the bundle
        fr = self.fiber_ring # radius away from the center of the fiber bundle
        ts = np.linspace(0, 2 * np.pi, 100) # thetas for drawing the individual fiber
        if t == 0: # if the fiber is on the right side of the x axis
            return [r * np.cos(ts), r * np.sin(ts) - r] 
        elif t < np.pi:
            return [r * np.cos(ts) - fr * np.cos(t), r * np.sin(ts) - fr * np.sin(t) - r]
        elif t == np.pi:
            return [r * np.cos(ts), r * np.sin(ts) + r]
        return [r * np.cos(ts) - fr * np.cos(t), r * np.sin(ts) - fr * np.sin(t) + r]
class FiberBundle:
    def __init__(self, r, fiber_r = 1):
        self.r = r
        self.fr = fiber_r
        self.fiber_rings = np.r_[self.fr, np.linspace(2 * self.fr, self.r - self.fr - (self.r - self.fr) % (2 * self.fr), int((self.r - self.fr) / (2 * self.fr)))]
        print(self.fiber_rings)
        self.bundle = self.make_bundle()
        self.count, self.fibers = self.make_bundle()
        return

    def make_bundle(self):
        n = 0
        f = np.array([])
        for ring in self.fiber_rings:
            ts = np.linspace(0, np.pi, int(np.pi / ((2 * ring * np.arccos(1 - self.fr**2 / (2 * ring ** 2))) / ring)))
            n += len(ts)
            for t in ts:
                f = np.append(f, Fiber(self.fr, t, ring))
            ts = np.linspace(np.pi, 2 * np.pi, int(np.pi / ((2 * ring * np.arccos(1 - self.fr**2 / (2 * ring ** 2))) / ring)))
            n += len(ts)
            for t in ts:
                f = np.append(f, Fiber(self.fr, t, ring))
        return n, f
    def draw_bundle(self):
        _, ax = plt.subplots(1, 1, figsize = (10, 10))
        ax.set_xlim(-self.r - 10, self.r + 10)
        ax.set_ylim(-self.r - 10, self.r + 10)
        for f in self.fibers:
            ax.plot(f.x, f.y)
            ax.scatter(f.center[0], f.center[1], s=1)
        ax.axline((0, 50), (50, 50))
        ax.axline((50, 50), (50, -50))
        ax.axline((-50, -50), (50, -50))
        ax.axline((-50, -50), (-50, 50))
        plt.show()