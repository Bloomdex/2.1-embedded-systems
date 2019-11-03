#include "rollerShutter.h"

#include "scheduler.h"
#include "portManipulator.h"

#define F_CPU 16E6    // Frequency definition for delay.h
#include <util/delay.h>


uint8_t animationActive = 0;


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
		digitalWrite(&PORTB, 0x0F, (1 << PINB1));
		SCH_Add_Task(&rollerShutterAnimate_part_2, 100, 0); // add task with delay 100 ticks, 1 tick is 10ms
	}
}
