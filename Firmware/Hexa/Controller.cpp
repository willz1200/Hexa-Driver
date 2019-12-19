/******************************************************************************
 * @File		Controller.cpp
 * @Brief		DC motor control systems are implemented here 
 * @Date		20/11/2019 (Last Updated)
 * @Author(s)	William Bednall
 ******************************************************************************/
#include <Arduino.h>
#include "Controller.h"

//Controller::Controller(const laFormat *_LA) : LinearActuator(_LA){}
Controller::Controller(const byte _LinearActuatorID) : LinearActuator(_LinearActuatorID){
	controllerMode = 0;
	posGain = 0.05;
	pos_Setpoint = 800.0;
	velDesired = 0.0;
	velGain = 0.05;
	velIntGain = 0.00001;
	timeKeep = millis();
	timeSinceUpdate = millis();
	timeSinceUpdateB = millis();
	sampleRate = 5; //Set default sample rate to 10 ms = 100 Hz
	sampleRateB = 10; //Set default sample rate to 10 ms = 100 Hz
	togglePosVel = false;
	togglePIdebug = true;
	velTotalError = 0;

	//Run time controll vars - Sweep mode
	dirA_runTime = 1000;
	dirB_runTime = 1000;
	duty_runTime = 75;

	//Run time controll vars - Single mode
	durationSingle_runTime = 500;
	flagSingle_runTime = false;

	sweepMS_runTime = millis();
	singleMS_runTime = millis();
}

void Controller::closedSpinTest(){
	if (GetEncoderPos() <= 0){
		SpinMotor(75, dirB); //Change turning to head towards end point
	}

	//at end point
	if (GetEncoderPos() >= 500){
		SpinMotor(75, dirA); //Change turning to head towards start point
	}

	if (getMotorDir() == true && GetEncoderPos() < 50){ SpinMotor(50, dirA); } //deceleration to start point
	if (getMotorDir() == true && GetEncoderPos() < 20){ SpinMotor(48, dirA); } //deceleration to start point
	if (getMotorDir() == true && GetEncoderPos() <= 5){ SpinMotor(47, dirA); } //deceleration to start point

	if (getMotorDir() == false && GetEncoderPos() > 450){ SpinMotor(50, dirB); } //deceleration to end point
	if (getMotorDir() == false && GetEncoderPos() > 480){ SpinMotor(48, dirB); } //deceleration to end point
	if (getMotorDir() == false && GetEncoderPos() >= 495){ SpinMotor(47, dirB); } //deceleration to end point

	//Serial.print(GetEncoderPos());
	//Serial.print(", ");
}

void Controller::setPosGain(float gain){
	posGain = gain;
}

void Controller::setVelGain(float gain){
	velGain = gain;
}

void Controller::setVelIntGain(float gain){
	velIntGain = gain;
}

void Controller::setPoint(float setpoint){
	pos_Setpoint = setpoint;
}

void Controller::setSampleRate(unsigned int rate){
	sampleRate = rate;
}

//Toggle position and velocity streaming
void Controller::streamPosVel(bool toggle){
	togglePosVel = toggle;
}

void Controller::update(){
	if (enableLA == true){
		//Controller mode selection
		if (controllerMode == 1){
			position();
		} else if(controllerMode == 2){
			runTimeSweep();
		} else if(controllerMode == 3){
			runTimeSingleUpdate();
		} else if(controllerMode == 4){
			stepResponse();
		} else {
			SpinMotor(0, dirB);
			velTotalError = 0; //Reset accumulated error
		}

		//Velocity sampling
		if (millis() - timeSinceUpdate > sampleRate){
			timeSinceUpdate = millis();
			VelocityUpdate();
		}

		//Real time graphing
		if (millis() - timeSinceUpdateB > sampleRateB){
			timeSinceUpdateB = millis();
			if (togglePosVel){
				Serial.print("s,");
				Serial.print(millis());
				Serial.print(",");
				Serial.print(GetEncoderPos());
				Serial.print(",");
				Serial.println(GetEncoderRPM());	
			} 
		}
	} else {
		SpinMotor(0, dirB);
	}
}

