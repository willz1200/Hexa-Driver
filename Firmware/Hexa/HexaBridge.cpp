/******************************************************************************
 * @File		HexaBridge.cpp
 * @Brief		Low level driver for the Hexa Bridge 
 				Linear Actuator Logic Interface
 * @Date		28/04/2020 (Last Updated)
 * @Author(s)	William Bednall
 ******************************************************************************/

#ifdef ESP8266
// --- Hexa Driver 2.0 ---

#include <Arduino.h>
#include "HexaBridge.h"

SPISettings HexaBridgeConf(1000000, MSBFIRST, SPI_MODE3);

HexaBridge::HexaBridge(){
	//Setup the Hexa Bridge here
	pinMode(15, OUTPUT);
	SPI.setDataMode(SPI_MODE3);
	SPI.setFrequency(1000000);
	SPI.setHwCs(true);
	SPI.begin();
}

void HexaBridge::init(){
	SPI.beginTransaction(HexaBridgeConf);
	SPI.transfer(HB_RESET);
	SPI.endTransaction();
}

int32_t HexaBridge::readEncoder(uint8_t laAddr){
	int32_t encoderData;
	if (laAddr == HB_LA0 || laAddr == HB_LA1 || laAddr == HB_LA2 || laAddr == HB_LA3 || laAddr == HB_LA4 || laAddr == HB_LA5){
		SPI.beginTransaction(HexaBridgeConf);
		SPI.transfer(HB_READ_ENCODER);
		SPI.transfer(laAddr);
		encoderData = SPI.transfer(0);
		encoderData |= SPI.transfer(0) << 8;
		encoderData |= SPI.transfer(0) << 16;
		encoderData |= SPI.transfer(0) << 24;
		SPI.endTransaction();
		return encoderData;
	}
	return 0;
}

void HexaBridge::setMotor(uint8_t laAddr, uint8_t en, uint8_t dir, uint8_t dutyCycle){
	//delayMicroseconds(20);
	if (laAddr == HB_LA0 || laAddr == HB_LA1 || laAddr == HB_LA2 || laAddr == HB_LA3 || laAddr == HB_LA4 || laAddr == HB_LA5){
		uint8_t cnf = (dir << 1) | en;
		//Serial.println(cnf);
		SPI.beginTransaction(HexaBridgeConf);
		SPI.transfer(HB_SET_MOTOR);
		SPI.transfer(laAddr);
		SPI.transfer(cnf);
		SPI.transfer(dutyCycle);
		SPI.endTransaction();
	}
	//delayMicroseconds(20);
}

uint8_t HexaBridge::getVersion(){
	uint8_t hbVersion;
	SPI.beginTransaction(HexaBridgeConf);
		SPI.transfer(HB_VERSION);
		hbVersion = SPI.transfer(0);
	SPI.endTransaction();
	return hbVersion;
}

uint8_t HexaBridge::getProtocol(){
	uint8_t hbProtocol;
	SPI.beginTransaction(HexaBridgeConf);
		SPI.transfer(HB_PROTOCOL);
		hbProtocol = SPI.transfer(0);
	SPI.endTransaction();
	return hbProtocol;
}

#elif defined MCU_STM32F103CB
// --- Hexa Driver 1.0 ---
// Do nothing as Hexa Driver 1.0 doesn't have a Hexa Bridge
#endif

