import asyncio
import requests
from bleak import BleakScanner

SERVER_URL = "http://localhost:5000/data"

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

    print(f"{name} | RSSI: {rssi} | {movement}")


async def main():
    scanner = BleakScanner(detection_callback)

    print("Scanning started...\n")

    await scanner.start()
    await asyncio.sleep(5) 
    await scanner.stop()

asyncio.run(main())