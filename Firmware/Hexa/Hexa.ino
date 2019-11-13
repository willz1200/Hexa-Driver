/******************************************************************************
 * @File		Hexa.ino
 * @Brief		Arduino file that uses Hexa class to spin up motor between a
 *				start/end point. Also Implements super janky deceleration code
 *				to help stop overshoot, current test speed is 75/255 duty.
 * @Date		12/04/2019 (Last Updated)
 * @Author(s)	William Bednall
 ******************************************************************************/

#include "LinearActuator.h"
#include "CommandDefinitions.h"

//Swap these numbers if its not stopping
#define dirA 1 //Spin ->
#define dirB 2 //Spin <-

void setup() {
	Serial.begin(250000);

	//Duty cycle can be 0-255
	LA0.SpinMotor(75, dirB); //Start Spinning Motor
	LA1.SpinMotor(75, dirB); //Start Spinning Motor
	LA2.SpinMotor(75, dirB); //Start Spinning Motor
	LA3.SpinMotor(75, dirB); //Start Spinning Motor
	LA4.SpinMotor(75, dirB); //Start Spinning Motor
	LA5.SpinMotor(75, dirB); //Start Spinning Motor
}

void loop() {
	closedSpinTest(LA0);
	closedSpinTest(LA1);
	closedSpinTest(LA2);
	closedSpinTest(LA3);
	closedSpinTest(LA4);
	closedSpinTest(LA5);
	Serial.println("");//Move to next line in serial monitor
}

//Super janky feedback loop :O
void closedSpinTest(LinearActuator &m){
	if (m.GetEncoderPos() <= 0){
		m.SpinMotor(75, dirB); //Change turning to head towards end point
	}

	//at end point
	if (m.GetEncoderPos() >= 500){
		m.SpinMotor(75, dirA); //Change turning to head towards start point
	}

	if (m.getMotorDir() == true && m.GetEncoderPos() < 50){ m.SpinMotor(50, dirA); } //deceleration to start point
	if (m.getMotorDir() == true && m.GetEncoderPos() < 20){ m.SpinMotor(48, dirA); } //deceleration to start point
	if (m.getMotorDir() == true && m.GetEncoderPos() <= 5){ m.SpinMotor(47, dirA); } //deceleration to start point

	if (m.getMotorDir() == false && m.GetEncoderPos() > 450){ m.SpinMotor(50, dirB); } //deceleration to end point
	if (m.getMotorDir() == false && m.GetEncoderPos() > 480){ m.SpinMotor(48, dirB); } //deceleration to end point
	if (m.getMotorDir() == false && m.GetEncoderPos() >= 495){ m.SpinMotor(47, dirB); } //deceleration to end point

	Serial.print(m.GetEncoderPos());
	Serial.print(", ");
}
