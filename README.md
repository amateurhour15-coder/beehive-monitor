# Bee Hive Weight & Environment Monitor (Raspberry Pi Zero W)

## Hardware
- Raspberry Pi Zero W
- 4x Load cells + 4x HX711 amplifier modules
- 2x BME280 sensors (I2C, addresses 0x76 and 0x77)
- MicroSD card (16GB+)
- Weatherproof enclosure
- 5V power supply (solar/battery recommended)

## Wiring
- Each load cell connects to its own HX711 (E+, E-, A+, A-).
- HX711 DT/SCK pins to Pi GPIOs: (5/6, 13/19, 20/21, 26/16).
- Both BME280 sensors connect to I2C bus: SDA (GPIO2), SCL (GPIO3).
  - Set inside sensor to address 0x76, outside sensor to 0x77 (see BME280 datasheet).
- All modules powered from Pi 5V/GND.

## Installation Steps

1. **Flash Raspberry Pi OS Lite** to SD card and boot Pi.
2. **Enable I2C:**  
   Run `sudo raspi-config` → Interface Options → I2C → Enable.  
   Reboot after enabling.
3. **System Update:**  
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv git
   ```
4. **Clone/download project files.**
5. **Create and activate a virtual environment:**  
   ```bash
   python3 -m venv ~/beehive-venv
   source ~/beehive-venv/bin/activate
   ```
6. **Install dependencies:**  
   ```bash
   pip install -r requirements.txt
   ```
7. **Create folders:**  
   Ensure `templates/` folder exists, and put `index.html` inside.
8. **Run the monitor:**  
   ```bash
   python beehive_monitor.py
   ```
9. **Access the web interface:**  
   Open `http://raspberrypi.local:5000` or Pi's IP address in your browser.

## Troubleshooting

### I2C Not Detected
- Ensure I2C is enabled in `raspi-config` and reboot.
- Check with `ls /dev/i2c*` (should list `/dev/i2c-1`).
- Use `sudo apt install i2c-tools` and `i2cdetect -y 1` to confirm sensor(s) are detected.

### pip install error: "externally-managed-environment"
- Use a virtual environment as shown above.

### busio or board import error
- Ensure you installed `adafruit-blinka` in the virtual environment.

### RPi.GPIO error
- Install with `pip install RPi.GPIO` in your virtualenv.

### No Hardware I2C error
- Confirm wiring to GPIO2 (SDA, pin 3) and GPIO3 (SCL, pin 5).
- Confirm I2C enabled and sensors connected.

## Measurements Logged
- Weight (total and individual)
- Inside temperature, humidity, pressure
- Outside temperature, humidity, pressure

## Graphs Provided
- Individual: Weight, Inside Temp, Inside Humidity, Outside Temp, Outside Humidity, Inside Pressure, Outside Pressure
- Combo: Inside Temp+Hum, Outside Temp+Hum, Weight+Inside Temp+Inside Hum
- All Data: Weight, Inside/Outside Temp, Inside/Outside Humidity, Inside/Outside Pressure

## Tips for Mounting Sensors
- **Load cells:** Mount at each hive corner, ensure stable/level base.
- **HX711 modules:** Inside enclosure, use short wires to load cells.
- **BME280 inside:** Shielded inside hive, away from bees/honey.
- **BME280 outside:** Protected from rain/sun, ideally shaded.

## Weatherproof Enclosure
- Use IP65/IP67 rated box.
- Add cable glands for sensor wires.
- Use mesh vent for condensation prevention.

## Power
- Use 5V solar battery pack for off-grid operation.
- Shut down Pi cleanly to avoid SD card corruption.

## Data & Graphs
- All data stored in `beehive_data.db` (SQLite).
- Web graphs regenerate from saved data automatically after reboot.
