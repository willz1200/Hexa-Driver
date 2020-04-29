/******************************************************************************
 * @File		PinDefinitionsRev2_00.h
 * @Brief		Pin definitions for revision 2.00 of the Hexa Driver PCB,
 *				based on the ESP8285 SoC and Hexa Bridge.
 * @Date		28/04/2020 (Last Updated)
 * @Author(s)	William Bednall
 ******************************************************************************/
#ifndef PinDefinitionsRev2_00_h
#define PinDefinitionsRev2_00_h

//I2C
#define I2C_SCL 1
#define I2C_SDA 0

//Boost

//Hexa Bridge
//	SPI & Reset

//Debug/Test Hardware
#define LED 2

//I2C Address
#define INA_1		0x0
#define INA_2		0x0
#define MAX_ADDR	0x0

//Hexa Bridge Commands
#define HB_RESET 		0x1
#define HB_LED_ON		0x2
#define HB_LED_OFF		0x3

#define HB_VERSION 		0x5
#define HB_PROTOCOL 	0x6

#define HB_READ_ENCODER 0xA
#define HB_SET_MOTOR 	0xD

//Hexa Bridge LA Addresses
#define HB_LA0 			0x1
#define HB_LA1 			0x2
#define HB_LA2 			0x4
#define HB_LA3 			0x8
#define HB_LA4 			0x10
#define HB_LA5 			0x20

//Encoder Constants
#define PulsesPerTurn 7.0
#define GearReduction 30.0 //Gear Reduction Ratio is 1:30

#endif
