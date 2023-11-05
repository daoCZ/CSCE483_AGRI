# Create script that, given an input time from the user, randomly prints the time at random intervals over the input time.
import random
import datetime
import time


# Ask user for duration
duration = float(input("How long would you like this script to run for (minutes)? "))

# Determine random number of events to print over duration
num_events = random.randint(1, 100)
print("Number of events: " + str(num_events))

# Get time between events
time_between_events = duration*60/num_events

# Store current time
start_time = datetime.datetime.now()
end_time = start_time + datetime.timedelta(minutes=duration)

for i in range(num_events):
    # Check if current time is greater than end time, if it is, break out of loop
    if datetime.datetime.now() > end_time:
        break
    # Print current time
    print(datetime.datetime.now())
    # Sleep for random time between 0 and time_between_events
    time.sleep(time_between_events)
    
