/*
 * Sweeping Arms.c
 *
 * Created: 4/25/2019 2:57:34 AM
 * Author : imals
 */ 

//This ensures that the servos function properly. Without a defined clock cycle, the motors don't move.
#ifndef F_CPU
#define F_CPU 8000000UL		//Changing this changes the range in which the claw opens. Somehow. Readjusted claw location in order to compensate change.
#endif

#include <avr/io.h>
#include <util/delay.h>
#include "timer.h"

enum servoFSM {Neutral, Sweep}servoState;
int button;

void sweepFunct(){
	switch(servoState){
		case Neutral:
			if (button == 0x01)
				servoState = Sweep;
			else
				servoState = Neutral;
			break;
		case Sweep:
			if (button == 0x01)
				servoState = Sweep;
			else
				servoState = Neutral;
		default:
			servoState = Neutral;
			break;
	}
	switch(servoState){
		case Neutral:
			break;
		case Sweep:
			for (int i = 0; i < 5; i++){							//5 is arbitrary
				PORTD = 0x01;										//Enable PORTD
				_delay_us(1000);									//Signal enabled for 1ms.
				PORTD = 0x00;										//Disable PORTD
				_delay_ms(19);										//Signal disabled for 19ms.
			}
			for (int i = 0; i < 5; i++){		//Arbitrary 5
				PORTD = 0x01;						//Enable the correct port for corresponding servo.
				_delay_us(2000);						//Open signal up (Duty cycle = 10%)
				PORTD = 0x00;						//Disable the port
				_delay_ms(18);							//Open signal down (Down = 90%)
			}
			break;
		default:
			break;
	}
}

int main(void){
	DDRB = 0xFF; PORTB = 0x00;			//PORTB is input, via button.
    DDRD = 0x00; PORTD = 0xFF;			//Servo PWM, set to output
	TimerSet(50);
	TimerOn();
	
    while (1) {
		button = ~PINB;
		sweepFunct();
		while(!TimerFlag);
		TimerFlag = 0;
    }
}

