import fiber
import laser
import csv
import numpy as np
from joblib import Parallel, delayed

def sound(t, amp = 0, freq = 1e3):
    return amp * np.cos(2 * np.pi * freq * t)

def time_step(dt, i, a, f, b, l):
    dy = sound(dt * i, amp = a, freq = f)
    copy_l = laser.Laser(xyz = l.dy(dy), waist = l.waist, power = 90)
    return [dt * i, b.diff_power(copy_l), dy]


def main(sampling_rate, trace_length, l, bundle, a = 1e-6, f = 1.08e5, filename = "", rings_to_drop = (0, 0)):
    samples = sampling_rate * trace_length
    dt = 1 / sampling_rate
    bundle.drop_rings(rings_to_drop)
    with open(filename, "w", newline = "") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["time (s)", "power (mW)", "amplitude (m) = " + str(a), "bundle radius = " + str(bundle.r), "fiber radius = " + str(bundle.fr), "# fibers = " + str(bundle.count), "beam waist = " + str(l.waist), "cladding radius = " + str(bundle.cladding), "total power (mW) = " + str(l.power), "sampling rate = " + str(sampling_rate), "trace length = " + str(trace_length), "signal frequency = " + str(f)])
        writer.writerows(Parallel(n_jobs = -1, backend = "threading")(delayed(time_step)(dt, i, a, f, bundle, l) for i in range(int(samples))))
    bundle.reset()
    # with open(filename, "w", newline = "") as csvfile:
    #     writer = csv.writer(csvfile)
    #     writer.writerows(Parallel(n_jobs = -1, backend = "threading")(delayed(split_beam)(dt, i, a, f, l) for i in range(int(samples))))
    #     csvfile.close()
def split_beam(dt, i, a, f, l):
    dy = sound(dt * i, a, f)
    return [dt * i, np.sum(l.P[np.where(l.y[np.where(np.isnan(l.y[:]) == False)[0]] > dy)[0]]) - np.sum(l.P[np.where(l.y[np.where(np.isnan(l.y[:]) == False)[0]] < dy)[0]]), dy]
if __name__ == "__main__":
    bundle = fiber.FiberBundle(3.3e-3, (250 / 2) * 1e-6, (125 / 2) * 1e-6)
    for i in range(0, 1):
        space = bundle.fiber_rings[i] - bundle.cladding
        bundle.drop_rings((0, i))
        for j in np.linspace(space, 2 * bundle.r, 2):
            l = laser.Laser(waist = j, power = 90)
            main(2e6, 0.0001, l, bundle, filename = "data/20250624/" + str(np.round(l.waist, 5)) + "waist_" + str(i) + "bundlesdropped.csv")
        bundle.reset()