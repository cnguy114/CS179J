/*
 * CS179J_arms.c
 * This is the motor code for the recycling sorter project.
 * This code controls the pushing and sorting motors for the project.
 */ 
#ifndef F_CPU
#define F_CPU 8000000UL		//Changing this changes the range in which the claw opens. Somehow. Readjusted claw location in order to compensate change.
#endif

#include <avr/io.h>
#include <stdlib.h> 
#include <util/delay.h>
#include "timer.h"

//The motors go AB, BC, CD, DA (x2) for full step. Go in reverse order for counter-clockwise motion.
#define AC 0x05	//0101
#define BC 0x06	//0110
#define BD 0x0A	//1010
#define AD 0x09	//1001

//USART, not UART. USART is PORTD.
int stepArr[] = {AC, BC, BD, AD};

//stepping tick functions
int state = 0;
unsigned char m1 = 0;
unsigned char m2 = 0;
void stepCW(){
	m1 = stepArr[state]; m2 = m1 << 4;
	PORTA = m2 | m1;
	if(state < 3)	{state += 1;}
	else			{state = 0;}
}
void stepCCW(){
	m1 = stepArr[state]; m2 = m1 << 4;
	PORTA = m2 | m1;
	if(state > 0)	{state -= 1;}
	else			{state = 3;}
}


//Wait for CVsignal
enum motorFSM{Start, Wait, Neutral, Left, LeftReturn, Right, RightReturn}motorState;
unsigned char CVsignal = 0;
unsigned char sort_ready = 0;

// 200 steps = 360 degrees
// 45 degree angle (25 steps)
#define TURN_ANGLE 25		
int numSteps = TURN_ANGLE; 
void MotorTick(){
	
	switch(motorState){
		case Start:			
			motorState = Wait;
		break;
		case Wait:
			if (CVsignal == 0x01)		{motorState = Left;}
			else if (CVsignal == 0x02)	{motorState = Neutral;}
			else if (CVsignal == 0x03)	{motorState = Right;}
			else						{motorState = Wait;}
		break;
		case Neutral:
			if(numSteps > 0)	{motorState = Neutral;}			
		break;
		case Left:
			if(numSteps > 0)	{motorState = Left;}
			else if (CVsignal)	{motorState = Left;}
			else				{motorState = LeftReturn;}
		break;
		case LeftReturn:
			if(numSteps > 0)	{motorState = LeftReturn;}
			else				{motorState = Wait;}
		break;
		case Right:
			if(numSteps > 0)	{motorState = Right;}
			else if (CVsignal)	{motorState = Right;}
			else				{motorState = RightReturn;}
		break;
		case RightReturn:
			if(numSteps > 0)	{motorState = RightReturn;}
			else				{motorState = Wait;}
		break;
		default:
			motorState = Wait;
		break;
	}
	
	switch(motorState){
		case Start:
		break;
		case Wait:
			// wait for signal 
		break;
		case Neutral:
			// do nothing but wait for bottle to drop
		break;
		case Left:								
			//Both spin CW
			if(numSteps > 0) {
				stepCW();
				numSteps -= 1;
			}
			else {
				sort_ready = 1;
				numSteps = TURN_ANGLE;
			}
		break;
		case LeftReturn:
			//spin back CCW
			if(numSteps > 0) {
				stepCCW();
				numSteps -= 1;
			}
			else {
				sort_ready = 0;
				numSteps = TURN_ANGLE;
			}
		break;
		case Right:								
			//Both spin CCW
			if(numSteps > 0) {
				stepCCW();
				numSteps -= 1;
			}
			else {
				sort_ready = 1;
				numSteps = TURN_ANGLE;
			}
		break;
		case RightReturn:
			//spin back CW
			if(numSteps > 0) {
				stepCW();
				numSteps -= 1;
			}
			else {
				sort_ready = 0;
				numSteps = TURN_ANGLE;
			}
		break;
	}
}


enum servoFSM {Idle, Sweep, Return}servoState;
void ServoTick(){
	switch(servoState){
		case Idle:
			if (sort_ready)	{servoState = Sweep;}
			else			{servoState = Idle;}
		break;
		case Sweep:
			servoState = Return;
		break;
		case Return:
			if(sort_ready)	{servoState = Return;}
			else			{servoState = Idle;}
		break;
		default:
			servoState = Idle;
		break;
	}
	switch(servoState){
		case Idle:
			// do nothing
		break;
		case Sweep:
			for (int i = 0; i < 5; i++){			//5 is arbitrary
				PORTC = 0x01;						//Enable PORTD
				_delay_us(1000);					//Signal enabled for 1ms.
				PORTC = 0x00;						//Disable PORTD
				_delay_ms(19);						//Signal disabled for 19ms.
			}
			for (int i = 0; i < 5; i++){			//Arbitrary 5
				PORTC = 0x01;						//Enable the correct port for corresponding servo.
				_delay_us(2000);					//Open signal up (Duty cycle = 10%)
				PORTC = 0x00;						//Disable the port
				_delay_ms(18);						//Open signal down (Down = 90%)
			}
		break;
		case Return:
			// do nothing return to idle
		break;
	}
}


int main(void){
	DDRA = 0xFF; PORTA = 0x00;		//PortA = output to servos
	DDRB = 0x00; PORTB = 0xFF;		//PortB = input from button
	DDRC = 0xFF; PORTC = 0x00;		//PortC = output to servo PWM
	DDRD = 0xFF; PORTD = 0x00;		//PortD = (RX, TX pins for USART are PD0 and PD1)
	TimerSet(12);					//Optimal Timer Setting
	TimerOn();
	
	int teststeps = 100;
    while (1) {
		CVsignal = ~PINB;				//input from Raspberry Pi (currently input through button
		
		//MotorTick();
		//ServoTick();		
				
		if(teststeps > 0){
			stepCW();
			teststeps -= 1;
		}
		
		while(!TimerFlag);
		TimerFlag = 0;
    }
}