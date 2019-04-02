# Hexa-Driver
Firmware for the Hexa H-Bridge driver board with encoder position feedback based on the STM32F103 MCU

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
