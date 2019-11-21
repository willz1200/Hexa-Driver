/******************************************************************************
 * @File		CommandDefinitions.cpp
 * @Brief		Put your custom commands in here
 * @Date		20/11/2019 (Last Updated)
 * @Author(s)	William Bednall
 ******************************************************************************/
#include <Arduino.h>
#include "CommandDefinitions.h"

uint8_t spinRunning = 0;

void ledfunc(){
	analogWrite(33, CLI.readInt());
}

void stepResponce(){
	int motor = CLI.readInt();
	int input = CLI.readInt();
	if ( motor == 0 ){
		LA0.SpinMotor(input , 2); //Start Spinning Motor
	} else if ( motor == 5 ){
		LA5.SpinMotor(input , 2); //Start Spinning Motor
	} else {
		// CLI.sendError("motor not found")
		// CLI.sendMessage("some message")
	}
}

void lsFunc(){
	Serial.println(Dev_LA->GetEncoderPos());
}

//Not currently working, seems to cause 12V rail to dip dramatically??? --> Issue with LA0 on my board now using LA5 :)
void spinFunc(){
	if (CLI.readBool()){
		spinRunning = 1;
	} else {
		spinRunning = 0;
	}
}

void posGainFunc(){ Dev_LA->setPosGain(CLI.readFloat()); }
void velGainFunc(){ Dev_LA->setVelGain(CLI.readFloat()); }
void velIntGainFunc(){ Dev_LA->setVelIntGain(CLI.readFloat()); }
void setpointFunc(){ Dev_LA->setPoint(CLI.readFloat()); }
void setSampleRateFunc(){ Dev_LA->setSampleRate(CLI.readInt()); }
void togPosVelFunc(){ Dev_LA->streamPosVel(CLI.readBool()); }
void togSDKmodeFunc(){ CLI.setSdkMode(CLI.readBool()); }

void moveSetPoint(){
	float setPointDesired = CLI.readFloat();
	Dev_LA->setPoint(setPointDesired);
}

void configRunTimeController(){
	char cmd = CLI.readChar();
	if (cmd == '0'){
		spinRunning = 0;
	} else if (cmd == '1'){
		spinRunning = 2;
	} else if (cmd == '2'){
		spinRunning = 3;
	} else if (cmd == 't'){
		uint16_t rtInt = CLI.readInt();
		Dev_LA->dirA_runTime = rtInt;
		Dev_LA->dirB_runTime = rtInt;
	} else if (cmd == 'a'){
		Dev_LA->dirA_runTime = CLI.readInt();
	} else if (cmd == 'b'){
		Dev_LA->dirB_runTime = CLI.readInt();
	} else if (cmd == 'v'){
		Dev_LA->duty_runTime = CLI.readInt();
	} else if (cmd == 's'){ //Signle shot mode
		uint16_t duration = CLI.readInt();
		uint8_t dir = CLI.readInt();
		uint8_t duty = CLI.readInt();
		Dev_LA->runTimeSingleFire(duration, dir, duty);
	} else {
		Serial.print(F(": sub command not found"));
	}
}