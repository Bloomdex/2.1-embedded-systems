PROGNAME=firmware
MCU=atmega328p
F_CPU=16000000
CC=avr-gcc
OBJCOPY=avr-objcopy
CFLAGS=-Os -I. -I../include -Wall -gdwarf-2
MAIN=main
VCD_OUTPUT=output.vcd
COM=/dev/ttyACM0

all:
	mkdir -p bin
	$(CC) $(CFLAGS) -DF_CPU=$(F_CPU) -mmcu=$(MCU) -c -o bin/$(MAIN).o src/$(MAIN).c
	$(CC) -DF_CPU=$(F_CPU) -mmcu=$(MCU) -o bin/$(MAIN).elf bin/$(MAIN).o
	$(OBJCOPY) -O ihex bin/$(MAIN).elf bin/$(MAIN).hex

debug:
	simavr -m $(MCU) -f $(F_CPU) bin/$(MAIN).elf -g

simulate:
	simulavr -c vcd:trace.txt:$(VCD_OUTPUT)  -f bin/$(MAIN).elf -d atmega328 -F $(F_CPU)

flash:
	avrdude -F -V -c arduino -p $(MCU) -P $(COM) -b 115200 -U flash:w:bin/$(MAIN).hex
