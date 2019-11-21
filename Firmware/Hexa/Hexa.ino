/******************************************************************************
 * @File		Hexa.ino
 * @Brief		Arduino file that uses Hexa class to spin up motor between a
 *				start/end point. Also Implements super janky deceleration code
 *				to help stop overshoot, current test speed is 75/255 duty.
 * @Date		20/11/2019 (Last Updated)
 * @Author(s)	William Bednall
 ******************************************************************************/

#include "CommandDefinitions.h"

Controller *Dev_LA = &LA5;

unsigned long timeSince;

void setup() {
	Serial.begin(115200);

	//Duty cycle can be 0-255

	CLI.bind(cmd_bind,cmd_total);
	timeSince = millis();
}

void loop() {
	if (millis() - timeSince > 100){
		CLI.loop();
		timeSince = millis();
		//Serial.println(LA5.GetEncoderRPM());
	}

	Dev_LA->update();

	if (spinRunning){
		//LA5.closedSpinTest();
		Dev_LA->position();
	} else {
		Dev_LA->SpinMotor(0, dirB);
	}

}
