import threading
import time


class Semaphore:
    def __init__(self, initial=1):
        self.lock = threading.Semaphore(initial)

    def acquire(self):
        self.lock.acquire()

    def release(self):
        self.lock.release()


class Bridge:
    def __init__(self):
        self.semaphore = Semaphore(1)  # Semaphore to control bridge access
        self.bridge_length = 5  # Length of the bridge
        self.vehicles_on_bridge = 0  # Number of vehicles currently on the bridge
        self.direction = Semaphore(1)  # Semaphore to control direction of vehicles

    def cross_bridge(self, vehicle_id, direction):
        print(f"Vehicle {vehicle_id} wants to cross the bridge from {direction} direction.")
        self.direction.acquire()

        self.semaphore.acquire()
        while self.vehicles_on_bridge + 1 > self.bridge_length:
            self.semaphore.release()
            time.sleep(0.5)  # Wait for the bridge to clear
            self.semaphore.acquire()

        self.vehicles_on_bridge += 1
        self.semaphore.release()

        print(f"Vehicle {vehicle_id} starts crossing the bridge from {direction} direction.")
        time.sleep(1)  # Crossing the bridge takes some time

        self.semaphore.acquire()
        self.vehicles_on_bridge -= 1
        print(f"Vehicle {vehicle_id} has crossed the bridge from {direction} direction.")
        self.semaphore.release()

        self.direction.release()


class BridgeSimulation:
    def __init__(self, bridge):
        self.bridge = bridge

    def simulate(self):
        vehicles = []
        for i in range(10):  # Simulating 10 vehicles crossing the bridge
            direction = 'East' if i % 2 == 0 else 'West'
            vehicle = threading.Thread(target=self.bridge.cross_bridge, args=(i+1, direction))
            vehicles.append(vehicle)
            vehicle.start()

        for vehicle in vehicles:
            vehicle.join()


# Testing the simulation
bridge = Bridge()
simulation = BridgeSimulation(bridge)
simulation.simulate()
