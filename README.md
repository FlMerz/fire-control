# Fire-Control
Burning control system for fireplace stoves using Nextion HMI and Raspberry Pi

#### This should work with all Raspberry Pi OS versions using Python 3

## Contents
 - [How it works](#how-it-works)
 - [Wishlist](#wishlist)


## How It Works
- With the help of two temperature sensors, the ambient air and the flue gas temperature of the fireplace stove are measured continuously.
- In addition, a controllable flap is installed, which regulates the supply air of the stove.
- The measured temperatures can be constantly viewed and the supply air damper controlled via a nextion touch screen display. There are two main modes:
	- Manual mode: the flap can be changed manually with the touchscreen.
	- Automatic mode: the flap will be controlled automatically by the system according to a previously defined burn-off plan. 

## How It Looks
![home_small](https://user-images.githubusercontent.com/53577414/123110636-8fc34f00-d43c-11eb-9348-e81a96ed954e.png)
![booting_small](https://user-images.githubusercontent.com/53577414/123110642-905be580-d43c-11eb-8eb2-37df1d14c5b0.png)
![settings_small](https://user-images.githubusercontent.com/53577414/123110644-90f47c00-d43c-11eb-8065-2305f856193a.png)

## Wishlist
- [x] Touch Screen User Interface
- [x] automatic burning control mode
- [x] Adjustable temperature thresholds
- [X] Adjustable flap angle
- [ ]Push Notifications
- [ ] Sensor Data History/Analysis

## Quick Start
### Required Components
- Raspberry Pi 2/3/4/Zero W
- 2x MAX6675 thermocouple temperature sensor (https://www.ebay.de/itm/263964113903?chn=ps&norover=1&mkevt=1&mkrid=707-134425-41852-0&mkcid=2&itemid=263964113903&targetid=1270189284895&device=c&mktype=pla&googleloc=9042036&poi=&campaignid=10215345553&mkgroupid=121910809866&rlsatarget=pla-1270189284895&abcId=1139676&merchantid=138392580&gclid=Cj0KCQjw2tCGBhCLARIsABJGmZ5eEra1b4BY8w6KihOV1sGYpxA53kfeBiOwwdrOmiQ_DBX4XFSt5ocaAoviEALw_wcB)
- Nextion HMI Display
- 5V Stepper Motor 28BYJ-48 (https://www.ebay.de/itm/124249372345?chn=ps&norover=1&mkevt=1&mkrid=707-134425-41852-0&mkcid=2&itemid=124249372345&targetid=1270189284895&device=c&mktype=pla&googleloc=9042036&poi=&campaignid=10215345553&mkgroupid=121910809866&rlsatarget=pla-1270189284895&abcId=1139676&merchantid=264423133&gclid=Cj0KCQjw2tCGBhCLARIsABJGmZ7SxR_i_RQwt0P7kzWOgs_puYKtfj3WOd3sbRYRelPgXiuvWWkBhAMaArTDEALw_wcB)
### Pinout 
![Pinout_fire-control](https://user-images.githubusercontent.com/53577414/123318071-19534980-d52f-11eb-9d3f-2edc4d2faeeb.png)



