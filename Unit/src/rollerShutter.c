#include "portManipulator.h"

#define F_CPU 16E6    // Frequency definition for delay.h
#include <util/delay.h>


uint8_t animationActive = 0;
uint8_t animationState = 0;


void setRollerShutterClosed() {
	digitalWrite('B', 0x0F, 0x08);
}

void setRollerShutterOpen() {
	digitalWrite('B', 0x0F, 0x01);
}


void setRollerShutterMoving() {
	animationActive = 1;
}

void setRollerShutterStill() {
	animationActive = 0;
}


void rollerShutterAnimate() {
	if(animationActive == 1) {
		if (animationState == 0) {
			digitalWrite(&PORTB, 0x0F, 0x02);
			animationState = 1;
		} else {
			digitalWrite(&PORTB, 0x0F, 0x04);
			animationState = 0;
		}
	}
}
