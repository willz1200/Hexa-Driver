# Hexa Driver
Firmware and overview for the Hexa H-Bridge driver board with encoder position feedback based on the STM32F103 MCU designed for Sheffield Bionics.

## Features

* STM32F103CBT6 Microcontroller (ARM 32-bit Cortex-M3)
  * Clock Speed 72 MHz
  * Flash 128 KB
  * RAM 20 KB
  * STM32duino Bootloader
* x6 Linear Actuator Channels Each Containing:
  * L9110S 800mA H-bridge Driver with PWM Control
  * INA219 Bidirectional Current Monitor (0.1Ω Shunt)
  * Quadrature Encoder Input with Hardware Schmitt Trigger Debouncing
* MPU-6050 Six-Axis (Gyro + Accelerometer)
* IO Expansion Header with 3.3V, ADC, I2C, SPI out, PWM, UART (SH1.0-10P)
* USB Micro B Port for Programming the MCU
* 12V 3.5A Boost Convert for the Linear Actuaor DC Motors
* 3.3V 800mA Low-Dropout Voltage Regulator
* 5V up to 4A Auto Switching External Power Input (5V 1.3mm DC Barrel Jack).
* Single Cell 1A Constant-Current / Constant-Voltage Linear Lithium Polymer Charger (Set to 800mA)
* Button and LED for Testing / Debugging Purposes
* 1.27mm Header for SWD & JTAG Interface

## How to Use Within the Arduino IDE

