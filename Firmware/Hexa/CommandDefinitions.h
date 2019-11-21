/******************************************************************************
 * @File		CommandDefinitions.h
 * @Brief		Put your custom commands in here
 * @Date		18/11/2019 (Last Updated)
 * @Author(s)	William Bednall
 ******************************************************************************/
#ifndef CommandDefinitions_h
#define CommandDefinitions_h

#include "Controller.h"
#include "CommandLineInterface.h"

extern Controller *Dev_LA;
extern bool spinRunning;
void ledfunc();
void stepResponce();
void lsFunc();
void spinFunc();
void posGainFunc();
void velGainFunc();
void velIntGainFunc();
void setpointFunc();
void setSampleRateFunc();
void togPosVelFunc();
void togSDKmodeFunc();
void moveSetPoint();

//Commands cannot contain spaces or `
#define cmd_total 12
const cmdFormat cmd_bind[cmd_total] PROGMEM = {
	{ "led", ledfunc },
	{ "step", stepResponce },
	{ "ls", lsFunc },
	{ "r", spinFunc },
	{ "pp", posGainFunc },
	{ "vp", velGainFunc },
	{ "vi", velIntGainFunc },
	{ "s", setpointFunc },
	{ "t", setSampleRateFunc },
	{ "v", togPosVelFunc },
	{ "z", togSDKmodeFunc },
	{ "mv", moveSetPoint }
};

#endif
