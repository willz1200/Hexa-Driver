/******************************************************************************
 * @File		HexaBridge.h
 * @Brief		Low level driver for the Hexa Bridge 
 				Linear Actuator Logic Interface
 * @Date		28/04/2020 (Last Updated)
 * @Author(s)	William Bednall
 ******************************************************************************/

#ifndef HexaBridge_h
#define HexaBridge_h

#ifdef ESP8266
// --- Hexa Driver 2.0 ---

#include "PinDefinitionsRev2_00.h"

class HexaBridge {

	private:

		
	public:
		HexaBridge();

};


#elif defined MCU_STM32F103CB
// --- Hexa Driver 1.0 ---
// Do nothing as Hexa Driver 1.0 doesn't have a Hexa Bridge
#endif

#endif
