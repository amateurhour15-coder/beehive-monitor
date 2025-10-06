# Bee Hive Weight & Environment Monitor (Raspberry Pi Zero W)

## Hardware
- Raspberry Pi Zero W
- 4x Load cell + 4x HX711 amplifier modules
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
2. **Enable I2C**:  
   Run `sudo raspi-config` → Interfacing Options → I2C → Enable.
3. **System Update:**  
   ```bash
   sudo apt update
   sudo apt install python3-pip git
   ```
4. **Clone/download project files.**
5. **Install dependencies:**  
   ```bash
   pip3 install -r requirements.txt
   ```
6. **Create folders:**  
   Ensure `templates/` folder exists, and put `index.html` inside.
7. **Run the monitor:**  
   ```bash
   python3 beehive_monitor.py
   ```
8. **Access the web interface:**  
   Open `http://raspberrypi.local:5000` or Pi's IP address in your browser.

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

## Measurements Logged
- Weight (total and individual)
- Inside temperature, humidity, pressure
- Outside temperature, humidity, pressure

## Graphs Provided
- Individual: Weight, Inside Temp, Inside Humidity, Outside Temp, Outside Humidity, Inside Pressure, Outside Pressure
- Combo: Inside Temp+Hum, Outside Temp+Hum, Weight+Inside Temp+Inside Hum
- All Data: Weight, Inside/Outside Temp, Inside/Outside Humidity, Inside/Outside Pressure

## Troubleshooting
- If sensors are not detected, check wiring and I2C addresses.
- If Flask does not start, check for missing modules in Python.
