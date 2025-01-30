# -*- coding: utf-8 -*-
# MPU6050 Air Mouse Script
# Author: Jurado, Van Dan 
# Description: This script turns an MPU6050 sensor into an air mouse using a Raspberry Pi.
# License: MIT License (Feel free to modify and share, but attribution is appreciated!)

import smbus
import time
import math
from evdev import UInput, ecodes as e

# Initialize I2C
bus = smbus.SMBus(1)
address = 0x68  # MPU6050 I2C address

# Wake up MPU6050
bus.write_byte_data(address, 0x6B, 0x01)

# Configure accelerometer range (+/-8g)
bus.write_byte_data(address, 0x1C, 0x10)

# Configure gyroscope range (+/-250°/s)
bus.write_byte_data(address, 0x1B, 0x00)

# Create virtual mouse
capabilities = {
    e.EV_KEY: [e.BTN_LEFT, e.BTN_RIGHT],
    e.EV_REL: [e.REL_X, e.REL_Y, e.REL_WHEEL]
}

try:
    ui = UInput(capabilities, name='MPU6050-Mouse')
except Exception as e:
    print(f"Failed to create UInput device: {e}")
    print("Ensure /dev/uinput exists and has proper permissions.")
    exit(1)

# Conversion factor for accelerometer (±8g range)
ACCEL_CONVERSION = 4096.0

# Dead zone to ignore small movements
DEAD_ZONE = 0.05

# Sensitivity adjustment
SENSITIVITY = 25

def read_word_2c(reg):
    """Read a 16-bit signed value from the MPU6050."""
    high = bus.read_byte_data(address, reg)
    low = bus.read_byte_data(address, reg+1)
    val = (high << 8) + low
    
    if val >= 0x8000:
        return -((65535 - val) + 1)
    else:
        return val

def get_accel():
    """Retrieve accelerometer values from the MPU6050."""
    x = read_word_2c(0x3B) / ACCEL_CONVERSION
    y = read_word_2c(0x3D) / ACCEL_CONVERSION
    z = read_word_2c(0x3F) / ACCEL_CONVERSION
    return x, y, z

# Calibration
print("Calibrating... Keep sensor flat and still!")
time.sleep(2)
sum_x = sum_y = 0
CALIBRATION_SAMPLES = 100

for _ in range(CALIBRATION_SAMPLES):
    x, y, z = get_accel()
    sum_x += x
    sum_y += y
    time.sleep(0.01)

offset_x = sum_x / CALIBRATION_SAMPLES
offset_y = sum_y / CALIBRATION_SAMPLES

print(f"Calibration complete. Offsets: X={offset_x:.2f}g, Y={offset_y:.2f}g")

try:
    while True:
        x, y, z = get_accel()
        print(f"Raw Accel: X={x:.2f}, Y={y:.2f}, Z={z:.2f}")
        
        # Apply calibration offsets
        x -= offset_x
        y -= offset_y
        
        # Apply dead zone
        if abs(x) < DEAD_ZONE:
            x = 0
        if abs(y) < DEAD_ZONE:
            y = 0
            
        # Calculate mouse movement
        move_x = int(x * SENSITIVITY)
        move_y = int(y * SENSITIVITY)
        
        # Send mouse events
        if move_x != 0 or move_y != 0:
            print(f"Sending mouse movement: X={move_x}, Y={move_y}")
            ui.write(e.EV_REL, e.REL_X, move_x)
            ui.write(e.EV_REL, e.REL_Y, move_y)
            ui.syn()
        
        time.sleep(0.01)

except KeyboardInterrupt:
    print("\nExiting...")
    ui.close()