* Install the [Arduino STM32](https://github.com/rogerclarkmelbourne/Arduino_STM32) add on via the following steps:
  * Download the Arduino STM32 repo as a zip file
  * Navigate to the arduino directory usually, Documents -> Arduino
  * Create a new folder in the arduino directory called "hardware" if it doesn't already exist
  * Unzip the Arduino STM32 repo into the hardware, ensuring the repo is in a folder called "Arduino_STM32"
* Install the "Arduino SAM boards (32-bits ARM Cortex-M3)" which can be found in Boards Manager by default
* Go to Documents/Arduino/hardware/Arduino_STM32/drivers/win and double click install_drivers.bat
* You will need to restart the Arduino IDE
* The Arduino IDE is now setup to flash the board which can be acomplished with the following steps:
  * Select "Maple Mini" Under 'Tools → Board' in the Arduino IDE
  * Select "Bootloader 2.0 (20k RAM, 120k Flash)" Under 'Tools → Bootloader Version' in the Arduino IDE
  * Select the Correct COM Port
  * Upload The Code

## Hexa Driver PCB

![Hexa Render](https://raw.githubusercontent.com/willz1200/Hexa-Driver/master/Documentation/PCB-R1_00-3D-Render.png "Hexa Driver 3D Render")

![Hexa Pinout](https://raw.githubusercontent.com/willz1200/Hexa-Driver/master/Documentation/PCB-R1_00-pinout.png "Hexa Driver Side View Pinout")

## Bugs That Will Be Fixed in the Next Release (Rev 1.0 -> Rev 2.0) 
* [ ] Minimum input voltage for the XL6009S 12V boost converter is 5V, the main power input is 5V but the lithium-ion battery is 3.7 - 4.2V. Therefore a boost converter with a minimum input voltage of at least 3.5V must be implemented, TPS611781RNWR looks promising.
* [ ] USB connector and power jack are slightly too close together, adding a few millimeters of space between them would be nice. Possibly replace both with one USB C port.
* [ ] The input polyfuse is causing a voltage drop at the 5V input, which is resulting in the XL6009S boost converter being under voltaged and not starting up correctly. In some cases the boost converter has been seen too output 25V in this unstable state. The temporary fix was to remove the polyfuse and directly connect the 5V input.
* [ ] When running the motor at full speed the STM32 starts to hang because it doesn't have enough clock cycles per second to handle all of the encoder interrupts. An FPGA (ICE40LP8K-CM81) could be used to track encoder movement and relieve the STM32.
* [ ] The main power switch has been known to fail, maybe an alternative could be used. Ideally a 3D printed casing should provide a switch covering.

## Linear Actuator Pin Definitions

| Linear Actuator No. | Motor PWM | Motor Direction | Encoder Interrupt | Encoder Phase |
|---------------------|-----------|-----------------|-------------------|---------------|
| 1                   | D3        | D2              | D13               | D11           |
| 2                   | D15       | D19             | D14               | D7            |
| 3                   | D16       | D20             | D12               | D10           |
| 4                   | D25       | D21             | D31               | D30           |
| 5                   | D26       | D22             | D17               | D5            |
| 6                   | D27       | D28             | D18               | D29           |

## PCB Pin Definitions (STM32F103CBT6)

| Pin | GPIO | ADC | Timer (PWM) | I2C    | UART  | SPI    | 5 V? | PCB Function           | Notes                                                                             |
|-----|------|-----|-------------|--------|-------|--------|------|------------------------|-----------------------------------------------------------------------------------|
| D0  | PB11 |     |             | 2_SDA  | 3_RX  |        | Yes  | I2C SDA / IO Expander  | Also used for current sense (Must be I2C)                                         |
| D1  | PB10 |     |             | 2_SCL  | 3_TX  |        | Yes  | I2C SCL / IO Expander  | Also used for current sense (Must be I2C)                                         |
| D2  | PB2  |     |             |        |       |        | Yes  | M1 Direction           |                                                                                   |
| D3  | PB0  | CH8 | 3_CH3       |        |       |        |      | M1 PWM                 |                                                                                   |
| D4  | PA7  | CH7 | 3_CH2       |        |       | 1_MOSI |      | SPI MOSI / IO Expander | Could be used for screen or analogue input                                        |
| D5  | PA6  | CH6 | 3_CH1       |        |       | 1_MISO |      | E5 Phase               |                                                                                   |
| D6  | PA5  | CH5 |             |        |       | 1_SCK  |      | SPI SCK / IO Expander  | Could be used for screen or analogue input                                        |
| D7  | PA4  | CH4 |             |        | 2_CK  | 1_NSS  |      | E2 Phase               |                                                                                   |
| D8  | PA3  | CH3 | 2_CH4       |        | 2_RX  |        |      | UART Rx / IO Expander  | uart or analogue input                                                            |
| D9  | PA2  | CH2 | 2_CH3       |        | 2_TX  |        |      | UART Tx / IO Expander  | uart or analogue input. Jumper to 12V Enable Line (only solder 1 of the jumpers!) |
| D10 | PA1  | CH1 | 2_CH2       |        | 2_RTS |        |      | E3 Phase               |                                                                                   |
| D11 | PA0  | CH0 | 2_CH1_ETR   |        | 2_CTS |        |      | E1 Phase               |                                                                                   |
| D12 | PC15 |     |             |        |       |        |      | E3 Interrupt           |                                                                                   |
| D13 | PC14 |     |             |        |       |        |      | E1 Interrupt           |                                                                                   |
| D14 | PC13 |     |             |        |       |        |      | E2 Interrupt           |                                                                                   |
| D15 | PB7  |     | 4_CH2       | 1_SDA  |       |        | Yes  | M2 PWM                 |                                                                                   |
| D16 | PB6  |     | 4_CH1       | 2_SCL  |       |        | Yes  | M3 PWM                 |                                                                                   |
| D17 | PB5  |     |             | 1_SMBA |       |        |      | E5 Interrupt           |                                                                                   |
| D18 | PB4  |     |             |        |       |        | Yes  | E6 Interrupt           |                                                                                   |
| D19 | PB3  |     |             |        |       |        | Yes  | M2 Direction           |                                                                                   |
| D20 | PA15 |     |             |        |       |        | Yes  | M3 Direction           |                                                                                   |
| D21 | PA14 |     |             |        |       |        | Yes  | M4 Direction           | SWCLK                                                                             |
| D22 | PA13 |     |             |        |       |        | Yes  | M5 Direction           | SWDIO                                                                             |
| D23 | PA12 |     | 1_ETR       |        | 1_RTS |        | Yes  | USB D+                 |                                                                                   |
| D24 | PA11 |     | 1_CH4       |        | 1_CTS |        | Yes  | USB D-                 |                                                                                   |
| D25 | PA10 |     | 1_CH3       |        | 1_RX  |        | Yes  | M4 PWM                 |                                                                                   |
| D26 | PA9  |     | 1_CH2       |        | 1_TX  |        | Yes  | M5 PWM                 |                                                                                   |
| D27 | PA8  |     | 1_CH1       |        | 1_CK  |        | Yes  | M6 PWM                 |                                                                                   |
| D28 | PB15 |     |             |        |       | 2_MOSI | Yes  | M6 Direction           |                                                                                   |
| D29 | PB14 |     |             |        | 3_RTS | 2_MISO | Yes  | E6 Phase               |                                                                                   |
| D30 | PB13 |     |             |        | 3_CTS | 2_SCK  | Yes  | E4 Phase               |                                                                                   |
| D31 | PB12 |     | 1_BKIN      | 2_SMBA | 3_CK  | 2_NSS  | Yes  | E4 Interrupt           |                                                                                   |
| D32 | PB8  |     | 4_CH3       |        |       |        | Yes  | Button / IO Expander   | Button can also put board in DFU (device firmware update) mode during boot        |
| D33 | PB1  | CH9 | 3_CH4       |        |       |        |      | LED / IO Expander      | Jumper to 12V Enable Line (only solder 1 of the jumpers!)                         |


## Useful Links

* [Arduino_STM32](https://github.com/rogerclarkmelbourne/Arduino_STM32)
* [Measure PWM Current with a Modified Moving Average](https://www.baldengineer.com/measure-pwm-current.html)
* [Quadrature Encoder Overview](https://www.dynapar.com/technology/encoder_basics/quadrature_encoder/)

## Licence
