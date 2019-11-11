#ifndef ULTRASONIC_H_
#define ULTRASONIC_H_

#include <avr/io.h>
#include <avr/interrupt.h>
#define F_CPU 16E6
#include <util/delay.h>

#define MAX_SECONDS 25E-3
#define MAX_CYCLES MAX_SECONDS * F_CPU

#define ECHO_PORT _BV(PD3)
#define TRIG_PORT _BV(PD2)

#define COUNTER_MULTIPLIER 8
#define CYCLES_TO_CM_DIVIDER (58 * 16)

#define PRESCALER_VALUE _BV(CS10)	// CS10 -> no prescaler, run on F_CPU
#define TIMER1_OVF_INT _BV(TOIE1)

#define MIN_DISTANCE_VALUE 35
#define MAX_DISTANCE_VALUE 70

void init_ultrasonic(void);
float measure_distance(void);

#endif /* ULTRASONIC_H_ */
