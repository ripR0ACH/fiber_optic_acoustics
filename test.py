import fiber
import laser
import csv
import numpy as np
from joblib import Parallel, delayed

def sound(t, amp = 0, freq = 1e3):
    return amp * np.cos(2 * np.pi * freq * t)

def time_step(dt, i, a, f, b, l):
    dy = sound(dt * i, amp = a, freq = f)
    copy_l = laser.Laser(xyz = l.dy(dy), waist = 8e-4, power = 90)
    return [dt * i, b.diff_power(copy_l), dy]

def main(sampling_rate, trace_length, bundle, l, a = 1e-6, f = 1.08e5, filename = ""):
    samples = sampling_rate * trace_length
    dt = 1 / sampling_rate
    with open(filename, "w", newline = "") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["time (s)", "power (mW)", "amplitude (m) = " + str(a), "bundle radius = " + str(bundle.r), "fiber radius = " + str(bundle.fr), "# fibers = " + str(bundle.count), "beam waist = " + str(l.waist), "cladding radius = " + str(bundle.cladding), "total power (mW) = " + str(l.power), "sampling rate = " + str(sampling_rate), "trace length = " + str(trace_length), "signal frequency = " + str(f)])
        writer.writerows(Parallel(n_jobs = -1, backend = "threading")(delayed(time_step)(dt, i, a, f, bundle, l) for i in range(int(samples))))

if __name__ == "__main__":
    # for i in np.linspace(3e-4, 1e-3, 50):
        bundle = fiber.FiberBundle(1.5e-4, 2.5e-5, 5e-5)
        l = laser.Laser(waist = 0.00013571428571428572, power = 90)
        bundle.plot(im = l, save = True, name = "bundle.png", c = "black")
        main(2e8, 0.0001, bundle, l, filename = "high_sample_rate.csv")
        print("success!")