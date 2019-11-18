/******************************************************************************
 * @File		CommandDefinitions.h
 * @Brief		Put your custom commands in here
 * @Date		17/11/2019 (Last Updated)
 * @Author(s)	William Bednall
 ******************************************************************************/
#ifndef CommandDefinitions_h
#define CommandDefinitions_h

#include "Controller.h"
#include "CommandLineInterface.h"

extern bool spinRunning;
void ledfunc();
void stepResponce();
void lsFunc();
void spinFunc();

//Commands cannot contain spaces or `
#define cmd_total 4
const cmdFormat cmd_bind[cmd_total] PROGMEM = {
	{ "led", ledfunc },
	{ "step", stepResponce },
	{ "ls", lsFunc },
	{ "spin", spinFunc }
};

#endif
