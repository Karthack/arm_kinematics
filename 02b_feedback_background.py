#!/usr/bin/env python3

import hebi
from time import sleep

lookup = hebi.Lookup()

# Wait 2 seconds for the module list to populate
sleep(2.0)

family_name = "X5-9"
module_name = "Actuator1"

group = lookup.get_group_from_names([family_name], [module_name])

if group is None:
  print('Group not found: Did you forget to set the module family and name above?')
  exit(1)

# This is by default 100 Hz. Setting this to 5 Hz allows the console output to be reasonable.
group.feedback_frequency = 5.0

def feedback_handler(group_feedback):
  #print('Feedback received. Positions are:\n{0}'.format(group_feedback.position))
  #gives x,y,z acceleration values.
  print('Feedback received. Positions are:\n{0}'.format(group_feedback.gyro))


group.add_feedback_handler(feedback_handler)

# Wait for 10 seconds
sleep(10.0)
