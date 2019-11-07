#include <avr/io.h>

#include "rollerShutter.h"

#include "scheduler.h"
#include "portManipulator.h"

#define F_CPU 16E6    // Frequency definition for delay.h
#include <util/delay.h>

uint8_t forcedState = 0;

enum rollerShutterStaticState { shutterClosed, shutterOpened, none };
enum rollerShutterStaticState currentRollerShutterStaticState = none;

enum rollerShutterDynamicState { done, shutterClosing, shutterOpening };
enum rollerShutterDynamicState currentRollerShutterDynamicState = done;	// Never change current
enum rollerShutterDynamicState targetRollerShutterDynamicState = done;	// Only change target


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
	targetRollerShutterDynamicState = shutterClosing;
}
void setShutterForceOpened() {
	forcedState = 1;
	targetRollerShutterDynamicState = shutterOpening;
}
void setShutterFree() {
	forcedState = 0;
}


void rollerShutterUpdate(int8_t temperature, int8_t lightIntensity, int8_t prefferedTemperature, int8_t prefferedLightIntensity) {
	// Determine which static state the rollerShutter is in
	if(currentRollerShutterDynamicState != targetRollerShutterDynamicState) {
		if(targetRollerShutterDynamicState == shutterClosing && currentRollerShutterStaticState != shutterClosed) {
			setRollerShutterAnimating();
			
			if(1) { // ----ATTENTION----: In deze if moet gekeken worden naar ultrasoon data
				currentRollerShutterDynamicState = done;
				targetRollerShutterDynamicState = done;
				
				currentRollerShutterStaticState = shutterClosed;
				setRollerShutterClosed();
			}
		}
		else if(targetRollerShutterDynamicState == shutterOpening && currentRollerShutterStaticState != shutterOpened) {
			setRollerShutterAnimating();
			
			if(1) { // ----ATTENTION----: In deze if moet gekeken worden naar ultrasoon data
				currentRollerShutterDynamicState = done;
				targetRollerShutterDynamicState = done;
				
				currentRollerShutterStaticState = shutterOpened;
				setRollerShutterOpened();
			}
		}
	}
	
	// Determine the next target state 
	if(forcedState == 0) { // If the target is not being forced by a basestation
		if(temperature >= prefferedTemperature && lightIntensity >= prefferedLightIntensity)
			targetRollerShutterDynamicState = shutterClosing;
		else
			targetRollerShutterDynamicState = shutterOpening;
	}
}
