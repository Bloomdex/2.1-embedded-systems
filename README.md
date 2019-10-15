# Project Embedded Systems

## Installing & Running Basestation

### Linux (Debian-based)

#### Installing

```
sudo apt install python3-venv
cd Basestation/
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Running

```
cd Basestation/
source venv/bin/activate
python3 main.py
```

## Generating Unit Firmware

### Linux (Debian-based)

#### Compiling

```
sudo apt install avr-gcc
cd Unit/
make
```

#### Flashing

```
sudo apt install avrdude
cd Unit/
make COM=/dev/ttyACM0 flash # where ttyACM0 is your com-dev
```
