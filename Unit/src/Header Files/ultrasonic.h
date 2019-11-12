#ifndef ULTRASONIC_H_
#define ULTRASONIC_H_

#include <avr/io.h>
#include <avr/interrupt.h>
#define F_CPU 16E6
#include <util/delay.h>

#define MAX_CENTIMETERS 400U
#define MAX_CYCLES UINT16_MAX / 8 - 1000

#define ECHO_PORT _BV(PD3)
#define TRIG_PORT _BV(PD2)

#define COUNTER_MULTIPLIER 8
#define CYCLES_TO_CM_DIVIDER (58 * 16)

#define PRESCALER_VALUE _BV(CS11)	// CS11 -> 8 prescaler
#define TIMER1_OVF_INT _BV(TOIE1)

#define MIN_DISTANCE_VALUE 2
#define MAX_DISTANCE_VALUE 70

void init_ultrasonic(void);
uint8_t measure_distance(void);

#endif /* ULTRASONIC_H_ */
