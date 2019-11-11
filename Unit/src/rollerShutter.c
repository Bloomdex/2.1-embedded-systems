#include <avr/io.h>
#include <stdlib.h>

#include "rollerShutter.h"

#include "scheduler.h"
#include "portManipulator.h"
#include "ultrasonic.h"

#define F_CPU 16E6    // Frequency definition for delay.h
#include <util/delay.h>

#define LED_OFF_PIN 0
#define LED_INDICATOR_PIN_1 1
#define LED_INDICATOR_PIN_2 2
#define LED_INDICATOR_PIN_3 3
#define LED_ON_PIN 4

uint8_t forcedState = 0;

enum rollerShutterState { shutterClosed, shutterClosing, shutterOpening, shutterOpened, none };
enum rollerShutterState currentRollerShutterState = none;	// Never change current
enum rollerShutterState targetRollerShutterState = none;	// Only change target


void setRollerShutterClosed() {
	digitalWrite(&PORTB, 0x1F, (1 << LED_OFF_PIN));
}

void setRollerShutterOpened() {
	digitalWrite(&PORTB, 0x1F, (1 << LED_ON_PIN));
}

void setRollerShutterAnimating(uint8_t openOrClosed) {
	// 0 animates towards the LED_ON_PIN
	// 1 animates towards the LED_OFF_PIN
	static uint8_t i = 1;
	uint8_t ledValues;
	
	// Determine the animation direction
	if(openOrClosed == 0)
		ledValues = i;
	else
		ledValues = 4 - i;
	
	// Determine the final portValues and apply them
	uint8_t portValues = (1 << ledValues);
	
	digitalWrite(&PORTB, 0x11,  0);
	digitalWrite(&PORTB, 0x0E,  portValues);
	
	// Increment i and determine if it is out of bounds
	i += 1;
	
	if(i == 4)
		i = 1;
	else if(i == 1)
		i = 4;
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
uint8_t getShutterForcedState() {
	return forcedState;
}

uint8_t getRollerShutterState() {
	return (uint8_t)currentRollerShutterState;
}

static uint8_t distanceClosestToMax(int8_t distance)
{
	return abs(distance - MAX_DISTANCE_VALUE) < abs(distance - MIN_DISTANCE_VALUE);
}

void rollerShutterUpdate(int8_t temperature, int8_t lightIntensity, int8_t prefferedTemperature, int8_t prefferedLightIntensity, int8_t distanceMeasurement) {
	// Determine which static state the rollerShutter is in
	if(currentRollerShutterState != targetRollerShutterState) {
		if(targetRollerShutterState == shutterClosing && currentRollerShutterState != shutterClosed) {
			setRollerShutterAnimating(1);
			
			// if distanceMeasurement is closer to being closed than being opened
			if(distanceClosestToMax(distanceMeasurement)) {
				targetRollerShutterState = shutterClosed;
				currentRollerShutterState = shutterClosed;
				setRollerShutterClosed();
			}
		}
		else if(targetRollerShutterState == shutterOpening && currentRollerShutterState != shutterOpened) {
			setRollerShutterAnimating(0);
			
			if(!distanceClosestToMax(distanceMeasurement)) {
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
