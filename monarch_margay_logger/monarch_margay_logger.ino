#include "Margay.h"
#include <DysonSW.h>
// #include "MCP3421.h"  //Inlcude ADC lib // doesn't need this library can use the initA

// MCP3421 CMP3(0x6B);  //Init with addres 0x6B

// DysonSW PyroUp(UP); //Initialzie Upward facing Monarch short wave
DysonSW PyroUp(DOWN);

String header = "Pyro [uV], "; //Information header
// uint8_t I2CVals[3] = {0x40, 0x1D, 0x6B}; 
uint8_t I2CVals[3] = {0x41, 0x1D, 0x6B}; 

unsigned long updateRate = 15; //Number of seconds between readings 

Margay Logger;

void setup() {
	header = header + PyroUp.GetHeader();
	Logger.begin(I2CVals, sizeof(I2CVals), header); //Pass header info to logger
	_init();
}

void loop() {
	Logger.run(update, updateRate);
}

String update() {
	_init(); //DEBUG!
	float Val1 = Logger.getVoltage()*(1.0e6); //Return val in uV, account for gain of amp (100 V/V)
  return String(Val1) + "," + PyroUp.GetString();
}

void _init() 
{
	PyroUp.begin();
}