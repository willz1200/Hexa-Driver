/******************************************************************************
 * @File		Hexa.ino
 * @Brief		Arduino file that uses Hexa class to spin up motor between a
 *				start/end point. Also Implements super janky deceleration code
 *				to help stop overshoot, current test speed is 75/255 duty.
 * @Date		20/11/2019 (Last Updated)
 * @Author(s)	William Bednall
 ******************************************************************************/

#include "CommandDefinitions.h"

Controller *Dev_LA = &LA0;

unsigned long timeSince;

void setup() {
	Serial.begin(115200);
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

	if (spinRunning == 1){
		Dev_LA->position();
	} else if(spinRunning == 2){
		Dev_LA->runTimeSweep();
	} else if(spinRunning == 3){
		Dev_LA->runTimeSingleUpdate();
	} else {
		Dev_LA->SpinMotor(0, dirB);
	}

}
