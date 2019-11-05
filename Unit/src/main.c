#include "main.h"

#include <avr/io.h>
#include <avr/interrupt.h>

#define F_CPU 16E6	// Frequency definition for delay.h
#include <util/delay.h>

#include "UART.h"
#include "sensors.h"
#include "rollerShutter.h"
#include "portManipulator.h"
#include "serial.h"
#include "scheduler.h"
#include "ledKeyUnit.h"
#include "userPreferenceHandler.h"

#define TEMPERATURE_TASK_PERIOD 100
#define LIGHT_TASK_PERIOD 50
#define LEDKEYUNIT_TASK_PERIOD 25
#define LEDKEYUNITBUTTONREADING_TASK_PERIOD 4


void setup(void) {
	DDRB = 0xFF;
	DDRD = (1 << PIND5) | (1 << PIND6) | (1 << PIND7);
	
	initUART();
	initPortManipulator();
	initLedKeyUnit();
	initUserPreferenceHandler();
	init_SCH();

	_delay_ms(1000);
}

void tempTask(void);

void init_SCH(void)
{
	SCH_Init_T1();

	SCH_Add_Task(&temperature_task, 0, TEMPERATURE_TASK_PERIOD);
	SCH_Add_Task(&light_task, 0, LIGHT_TASK_PERIOD);
	SCH_Add_Task(&ledKeyUnit_task, 0, LEDKEYUNIT_TASK_PERIOD);
	SCH_Add_Task(&ledKeyUnitButtonReading_task, 0, LEDKEYUNITBUTTONREADING_TASK_PERIOD);
	SCH_Add_Task(&rollerShutterAnimate, 0, 100);
	SCH_Add_Task(&handleInstructions, 0, 5);
}


void temperature_task(void)
{
	int8_t temperatureReading = (int8_t)getTemperature();
	if(temperatureReading != -1)
		addTemperatureToBuffer(temperatureReading);
}

void light_task(void)
{
	int8_t lightReading = (int8_t)getLightIntensity();
	if(lightReading != -1)
		addLightToBuffer(lightReading);
}

void ledKeyUnit_task(void)
{
	int8_t temperatureReading = (int8_t)getTemperature();
	int8_t lightReading = (int8_t)getLightIntensity();
	updateLedKeyUnit(temperatureReading, lightReading);
}

void ledKeyUnitButtonReading_task(void)
{
	updateButtonReadings(readButtons());
}

int main(void)
{
	setup();
	setRollerShutterMoving();
	
	SCH_Start();

	return 0;
}

//Interrupt Service Routine for when data is received.
ISR(USART_RX_vect)
{
	//Checks if any data has been sent.
	if (UCSR0A & (1<<RXC0)) {
		unsigned char data = UDR0;

		//Stores the data in the received_data queue, so it can handle the received data at a later moment.
    	received_data[received_data_index] = data;
    	received_data_index = (received_data_index + 1) % RECEIVED_DATA_SIZE;
	}
}
