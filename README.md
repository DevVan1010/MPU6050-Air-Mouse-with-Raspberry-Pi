# MPU6050 Air Mouse with Raspberry Pi

This project turns an MPU6050 accelerometer and gyroscope sensor into an air mouse using a Raspberry Pi. The sensor data is used to control the mouse cursor on the screen.

## Table of Contents
- [Hardware Requirements](#hardware-requirements)
- [Setup Instructions](#setup-instructions)
- [Wiring Diagram](#wiring-diagram)
- [Software Installation](#software-installation)
- [Running the Script](#running-the-script)
- [Troubleshooting](#troubleshooting)
- [License](#license)
- [Contributing](#contributing)
- [Acknowledgments](#acknowledgments)

## Hardware Requirements
- Raspberry Pi (any model with GPIO pins)
- MPU6050 sensor
- Jumper wires (female-to-female or male-to-female)
- Power supply for Raspberry Pi

## Setup Instructions
### 1. Enable I2C on Raspberry Pi
Open the Raspberry Pi configuration tool:

```bash
sudo raspi-config
```
Navigate to `Interface Options → I2C → Yes`.

Reboot the Raspberry Pi:

```bash
sudo reboot
```

### 2. Install Required Software
Update your system and install the necessary libraries:

```bash
sudo apt update
sudo apt upgrade
sudo apt install i2c-tools python3-smbus python3-evdev
```

## Wiring Diagram
Connect the MPU6050 to the Raspberry Pi as follows:

```
MPU6050    Raspberry Pi
VCC    →    3.3V (Pin 1)
GND    →    GND (Pin 6/9/14/20/25/etc)
SDA    →    GPIO2 (SDA, Pin 3)
SCL    →    GPIO3 (SCL, Pin 5)
```
> **Note:** Do not connect the MPU6050 to 5V, as it may damage the sensor.

## Software Installation
Clone this repository or download the script:

```bash
git clone https://github.com/your-username/mpu6050-air-mouse.git
cd mpu6050-air-mouse
```

Make the script executable:

```bash
chmod +x mpu6050_mouse.py
```

## Running the Script
Run the script with `sudo`:

```bash
sudo python3 mpu6050_mouse.py
```

### Calibration:
- Keep the MPU6050 sensor flat and still during the calibration phase.
- The script will automatically calibrate the sensor.

### Control the Mouse:
- Tilt the MPU6050 sensor to move the mouse cursor.
- The cursor will move based on the sensor's orientation.

## Troubleshooting
### No Cursor Movement?
- Check the wiring.
- Verify that the MPU6050 is detected:

```bash
sudo i2cdetect -y 1
```

You should see `0x68` (or `0x69` if AD0 is pulled high).

- Add debug prints to check sensor data:

```python
print(f"Accel: X={x:.2f}, Y={y:.2f}, Z={z:.2f}")
```

- Ensure `/dev/uinput` has proper permissions:

```bash
sudo chmod 0666 /dev/uinput
```

### Cursor Movement Too Slow/Fast?
Adjust the `SENSITIVITY` variable in the script:

```python
SENSITIVITY = 25  # Increase or decrease as needed
```

### Cursor Drifting?
Recalibrate the sensor by keeping it flat and still during the calibration phase.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request.

## Acknowledgments
Thanks to the Raspberry Pi community for their support.

Inspired by various MPU6050 projects online.
