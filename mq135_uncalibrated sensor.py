from machine import Pin, ADC
import time

#attach sensor to the listed pin - check that this matches
mq135 = ADC(Pin(26))

#turn on the onboard LED
led = Pin("LED", Pin.OUT)

#set the threshold - at this stage its arbitrary units
threshold = 10100
while True:
    #get an analog output - NB its just numbers at this stage
    sensor_value = mq135.read_u16()
    
    print("Sensor Value:", sensor_value)
    
    if sensor_value > threshold:
        lef.on()
    else:
        led.off()
        
    time.sleep(0.5)