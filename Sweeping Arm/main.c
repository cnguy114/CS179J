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
bool isSweeping;		//True once cycles are complete. False otherwise.

void sweepFunct(){
	switch(servoState){
		case Neutral:
			if (button == 0x01)
				servoState = Sweep;
			else
				servoState = Neutral;
			break;
		case Sweep:
			if (isSweeping)
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
			PORTD = 0x01;		//Enable the correct port for corresponding servo.
			_delay_us(2000);						//Open signal up (Duty cycle = 10%)
			PORTD = 0x00;						//Disable the port
			_delay_ms(18);							//Open signal down (Down = 90%)
			break;
		default:
			break;
	}
}

int main(void){
  DDRD = 0x00; PORTD = 0xFF;			//Not sure if other ports needed.
	TimerSet(50);
	TimerOn();
	
    while (1) {
		  sweepFunct();
		  while(!TimerFlag);
		  TimerFlag = 0;
    }
}