//The position controller is a P loop with a single proportional gain.
void Controller::position(){

	/*

	//Position error calc
	float posError = pos_Setpoint - GetEncoderPos();

	//Position proportional calc
	velDesired += posGain * posError;

	//Limit the ouput velocity to 20258 RPM
	uint16_t vel_Limit = 5000; //
	if (velDesired > vel_Limit) velDesired = vel_Limit;
	if (velDesired < -vel_Limit) velDesired = -vel_Limit;

	*/

	//---

	// Velocity PI controller not yet working correctly
	velDesired = pos_Setpoint;
	// Velocity error calc
	float velError = velDesired - GetEncoderRPM();//-GetEncoderFilteredRPM

	// Accumulate the error
	velTotalError += velError;


	float controlVariable = (velGain * velError) + (velIntGain * velTotalError);

	//Velocity proportional calc
	//outDesired += velGain * velError;
	
	//Velocity integral calc
	//outDesired += velIntGain * velTotalError;//velError * GetEncoderRPM();

	//Velocity derivative calc
	//outDesired += velDerGain * (error-lastError)

	//Limit the ouput velocity to 75/255 duty
    uint8_t duty_Limit = 150;
    if (controlVariable > duty_Limit) controlVariable = duty_Limit;
    if (controlVariable < -duty_Limit) controlVariable = -duty_Limit;

    //Set motor direction
	// uint8_t dirSet = 0;
	// if (outDesired < 0){
	// 	dirSet = 1;
	// } else {
	// 	dirSet = 2;
	// }

	// SpinMotor(abs(velDesired), dirSet);

	//Temp to skip velocity PI stage


	//Set motor direction
	uint8_t dirSet = 0;
	if (controlVariable < 0){
		dirSet = 1;
	} else {
		dirSet = 2;
	}

	if (togglePIdebug){
		//Limit print speed
		if (millis() - timeKeep > 50){
			Serial.print("p,");
			Serial.print(GetEncoderFilteredRPM()); //posError //velTotalError
			Serial.print(",");
			Serial.print(velError);
			Serial.print(",");
			Serial.print(0); //GetEncoderPos()
			Serial.print(",");
			Serial.print(velDesired);
			Serial.print(",");
			Serial.print(controlVariable);
			Serial.print(",");
			Serial.println(GetEncoderRPM());
			timeKeep = millis();
		}
	}

	SpinMotor(abs(controlVariable), dirSet);


}

//Simple controller to switch motor direction based on a time delay
void Controller::runTimeSweep(){
	if (getMotorDir() == true){
		if (millis() - sweepMS_runTime > dirA_runTime){
			SpinMotor(duty_runTime, 2);
			sweepMS_runTime = millis();
			//Serial.println(GetEncoderPos());
		}

	} else if(getMotorDir() == false) {
		if (millis() - sweepMS_runTime > dirB_runTime){
			SpinMotor(duty_runTime, 1);
			sweepMS_runTime = millis();
			//Serial.println(GetEncoderPos());
		}

	}
}

void Controller::runTimeSingleFire(uint16_t duration, uint8_t dir, uint8_t duty){
	durationSingle_runTime = duration;
	flagSingle_runTime = true; //Raise a single shot flag
	sweepMS_runTime = millis();
	SpinMotor(duty, dir);
}

void Controller::runTimeSingleUpdate(){
	if (flagSingle_runTime){ //Check if single command is currently running motor
		if (millis() - sweepMS_runTime > durationSingle_runTime){
			SpinMotor(0, dirB); //Stop motor
			flagSingle_runTime = false; //drop flag
		}
	}
}

void Controller::stepResponseSetup( unsigned char Speed ){
	

	// chainges some class variable
	stepResponseSpeed = Speed;
	// chaing controlerMode to 4
	controllerMode = 4;
	stepStartTime = millis();
	togglePosVel = true;
}


void Controller::stepResponse(){
	

	// get current time 
	stepCurrentTime = millis() - stepStartTime;
	
	// stop step if 12 secconds
	if (stepCurrentTime > 12000){
		SpinMotor( 0 , dirB ); //Start motor
		togglePosVel = false;
	} else if (stepCurrentTime > 2000){
		// start step if 2 secconds
		SpinMotor(stepResponseSpeed, dirB); //Stop motor
	}
	
	//...
	// Stream data
}

Controller* idToInstance(uint8_t LA_ID){
	if (LA_ID == 0){
		return &LA0;
	} else if (LA_ID == 1){
		return &LA1;
	} else if (LA_ID == 2){
		return &LA2;
	} else if (LA_ID == 3){
		return &LA3;
	} else if (LA_ID == 4){
		return &LA4;
	} else if (LA_ID == 5){
		return &LA5;
	}
	//return LA0.getInstance(LA_ID);
}

//Instantiate 6 Linear Actuator Objects and Allocate Their IO
Controller LA0(0);
Controller LA1(1);
Controller LA2(2);
Controller LA3(3);
Controller LA4(4);
Controller LA5(5);