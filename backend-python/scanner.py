import asyncio
import requests
from bleak import BleakScanner

import math
import random


device_angles = {}

def get_position(address, distance):
    if address not in device_angles:
        device_angles[address] = random.uniform(0, 2 * math.pi)

    angle = device_angles[address]
    angle += 0.05
    device_angles[address] = angle

    x = distance * math.cos(angle)
    y = distance * math.sin(angle)

    return x, y





SERVER_URL = "http://localhost:5000/data"


def rssi_to_distance(rssi):
    TX_POWER = -59   
    n = 2            

    distance = 10 ** ((TX_POWER - rssi) / (10 * n))
    return distance



previous_rssi = {}

def detection_callback(device, advertisement_data):
    global previous_rssi

    name = device.name if device.name else "Unknown"
    address = device.address
    rssi = advertisement_data.rssi

    movement = "No Movement"

    if address in previous_rssi:
        diff = abs(rssi - previous_rssi[address])

        if diff > 2:
            movement = "Movement Detected"

    previous_rssi[address] = rssi

    # print(f"{name} | Current RSSI: {rssi} | {movement}")
    distance = rssi_to_distance(rssi)

    distance = rssi_to_distance(rssi)
    scaled_distance = distance * 100 

    x, y = get_position(address, scaled_distance)

    print(f"{name} | RSSI: {rssi} | Distance: {round(distance,2)} | {movement} | Pos: ({int(x)}, {int(y)})")


async def main():
    scanner = BleakScanner(detection_callback)

    print("Scanning started...\n")

    await scanner.start()
    await asyncio.sleep(10) 
    await scanner.stop()

asyncio.run(main())