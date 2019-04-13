/******************************************************************************
 * @File		LinearActuator.h
 * @Brief		Linear actuator class, used to drive the motor H-Bridge and track
 *				encoder steps.
 * @Date		12/04/2019 (Last Updated)
 * @Author(s)	William Bednall
 ******************************************************************************/
#ifndef LinearActuator_h
#define LinearActuator_h

#include "PinDefinitionsRev1_00.h"

class LinearActuator {

	static LinearActuator *instances[6];

	//Glue routines to connect ISR to a specific class instance
	static void HandleGlueRoutine_0 ();
	static void HandleGlueRoutine_1 ();
	static void HandleGlueRoutine_2 ();
	static void HandleGlueRoutine_3 ();
	static void HandleGlueRoutine_4 ();
	static void HandleGlueRoutine_5 ();

	private:
		const byte LinearActuatorID;
		const unsigned char MotorPWM;
		const unsigned char MotorDIR;
		const unsigned char EncoderINT;
		const unsigned char EncoderPHA;
		const bool EncoderFlip;

		volatile int virtualPosition; //Updated by the ISR through a glue routine
		bool motorDirection;
		
	public:
		LinearActuator(const byte _LinearActuatorID, const unsigned char _MotorPWM, const unsigned char _MotorDIR, const unsigned char _EncoderINT, const unsigned char _EncoderPHA, const bool _EncoderFlip);
		void EncoderInterruptHandler();
		int GetEncoderPos();
		void ResetEncoderPos();
		void SpinMotor(unsigned char dutyCycle, unsigned char direction);
		bool getMotorDir();
};

extern LinearActuator LA0;
extern LinearActuator LA1;
extern LinearActuator LA2;
extern LinearActuator LA3;
extern LinearActuator LA4;
extern LinearActuator LA5;

#endif
