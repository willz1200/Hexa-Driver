/******************************************************************************
 * @File		Controller.h
 * @Brief		DC motor control systems are implemented here
 * @Date		20/11/2019 (Last Updated)
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
		void setPosGain(float gain);
		void setVelGain(float gain);
		void setVelIntGain(float gain);
		void setPoint(float setpoint);
		void setSampleRate(unsigned int rate);
		void streamPosVel(bool toggle);
		void update();
		void position();
	private:
		float posGain;
		float pos_Setpoint;
		float velDesired;
		float velGain;
		float velIntGain;
		float outDesired;
		unsigned int sampleRate;
		unsigned long timeKeep, timeSinceUpdate;
		bool togglePosVel;

};

extern Controller LA0;
extern Controller LA1;
extern Controller LA2;
extern Controller LA3;
extern Controller LA4;
extern Controller LA5;

#endif
