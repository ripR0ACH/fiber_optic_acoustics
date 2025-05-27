import fiber
import laser
import csv
import numpy as np
from joblib import Parallel, delayed
import time

def sound(t, amp = 0, freq = 1e3):
    return amp * np.cos(2 * np.pi * freq * t)

def time_step(dt, i, a, f, b, l):
    dy = sound(dt * i, amp = a, freq = f)
    copy_l = laser.Laser(xyz = l.dy(dy), waist = 8e-4, power = 90)
    return [dt * i, b.diff_power(copy_l), dy]

def main(sampling_rate, trace_length, bundle, l, a = 1e-6, f = 4e4, filename = ""):
    samples = sampling_rate * trace_length
    dt = 1 / sampling_rate
    with open(filename, "w", newline = "") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["time (s)", "power (mW)", "amplitude (m)"])
        writer.writerows(Parallel(n_jobs = -1, backend = "threading")(delayed(time_step)(dt, i, a, f, bundle, l) for i in range(int(samples))))

if __name__ == "__main__":
    for i in np.linspace(5e-5, 2e-4, 50):
        bundle = fiber.FiberBundle(3e-3, 1e-4)
        l = laser.Laser(waist = i, power = 90)   
        # bundle.plot(im = l, save = True, name = "bundle.png")
        main(1e6, 0.0001, bundle, l, filename = str(bundle.count) + "fibers_" + str(l.waist) + "beam_waist.csv")