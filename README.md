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

#### Groups

To make serial-communication work using pySerial your local user has to be part of the `dialout` group. You can check this using the `groups` command. If not, add your user to the dialout group:

```
sudo usermod -a -G dialout USERNAME
```

#### Running

```
cd Basestation/
source venv/bin/activate
python3 main.py
```

### Windows

#### Installing

```
cd Basestation/
python -m venv venv
venv\Scripts\activate  
pip install -r requirements.txt
```

#### Running

```
cd Basestation/
venv\Scripts\activate  
python main.py
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

## Arduino schematics

![](https://i.imgur.com/DcspXkq.png)
