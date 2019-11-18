/******************************************************************************
 * @File		CommandDefinitions.cpp
 * @Brief		Put your custom commands in here
 * @Date		17/11/2019 (Last Updated)
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
		LA0.SpinMotor( input , 2); //Start Spinning Motor
	} else {
		// CLI.sendError("motor not found")
		// CLI.sendMessage("some message")
	}
	
}

void lsFunc(){
	Serial.println(LA0.GetEncoderPos());
}

//Not currently work, seems to cause 12V rail to dip dramatically???
void spinFunc(){
	//spinRunning = CLI.readBool();
}