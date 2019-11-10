#include "ultrasonic.h"

volatile uint8_t overflows = 0;

static void init(void)
{
	// setup ports
	DDRD |= TRIG_PORT;
	DDRD &= ~ECHO_PORT;

	// pull-down
	PORTD &= ~TRIG_PORT;
	_delay_us(2);

	// init timer
	TCNT1 = 0;
	TCCR1A = 0;
	TCCR1B = 0;
	TCCR1C = 0;
	TIMSK1 = 0;
	TIMSK1 |= TIMER1_OVF_INT;

	// set overflows to 0
	overflows = 0;
}

static void cleanup(void)
{
	stop_timer();
}

static void start_timer(void)
{
	TCCR1B |= PRESCALER_VALUE;
}

static void stop_timer(void)
{
	TCCR1B &= ~(_BV(CS12) | _BV(CS11) | _BV(CS10));
}

int8_t measure_distance(void)
{
	init();

	// send 10µs pulse to TRIG_PORT
	PORTD |= TRIG_PORT;
	_delay_us(10);
	PORTD &= ~TRIG_PORT;

	// wait for echo pulse to come back
	while (!(PIND & ECHO_PORT));

	start_timer();
	while (PIND & ECHO_PORT)
	{
		// check that the pulse doesn't take too long
		if ((overflows * UINT16_MAX) + TCNT1 > MAX_CYCLES)
		{
			cleanup();
			return -1;
		}
	}
	// echo pulse is finished
	cleanup();

	uint32_t total_cycles = overflows * UINT16_MAX + TCNT1;
	uint16_t cm = total_cycles / CYCLES_TO_CM_DIVIDER;
	// return decimeters so it fits within int8_t which is used as the 
	// standard data transfer type
	return (int8_t)(cm / 10);
}

ISR(TIMER1_OVF_vect)
{
	overflows++;
}
