/******************************************************************************
 * @File		LinearActuator.cpp
 * @Brief		Linear actuator class, used to drive the motor H-Bridge and track
 *				encoder steps.
 * @Date		27/11/2019 (Last Updated)
 * @Author(s)	William Bednall
 ******************************************************************************/
#include <Arduino.h>
#include "LinearActuator.h"

//Linear Actuator Constructor
LinearActuator::LinearActuator(const byte _LinearActuatorID)
	: LinearActuatorID (_LinearActuatorID){ //Used to store const values

	LA = &LinearActuatorsAvailable[LinearActuatorID];
	//Setup Motor and Encoder Pins
	pinMode(LA->MotorPWM, OUTPUT);
	pinMode(LA->MotorDIR, OUTPUT);
	pinMode(LA->EncoderINT, INPUT);
	pinMode(LA->EncoderPHA, INPUT);

	//Turn Motor Off
	SpinMotor(0, 0);

	motorDirection = false;
	enableLA = false;
	velocityTime = millis();
	velocityLastPos = 0;
	rpm = 0;
	filteredRpm = 0;

	//Attach each encoder interrupt to its Glue routine (MAX of 6)
	switch (LinearActuatorID){
		case 0:
			attachInterrupt(LA->EncoderINT, HandleGlueRoutine_0, FALLING);
			instances[0] = this;
			break;

		case 1:
			attachInterrupt(LA->EncoderINT, HandleGlueRoutine_1, FALLING);
			instances[1] = this;
			break;

		case 2:
			attachInterrupt(LA->EncoderINT, HandleGlueRoutine_2, FALLING);
			instances[2] = this;
			break;

		case 3:
			attachInterrupt(LA->EncoderINT, HandleGlueRoutine_3, FALLING);
			instances[3] = this;
			break;

		case 4:
			attachInterrupt(LA->EncoderINT, HandleGlueRoutine_4, FALLING);
			instances[4] = this;
			break;

		case 5:
			attachInterrupt(LA->EncoderINT, HandleGlueRoutine_5, FALLING);
			instances[5] = this;
			break;
	}

}

//Encoder Functions

void LinearActuator::EncoderInterruptHandler(){
	if (digitalRead(LA->EncoderPHA) == LA->EncoderFlip){ //Check phase of encoder pulse to figure out spin direction
		virtualPosition--;
	} else {
		virtualPosition++;
	}
}

void LinearActuator::VelocityUpdate(){
	int8_t dir;
	int pulseDelta;
	if (virtualPosition > velocityLastPos){
		pulseDelta = virtualPosition - velocityLastPos;
		dir = 1;
	} else {
		pulseDelta = velocityLastPos - virtualPosition;
		dir = -1;
	}
	
	//60000 milliseconds in 1 minute, used for rpm.
	rpm = (pulseDelta * (60000 / (millis() - velocityTime))) / PulsesPerTurn;
	//rpm = rpm / GearReduction; //Include Gear Reduction Ratio
	rpm = dir * rpm;

	// Use Exponential Kalman filter to reduce noise on speed data
	filteredRpm += 0.01 * (rpm - filteredRpm); // 0.01 is a tuning constant

	velocityLastPos = virtualPosition;
	velocityTime = millis();
}

int LinearActuator::GetEncoderPos(){
	return virtualPosition;
}

float LinearActuator::GetEncoderRPM(){
	return filteredRpm;
}

void LinearActuator::ResetEncoderPos(){
	virtualPosition = 0;
}

LinearActuator *LinearActuator::instances[6]; //Allow glue routines to reference the class instances

void LinearActuator::HandleGlueRoutine_0(){
	if (instances[0] != NULL) //Check for NULL pointer
		instances[0]->EncoderInterruptHandler();//Run handler for correct instance
}

void LinearActuator::HandleGlueRoutine_1(){
	if (instances[1] != NULL)
		instances[1]->EncoderInterruptHandler();
}
  
void LinearActuator::HandleGlueRoutine_2(){
	if (instances[2] != NULL)
		instances[2]->EncoderInterruptHandler();
}

void LinearActuator::HandleGlueRoutine_3(){
	if (instances[3] != NULL)
		instances[3]->EncoderInterruptHandler();
}

void LinearActuator::HandleGlueRoutine_4(){
	if (instances[4] != NULL)
		instances[4]->EncoderInterruptHandler();
}

void LinearActuator::HandleGlueRoutine_5(){
	if (instances[5] != NULL)
		instances[5]->EncoderInterruptHandler();
}

LinearActuator* LinearActuator::getInstance(uint8_t instanceID){
	return instances[instanceID];
}

//Motor Functions

void LinearActuator::SpinMotor(unsigned char dutyCycle, unsigned char direction){
	// static unsigned char logChange;

	// if (logChange != dutyCycle){
	// 	logChange = dutyCycle;
	// 	Serial.println(dutyCycle);
	// }
	
	switch(direction){
		case 0: //Off
			digitalWrite(LA->MotorPWM, LOW);
			digitalWrite(LA->MotorDIR, LOW);
			break;

		case 1: //Spin ->
			analogWrite(LA->MotorPWM, dutyCycle); //Currently only 8-bit PWM but the MCU supports 16-bit PWM
			digitalWrite(LA->MotorDIR, LOW);
			motorDirection = true;
			break;

		case 2: //Spin <-
			analogWrite(LA->MotorPWM, 255-dutyCycle);
			digitalWrite(LA->MotorDIR, HIGH);
			motorDirection = false;
			break;
	}

	
}

bool LinearActuator::getMotorDir(){
	return motorDirection;
}
