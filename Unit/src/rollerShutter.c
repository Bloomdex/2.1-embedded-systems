#include "rollerShutter.h"

#include "scheduler.h"
#include "portManipulator.h"

#define F_CPU 16E6    // Frequency definition for delay.h
#include <util/delay.h>


uint8_t animationActive = 0;
uint8_t animationState = 0;


void setRollerShutterClosed() {
	digitalWrite(&PORTB, 0x0F, (1 << PINB3));
}

void setRollerShutterOpen() {
	digitalWrite(&PORTB, 0x0F, (1 << PINB0));
}

void setRollerShutterMoving() {
	animationActive = 1;
}

void setRollerShutterStill() {
	animationActive = 0;
}

void rollerShutterAnimate_part_2(void)
{
	digitalWrite(&PORTB, 0x0F, (1 << PINB2));
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
