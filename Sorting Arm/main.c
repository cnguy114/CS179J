/*
 * Sorting Arm main.c file.
 * This is the code for the sorting arm portion of the recycling sorter project.
 * This code controls the stepper motors.
 */ 

#include <avr/io.h>
#include <stdlib.h>
#include "timer.h"

//The motors go A, AB, B, BC, C, CD, D, DA, A... Go in reverse order for counter-clockwise motion.
	//Pulled from 122a stepper lab
#define A 0x1			//0001
#define AB 0x3			//0011
#define B 0x2			//0010
#define BC 0x6			//0110
#define C 0x4			//0100
#define CD 0xC			//1100
#define D 0x8			//1000
#define DA 0x9			//1001

enum motorFSM{Start, Neutral, Left, Mid, Right}motorState;
unsigned char button;
unsigned int motor1;
unsigned int motor2;
int i1, i2;						//iterators for array
int stepArr = [A, AB, B, BC, C, CD, D, DA];

void MotorTick(){
	switch(motorState){
		case Start:
			i1 = 0;
			i2 = 0;
			motorState = Neutral;
			break;
		case Neutral:
			if (button == 0x01)
				motorState = Left;
			else if (button == 0x02)
				motorState = Mid;
			else if (button == 0x04)
				motorState = Right;
			else
				motorState = Neutral;
			break;
		case Left:
			if (button == 0x01)
				motorState = Left;
			else if (button == 0x02)
				motorState = Mid;
			else if (button == 0x04)
				motorState = Right;
			else
				motorState = Neutral;
			break;
		case Mid:
			if (button == 0x01)
				motorState = Left;
			else if (button == 0x02)
				motorState = Mid;
			else if (button == 0x04)
				motorState = Right;
			else
				motorState = Neutral;
			break;
		case Right:
			if (button == 0x01)
				motorState = Left;
			else if (button == 0x02)
				motorState = Mid;
			else if (button == 0x04)
				motorState = Right;
			else
				motorState = Neutral;
			break;
		default:
			motorState = Start;
			break;
	}
	switch(motorState){
		case Start:
			break;
		case Neutral:
			motor1 = stepArr[i1];				//Start at A for both motors
			motor2 = stepArr[i2];
			break;
		case Left:
			if (i1 < sizeof(stepArr))						//As long as either motor is not at the end of the array, increment by 1.
				i1 +=1;								//otherwise, set back to the start of the array.
			else
				i1 = 0;
			//Both spin right
			break;
		case Mid:
			//One motor spins left, other spins right.
			break;
		case Right:
			//Both spin left
			break;
		default:
			break;
	}
}

int main(void){
	DDRA = 0x00; PORTA = 0xFF;
	DDRB = 0xFF; PORTB = 0x00;
	TimerSet(300);					//Lab manual suggests 3ms between ticks
	TimerOn();
	
	
    while (1) {
		MotorTick();
		while(!TimerFlag);
		TimerFlag = 0;
    }
}

