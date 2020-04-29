/******************************************************************************
 * @File		LinearActuator.h
 * @Brief		Linear actuator class, used to drive the motor H-Bridge and track
 *				encoder steps.
 * @Date		28/04/2020 (Last Updated)
 * @Author(s)	William Bednall
 ******************************************************************************/
#ifndef LinearActuator_h
#define LinearActuator_h

#ifdef ESP8266
// -------------------------------- Hexa Driver 2.0 --------------------------------

	#include "PinDefinitionsRev2_00.h"
	#include "HexaBridge.h"

class LinearActuator: public HexaBridge {

	private:
		const byte LinearActuatorID;


		int virtualPosition;
		bool motorDirection;
		unsigned long velocityTime;
		int velocityLastPos;
		float rpm;

	public:
		LinearActuator(const byte _LinearActuatorID);
		void VelocityUpdate();
		int GetEncoderPos();
		float GetEncoderRPM();
		bool getMotorDir();
		void SpinMotor(unsigned char dutyCycle, unsigned char direction);
		void encoderUpdate();
		
		bool enableLA;
};


#elif defined MCU_STM32F103CB
// -------------------------------- Hexa Driver 1.0 --------------------------------

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
		const laFormat *LA;

		volatile int virtualPosition; //Updated by the ISR through a glue routine
		bool motorDirection;
		unsigned long velocityTime;
		int velocityLastPos;
		float rpm;
		
	public:
		LinearActuator(const byte _LinearActuatorID);
		void EncoderInterruptHandler();
		void VelocityUpdate();
		int GetEncoderPos();
		float GetEncoderRPM();
		void ResetEncoderPos();
		LinearActuator* getInstance(uint8_t instanceID);
		void SpinMotor(unsigned char dutyCycle, unsigned char direction);
		bool getMotorDir();
		bool enableLA;
};

#endif

#endif
