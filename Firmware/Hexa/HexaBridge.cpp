/******************************************************************************
 * @File		HexaBridge.cpp
 * @Brief		Low level driver for the Hexa Bridge 
 				Linear Actuator Logic Interface
 * @Date		28/04/2020 (Last Updated)
 * @Author(s)	William Bednall
 ******************************************************************************/

#ifdef ESP8266
// --- Hexa Driver 2.0 ---

#include "HexaBridge.h"

HexaBridge::HexaBridge(){
	//Setup the Hexa Bridge here


}


#elif defined MCU_STM32F103CB
// --- Hexa Driver 1.0 ---
// Do nothing as Hexa Driver 1.0 doesn't have a Hexa Bridge
#endif

