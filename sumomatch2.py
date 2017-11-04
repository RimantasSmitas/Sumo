import RPi.GPIO as GPIO
import time
import atexit

PWMA = 2
PWMB = 3

AIN1 = 17
AIN2 = 27
BIN1 = 22
BIN2 = 10

A = 13 #Left
B = 6 #Middle
C = 5 # Right
D = 19 # Back

sonarIn = 21
sonarOut = 20

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

#setting the motors
GPIO.setup(PWMA, GPIO.OUT)
GPIO.setup(PWMB, GPIO.OUT)
GPIO.setup(AIN1, GPIO.OUT)
GPIO.setup(AIN2, GPIO.OUT)
GPIO.setup(BIN1, GPIO.OUT)
GPIO.setup(BIN2, GPIO.OUT)

#setting up the IR sensors
GPIO.setup(A, GPIO.IN)
GPIO.setup(B, GPIO.IN)
GPIO.setup(C, GPIO.IN)
GPIO.setup(D, GPIO.IN)

#setting up the sonar
GPIO.setup(sonarOut, GPIO.OUT)
GPIO.setup(sonarIn, GPIO.IN)

#exit function
@atexit.register
def goodbye():
        GPIO.cleanup()


#reading the sonar function returns the distance
#code from the teacher
def findEnemyDistance(sensor):
    pingtime = 0
    echotime = 0
    if sensor == 0:
        GPIO.output(sonarOut,GPIO.LOW)
        GPIO.output(sonarOut,GPIO.HIGH)
        pingtime=time.time()
        time.sleep(0.00001)
        GPIO.output(sonarOut,GPIO.LOW)
        while GPIO.input(sonarIn)==0:
            pingtime = time.time()
        while GPIO.input(sonarIn)==1:
            echotime=time.time()
        if (echotime is not None) and (pingtime is not None):
            elapsedtime = echotime - pingtime
            distance = elapsedtime * 17000
        else:
            distance = 0
        print(pingtime)
        print(echotime)
        return distance

#turn motor functions

def setMotorA(motorShouldRun):
    if (motorShouldRun):
        GPIO.output(AIN1, GPIO.HIGH)
        GPIO.output(AIN2, GPIO.LOW)
        GPIO.output(PWMA, GPIO.HIGH)
    else:
        GPIO.output(PWMA, GPIO.LOW)

def setMotorABackwards(motorShouldRun):
    if (motorShouldRun):
        GPIO.output(AIN1, GPIO.LOW)
        GPIO.output(AIN2, GPIO.HIGH)
        GPIO.output(PWMA, GPIO.HIGH)
    else:
        GPIO.output(PWMA, GPIO.LOW)


def setMotorB(motorShouldRun):
    if (motorShouldRun):
        GPIO.output(BIN1, GPIO.HIGH)
        GPIO.output(BIN2, GPIO.LOW)
        GPIO.output(PWMB, GPIO.HIGH)
    else:
        GPIO.output(PWMB, GPIO.LOW)


def setMotorBBackwards(motorShouldRun):
    if (motorShouldRun):
        GPIO.output(BIN1, GPIO.LOW)
        GPIO.output(BIN2, GPIO.HIGH)
        GPIO.output(PWMB, GPIO.HIGH)
    else:
        GPIO.output(PWMB, GPIO.LOW)


def forward():
    print('Going forwards')
    setMotorA(True)
    setMotorB(True)


def stop():
    print('Set both motors to stop')
    setMotorA(False)
    setMotorB(False)

def right():
    print('Turn right')
    setMotorABackwards(True)
    setMotorB(True)

def left():
    print('Turn left')
    setMotorA(True)
    setMotorBBackwards(True)

def backwards():
    # Reversing the GPIO direction for backwards flow.
    print("Going backwards")
    setMotorABackwards(True)
    setMotorBBackwards(True)


#Fighting functions
def escapeBack():
    print("Escaping to the back.")
    backwards()
    time.sleep(2)
    stop()

def charge():
    print("Charge forward")
    while sensorsFrontClean() == True:
        forward()
        
    escapeBack()

#Checking the sensors around the car

def sensorsFrontClean():
    if A == 0 and B == 0 and C == 0:
        return True
	print(A, B, C)
    return False


def sensorBackClean():
    if D == 0:
        return True
    return False


#main code
def lookForEnemy():
    range = findEnemyDistance(0)
    if sensorsFrontClean() == False:
        escapeBack()
    elif sensorBackClean() == False:
        charge()
    else:
        if range > 50:
            left()
        elif range < 50:
            charge()


#the actual code run
while True:
    lookForEnemy()
    time.sleep(.1)



