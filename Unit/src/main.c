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
#include "dataHandler.h"

#define UPDATESENSORDATA_TASK_PERIOD 3
#define TEMPERATURE_TASK_PERIOD 100
#define LIGHT_TASK_PERIOD 50
#define LEDKEYUNIT_TASK_PERIOD 25
#define LEDKEYUNITBUTTONREADING_TASK_PERIOD 4
#define ROLLERSHUTTER_TASK_PERIOD 70
#define HANDLEINSTRUCTIONS_PERIOD 5


void setup(void) {
	DDRB = (1 << PIND0) | (1 << PIND1) | (1 << PIND2) | (1 << PIND3) | (1 << PIND4);
	DDRD = (1 << PIND5) | (1 << PIND6) | (1 << PIND7);
	
	initUART();
	initPortManipulator();
	initLedKeyUnit();
	initUserPreferenceHandler();
	init_SCH();

	_delay_ms(1000);
}

void init_SCH(void)
{
	SCH_Init_T1();

	SCH_Add_Task(&updateSensorData_task, 0, UPDATESENSORDATA_TASK_PERIOD);
	SCH_Add_Task(&temperature_task, 0, TEMPERATURE_TASK_PERIOD);
	SCH_Add_Task(&light_task, 0, LIGHT_TASK_PERIOD);
	SCH_Add_Task(&ledKeyUnit_task, 0, LEDKEYUNIT_TASK_PERIOD);
	SCH_Add_Task(&ledKeyUnitButtonReading_task, 0, LEDKEYUNITBUTTONREADING_TASK_PERIOD);
	SCH_Add_Task(&rollerShutter_task, 0, ROLLERSHUTTER_TASK_PERIOD);
	SCH_Add_Task(&handleInstructions, 0, HANDLEINSTRUCTIONS_PERIOD);
}

void updateSensorData_task(void) {
	int8_t temperatureReading = (int8_t)getTemperature();
	int8_t lightReading = (int8_t)getLightIntensity();
	
	updateSensorData(temperatureReading, lightReading);
}

void temperature_task(void)
{
	int8_t temperatureReading = (int8_t)getTemperature();
	currentTemperatureReading = getTemperatureMod();

	if(temperatureReading != INVALID_READING_VALUE)
		addTemperatureToBuffer(temperatureReading);
}

void light_task(void)
{
	int8_t lightReading = (int8_t)getLightIntensity();
	currentLightReading = getLightIntensityMod();

	if(lightReading != INVALID_READING_VALUE)
		addLightToBuffer(lightReading);
}

void ledKeyUnit_task(void)
{
	updateLedKeyUnit(getTemperatureMod(), getLightIntensityMod());
}

void ledKeyUnitButtonReading_task(void)
{
	updateButtonReadings(readButtons());
}

void rollerShutter_task(void)
{
	rollerShutterUpdate(getTemperatureMod(), getLightIntensityMod(), getUserTempPreference(), getUserLightPreference());
}

int main(void)
{
	setup();
	
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
