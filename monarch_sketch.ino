#include "Margay.h"
#include "MonarchSW.h"
#include "MonarchLW.h"

// Instantiate classes
Margay Logger;
MonarchSW PyroUp(UP);

// Empty header to start; will include sensor labels and information
String Header = "";

//Number of seconds between readings
uint32_t updateRate = 5;

void setup(){
    Header = Header + "Kipp and Zonen Voltage [uV], "+ PyroUp.GetHeader();
    Logger.begin(Header);
    initialize();
}

void loop(){
    Logger.run(update, updateRate);
}

String update() 
{
    initialize();
    String kz = String(1E6*Logger.getVoltage(), 2);
    String P_update = PyroUp.GetString();
    return kz + ", " + P_update;
}

void initialize()
{
  PyroUp.begin();
}
