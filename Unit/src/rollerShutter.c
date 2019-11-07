#include <avr/io.h>

#include "rollerShutter.h"

#include "scheduler.h"
#include "portManipulator.h"

#define F_CPU 16E6    // Frequency definition for delay.h
#include <util/delay.h>

enum rollerShutterState {shutterForceClosed, shutterClosed, shutterClosing, shutterOpening, shutterOpened, shutterForceOpened};
enum rollerShutterState currentRollerShutterState = shutterOpened;


void setRollerShutterClosed() {
	digitalWrite(&PORTB, 0x0F, (1 << PINB3));
}

void setRollerShutterOpened() {
	digitalWrite(&PORTB, 0x0F, (1 << PINB0));
}

void setRollerShutterAnimating() {
	static uint8_t portValues = 0x02;
	portValues = ~portValues;
	
	digitalWrite(&PORTB, 0x06,  portValues);
}

void rollerShutterUpdate(int8_t temperature, int8_t lightIntensity, int8_t prefferedTemperature, int8_t prefferedLightIntensity) {
	if(currentRollerShutterState == shutterForceClosed
		|| (currentRollerShutterState != shutterForceClosed && temperature >= prefferedTemperature && lightIntensity >= prefferedLightIntensity)) 
	{
		// HIER CODE DIE KIJKT HOE VER DE ULTRASOONSENSOR IS
		currentRollerShutterState = shutterClosed;
	}
	else if(currentRollerShutterState == shutterForceOpened
		|| (currentRollerShutterState != shutterForceOpened && temperature < prefferedTemperature)
		|| (currentRollerShutterState != shutterForceOpened && lightIntensity < prefferedLightIntensity))
	{
		// HIER CODE DIE KIJKT HOE VER DE ULTRASOONSENSOR IS
		currentRollerShutterState = shutterOpened;
	}

	// Do actions based on the current state
	if(currentRollerShutterState == shutterClosing || currentRollerShutterState == shutterOpening)
		setRollerShutterAnimating();
	else if(currentRollerShutterState == shutterClosed || currentRollerShutterState == shutterForceClosed)
		setRollerShutterClosed();
	else if(currentRollerShutterState == shutterOpened || currentRollerShutterState == shutterForceOpened)
		setRollerShutterOpened();
}
