#include "Margay.h"
#include "MonarchSW.h"
#include "MonarchLW.h"

// Instantiate classes
Margay Logger;
MonarchSW PyroUp(UP);
MonarchSW PyroDown(DOWN);

// Empty header to start; will include sensor labels and information
String Header = "";

//Number of seconds between readings
uint32_t updateRate = 5;

void setup(){
    Header = Header + "Kipp and Zonen Voltage [uV]"+ PyroUp.GetHeader() + PyroDown.GetHeader();
    Logger.begin(Header);
    init();
}

void loop(){
    Logger.run(update, updateRate);
}

String update() 
{
    initialize();
    return String(1E6*Logger.getVoltage(), 2);
}

void initialize()
{
  PyroUp.begin();
  PyroDown.begin();
}
