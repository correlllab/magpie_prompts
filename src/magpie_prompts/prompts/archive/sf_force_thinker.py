prompt_force_thinker = """
Given the user instruction, position goals relative to the world and wrist frame, and a three-part image containing a wrist view with world-frame axes labeling, a third-person view in the middle, and a wrist view with wrist-frame axes labeling on the right, generate a structured physical plan for robot end-effector forces and torques interacting with the environment.
The task is to {task} while grasping the {obj}.

The robot is controlled using position and torque-based control, with access to contact feedback and 6D motion capabilities. 
Motions can include grasping, lifting, pushing, tapping, sliding, rotating, or any interaction with objects or surfaces.

Assume the robot has access to:
- Object geometry and contact points (from the image)
- Force/torque sensing at the wrist
- Prior knowledge of object material types and mass estimates
- Environmental knowledge (table, gravity, hinge resistance, etc.)

The left image is labeled with the axes of motion relative to the base frame of the robot, as in the canonical world-axes (for example, the red positive Z-axis will always represent upward direction in the world).
The middle image is a third-person view of the robot labeled with the base frame orientation of the robot, which may be used to help with the understanding the environmental properties and motion within the environment.
The right image is labeled with the axes of motion relative to the wrist of the robot. The wrist of the robot may be oriented differently from the canonical world-axes.
Use physical reasoning to complete the following plan in a structured format. Carefully map the required motion in the world to the required motion, forces, and torques at the wrist.
We want to reason about forces and torques relative to the wrist frame because that is the frame of reference for the F/T sensor.
More importantly, as the wrist's end-effector is grasping the object, assuming no slip, the requisite applied forces and especially torques on the object to accomplish the task will be the same as the forces and torques on the wrist frame.

[start of wrench plan]
Aligning Image With Motion:
The task is to {task} while grasping the {obj}.
The world frame motion to accomplish this task is {world_motion_vector} (x, y, z in meters) which resolves to the following positional motion along wrist frame: {wrist_motion_vector}.
In the right image with the labeled wrist axes, the center red dot into the page represents motion along the wrist Z-axis. That is why, based off knowledge of the task and motion in the world frame the the motion along the wrist Z-axis is {wrist_motion_vector[2]}, since {{DESCRIPTION: the object's required motion in the wrist frame to accomplish the task}}.
Then, the green axis represents motion along the wrist's X-axis. That is why, based off knowledge of the task and motion in the world frame the the motion along the wrist X-axis is {wrist_motion_vector[0]}, since {{DESCRIPTION: the object's required motion in the wrist frame to accomplish the task}}.
Finally, the blue axis represents motion along the wrist's Y-axis. That is why, based off knowledge of the task and motion in the world frame the the motion along the wrist Y-axis is {wrist_motion_vector[1]}, since {{DESCRIPTION: the object's required motion in the wrist frame to accomplish the task}}.
Thus, to accomplish the task in the wrist frame, the object must be moved {{DESCRIPTION: describe the motion required along which wrist axes of motion to accomplish the task}}.

Understanding Forces and Torques Required for Motion:
To estimate the forces and torques required to accomplish {task} while grasping the {obj}, we must consider the following:
- The relevant object is {{DESCRIPTION: describe the object and its properties}} has mass {{NUM}} kg and, with the robot gripper, has a static friction coefficient of {{NUM}}.
- The surface of interaction is {{DESCRIPTION: describe the surface and its properties}} has a static friction coefficient of {{NUM}} with the object.
- Contact Types: {{DESCRIPTION: consideration of various contacts such as edge contact, maintaining surface contact, maintaining a pinch grasp, etc.}}.
- Motion Type: {{DESCRIPTION: consideration of forceful motion(s) involved in accomplishing task such as pushing forward while pressing down, rotating around hinge by pulling up and out, or sliding while maintaining contact}}.
- Contact Considerations: {{DESCRIPTION: explicitly consider whether additional axes of force are required to maintain contact with the object, robot, and environmen and accomplish the motion goal}}.
- Motion along axes: {{DESCRIPTION: e.g., the robot exerts motion in a “linear,” “rotational,” “some combination” fashion along the [x, y, z, rx, ry, rz] axes}}.

Physical Model Computations:
- Relevant quantities and estimates: {{DESCRIPTION: include any relevant quantities and estimates used in the calculations}}.
- Relevant equations: {{DESCRIPTION: include any relevant equations used in the calculations}}.
- Relevant assumptions: {{DESCRIPTION: include any relevant assumptions made in the calculations}}.
- Computations: {{DESCRIPTION: include in full detail any relevant calculations using the above information}}.
- Force/torque motion computations with object of mass {{NUM}} kg and static friction coefficient of {{NUM}} along the surface: {{DESCRIPTION: for the derived or estimated motion, compute the surface friction using appropriate formulae and quantities}}.

Force/Torque Motion Estimation:
Linear X-axis:   {{DESCRIPTION: estimated force range and justification based on friction, mass, resistance}}, thus {{NUM}} to {{NUM}}.
Linear Y-axis:   {{DESCRIPTION: estimated force range and justification based on friction, mass, resistance}}, thus {{NUM}} to {{NUM}}.
Linear Z-axis:   {{DESCRIPTION: estimated force range and justification based on friction, mass, resistance}}, thus {{NUM}} to {{NUM}} N.
Angular X-axis: {{DESCRIPTION: estimated torque range and justification based on friction, mass, resistance}}, thus {{NUM}} to {{NUM}} N-m.
Angular Y-axis: {{DESCRIPTION: estimated torque range and justification based on friction, mass, resistance}}, thus {{NUM}} to {{NUM}} N-m.
Angular Z-axis: {{DESCRIPTION: estimated torque range and justification based on friction, mass, resistance}}, thus {{NUM}} to {{NUM}} N-m.
Grasping force:  {{DESCRIPTION: estimated force range and justification based on friction, mass, resistance}}, thus {{PNUM}} to {{PNUM}} N .

Python Code with Final Motion Plan:
```python
# explicitly state the forces along the [x, y, z] axes
wrench_description = "{{DESCRIPTION: describe succinctly the forces and torques required along which wrist axes of motion to accomplish the task}}"
# explicitly state the forces and torques along the [x, y, z, rx, ry, rz] axes with the correct signs for direction
wrench = [{{NUM}}, {{NUM}}, {{NUM}}, {{NUM}}, {{NUM}}, {{NUM}}]
# explicitly state the grasping force, which must be positive
grasp_force = {{PNUM}}
# explicitly state the task duration, which must be positive
duration = {{PNUM}}
```

[end of wrench plan]

Rules:
1. Replace all {{DESCRIPTION: ...}}, {{PNUM}}, {{NUM}}, and {{CHOICE}} entries with specific values or statements. For example, {{PNUM}} should be replaced with a positive number like 0.5. {{NUM}} should be replaced with a number like -5. You must remove the double brackets, symbol, and colon, leaving only the estimated value. This is very important for downstream parsing!!
2. Use best physical reasoning based on known robot/environmental capabilities. Remember that the robot may have to exert forces in additional axes compared to the motion direction axes in order to maintain contacts between the object, robot, and environment.
3. Always include motion for all axes of motion, even if it's "No motion required."
4. Keep the explanation concise but physically grounded. Prioritize interpretability and reproducibility.
5. Use common sense where exact properties are ambiguous, and explain assumptions.
6. Do not include any sections outside the start/end blocks or add non-specified bullet points.
7. Make sure to provide the final python code for each requested force in a code block.
8. Remember that position motion along one axis in the world frame is resolved to potentially multiple axes of motion in the wrist frame.
9. Remember that the wrist frame and world frame are not aligned, and the axes of motion in the wrist frame may not correspond to the axes of motion in the world frame. It will be helpful to figure out what wrist-axes correspond to world-axes of up or down (Z), left or right (X), or backward and forward (Y) motion.
10. Do not abbreviate the prompt when generating the response. Fully reproduce the template, but filled in with your reasoning.
11. While it is fine to exert additional forces, relative ratios and signs of of wrist forces otherwise should match the relative ratios and signs of the provided wrist motion vector. Specifically, if the motion vector is [0.1, -0.2, 0.3], the forces should be in the same ratio, e.g., [0.1, -0.2, 0.3] or [1.0, 2.0, 3.0] or [10.0, -20.0, 30.0]. The exact values are not important. This is because before considering additional contact forces, similar ratios and directions of forces are required to accomplish the same ratios and directions of motion.
"""
