/*
 * Sorting Arm.c
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
int stepArr[] = {A, AB, B, BC, C, CD, D, DA};

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
			motor1 = stepArr[i1];
			motor2 = stepArr[i2];
			break;
		case Neutral:
			motor1 = stepArr[0];				//Start at A for both motors
			motor2 = stepArr[0];
			PINA = (motor1 << 4) | motor2;
			break;
		case Left:								//Both spin right
			if (i1 < sizeof(stepArr))						//As long as either motor is not at the end of the array, increment by 1.
				i1 += 1;								//otherwise, set back to the start of the array.
			else
				i1 = 0;
			if (i2 < sizeof(stepArr))
				i2 += 1;
			else
				i2 = 0;
			motor1 = stepArr[i1];
			motor2 = stepArr[i2];
			PINA = (motor1 << 4) | motor2;			//Send byte to motors. One nibble = 1 motor
			break;
		case Mid:								//One motor spins left, other spins right.
			if (i1 > 0)							//Still unsure of direction. As long as both start and end on different values, it's fine.
				i1 -= 1;
			else
				i1 = sizeof(stepArr);
			if (i2 < sizeof(stepArr))
				i2 += 1;
			else
				i2 = 0;
			motor1 = i1;
			motor2 = i2;
			PINA = (motor1 << 4) | motor2;
			break;
		case Right:								//Both spin left
			if (i1 > 0)
				i1 -= 0;
			else
				i1 = sizeof(stepArr);
			if (i2 > 0)
				i2 -= 1;
			else
				i2 = sizeof(stepArr);
			motor1 = i1;
			motor2 = i2;
			PINA = (motor1 << 4) | motor2;
			break;
		default:
			break;
	}
}

// 4/27 MOTORS WORK FINALLY AHAHAA
// 4/28 Button logic isn't working. Motors are both vibrating, unsure of direction.
int main(void){
	DDRA = 0xFF; PORTA = 0x00;		//PortA is output.
	DDRB = 0x00; PORTB = 0xFF;		//PortB is input.
	TimerSet(2);					//Need small timer or motors won't spin. Maybe not enough power going through?
	TimerOn();
	
    while (1) {
		button = ~PINB;				//Enable pin
		MotorTick();				//Tick function
/*		int i = 0;
		while (i < sizeof(stepArr)){
			PINA = (stepArr[i] << 4) | stepArr[i]; 
			i++;
			if (i >= sizeof(stepArr))
				i = 0;
		}
	*/	
		while(!TimerFlag);
		TimerFlag = 0;
    }
}

