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
		void stepResponse( float input );

		//Time based controller
		void runTimeSweep();
		void runTimeSingleFire(uint16_t duration, uint8_t dir, uint8_t duty);
		void runTimeSingleUpdate();
		uint16_t dirA_runTime, dirB_runTime, durationSingle_runTime;
		uint8_t duty_runTime;
		uint8_t controllerMode;
	private:
		float posGain;
		float pos_Setpoint;
		float velDesired;
		float velGain;
		float velIntGain;
		float outDesired;
		unsigned int sampleRate;
		unsigned long timeKeep, timeSinceUpdate, sweepMS_runTime, singleMS_runTime; //Time keeping vars
		bool togglePosVel;
		bool togglePIdebug;

		bool flagSingle_runTime;
};

Controller* idToInstance(uint8_t LA_ID);

extern Controller LA0;
extern Controller LA1;
extern Controller LA2;
extern Controller LA3;
extern Controller LA4;
extern Controller LA5;

#endif
