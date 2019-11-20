/******************************************************************************
 * @File		Hexa.ino
 * @Brief		Arduino file that uses Hexa class to spin up motor between a
 *				start/end point. Also Implements super janky deceleration code
 *				to help stop overshoot, current test speed is 75/255 duty.
 * @Date		20/11/2019 (Last Updated)
 * @Author(s)	William Bednall
 ******************************************************************************/

#include "CommandDefinitions.h"

//Swap these numbers if its not stopping
#define dirA 1 //Spin ->
#define dirB 2 //Spin <-

unsigned long timeSince, timeSinceB;

void setup() {
	Serial.begin(115200);

	//Duty cycle can be 0-255
	//LA0.SpinMotor(0, dirB); //Start Spinning Motor

	/* - Only testing on LA0 for now
	LA1.SpinMotor(75, dirB); //Start Spinning Motor
	LA2.SpinMotor(75, dirB); //Start Spinning Motor
	LA3.SpinMotor(75, dirB); //Start Spinning Motor
	LA4.SpinMotor(75, dirB); //Start Spinning Motor
	LA5.SpinMotor(75, dirB); //Start Spinning Motor
	*/

	CLI.bind(cmd_bind,cmd_total);
	timeSince = millis();
	timeSinceB = millis();
}

void loop() {
	//closedSpinTest(LA0);
	if (millis() - timeSince > 100){
		CLI.loop();
		timeSince = millis();
		//Serial.println(LA5.GetEncoderRPM());
	}

	if (millis() - timeSinceB > 20){
		timeSinceB = millis();
		LA5.VelocityUpdate();
		Serial.print(LA5.GetEncoderPos());
		Serial.print(", ");
		Serial.println(LA5.GetEncoderRPM());
	}

	if (spinRunning){
		//LA5.closedSpinTest();
		LA5.position();
	} else {
		LA5.SpinMotor(0, dirB);
	}
	

	/* - Only testing on LA0 for now
	closedSpinTest(LA1);
	closedSpinTest(LA2);
	closedSpinTest(LA3);
	closedSpinTest(LA4);
	closedSpinTest(LA5);
	*/

	//Serial.println("");//Move to next line in serial monitor
}

//Super janky feedback loop :O
/*void closedSpinTest(Controller &m){
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
}*/
