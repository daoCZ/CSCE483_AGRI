# fov, 130 d, 100 h
# res, 480p 90fps

import numpy as np
import time
import RPi.GPIO as GPIO
import concurrent.futures
# look at library test files for context
from RpiMotorLib import RpiMotorLib

SampleTime = 1

YawlastTime = None
YawSetpoint = None
YawerrSum = None
YawlastErr = None
Yawkp = None
Yawki = None
Yawkd = None
YawOutput = None

def ComputeYaw():
	# compute time delta
	now = time.perf_counter()
	timeChange = now - YawlastTime
	if timeChange >= SampleTime:
		# error computations
		error = YawSetpoint
		YawerrSum += error * timeChange
		dErr = (error - YawlastErr) / timeChange
		
		# compute output
		YawOutput = Yawkp * error + Yawki * YawerrSum + Yawkd * dErr
		
		# memory
		YawlastErr = error
		YawlastTime = now

def SetTuningsYaw(Kp, Ki, Kd):
	Yawkp = Kp
	Yawki = Ki
	Yawkd = Kd

PitchlastTime = None
PitchSetpoint = None
PitcherrSum = None
PitchlastErr = None
Pitchkp = None
Pitchki = None
Pitchkd = None
PitchOutput = None

def ComputePitch():
	# compute time delta
	now = time.perf_counter()
	timeChange = now - PitchlastTime
	if timeChange >= SampleTime:
		# error computations
		error = PitchSetpoint
		PitcherrSum += error * timeChange
		dErr = (error - PitchlastErr) / timeChange
		
		# compute output
		PitchOutput = Pitchkp * error + Pitchki * PitcherrSum + Pitchkd * dErr
		
		# memory
		PitchlastErr = error
		PitchlastTime = now

def SetTuningsPitch(Kp, Ki, Kd):
	Pitchkp = Kp
	Pitchki = Ki
	Pitchkd = Kd

def SetSampleTime(NewSampleTime):
	if NewSampleTime > 0:
		ratio = NewSampleTime/SampleTime
		Yawki *= ratio
		Yawkd /= ratio
		Pitchki *= ratio
		Pitchkd /= ratio
		SampleTime = NewSampleTime

pinsYaw = [17, 27, 22, 5]
pinsPitch = [23, 24, 25, 16]

YawMotor = RpiMotorLib.BYJMotor("YawMotor", "28BYJ")
PitchMotor = RpiMotorLib.BYJMotor("PitchMotor", "28BYJ")

