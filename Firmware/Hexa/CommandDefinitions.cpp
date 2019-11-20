/******************************************************************************
 * @File		CommandDefinitions.cpp
 * @Brief		Put your custom commands in here
 * @Date		20/11/2019 (Last Updated)
 * @Author(s)	William Bednall
 ******************************************************************************/
#include <Arduino.h>
#include "CommandDefinitions.h"

bool spinRunning = 0;

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
	spinRunning = CLI.readBool();
}

void gainFunc(){ Dev_LA->setGain(CLI.readFloat()); }
void setpointFunc(){ Dev_LA->setPoint(CLI.readFloat()); }
void setSampleRateFunc(){ Dev_LA->setSampleRate(CLI.readInt()); }
void togPosVelFunc(){ Dev_LA->streamPosVel(CLI.readBool()); }

void togSDKmodeFunc(){ CLI.setSdkMode(CLI.readBool()); }