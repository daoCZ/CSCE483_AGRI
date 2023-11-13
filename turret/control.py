# fov, 130 d, 100 h
# res, 480p 90fps

import numpy as np
import time
import RPi.GPIO as GPIO
import concurrent.futures
# look at library test files for context
from RpiMotorLib import RpiMotorLib

lastTime = None
Setpoint = None
errSum = None
lastErr = None
kp = None
ki = None
kd = None
SampleTime = 1

def Compute():
	# compute time delta
	now = time.perf_counter()
	timeChange = now - lastTime
	if timeChange >= SampleTime:
		# error computations
		error = Setpoint
		errSum += error * timeChange
		dErr = (error - lastErr) / timeChange
		
		# compute output
		Output = kp * error + ki * errSum + kd * dErr
		
		# memory
		lastErr = error
		lastTime = now

def SetTunings(Kp, Ki, Kd):
	kp = Kp
	ki = Ki
	kd = Kd

def SetSampleTime(NewSampleTime):
	if NewSampleTime > 0:
		ratio = NewSampleTime/SampleTime
		ki *= ratio
		kd /= ratio
		SampleTime = NewSampleTime

pinsYaw = [17, 27, 22, 5]
pinsPitch = [23, 24, 25, 16]

YawMotor = RpiMotorLib.BYJMotor("YawMotor", "28BYJ")
PitchMotor = RpiMotorLib.BYJMotor("PitchMotor", "28BYJ")

