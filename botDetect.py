from gpiozero import Button
from gpiozero import LED
import time
import camCap
#this checks a a gpio from the arduino. If the pin goes high, there is an object on the staging area

photoRes = Button(26,hold_time=0.5)
sig0 = LED(20)
sig1 = LED(21)
ready = LED(16)
state = 0
#check for arduino signal
ready.on()
def sendMsg(c):
	if c == 0:
		sig0.off()
		sig1.off()
	elif c == 1:
		sig0.on()
		sig1.off()
	elif c == 2:
		sig0.off()
		sig1.on()
	elif c == 3:
		sig0.on()
		sig1.on()
	else:
		print("ERROR: Invalid Classification")
	photoRes.wait_for_release()

def imgCap():
    return camCap.takePic()

def changeState():
    if photoRes.is_held:
        return imgCap()
    else:
        return 0

while True:
    state = changeState()
    
    #print ("state: " + str(state))
    sendMsg(state)

    time.sleep(1)
    state = 0
