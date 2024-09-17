# Monarch Solar Radiation
~ an on-going research project~

---
**Last updated:** 
2024-09-17 
![Zeros in IR S in bins](zeros_in_IR_S_u.png)

I was wondering if the the zeros from IR short wave frequently around a specific time of the day but turn out after I bin them into hours and bar graph all of the zeros with high Pyrometer values, the patterns tells me it happened a lot around the early hours and interestingly the whole day of 25 of June. I checked the photos of the sky it looks blue and with normal clouds. Still don't know why, perhaps this is due to hardware issue?

![Sky BGR signature](completeskysignature.png)

*Figure 1: Sky BRG Signature between the 7 June to 28 August*

Interesting finding: between the 14 and 16 of June, I checked with the past weather and they reported those days to have a lot of smoke in the air.
We can also see the day light getting shorter approaching August.

![Sensors data](convertUTC_hour6_to_hour17.png)

*Figure 2: Sensors data v Pyro between the hour 6 to hour 17*

Converted UTC to Central Time and only select data between 6 AM and 5 PM
Data is filtered to remove error data which usually occur by hardware or during night time. Still need to check on why short wavelength of IR caused the staircase patterns.

![Blue Value vs Pyros](blue_v_pyro_hour6_to_hour17.png)

*Figure 3: Blue value vs Pyro between the 7 to 30*

I averaged the Pyro data and the Blue value data with mean of interval of 15 mins (only able to look into the data between the 7 of June to 30 of June, my computer is still processing for the month of July)


---

Using Arduino IDE version 1.8.9 and libraries found here: https://github.com/NorthernWidget/NorthernWidget-libraries
