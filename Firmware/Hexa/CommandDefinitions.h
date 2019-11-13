/******************************************************************************
 * @File		CommandDefinitions.h
 * @Brief		Put your custom commands in here
 * @Date		13/11/2019 (Last Updated)
 * @Author(s)	William Bednall
 ******************************************************************************/
#ifndef CommandDefinitions_h
#define CommandDefinitions_h

#include "LinearActuator.h"
#include "CommandLineInterface.h"

void ledfunc();
void stepResponce();

//Commands cannot contain spaces or `
#define cmd_total 2
const cmdFormat cmd_bind[cmd_total] PROGMEM = {
	{ "led", ledfunc },
	{ "step", stepResponce }
};

#endif
