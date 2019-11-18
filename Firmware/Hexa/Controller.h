/******************************************************************************
 * @File		Controller.h
 * @Brief		DC motor control systems are implemented here
 * @Date		18/11/2019 (Last Updated)
 * @Author(s)	William Bednall
 ******************************************************************************/

#ifndef Controller_h
#define Controller_h

#include "LinearActuator.h"
#include "CommandLineInterface.h"

//Swap these numbers if its not stopping
#define dirA 1 //Spin ->
#define dirB 2 //Spin <-

class Controller: public LinearActuator {
	public:
		//using LinearActuator::GetEncoderPos;
		Controller(const byte _LinearActuatorID);
		void closedSpinTest();
		void setGain(float gain);
		void setPoint(float setpoint);
		void position();
	private:
		float posGain;
		float pos_Setpoint;
		float velDesired;
		unsigned long timeKeep;

};

extern Controller LA0;
extern Controller LA1;
extern Controller LA2;
extern Controller LA3;
extern Controller LA4;
extern Controller LA5;

#endif
