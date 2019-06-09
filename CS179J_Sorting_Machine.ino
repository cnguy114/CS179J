 /*
 * CS179J_arms.c
 * This is the motor code for the recycling sorter project.
 * This code controls the pushing and sorting motors for the project.
 */ 
#include <Servo.h>

// defines pins numbers
const int p_servo1 = 5; 
const int p_servo2 = 6;
const int r_servo1 = 10;
const int r_servo2 = 11;
const int raspi1 = 1;
const int raspi0 = 0;
const int sensor = 2;
const int pResistor = A0;

Servo p1;
Servo p2;
Servo r1;
Servo r2;

void setup() {

  // Sets pins as Outputs
  p1.attach(p_servo1);
  p2.attach(p_servo2);
  r1.attach(r_servo1); //10 => RIGHT
  r2.attach(r_servo2); //11 => LEFT 
  
  // set serial communication
  Serial.begin(9600);
  
  // (Raspi input are Pin0 and Pin1)
  pinMode(raspi0, INPUT);
  pinMode(raspi1, INPUT);
  pinMode(sensor, OUTPUT);
  pinMode(pResistor, INPUT);
  
}


//Wait for CVsignal
enum motorFSM{Start, Wait, Neutral, Left, Right, Sweep, Return}motorState = Start;
unsigned char CVsignal = 0;
void ServoTick(){
  
  switch(motorState){
    case Start:     
      motorState = Wait;
    break;
    
    case Wait:
      if (CVsignal == 1)       {motorState = Left;}
      else if (CVsignal == 2)  {motorState = Neutral;}
      else if (CVsignal == 3)  {motorState = Right;}
      else                     {motorState = Wait;}
    break;
    
    case Neutral:
      motorState = Sweep;
    break;
    
    case Left:
      motorState = Sweep;
    break;
    
    case Right:
      motorState = Sweep;
    break;

    case Sweep:
      motorState = Return;
    break;

    case Return:
      if (CVsignal) {motorState = Return;}
      else          {motorState = Wait;}
    break;
    
    default:
      motorState = Wait;
    break;
  }
  
  switch(motorState){
    case Start:
    break;
    
    case Wait:
      // do nothing
      // wait for signal 
    break;
    
    case Neutral:
      r1.write(70);
      r2.write(105);
    break;
    
    case Left:                
      // both move left
      r1.write(150);
      r2.write(105);
    break;
    
    case Right:               
      //Both move right
      r1.write(70);
      r2.write(15);
    break;

    case Sweep:
      delay(200);
      p1.write(115);
      p2.write(115);
      delay(1200);
    break; 

    case Return:
      p1.write(0);
      p2.write(0);
    break;
  }
}

// signal values from raspi 
int s0 = 0;
int s1 = 0;
int PRval; // pResistor value
const int THRESHOLD = 140; // sensor threshold cutoff
unsigned long previousMillis=0;
unsigned long currentMillis=0; // for change in time
const long interval = 1000;

void loop() {
   
    /*
    //2bit signal from RasPi 
    s0 = digitalRead(raspi0);
    s1 = digitalRead(raspi1);
    if(!s1 && s0) {
      CVsignal = 1;
    }
    else if(s1 && !s0) {
      CVsignal = 2;
    }
    else if(s1 && s1) {
      CVsignal = 3;
    }
    else {
      CVsignal = 0;
    }
    Serial.print("recieved data: ");
    Serial.println(CVsignal);
    */

    // photosensor detect object send to raspi
    PRval = analogRead(pResistor);
    if(PRval > THRESHOLD) {
      // no object
      currentMillis = millis();
      if(currentMillis - previousMillis >= interval) {
          digitalWrite(sensor, HIGH);
      }
    }
    else {
      // object
      digitalWrite(sensor, LOW);
      previousMillis = millis();
    }
    
//    ServoTick();    
    
    p1.write(10); // Enables the motor to move in a particular direction
    p2.write(10);
    delay(5000); // One ms delay
    
    //RIGHT
    r1.write(70); // Enables the motor to move in a particular direction
    r2.write(15);
    delay(1000); // One ms delay
    
    p1.write(130);  //Changes the rotations direction
    p2.write(130);
    delay(1000);
    
    p1.write(10); // Enables the motor to move in a particular direction
    p2.write(10);
    delay(5000); // One ms delay
    
    //MIDDLE
    r1.write(70); // Enables the motor to move in a particular direction
    r2.write(105);
    delay(1000); // One ms delay

    p1.write(130);  //Changes the rotations direction
    p2.write(130);
    delay(1000);
    
    p1.write(10); // Enables the motor to move in a particular direction
    p2.write(10);
    delay(5000); // One ms delay
    
    //LEFT
    r1.write(150); // Enables the motor to move in a particular direction
    r2.write(105);
    delay(1000); // One ms delay
    
    
    p1.write(130);  //Changes the rotations direction
    p2.write(130);
    delay(1000);

    /*
    p1.write(10); // Enables the motor to move in a particular direction
    p2.write(10);
    delay(5000); // One ms delay
    */
}

//LEFT:  leftMAX=105, rightMAX=15
//RIGHT: leftMAX=150, rightMAX=70

