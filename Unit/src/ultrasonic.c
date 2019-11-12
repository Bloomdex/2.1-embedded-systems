#include "ultrasonic.h"

static void start_timer(void)
{
	TCCR1B |= PRESCALER_VALUE;
}

static void stop_timer(void)
{
	TCCR1B &= ~(_BV(CS12) | _BV(CS11) | _BV(CS10));
}

static void reset_timer(void)
{
	TCNT1 = 0;
}

static void cleanup(void)
{
	stop_timer();
	reset_timer();
}

static uint32_t total_cycles(void)
{
	return TCNT1 * 8;
}

/* init_ultrasonic
 * Prepare ports and timer settings for measuring distance with the ultrasonic
 * sensor.
*/
void init_ultrasonic(void)
{
	// setup ports
	DDRD |= TRIG_PORT;
	DDRD &= ~ECHO_PORT;

	// pull-down
	PORTD &= ~TRIG_PORT;
	_delay_us(2);

	// init timer
	TCCR1A = 0;
	TCCR1B = 0;
	TCCR1C = 0;
	TIMSK1 = 0;
	cleanup();
}

/* measure_distance
 * this is a synchronous, blocking version that measures distance with the
 * ultrasonic sensor.
 * 
 * It returns a float with the amount of centimeters measured.
*/
uint8_t measure_distance(void)
{
	cleanup();
	// send 10µs pulse to TRIG_PORT
	PORTD |= TRIG_PORT;
	_delay_us(10);
	PORTD &= ~TRIG_PORT;


	start_timer();
	// wait for echo pulse to come back
	while (!(PIND & ECHO_PORT))
	{
		// if the pulse doesn't come back within MAX_CYCLES
		if (total_cycles() > MAX_CYCLES)
		{
			// run cleanup and return -1 for invalid
			cleanup();
			return 0;
		}
	}
	cleanup();

	start_timer();
	while (PIND & ECHO_PORT)
	{
		// check that the pulse doesn't take too long
		if (total_cycles() > MAX_CYCLES)
		{
			return 0;
		}
	}
	// echo pulse is finished
	uint16_t cm = total_cycles() / CYCLES_TO_CM_DIVIDER;
	if (cm > UINT8_MAX)
		return UINT8_MAX;
	return (uint8_t)cm;
}
