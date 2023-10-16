from simple_pid import PID

#	instantiate the pitch (y axis) and yaw (x axis) controllers
#	horizontal fov = 100 deg, vertical fov = 62.6438129017 deg, 90fps
pitch_pid = PID(1, 0.1, 0.05, 0, 0.0111111111, (0.0, 180.0))
yaw_pid = PID(1, 0.1, 0.05, 0, 0.0111111111, (0.0, 180.0))

#	values camera code is supposed to come up with, stubs
target_dX = 0
target_dY = 0

#	values control code converts from given camera values, assuming 480p, 4:3 aspect ratio
target_eY = 0.15625 * target_dX
target_eP = 0.130507943545 * target_dY

#	loop to update control, may/should be a part of main program loop