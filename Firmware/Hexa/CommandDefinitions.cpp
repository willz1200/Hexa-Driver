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
	int input = CLI.readInt();
	LA0.SpinMotor( input , dirB); //Start Spinning Motor

}