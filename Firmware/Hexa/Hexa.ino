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

	LA5.update();

	if (spinRunning){
		//LA5.closedSpinTest();
		LA5.position();
	} else {
		LA5.SpinMotor(0, dirB);
	}

}
