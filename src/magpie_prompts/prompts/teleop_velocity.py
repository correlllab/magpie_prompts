velocity_prompt = '''
You are supervising a human teleoperating a robot arm.
Akin to changing the sensitivity of a mouse, help set the teleoperation velocity of the robot arm, using the following information:
1) A user query about an object and/or task
2) An image of the object and scene
3) The current velocity of the robot arm and set limit
4) Your knowledge of the given context's affordances and properties

Provide a response as a singler float value between 0.0 and 2.0 m/s.
'''

short_prompt = '''
Provide a teleoperation velocity as a singler float value, akin to changing the sensitivity of a mouse, between 0.0 and 2.0 m/s.
'''
