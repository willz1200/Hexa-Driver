/******************************************************************************
 * @File		PinDefinitionsRev1_00.h
 * @Brief		Pin definitions for revision 1.00 of the hexa driver PCB,
 *				based on the STM32F103CBT6 MCU.
 * @Date		17/11/2019 (Last Updated)
 * @Author(s)	William Bednall
 ******************************************************************************/
#ifndef PinDefinitionsRev1_00_h
#define PinDefinitionsRev1_00_h

//Motor Drivers
#define Motor1_PWM 3
#define Motor2_PWM 15
#define Motor3_PWM 16
#define Motor4_PWM 25
#define Motor5_PWM 26
#define Motor6_PWM 27

#define Motor1_DIR 2
#define Motor2_DIR 19
#define Motor3_DIR 20
#define Motor4_DIR 21
#define Motor5_DIR 22
#define Motor6_DIR 28

//Hall Effect Quadrature Encoders
#define Encoder1_INT 13
#define Encoder2_INT 14
#define Encoder3_INT 12
#define Encoder4_INT 31
#define Encoder5_INT 17
#define Encoder6_INT 18

#define Encoder1_PHA 11
#define Encoder2_PHA 7
#define Encoder3_PHA 10
#define Encoder4_PHA 30
#define Encoder5_PHA 5
#define Encoder6_PHA 29

#define Encoder1_Flip 1 //Some of the C1 and C2 lines for the encoder are swapped on the PCB
#define Encoder2_Flip 0
#define Encoder3_Flip 1
#define Encoder4_Flip 1
#define Encoder5_Flip 1
#define Encoder6_Flip 0

//Linear Actuator Signal Structure
struct laFormat {
	const unsigned char MotorPWM;
	const unsigned char MotorDIR;
	const unsigned char EncoderINT;
	const unsigned char EncoderPHA;
	const bool EncoderFlip;
};

const laFormat LinearActuatorsAvailable[6] PROGMEM = {
	{ Motor1_PWM, Motor1_DIR, Encoder1_INT, Encoder1_PHA, Encoder1_Flip },
	{ Motor2_PWM, Motor2_DIR, Encoder2_INT, Encoder2_PHA, Encoder2_Flip },
	{ Motor3_PWM, Motor3_DIR, Encoder3_INT, Encoder3_PHA, Encoder3_Flip },
	{ Motor4_PWM, Motor4_DIR, Encoder4_INT, Encoder4_PHA, Encoder4_Flip },
	{ Motor5_PWM, Motor5_DIR, Encoder5_INT, Encoder5_PHA, Encoder5_Flip },
	{ Motor6_PWM, Motor6_DIR, Encoder6_INT, Encoder6_PHA, Encoder6_Flip }
};

//I2C
#define I2C_SCL 1
#define I2C_SDA 0

//Debug/Test Hardware
#define LED 33
#define BUTTON 32

//I2C Address
#define INA219_1		0x40
#define INA219_2		0x41
#define INA219_3		0x42
#define INA219_4		0x43
#define INA219_5		0x44
#define INA219_6		0x45
#define MPU6050_ADDR	0x68

//IO Expander Breakout 						(Connector = SH1-0 10P 1.0mm)
					//3.3V (up to 500mA)	(Pin 1)
#define ExpIO_1 0	//I2C SDA				(Pin 2)
#define ExpIO_2 1	//I2C SCL				(Pin 3)
#define ExpIO_3 9	//UART Tx, PWM, ADC		(Pin 4)
#define ExpIO_4 8	//UART Rx, PWM, ADC		(Pin 5)
#define ExpIO_5 6	//SPI SCK, ADC			(Pin 6)
#define ExpIO_6 4	//SPI MOSI, PWM, ADC	(Pin 7)
#define ExpIO_7 32	//Button				(Pin 8)
#define ExpIO_8 33	//LED					(Pin 9)
					//GND					(Pin 10)

#endif
