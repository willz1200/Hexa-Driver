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
#define LED 33

//I2C Address
#define INA_1		0x0
#define INA_2		0x0
#define MAX_ADDR	0x0

//Encoder Constants
#define PulsesPerTurn 7.0
#define GearReduction 30.0 //Gear Reduction Ratio is 1:30

#endif
