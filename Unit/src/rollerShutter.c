#include <avr/io.h>

#include "rollerShutter.h"

#include "scheduler.h"
#include "portManipulator.h"

#define F_CPU 16E6    // Frequency definition for delay.h
#include <util/delay.h>

uint8_t forcedState = 0;

enum rollerShutterState { shutterClosed, shutterClosing, shutterOpening, shutterOpened, none };
enum rollerShutterState currentRollerShutterState = none;	// Never change current
enum rollerShutterState targetRollerShutterState = none;	// Only change target


void setRollerShutterClosed() {
	digitalWrite(&PORTB, 0x0F, (1 << PINB0));
}

void setRollerShutterOpened() {
	digitalWrite(&PORTB, 0x0F, (1 << PINB3));
}

void setRollerShutterAnimating() {
	static uint8_t portValues = 0x02;
	portValues = ~portValues;
	
	digitalWrite(&PORTB, 0x09,  0);
	digitalWrite(&PORTB, 0x06,  portValues);
}


void setShutterForceClosed() {
	forcedState = 1;
	targetRollerShutterState = shutterClosing;
}
void setShutterForceOpened() {
	forcedState = 1;
	targetRollerShutterState = shutterOpening;
}
void setShutterFreed() {
	forcedState = 0;
}


void rollerShutterUpdate(int8_t temperature, int8_t lightIntensity, int8_t prefferedTemperature, int8_t prefferedLightIntensity) {
	// Determine which static state the rollerShutter is in
	if(currentRollerShutterState != targetRollerShutterState) {
		if(targetRollerShutterState == shutterClosing && currentRollerShutterState != shutterClosed) {
			setRollerShutterAnimating();
			transmitData(1);
			
			if(1) { // ----ATTENTION----: In deze if moet gekeken worden naar ultrasoon data
				targetRollerShutterState = shutterClosed;
				currentRollerShutterState = shutterClosed;
				setRollerShutterClosed();
			}
		}
		else if(targetRollerShutterState == shutterOpening && currentRollerShutterState != shutterOpened) {
			setRollerShutterAnimating();
			transmitData(1);
			
			if(1) { // ----ATTENTION----: In deze if moet gekeken worden naar ultrasoon data
				targetRollerShutterState = shutterOpened;
				currentRollerShutterState = shutterOpened;
				setRollerShutterOpened();
			}
		}
	}
	
	// Determine the next target state 
	if(forcedState == 0) { // If the target is not being forced by a basestation
		if(temperature >= prefferedTemperature && lightIntensity >= prefferedLightIntensity)
			targetRollerShutterState = shutterClosing;
		else
			targetRollerShutterState = shutterOpening;
	}
}
