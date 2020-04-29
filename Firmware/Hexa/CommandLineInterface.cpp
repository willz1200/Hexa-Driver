/******************************************************************************
 * @File		CommandLineInterface.cpp
 * @Brief		The User Interface / Command Line Interface backend
 * @Date		13/11/2019 (Last Updated)
 * @Author(s)	William Bednall
 ******************************************************************************/
#include <Arduino.h>
#include "CommandLineInterface.h"

CommandLineInterface::CommandLineInterface(Stream &targetSerial){ //Use Stream instead of HardwareSerial for greater support
	refSerial = &targetSerial;
	sdkMode = false;
}

void CommandLineInterface::bind(const cmdFormat *cmdTable, uint16_t size){
	cmdUserBindings = cmdTable;
	cmdUserSize = size;
}

void CommandLineInterface::setSdkMode(bool toggle){
	sdkMode = toggle;
}

void CommandLineInterface::setup(){
	refSerial->println(F("Press any key to activate the console"));
	resetBuffer();
}

void CommandLineInterface::loop(){
	if (refSerial->available() > 0){
		while (refSerial->available() > 0){
			newChar = refSerial->read();
			if (newChar >= 32 && newChar <= 126){ //Space - ~
				if (countString < maxCharCommand){ //Store character in buffer and write to screen
					if (!sdkMode){
						refSerial->print(newChar);
					}
					inputBuffer[countString] = newChar;
					countString++;
				}
			} else if (newChar == 13){ //Carriage return
				if (inputBuffer[0] == 0 && !sdkMode) {
					refSerial->println("");
				} else if (!userCmd()){ //Run the command
					if (!sdkMode){
						refSerial->println(F(": command not found"));
					} else {
						refSerial->println(F("error"));
					}
				}
				resetBuffer();
			}
		}
	}
}

//User defined commands
bool CommandLineInterface::userCmd(){
	if (cmdUserBindings == NULL) //Check the pointer has been initialised
		return false;
	String inputStr = String(inputBuffer);
	separatorPos = inputStr.indexOf(' '); //Find the end of the command
	if (separatorPos != -1) //No need to isolate because the command has no arguments
		inputStr = inputStr.substring(0, separatorPos); //Isolate the command
	for (uint8_t count = 0; count < cmdUserSize; count++){
		if (inputStr == cmdUserBindings[count].term){
			if (!sdkMode){
				refSerial->println("");
			}
			cmdUserBindings[count].func();
			//if (paramError == true)
				//refSerial->println(F("Parameter Error")); //E: Invalid operation <param>
			//paramError = false;
			separatorPos = 0;
			return true;
		}
	}
	return false;
}

String CommandLineInterface::paramHandle(){
	String inputStr = String(inputBuffer);
	int posTemp = 0;
	if (separatorPos != -1){
		//There is a space after the command or previous argument
		if (inputStr[separatorPos + 1] == '`'){ //Look for string indicator first
			//The argument is a string
			posTemp = inputStr.indexOf('`', separatorPos + 2); //+ 2 so it skips the first `
			if (posTemp != -1){	//Make sure user has closed the string
				String output = inputStr.substring(separatorPos + 2, posTemp);
				separatorPos = posTemp + 1;
				if (separatorPos >= maxCharCommand)
					separatorPos = -1; //End of the buffer was reached
				return output;
			} else {
				//String wasn't terminated correctly
				//paramError = true;
			}
		} else {
			//The argument is a single word or other data type
			posTemp = inputStr.indexOf(' ', separatorPos + 1);
			if (posTemp != -1){
				//There is a space after the argument
				String output = inputStr.substring(separatorPos + 1, posTemp);
				separatorPos = posTemp;
				return output;
			} else {
				posTemp = inputStr.indexOf(0, separatorPos + 1);
				if (posTemp != -1){
					//There is a null terminator after the argument
					String output = inputStr.substring(separatorPos + 1, posTemp);
					separatorPos = posTemp;
					return output;
				} else {
					//Particular argument no given
					//paramError = true;
				}
			}
		}
	} else {
		//No arguments given or all arguments have been processed
		//paramError = true;
	}
	return "";
}

int CommandLineInterface::readInt(){
	return paramHandle().toInt();
}

long CommandLineInterface::readLong(){
	return paramHandle().toInt(); //Even though its called toInt it returns a long
}

bool CommandLineInterface::readBool(){
	if (readInt() != 0){
		return true;
	} else {
		return false;
	}
}

float CommandLineInterface::readFloat(){
	return paramHandle().toFloat();
}

double CommandLineInterface::readDouble(){
	#ifdef ESP8266
	// -------------------------------- Hexa Driver 2.0 --------------------------------
	
	return paramHandle().toDouble();
	
	#elif defined MCU_STM32F103CB
	// -------------------------------- Hexa Driver 1.0 --------------------------------
	
	return atof(paramHandle().c_str()); // toDouble command missing from Arduino_STM32 :(
	
	#endif	
}

char CommandLineInterface::readChar(){
	return paramHandle().charAt(0);
}

String CommandLineInterface::readString(){
	return paramHandle();
}

void CommandLineInterface::resetBuffer(){
	memset(inputBuffer,0,sizeof(inputBuffer));
	countString = 0;
}

CommandLineInterface CLI(Serial);