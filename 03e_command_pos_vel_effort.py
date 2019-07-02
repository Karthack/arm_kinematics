#!/usr/bin/env python3

import hebi
from math import cos, pi, sin
from time import sleep, time

lookup = hebi.Lookup()

# Wait 2 seconds for the module list to populate
sleep(2.0)

family_name = "X5-9"
module_name = "Actuator1"

group = lookup.get_group_from_names([family_name], [module_name])

if group is None:
  print('Group not found! Check that the family and name of a module on the network')
  print('matches what is given in the source file.')
  exit(1)

group_command  = hebi.GroupCommand(group.size)
group_feedback = hebi.GroupFeedback(group.size)

# Start logging in the background
group.start_log('logs')

freq_hz = 0.5                 # [Hz]
freq    = freq_hz * 2.0 * pi  # [rad / sec]
amp     = pi * 0.25           # [rad] (45 degrees)

# Inertia parameters for converting acceleration to torque. This inertia value corresponds
# to roughly a 300mm X5 link extending off the output.
inertia = 0.01                # [kg * m^2]

duration = 10.0               # [sec]
start = time()
t = time() - start

while t < duration:
  # Even though we don't use the feedback, getting feedback conveniently
  # limits the loop rate to the feedback frequency
  group.get_next_feedback(reuse_fbk=group_feedback)
  t = time() - start

  # Position command
  group_command.position = amp * sin(freq * t)
  # Velocity command (time derivative of position)
  group_command.velocity = freq * amp * cos(freq * t)
  # Acceleration command (time derivative of velocity)
  accel = -freq * freq * amp * sin(freq * t)
  # Convert to torque
  group_command.effort = accel * inertia
  group.send_command(group_command)

# Stop logging. `log_file` contains the contents of the file
log_file = group.stop_log()