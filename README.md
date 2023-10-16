<h1 align="center">
  <br>
  <a href="https://github.com/her3ticAVI/TOUCANBus"><img src="./images/toucanbus.png" alt="toucan"></a>
  <br>
</h1>

This is a tool to automate the usage of can-utils and turn pentesting Car CANBUS into a streamlined process.

## Capabillities:
1. Record CAN Bus Data and dump the output into a log file specified by the user
2. Dump live CAN Data into the terminal to monitor live CAN Bus activity and traffic
3. Select and equipt CAN Bus log files for attacks and parsing 
4. Parse Can Bus log Files to compare static recording to mutated recording to find can codes for specific actions 
5. Play file back into the can bus, AKA replay attack
6. Find specific Codes in a file that do specified things by process of elimination
7. Play Specified Code selected by the user back into the can bus for more precise attacks 
8. Filters that can be saved and loaded from a log file to filter out data during run-time

## Use-Cases:
1. Can be used for vehicular pentesting on and off the field
2. Trouble shooting CAN bus error codes, check engine light, etc
3. Party tricks such as remote control
4. Deeper understanding of the CAN Bus protocal

## Hardware Required:
1. https://www.8devices.com/products/usb2can_korlan
2. https://www.raspberrypi.com/
3. Any sort of power supply.

## Setup:
###  Headless:
* Download RaspAP[^1] on a raspberry pi setup an ssh connection and use this script for remote can bus interaction
###  Computer:
*    Plug the usb2can into the computer and have fun :)
[^1]: https://github.com/RaspAP/raspap-webgui
