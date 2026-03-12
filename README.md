# H1 - Pico_Projects
This is not yet pretty but functions - images to be added later

## H2 - mq135_uncalibrated sensor
Using the mq135 and a raspberry pico the raw readout from the sensor can be monitored using the Thonny plotting interface. The threshold is set arbirarily to light the LED

Modifications would include - converting the readout to usable values
                            - making the system read to remote access 
                            - Traffic light system green is good red is bad

## H3 - AS7341
The as7341.py file is a library which is micropython compatible (does not make an error due to a lack of circuit python)
In order to make this work, download the file and then save the file to the root of your pico (not in the lib folder)
