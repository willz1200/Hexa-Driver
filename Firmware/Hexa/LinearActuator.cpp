/******************************************************************************
 * @File		LinearActuator.cpp
 * @Brief		Linear actuator class, used to drive the motor H-Bridge and track
 *				encoder steps.
 * @Date		12/04/2019 (Last Updated)
 * @Author(s)	William Bednall
 ******************************************************************************/
#include <Arduino.h>
#include "LinearActuator.h"

//Linear Actuator Constructor
LinearActuator::LinearActuator(const byte _LinearActuatorID, const unsigned char _MotorPWM, unsigned char _MotorDIR, unsigned char _EncoderINT, unsigned char _EncoderPHA, bool _EncoderFlip)
	: LinearActuatorID (_LinearActuatorID), MotorPWM (_MotorPWM), MotorDIR (_MotorDIR), EncoderINT (_EncoderINT), EncoderPHA (_EncoderPHA), EncoderFlip (_EncoderFlip){ //Used to store const values

	//Setup Motor and Encoder Pins
	pinMode(MotorPWM, OUTPUT);
	pinMode(MotorDIR, OUTPUT);
	pinMode(EncoderINT, INPUT);
	pinMode(EncoderPHA, INPUT);

	//Turn Motor Off
	SpinMotor(0, 0);

	motorDirection = false;

	//Attach each encoder interrupt to its Glue routine (MAX of 6)
	switch (LinearActuatorID){
		case 0:
			attachInterrupt(EncoderINT, HandleGlueRoutine_0, FALLING);
			instances[0] = this;
			break;

		case 1:
			attachInterrupt(EncoderINT, HandleGlueRoutine_1, FALLING);
			instances[1] = this;
			break;

		case 2:
			attachInterrupt(EncoderINT, HandleGlueRoutine_2, FALLING);
			instances[2] = this;
			break;

		case 3:
			attachInterrupt(EncoderINT, HandleGlueRoutine_3, FALLING);
			instances[3] = this;
			break;

		case 4:
			attachInterrupt(EncoderINT, HandleGlueRoutine_4, FALLING);
			instances[4] = this;
			break;

		case 5:
			attachInterrupt(EncoderINT, HandleGlueRoutine_5, FALLING);
			instances[5] = this;
			break;
	}

}

//Encoder Functions

void LinearActuator::EncoderInterruptHandler(){
	if (digitalRead(EncoderPHA) == EncoderFlip){ //Check phase of encoder pulse to figure out spin direction
		virtualPosition--;
	} else {
		virtualPosition++;
	}
}

int LinearActuator::GetEncoderPos(){
	return virtualPosition;
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

//Motor Functions

void LinearActuator::SpinMotor(unsigned char dutyCycle, unsigned char direction){
	switch(direction){
		case 0: //Off
			digitalWrite(MotorPWM, LOW);
			digitalWrite(MotorDIR, LOW);
			break;

		case 1: //Spin ->
			analogWrite(MotorPWM, dutyCycle); //Currently only 8-bit PWM but the MCU supports 16-bit PWM
			digitalWrite(MotorDIR, LOW);
			motorDirection = true;
			break;

		case 2: //Spin <-
			analogWrite(MotorPWM, 255-dutyCycle);
			digitalWrite(MotorDIR, HIGH);
			motorDirection = false;
			break;
	}
}

bool LinearActuator::getMotorDir(){
	return motorDirection;
}

//Instantiate 6 Linear Actuator Objects and Allocate Their IO
LinearActuator LA0(0, Motor1_PWM, Motor1_DIR, Encoder1_INT, Encoder1_PHA, Encoder1_Flip);
LinearActuator LA1(1, Motor2_PWM, Motor2_DIR, Encoder2_INT, Encoder2_PHA, Encoder2_Flip);
LinearActuator LA2(2, Motor3_PWM, Motor3_DIR, Encoder3_INT, Encoder3_PHA, Encoder3_Flip);
LinearActuator LA3(3, Motor4_PWM, Motor4_DIR, Encoder4_INT, Encoder4_PHA, Encoder4_Flip);
LinearActuator LA4(4, Motor5_PWM, Motor5_DIR, Encoder5_INT, Encoder5_PHA, Encoder5_Flip);
LinearActuator LA5(5, Motor6_PWM, Motor6_DIR, Encoder6_INT, Encoder6_PHA, Encoder6_Flip);
