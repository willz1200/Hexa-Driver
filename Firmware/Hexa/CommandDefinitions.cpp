/******************************************************************************
 * @File		CommandDefinitions.cpp
 * @Brief		Put your custom commands in here
 * @Date		13/11/2019 (Last Updated)
 * @Author(s)	William Bednall
 ******************************************************************************/
#include <Arduino.h>
#include "CommandDefinitions.h"

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