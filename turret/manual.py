import RPi.GPIO as GPIO

# import the library
import concurrent.futures
from RpiMotorLib import RpiMotorLib


GPIOyaw = [17, 27, 22, 5]
GPIOpitch = [23, 24, 25, 16]

GPIO.setmode(GPIO.BCM)
GPIO.setup(6, GPIO.OUT)
GPIO.output(6, True)

# Declare an named instance of class pass a name and motor type
mymotortestYaw = RpiMotorLib.BYJMotor("MyMotorOne", "28BYJ")
mymotortestPitch = RpiMotorLib.BYJMotor("MyMotorTwo", "28BYJ")

# call the function , pass the parameters
# SEQUENTIAL: mymotortest.motor_run(GpioPins , .001, 512, False, True, "full", .05)

yawNEG = True
yawSteps = 256

pitchPOS = True
pitchSteps = 256


# CONCURRENT
with concurrent.futures.ThreadPoolExecutor() as executor:
        f1 = executor.submit(mymotortestYaw.motor_run, GPIOyaw, .001 , yawSteps, yawNEG, False, "full", .05)
        f2 = executor.submit(mymotortestPitch.motor_run, GPIOpitch, .001 , pitchSteps, pitchPOS, False, "full", .05)


GPIO.output(6, False)