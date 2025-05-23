import fiber
import laser
import time

def main():
    bundle = fiber.FiberBundle(3.8e-3, 1e-4)
    l = laser.Laser(waist = 1e-3, power = 200)
    t1 = time.time()
    print(bundle.sum_power(l))
    print(time.time() - t1)

if __name__ == "__main__":
    main()