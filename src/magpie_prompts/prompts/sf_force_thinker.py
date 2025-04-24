wrist_base_string = "The left image is labeled with the axes of motion relative to the base frame of the robot, as in the canonical world-axes (for example, the red positive Z-axis will always represent upward direction in the world)."
wrist_wrist_string = "The right image is labeled with the axes of motion relative to the wrist of the robot. The wrist of the robot may be oriented differently from the canonical world-axes."
third_base_string = "The middle image is a third-person view of the robot labeled with the base frame orientation of the robot, which may be used to help with the understanding the environmental properties and motion within the environment."

wrist_base_third_thinker = """
Given the user instruction and three-part image containing a robot wrist-image view on the left, a third-person view in the middle, and another wrist view on the right, generate a structured physical plan for a robot end-effector interacting with the environment.
The task is to {task} while grasping the {obj}.

The robot is controlled using position and torque-based control, with access to contact feedback and 6D motion capabilities. 
Motions can include grasping, lifting, pushing, tapping, sliding, rotating, or any interaction with objects or surfaces.

Reason about the provided and implicit information in the images and task description to generate a structured plan for the robot's motion. Think about:
- Object geometry and contact points (from the image)
- Force/torque sensing at the wrist
- Prior knowledge of object material types and mass estimates
- Environmental knowledge (table, gravity, hinge resistance, etc.)

The left image is labeled with the axes of motion relative to the base frame of the robot, as in the canonical world-axes (for example, the red positive Z-axis will always represent upward direction in the world).
The middle image is a third-person view of the robot labeled with the base frame orientation of the robot, which may be used to help with the understanding the environmental properties and motion within the environment.
The right image is labeled with the axes of motion relative to the wrist of the robot. The wrist of the robot may be oriented differently from the canonical world-axes.
Use physical reasoning to complete the following plan in a structured format. Carefully map the required motion in the world to the required motion, forces, and torques at the wrist.

[start of motion plan]
The task is to {task} while grasping the {obj}.

Aligning Images With World Motion:
The provided images in the three-part image confirm {{DESCRIPTION: the object and environment in the image and their properties, such as color, shape, and material, and their correspondence to the requested task}}.
The blue axis representing the world Z-axis in the left and middle images corresponds to upward (positive) and downward (negative) motion in the world. 
To complete the task, the object in the image should have {{CHOICE: [upward, downward, no]}} linear motion along the world Z-axis with magnitude {{PNUM}} meters.
The red axis representing the world X-axis in the left and middle images corresponds to right (positive) and left (negative) motion in the world, relative to the robot. 
To complete the task, the object in the image should have {{CHOICE: [leftward, rightward, no]}} linear motion along the world X-axis with magnitude {{PNUM}} meters.
The green axis representing the world Y-axis in the left and middle images corresponds to forward (positive) and backward (negative) motion in the world, relative to the robot. 
To complete the task, the object in the image should have {{CHOICE: [backward, forward, no]}} linear motion along the world Y-axis with magnitude {{PNUM}} meters.
To accomplish the task in the world frame, the object must be moved {{DESCRIPTION: the object's required motion in the world frame to accomplish the task}}.

Mapping World Motion to Wrist Motion:
The right part of the image with the labeled wrist axes shows the wrist frame of the robot {{DESCRIPTION: describe the wrist frame and its axes of motion}}.
The blue dot going into (positive) the image represents wrist Z-axis motion. 
Based off knowledge of the task and motion, in the wrist Z-axis, the object must move {{DESCRIPTION: the object's required motion in the wrist Z-axis to accomplish the task}}.
The red axis going down (positive) the image represents wrist X-axis motion. 
Based off knowledge of the task and motion, in the wrist X-axis, the object must move {{DESCRIPTION: the object's required motion in the wrist X-axis to accomplish the task}}.
The green axis going left (positive) across the image represents wrist Y-axis motion. 
Based off knowledge of the task and motion, in the wrist Y-axis, the object must move {{DESCRIPTION: the object's required motion in the wrist Y-axis to accomplish the task}}.
To accomplish the task in the wrist frame, the object must be moved {{DESCRIPTION: the object's required motion in the wrist frame to accomplish the task}}.

Understanding Robot-Applied Forces and Torques to Move Object in the Wrist Frame:
To estimate the forces and torques required to accomplish {task} while grasping the {obj}, we must consider the following:
- Object Properties: {{DESCRIPTION: Think very carefully about the estimated mass, material, stiffness, friction coefficient of the object based off the visual information and semantic knowledge about the object. If object is articulated, do the same reasoning for whatever joint / degree of freedom enables motion. }}.
- Environmental Factors: {{DESCRIPTION: Think very carefully about the various environmental factors in task like gravity, surface friction, damping, hinge resistance that would interact with the object over the course of the task}}.
- The relevant object is {{DESCRIPTION: describe the object and its properties}} has mass {{NUM}} kg and, with the robot gripper, has a static friction coefficient of {{NUM}}.
- The surface of interaction is {{DESCRIPTION: describe the surface and its properties}} has a static friction coefficient of {{NUM}} with the object.
- Contact Types: {{DESCRIPTION: consideration of various contacts such as edge contact, maintaining surface contact, maintaining a pinch grasp, etc.}}.
- Motion Type: {{DESCRIPTION: consideration of forceful motion(s) involved in accomplishing task such as pushing forward while pressing down, rotating around hinge by pulling up and out, or sliding while maintaining contact}}.
- Contact Considerations: {{DESCRIPTION: explicitly consider whether additional axes of force are required to maintain contact with the object, robot, and environmen and accomplish the motion goal}}.
- Motion along axes: {{DESCRIPTION: e.g., the robot exerts motion in a “linear,” “rotational,” “some combination” fashion along the wrist's [x, y, z, rx, ry, rz] axes}}.
- Task duration: {{DESCRIPTION: reasoning about the task motion, forces, and other properties to determine an approximate time duration of the task, which must be positive}}.

Physical Model (if applicable):
- Relevant quantities and estimates: {{DESCRIPTION: include any relevant quantities and estimates used in the calculations}}.
- Relevant equations: {{DESCRIPTION: include any relevant equations used in the calculations}}.
- Relevant assumptions: {{DESCRIPTION: include any relevant assumptions made in the calculations}}.
- Computations: {{DESCRIPTION: include in full detail any relevant calculations using the above information}}.
- Force/torque motion computations with object of mass {{NUM}} kg and static friction coefficient of {{NUM}} along the surface: {{DESCRIPTION: for the derived or estimated motion, compute the surface friction using appropriate formulae and quantities}}.

Wrist Force/Torque Motion Estimation:
Linear X-axis:  To complete the task and based upon {{DESCRIPTION: reasoning about and estimation of task physical properties}}, the object in the image must exert {{CHOICE: [positive, negative, no]}} force along the X-axis with magnitude {{PNUM}} N.
Linear Y-axis:  To complete the task and based upon {{DESCRIPTION: reasoning about and estimation of task physical properties}}, the object in the image must exert {{CHOICE: [positive, negative, no]}} force along the Y-axis with magnitude {{PNUM}} N.
Linear Z-axis:  To complete the task and based upon {{DESCRIPTION: reasoning about and estimation of task physical properties}}, the object in the image must exert {{CHOICE: linear [positive, negative, no]}} force along the Z-axis with magnitude {{PNUM}} N.
Angular X-axis: To complete the task and based upon {{DESCRIPTION: reasoning about and estimation of task physical properties}}, the object in the image must exert {{CHOICE: angular [counterclockwise, clockwise, no]}} torque about the X-axis with magnitude {{PNUM}} N-m.
Angular Y-axis: To complete the task and based upon {{DESCRIPTION: reasoning about and estimation of task physical properties}}, the object in the image must exert {{CHOICE: angular [counterclockwise, clockwise, no]}} torque about the Y-axis with magnitude {{PNUM}} N-m.
Angular Z-axis: To complete the task and based upon {{DESCRIPTION: reasoning about and estimation of task physical properties}}, the object in the image must exert {{CHOICE: angular [counterclockwise, clockwise, no]}} torque about the Z-axis with magnitude {{PNUM}} N-m.
Grasping force:  {{DESCRIPTION: estimated force range and justification based on friction, mass, resistance}}, thus {{PNUM}} to {{PNUM}} N .

Python Code with Final Motion Plan:
```python
# succinct text description of the explicit estimated physical properties of the object, including mass, material, friction coefficients, etc.
property_description = "{{DESCRIPTION: describe succinctly the object and its properties}}"
# succinct text description of the motion plan along the wrist axes
wrist_motion_description = "{{DESCRIPTION: the object's required position motion in the wrist frame to accomplish the task}}"
# the vector (sign of direction * magnitude) of motion across the wrist axes [x, y ,z]. 
wrist_motion_vector = [{{NUM}}, {{NUM}}, {{NUM}}]
# the vector (sign of direction * magnitude) of the forces and torques along the wrist's [x, y, z, rx, ry, rz] axes
wrist_wrench = [{{NUM}}, {{NUM}}, {{NUM}}, {{NUM}}, {{NUM}}, {{NUM}}]
# the grasping force, which must be positive
grasp_force = {{PNUM}}
# the task duration, which must be positive
duration = {{PNUM}}
```

[end of motion plan]

Rules:
1. Replace all {{DESCRIPTION: ...}}, {{PNUM: ...}}, {{NUM: ...}}, and {{CHOICE}} entries with specific values or statements.
2. Use best physical reasoning based on known robot/environmental capabilities. Remember that the robot may have to exert forces in additional axes compared to the motion direction axes in order to maintain contacts between the object, robot, and environment.
3. Always include motion for all three axes, even if it's "No motion required."
4. Keep the explanation concise but physically grounded. Prioritize interpretability and reproducibility.
5. Use common sense where exact properties are ambiguous, and explain assumptions.
6. Do not include any sections outside the start/end blocks or add non-specified bullet points.
7. Make sure to provide the final python code for each requested force in a code block.
"""

wrist_third_thinker = """
Given the user instruction and a two-part image containing a third-person view on the left, and a robot wrist view on the right, generate a structured physical plan for a robot end-effector interacting with the environment.
The task is to {task} while grasping the {obj}.

The robot is controlled using position and torque-based control, with access to contact feedback and 6D motion capabilities. 
Motions can include grasping, lifting, pushing, tapping, sliding, rotating, or any interaction with objects or surfaces.

Reason about the provided and implicit information in the images and task description to generate a structured plan for the robot's motion. Think about:
- Object geometry and contact points (from the image)
- Force/torque sensing at the wrist
- Prior knowledge of object material types and mass estimates
- Environmental knowledge (table, gravity, hinge resistance, etc.)

The left image is a third-person view of the robot and the environment, which may be used to help with the understanding the environmental properties and motion within the environment.
The right image is labeled with the axes of motion relative to the wrist of the robot. The wrist of the robot may be oriented differently from the canonical world-axes.
Use physical reasoning to complete the following plan in a structured format. Carefully map the required motion in the world to the required motion, forces, and torques at the wrist.

[start of motion plan]
The task is to {task} while grasping the {obj}.

Mapping World Motion to Wrist Motion:
The right part of the image with the labeled wrist axes shows the wrist frame of the robot {{DESCRIPTION: describe the wrist frame and its axes of motion}}.
The blue dot going into (positive) the image represents wrist Z-axis motion. 
Based off knowledge of the task and motion, in the wrist Z-axis, the object must move {{DESCRIPTION: the object's required motion in the wrist Z-axis to accomplish the task}}.
The red axis going down (positive) the image represents wrist X-axis motion. 
Based off knowledge of the task and motion, in the wrist X-axis, the object must move {{DESCRIPTION: the object's required motion in the wrist X-axis to accomplish the task}}.
The green axis going left (positive) across the image represents wrist Y-axis motion. 
Based off knowledge of the task and motion, in the wrist Y-axis, the object must move {{DESCRIPTION: the object's required motion in the wrist Y-axis to accomplish the task}}.
To accomplish the task in the wrist frame, the object must be moved {{DESCRIPTION: the object's required motion in the wrist frame to accomplish the task}}.

Understanding Robot-Applied Forces and Torques to Move Object in the Wrist Frame:
To estimate the forces and torques required to accomplish {task} while grasping the {obj}, we must consider the following:
- Object Properties: {{DESCRIPTION: Think very carefully about the estimated mass, material, stiffness, friction coefficient of the object based off the visual information and semantic knowledge about the object. If object is articulated, do the same reasoning for whatever joint / degree of freedom enables motion. }}.
- Environmental Factors: {{DESCRIPTION: Think very carefully about the various environmental factors in task like gravity, surface friction, damping, hinge resistance that would interact with the object over the course of the task}}.
- The relevant object is {{DESCRIPTION: describe the object and its properties}} has mass {{NUM}} kg and, with the robot gripper, has a static friction coefficient of {{NUM}}.
- The surface of interaction is {{DESCRIPTION: describe the surface and its properties}} has a static friction coefficient of {{NUM}} with the object.
- Contact Types: {{DESCRIPTION: consideration of various contacts such as edge contact, maintaining surface contact, maintaining a pinch grasp, etc.}}.
- Motion Type: {{DESCRIPTION: consideration of forceful motion(s) involved in accomplishing task such as pushing forward while pressing down, rotating around hinge by pulling up and out, or sliding while maintaining contact}}.
- Contact Considerations: {{DESCRIPTION: explicitly consider whether additional axes of force are required to maintain contact with the object, robot, and environmen and accomplish the motion goal}}.
- Motion along axes: {{DESCRIPTION: e.g., the robot exerts motion in a “linear,” “rotational,” “some combination” fashion along the wrist's [x, y, z, rx, ry, rz] axes}}.
- Task duration: {{DESCRIPTION: reasoning about the task motion, forces, and other properties to determine an approximate time duration of the task, which must be positive}}.

Physical Model (if applicable):
- Relevant quantities and estimates: {{DESCRIPTION: include any relevant quantities and estimates used in the calculations}}.
- Relevant equations: {{DESCRIPTION: include any relevant equations used in the calculations}}.
- Relevant assumptions: {{DESCRIPTION: include any relevant assumptions made in the calculations}}.
- Computations: {{DESCRIPTION: include in full detail any relevant calculations using the above information}}.
- Force/torque motion computations with object of mass {{NUM}} kg and static friction coefficient of {{NUM}} along the surface: {{DESCRIPTION: for the derived or estimated motion, compute the surface friction using appropriate formulae and quantities}}.

Wrist Force/Torque Motion Estimation:
Linear X-axis:  To complete the task and based upon {{DESCRIPTION: reasoning about and estimation of task physical properties}}, the object in the image must exert {{CHOICE: [positive, negative, no]}} force along the X-axis with magnitude {{PNUM}} N.
Linear Y-axis:  To complete the task and based upon {{DESCRIPTION: reasoning about and estimation of task physical properties}}, the object in the image must exert {{CHOICE: [positive, negative, no]}} force along the Y-axis with magnitude {{PNUM}} N.
Linear Z-axis:  To complete the task and based upon {{DESCRIPTION: reasoning about and estimation of task physical properties}}, the object in the image must exert {{CHOICE: linear [positive, negative, no]}} force along the Z-axis with magnitude {{PNUM}} N.
Angular X-axis: To complete the task and based upon {{DESCRIPTION: reasoning about and estimation of task physical properties}}, the object in the image must exert {{CHOICE: angular [counterclockwise, clockwise, no]}} torque about the X-axis with magnitude {{PNUM}} N-m.
Angular Y-axis: To complete the task and based upon {{DESCRIPTION: reasoning about and estimation of task physical properties}}, the object in the image must exert {{CHOICE: angular [counterclockwise, clockwise, no]}} torque about the Y-axis with magnitude {{PNUM}} N-m.
Angular Z-axis: To complete the task and based upon {{DESCRIPTION: reasoning about and estimation of task physical properties}}, the object in the image must exert {{CHOICE: angular [counterclockwise, clockwise, no]}} torque about the Z-axis with magnitude {{PNUM}} N-m.
Grasping force:  {{DESCRIPTION: estimated force range and justification based on friction, mass, resistance}}, thus {{PNUM}} to {{PNUM}} N .

Python Code with Final Motion Plan:
```python
# succinct text description of the explicit estimated physical properties of the object, including mass, material, friction coefficients, etc.
property_description = "{{DESCRIPTION: describe succinctly the object and its properties}}"
# succinct text description of the motion plan along the wrist axes
wrist_motion_description = "{{DESCRIPTION: the object's required position motion in the wrist frame to accomplish the task}}"
# the vector (sign of direction * magnitude) of motion across the wrist axes [x, y ,z]. 
wrist_motion_vector = [{{NUM}}, {{NUM}}, {{NUM}}]
# the vector (sign of direction * magnitude) of the forces and torques along the wrist's [x, y, z, rx, ry, rz] axes
wrist_wrench = [{{NUM}}, {{NUM}}, {{NUM}}, {{NUM}}, {{NUM}}, {{NUM}}]
# the grasping force, which must be positive
grasp_force = {{PNUM}}
# the task duration, which must be positive
duration = {{PNUM}}
```

[end of motion plan]

Rules:
1. Replace all {{DESCRIPTION: ...}}, {{PNUM: ...}}, {{NUM: ...}}, and {{CHOICE}} entries with specific values or statements.
2. Use best physical reasoning based on known robot/environmental capabilities. Remember that the robot may have to exert forces in additional axes compared to the motion direction axes in order to maintain contacts between the object, robot, and environment.
3. Always include motion for all three axes, even if it's "No motion required."
4. Keep the explanation concise but physically grounded. Prioritize interpretability and reproducibility.
5. Use common sense where exact properties are ambiguous, and explain assumptions.
6. Do not include any sections outside the start/end blocks or add non-specified bullet points.
7. Make sure to provide the final python code for each requested force in a code block.
"""

wrist_thinker = """
Given the user instruction and an image of the robot wrist view on the right, generate a structured physical plan for a robot end-effector interacting with the environment.
The task is to {task} while grasping the {obj}.

The robot is controlled using position and torque-based control, with access to contact feedback and 6D motion capabilities. 
Motions can include grasping, lifting, pushing, tapping, sliding, rotating, or any interaction with objects or surfaces.

Reason about the provided and implicit information in the images and task description to generate a structured plan for the robot's motion. Think about:
- Object geometry and contact points (from the image)
- Force/torque sensing at the wrist
- Prior knowledge of object material types and mass estimates
- Environmental knowledge (table, gravity, hinge resistance, etc.)

The image is labeled with the axes of motion relative to the wrist of the robot. The wrist of the robot may be oriented differently from the canonical world-axes.
Use physical reasoning to complete the following plan in a structured format. Carefully map the required motion in the world to the required motion, forces, and torques at the wrist.

[start of motion plan]
The task is to {task} while grasping the {obj}.

Mapping World Motion to Wrist Motion:
The right part of the image with the labeled wrist axes shows the wrist frame of the robot {{DESCRIPTION: describe the wrist frame and its axes of motion}}.
The blue dot going into (positive) the image represents wrist Z-axis motion. 
Based off knowledge of the task and motion, in the wrist Z-axis, the object must move {{DESCRIPTION: the object's required motion in the wrist Z-axis to accomplish the task}}.
The red axis going down (positive) the image represents wrist X-axis motion. 
Based off knowledge of the task and motion, in the wrist X-axis, the object must move {{DESCRIPTION: the object's required motion in the wrist X-axis to accomplish the task}}.
The green axis going left (positive) across the image represents wrist Y-axis motion. 
Based off knowledge of the task and motion, in the wrist Y-axis, the object must move {{DESCRIPTION: the object's required motion in the wrist Y-axis to accomplish the task}}.
To accomplish the task in the wrist frame, the object must be moved {{DESCRIPTION: the object's required motion in the wrist frame to accomplish the task}}.

Understanding Robot-Applied Forces and Torques to Move Object in the Wrist Frame:
To estimate the forces and torques required to accomplish {task} while grasping the {obj}, we must consider the following:
- Object Properties: {{DESCRIPTION: Think very carefully about the estimated mass, material, stiffness, friction coefficient of the object based off the visual information and semantic knowledge about the object. If object is articulated, do the same reasoning for whatever joint / degree of freedom enables motion. }}.
- Environmental Factors: {{DESCRIPTION: Think very carefully about the various environmental factors in task like gravity, surface friction, damping, hinge resistance that would interact with the object over the course of the task}}.
- The relevant object is {{DESCRIPTION: describe the object and its properties}} has mass {{NUM}} kg and, with the robot gripper, has a static friction coefficient of {{NUM}}.
- The surface of interaction is {{DESCRIPTION: describe the surface and its properties}} has a static friction coefficient of {{NUM}} with the object.
- Contact Types: {{DESCRIPTION: consideration of various contacts such as edge contact, maintaining surface contact, maintaining a pinch grasp, etc.}}.
- Motion Type: {{DESCRIPTION: consideration of forceful motion(s) involved in accomplishing task such as pushing forward while pressing down, rotating around hinge by pulling up and out, or sliding while maintaining contact}}.
- Contact Considerations: {{DESCRIPTION: explicitly consider whether additional axes of force are required to maintain contact with the object, robot, and environmen and accomplish the motion goal}}.
- Motion along axes: {{DESCRIPTION: e.g., the robot exerts motion in a “linear,” “rotational,” “some combination” fashion along the wrist's [x, y, z, rx, ry, rz] axes}}.
- Task duration: {{DESCRIPTION: reasoning about the task motion, forces, and other properties to determine an approximate time duration of the task, which must be positive}}.

Physical Model (if applicable):
- Relevant quantities and estimates: {{DESCRIPTION: include any relevant quantities and estimates used in the calculations}}.
- Relevant equations: {{DESCRIPTION: include any relevant equations used in the calculations}}.
- Relevant assumptions: {{DESCRIPTION: include any relevant assumptions made in the calculations}}.
- Computations: {{DESCRIPTION: include in full detail any relevant calculations using the above information}}.
- Force/torque motion computations with object of mass {{NUM}} kg and static friction coefficient of {{NUM}} along the surface: {{DESCRIPTION: for the derived or estimated motion, compute the surface friction using appropriate formulae and quantities}}.

Wrist Force/Torque Motion Estimation:
Linear X-axis:  To complete the task and based upon {{DESCRIPTION: reasoning about and estimation of task physical properties}}, the object in the image must exert {{CHOICE: [positive, negative, no]}} force along the X-axis with magnitude {{PNUM}} N.
Linear Y-axis:  To complete the task and based upon {{DESCRIPTION: reasoning about and estimation of task physical properties}}, the object in the image must exert {{CHOICE: [positive, negative, no]}} force along the Y-axis with magnitude {{PNUM}} N.
Linear Z-axis:  To complete the task and based upon {{DESCRIPTION: reasoning about and estimation of task physical properties}}, the object in the image must exert {{CHOICE: linear [positive, negative, no]}} force along the Z-axis with magnitude {{PNUM}} N.
Angular X-axis: To complete the task and based upon {{DESCRIPTION: reasoning about and estimation of task physical properties}}, the object in the image must exert {{CHOICE: angular [counterclockwise, clockwise, no]}} torque about the X-axis with magnitude {{PNUM}} N-m.
Angular Y-axis: To complete the task and based upon {{DESCRIPTION: reasoning about and estimation of task physical properties}}, the object in the image must exert {{CHOICE: angular [counterclockwise, clockwise, no]}} torque about the Y-axis with magnitude {{PNUM}} N-m.
Angular Z-axis: To complete the task and based upon {{DESCRIPTION: reasoning about and estimation of task physical properties}}, the object in the image must exert {{CHOICE: angular [counterclockwise, clockwise, no]}} torque about the Z-axis with magnitude {{PNUM}} N-m.
Grasping force:  {{DESCRIPTION: estimated force range and justification based on friction, mass, resistance}}, thus {{PNUM}} to {{PNUM}} N .

Python Code with Final Motion Plan:
```python
# succinct text description of the explicit estimated physical properties of the object, including mass, material, friction coefficients, etc.
property_description = "{{DESCRIPTION: describe succinctly the object and its properties}}"
# succinct text description of the motion plan along the wrist axes
wrist_motion_description = "{{DESCRIPTION: the object's required position motion in the wrist frame to accomplish the task}}"
# the vector (sign of direction * magnitude) of motion across the wrist axes [x, y ,z]. 
wrist_motion_vector = [{{NUM}}, {{NUM}}, {{NUM}}]
# the vector (sign of direction * magnitude) of the forces and torques along the wrist's [x, y, z, rx, ry, rz] axes
wrist_wrench = [{{NUM}}, {{NUM}}, {{NUM}}, {{NUM}}, {{NUM}}, {{NUM}}]
# the grasping force, which must be positive
grasp_force = {{PNUM}}
# the task duration, which must be positive
duration = {{PNUM}}
```

[end of motion plan]

Rules:
1. Replace all {{DESCRIPTION: ...}}, {{PNUM: ...}}, {{NUM: ...}}, and {{CHOICE}} entries with specific values or statements.
2. Use best physical reasoning based on known robot/environmental capabilities. Remember that the robot may have to exert forces in additional axes compared to the motion direction axes in order to maintain contacts between the object, robot, and environment.
3. Always include motion for all three axes, even if it's "No motion required."
4. Keep the explanation concise but physically grounded. Prioritize interpretability and reproducibility.
5. Use common sense where exact properties are ambiguous, and explain assumptions.
6. Do not include any sections outside the start/end blocks or add non-specified bullet points.
7. Make sure to provide the final python code for each requested force in a code block.
"""

third_thinker = """
Given the user instruction and an image containing a third-person view of a robot and its environment, generate a structured physical plan for a robot end-effector interacting with the environment.
The task is to {task} while grasping the {obj}.

The robot is controlled using position and torque-based control, with access to contact feedback and 6D motion capabilities. 
Motions can include grasping, lifting, pushing, tapping, sliding, rotating, or any interaction with objects or surfaces.

Reason about the provided and implicit information in the images and task description to generate a structured plan for the robot's positional motion. Think about:
- Object geometry and contact points (from the image)
- Prior knowledge of object material types and mass estimates
- Force/torque sensing at the wrist
- Environmental knowledge (table, gravity, hinge resistance, etc.)

The image is a third-person view of the robot, labeled with the coordinate frame of the robot's base and world, which may be used to help with the mapping of the axes and understanding the environment
We must use the provided image data and physical reasoning to carefully map the true motion in the world frame to accomplish the task.
We want to reason about forces and torques relative to the world frame.

[start of motion plan]
The task is to {task} while grasping the {obj}.

Understanding Object-Centric Motion in the World Frame:
The provided images in the two-part image confirm {{DESCRIPTION: the object and environment in the image and their properties, such as color, shape, and material, and their correspondence to the requested task}}.
The blue axis representing the world Z-axis corresponds to upward (positive) and downward (negative) motion in the world. 
To complete the task, the object in the image should have {{CHOICE: [upward, downward, no]}} linear motion along the Z-axis with magnitude {{PNUM}} meters.
The red axis representing the world X-axis corresponds to right (positive) and left (negative) motion in the world, relative to the robot. 
To complete the task, the object in the image should have {{CHOICE: [leftward, rightward, no]}} linear motion along the X-axis with magnitude {{PNUM}} meters.
The green axis representing the world Y-axis corresponds to forward (positive) and backward (negative) motion in the world, relative to the robot. 
To complete the task, the object in the image should have {{CHOICE: [backward, forward, no]}} linear motion along the Y-axis with magnitude {{PNUM}} meters.
To accomplish the task in the world frame, the object must be moved {{DESCRIPTION: the object's required motion in the world frame to accomplish the task}}.

Understanding Robot-Applied Forces and Torques to Move Object in the World Frame:
To estimate the forces and torques required to accomplish {task} while grasping the {obj}, we must consider the following:
- Object Properties: {{DESCRIPTION: Think very carefully about the estimated mass, material, stiffness, friction coefficient of the object based off the visual information and semantic knowledge about the object. If object is articulated, do the same reasoning for whatever joint / degree of freedom enables motion. }}.
- Environmental Factors: {{DESCRIPTION: Think very carefully about the various environmental factors in task like gravity, surface friction, damping, hinge resistance that would interact with the object over the course of the task}}.
- The relevant object is {{DESCRIPTION: describe the object and its properties}} has mass {{NUM}} kg and, with the robot gripper, has a static friction coefficient of {{NUM}}.
- The surface of interaction is {{DESCRIPTION: describe the surface and its properties}} has a static friction coefficient of {{NUM}} with the object.
- Contact Types: {{DESCRIPTION: consideration of various contacts such as edge contact, maintaining surface contact, maintaining a pinch grasp, etc.}}.
- Motion Type: {{DESCRIPTION: consideration of forceful motion(s) involved in accomplishing task such as pushing forward while pressing down, rotating around hinge by pulling up and out, or sliding while maintaining contact}}.
- Contact Considerations: {{DESCRIPTION: explicitly consider whether additional axes of force are required to maintain contact with the object, robot, and environmen and accomplish the motion goal}}.
- Motion along axes: {{DESCRIPTION: e.g., the robot exerts motion in a “linear,” “rotational,” “some combination” fashion along the [x, y, z, rx, ry, rz] axes}}.
- Task duration: {{DESCRIPTION: reasoning about the task motion, forces, and other properties to determine an approximate time duration of the task, which must be positive}}.

Physical Model Computations:
- Relevant quantities and estimates: {{DESCRIPTION: include any relevant quantities and estimates used in the calculations}}.
- Relevant equations: {{DESCRIPTION: include any relevant equations used in the calculations}}.
- Relevant assumptions: {{DESCRIPTION: include any relevant assumptions made in the calculations}}.
- Computations: {{DESCRIPTION: include in full detail any relevant calculations using the above information}}.
- Grasping force computations: {{DESCRIPTION: typically, using the estimated mass m and estimated gripper-object friction mu, a good grasping force is (m*g)/mu. Use this calculation first and only modify it if deemed appropriate}}.
- Force/torque motion computations with object of mass {{NUM}} kg and static friction coefficient of {{NUM}} along the surface: {{DESCRIPTION: for the derived or estimated motion, compute the surface friction using appropriate formulae and quantities}}.

Force/Torque Motion Estimation:
Linear X-axis:  To complete the task and based upon {{DESCRIPTION: reasoning about and estimation of task physical properties}}, the object in the image must exert {{CHOICE: [leftward, rightward, no]}} force along the X-axis with magnitude {{PNUM}} N.
Linear Y-axis:  To complete the task and based upon {{DESCRIPTION: reasoning about and estimation of task physical properties}}, the object in the image must exert {{CHOICE: [backward, forward, no]}} force along the Y-axis with magnitude {{PNUM}} N.
Linear Z-axis:  To complete the task and based upon {{DESCRIPTION: reasoning about and estimation of task physical properties}}, the object in the image must exert {{CHOICE: linear [upward, downward, no]}} force along the Z-axis with magnitude {{PNUM}} N.
Angular X-axis: To complete the task and based upon {{DESCRIPTION: reasoning about and estimation of task physical properties}}, the object in the image must exert {{CHOICE: angular [counterclockwise, clockwise, no]}} torque about the X-axis with magnitude {{PNUM}} N-m.
Angular Y-axis: To complete the task and based upon {{DESCRIPTION: reasoning about and estimation of task physical properties}}, the object in the image must exert {{CHOICE: angular [counterclockwise, clockwise, no]}} torque about the Y-axis with magnitude {{PNUM}} N-m.
Angular Z-axis: To complete the task and based upon {{DESCRIPTION: reasoning about and estimation of task physical properties}}, the object in the image must exert {{CHOICE: angular [counterclockwise, clockwise, no]}} torque about the Z-axis with magnitude {{PNUM}} N-m.
Grasping force:  {{DESCRIPTION: estimated force range and justification based on friction, mass, resistance}}, thus {{PNUM}} to {{PNUM}} N .


Python Code with Final Motion Plan:
```python
# succinct text description of the explicit estimated physical properties of the object, including mass, material, friction coefficients, etc.
property_description = "{{DESCRIPTION: describe succinctly the object and its properties}}"
# succinct text description of the motion plan along the world axes
world_motion_description = "{{DESCRIPTION: the object's required position motion in the world frame to accomplish the task}}"
# describe the motion along the [x, y, z] axes as either positive, negative, or no motion, based on the mapping of world-relative motion to positive/negative motion provided in the direction guide
world_motion_direction = [{{CHOICE: [-1, 0, 1]}}, {{CHOICE: [-1, 0, 1]}}, {{CHOICE: [-1, 0, 1]}}]
# the magnitude of motion across the motion direction axes [x, y ,z]
world_motion_magnitude = [{{PNUM}}, {{PNUM}}, {{PNUM}}]
# the vector (sign of direction * magnitude) of motion across the motion direction axes [x, y ,z]. 
world_motion_vector = [{{NUM}}, {{NUM}}, {{NUM}}]
# succinct text description of the planned forces and torques on the object in the world frame
ft_description = "{{DESCRIPTION: describe succinctly the forces and torques required in the world frame to accomplish the task}}"
# the magnitudes of the forces and torques along the [x, y, z, rx, ry, rz] axes
ft_magnitude = [{{PNUM}}, {{PNUM}}, {{PNUM}}, {{PNUM}}, {{PNUM}}, {{PNUM}}]
# the vector (sign of direction * magnitude) of the forces and torques along the [x, y, z, rx, ry, rz] axes
ft_vector = [{{NUM}}, {{NUM}}, {{NUM}}, {{NUM}}, {{NUM}}, {{NUM}}]
# the grasping force, which must be positive
grasp_force = {{PNUM}}
# the task duration, which must be positive
duration = {{PNUM}}
```

[end of motion plan]

Rules:
1. Replace all {{DESCRIPTION: ...}}, {{PNUM}}, {{NUM}}, and {{CHOICE: ...}} entries with specific values or statements. For example, {{PNUM}} should be replaced with a number like 0.5. This is very important for downstream parsing!!
2. Use best physical reasoning based on known robot/environmental capabilities. Remember that the robot may have to exert forces in additional axes compared to the motion direction axes in order to maintain contacts between the object, robot, and environment.
3. Always include motion for all axes of motion, even if it's "No motion required."
4. Keep the explanation concise but physically grounded. Prioritize interpretability and reproducibility.
5. Use common sense where exact properties are ambiguous, and explain assumptions.
6. Do not include any sections outside the start/end blocks or add non-specified bullet points.
7. Make sure to provide the final python code for each requested force in a code block. Remember to fully replace the placeholder text with the actual values!
8. Do not abbreviate the prompt when generating the response. Fully reproduce the template, but filled in with your reasoning.
9. Make sure to refer to the provided correspondence in the direction guide between motion in the world frame and positive/negative motion in the respective axes.
"""

base_thinker = """
Given the user instruction and an image of a robot wrist-image view, generate a structured physical plan for a robot end-effector interacting with the environment.
The task is to {task} while grasping the {obj}.

The robot is controlled using position and torque-based control, with access to contact feedback and 6D motion capabilities. 
Motions can include grasping, lifting, pushing, tapping, sliding, rotating, or any interaction with objects or surfaces.

Reason about the provided and implicit information in the images and task description to generate a structured plan for the robot's positional motion. Think about:
- Object geometry and contact points (from the image)
- Prior knowledge of object material types and mass estimates
- Force/torque sensing at the wrist
- Environmental knowledge (table, gravity, hinge resistance, etc.)

The image is labeled with the axes of motion relative to the base frame of the robot, as in the canonical world-axes (for example, the red positive Z-axis will always represent upward direction in the world).
We must use the provided image data and physical reasoning to carefully map the true motion in the world frame to accomplish the task.
We want to reason about forces and torques relative to the world frame.

[start of motion plan]
The task is to {task} while grasping the {obj}.

Understanding Object-Centric Motion in the World Frame:
The provided images in the two-part image confirm {{DESCRIPTION: the object and environment in the image and their properties, such as color, shape, and material, and their correspondence to the requested task}}.
The blue axis representing the world Z-axis corresponds to upward (positive) and downward (negative) motion in the world. 
To complete the task, the object in the image should have {{CHOICE: [upward, downward, no]}} linear motion along the Z-axis with magnitude {{PNUM}} meters.
The red axis representing the world X-axis corresponds to right (positive) and left (negative) motion in the world, relative to the robot. 
To complete the task, the object in the image should have {{CHOICE: [leftward, rightward, no]}} linear motion along the X-axis with magnitude {{PNUM}} meters.
The green axis representing the world Y-axis corresponds to forward (positive) and backward (negative) motion in the world, relative to the robot. 
To complete the task, the object in the image should have {{CHOICE: [backward, forward, no]}} linear motion along the Y-axis with magnitude {{PNUM}} meters.
To accomplish the task in the world frame, the object must be moved {{DESCRIPTION: the object's required motion in the world frame to accomplish the task}}.

Understanding Robot-Applied Forces and Torques to Move Object in the World Frame:
To estimate the forces and torques required to accomplish {task} while grasping the {obj}, we must consider the following:
- Object Properties: {{DESCRIPTION: Think very carefully about the estimated mass, material, stiffness, friction coefficient of the object based off the visual information and semantic knowledge about the object. If object is articulated, do the same reasoning for whatever joint / degree of freedom enables motion. }}.
- Environmental Factors: {{DESCRIPTION: Think very carefully about the various environmental factors in task like gravity, surface friction, damping, hinge resistance that would interact with the object over the course of the task}}.
- The relevant object is {{DESCRIPTION: describe the object and its properties}} has mass {{NUM}} kg and, with the robot gripper, has a static friction coefficient of {{NUM}}.
- The surface of interaction is {{DESCRIPTION: describe the surface and its properties}} has a static friction coefficient of {{NUM}} with the object.
- Contact Types: {{DESCRIPTION: consideration of various contacts such as edge contact, maintaining surface contact, maintaining a pinch grasp, etc.}}.
- Motion Type: {{DESCRIPTION: consideration of forceful motion(s) involved in accomplishing task such as pushing forward while pressing down, rotating around hinge by pulling up and out, or sliding while maintaining contact}}.
- Contact Considerations: {{DESCRIPTION: explicitly consider whether additional axes of force are required to maintain contact with the object, robot, and environmen and accomplish the motion goal}}.
- Motion along axes: {{DESCRIPTION: e.g., the robot exerts motion in a “linear,” “rotational,” “some combination” fashion along the [x, y, z, rx, ry, rz] axes}}.
- Task duration: {{DESCRIPTION: reasoning about the task motion, forces, and other properties to determine an approximate time duration of the task, which must be positive}}.

Physical Model Computations:
- Relevant quantities and estimates: {{DESCRIPTION: include any relevant quantities and estimates used in the calculations}}.
- Relevant equations: {{DESCRIPTION: include any relevant equations used in the calculations}}.
- Relevant assumptions: {{DESCRIPTION: include any relevant assumptions made in the calculations}}.
- Computations: {{DESCRIPTION: include in full detail any relevant calculations using the above information}}.
- Grasping force computations: {{DESCRIPTION: typically, using the estimated mass m and estimated gripper-object friction mu, a good grasping force is (m*g)/mu. Use this calculation first and only modify it if deemed appropriate}}.
- Force/torque motion computations with object of mass {{NUM}} kg and static friction coefficient of {{NUM}} along the surface: {{DESCRIPTION: for the derived or estimated motion, compute the surface friction using appropriate formulae and quantities}}.

Force/Torque Motion Estimation:
Linear X-axis:  To complete the task and based upon {{DESCRIPTION: reasoning about and estimation of task physical properties}}, the object in the image must exert {{CHOICE: [leftward, rightward, no]}} force along the X-axis with magnitude {{PNUM}} N.
Linear Y-axis:  To complete the task and based upon {{DESCRIPTION: reasoning about and estimation of task physical properties}}, the object in the image must exert {{CHOICE: [backward, forward, no]}} force along the Y-axis with magnitude {{PNUM}} N.
Linear Z-axis:  To complete the task and based upon {{DESCRIPTION: reasoning about and estimation of task physical properties}}, the object in the image must exert {{CHOICE: linear [upward, downward, no]}} force along the Z-axis with magnitude {{PNUM}} N.
Angular X-axis: To complete the task and based upon {{DESCRIPTION: reasoning about and estimation of task physical properties}}, the object in the image must exert {{CHOICE: angular [counterclockwise, clockwise, no]}} torque about the X-axis with magnitude {{PNUM}} N-m.
Angular Y-axis: To complete the task and based upon {{DESCRIPTION: reasoning about and estimation of task physical properties}}, the object in the image must exert {{CHOICE: angular [counterclockwise, clockwise, no]}} torque about the Y-axis with magnitude {{PNUM}} N-m.
Angular Z-axis: To complete the task and based upon {{DESCRIPTION: reasoning about and estimation of task physical properties}}, the object in the image must exert {{CHOICE: angular [counterclockwise, clockwise, no]}} torque about the Z-axis with magnitude {{PNUM}} N-m.
Grasping force:  {{DESCRIPTION: estimated force range and justification based on friction, mass, resistance}}, thus {{PNUM}} to {{PNUM}} N .


Python Code with Final Motion Plan:
```python
# succinct text description of the explicit estimated physical properties of the object, including mass, material, friction coefficients, etc.
property_description = "{{DESCRIPTION: describe succinctly the object and its properties}}"
# succinct text description of the motion plan along the world axes
world_motion_description = "{{DESCRIPTION: the object's required position motion in the world frame to accomplish the task}}"
# describe the motion along the [x, y, z] axes as either positive, negative, or no motion, based on the mapping of world-relative motion to positive/negative motion provided in the direction guide
world_motion_direction = [{{CHOICE: [-1, 0, 1]}}, {{CHOICE: [-1, 0, 1]}}, {{CHOICE: [-1, 0, 1]}}]
# the magnitude of motion across the motion direction axes [x, y ,z]
world_motion_magnitude = [{{PNUM}}, {{PNUM}}, {{PNUM}}]
# the vector (sign of direction * magnitude) of motion across the motion direction axes [x, y ,z]. 
world_motion_vector = [{{NUM}}, {{NUM}}, {{NUM}}]
# succinct text description of the planned forces and torques on the object in the world frame
ft_description = "{{DESCRIPTION: describe succinctly the forces and torques required in the world frame to accomplish the task}}"
# the magnitudes of the forces and torques along the [x, y, z, rx, ry, rz] axes
ft_magnitude = [{{PNUM}}, {{PNUM}}, {{PNUM}}, {{PNUM}}, {{PNUM}}, {{PNUM}}]
# the vector (sign of direction * magnitude) of the forces and torques along the [x, y, z, rx, ry, rz] axes
ft_vector = [{{NUM}}, {{NUM}}, {{NUM}}, {{NUM}}, {{NUM}}, {{NUM}}]
# the grasping force, which must be positive
grasp_force = {{PNUM}}
# the task duration, which must be positive
duration = {{PNUM}}
```

[end of motion plan]

Rules:
1. Replace all {{DESCRIPTION: ...}}, {{PNUM}}, {{NUM}}, and {{CHOICE: ...}} entries with specific values or statements. For example, {{PNUM}} should be replaced with a number like 0.5. This is very important for downstream parsing!!
2. Use best physical reasoning based on known robot/environmental capabilities. Remember that the robot may have to exert forces in additional axes compared to the motion direction axes in order to maintain contacts between the object, robot, and environment.
3. Always include motion for all axes of motion, even if it's "No motion required."
4. Keep the explanation concise but physically grounded. Prioritize interpretability and reproducibility.
5. Use common sense where exact properties are ambiguous, and explain assumptions.
6. Do not include any sections outside the start/end blocks or add non-specified bullet points.
7. Make sure to provide the final python code for each requested force in a code block. Remember to fully replace the placeholder text with the actual values!
8. Do not abbreviate the prompt when generating the response. Fully reproduce the template, but filled in with your reasoning.
9. Make sure to refer to the provided correspondence in the direction guide between motion in the world frame and positive/negative motion in the respective axes.
"""

base_third_thinker = """
Given the user instruction and two-part image containing a robot wrist-image view on the left, a third-person view on the right, generate a structured physical plan for a robot end-effector interacting with the environment.
The task is to {task} while grasping the {obj}.

The robot is controlled using position and torque-based control, with access to contact feedback and 6D motion capabilities. 
Motions can include grasping, lifting, pushing, tapping, sliding, rotating, or any interaction with objects or surfaces.

Reason about the provided and implicit information in the images and task description to generate a structured plan for the robot's positional motion. Think about:
- Object geometry and contact points (from the image)
- Prior knowledge of object material types and mass estimates
- Force/torque sensing at the wrist
- Environmental knowledge (table, gravity, hinge resistance, etc.)

The left image is labeled with the axes of motion relative to the base frame of the robot, as in the canonical world-axes (for example, the red positive Z-axis will always represent upward direction in the world).
The right image is a third-person view of the robot, which may be used to help with the mapping of the axes and understanding the environment
We must use the provided image data and physical reasoning to carefully map the true motion in the world frame to accomplish the task.
We want to reason about forces and torques relative to the world frame.

[start of motion plan]
The task is to {task} while grasping the {obj}.

Understanding Object-Centric Motion in the World Frame:
The provided images in the two-part image confirm {{DESCRIPTION: the object and environment in the image and their properties, such as color, shape, and material, and their correspondence to the requested task}}.
The blue axis representing the world Z-axis corresponds to upward (positive) and downward (negative) motion in the world. 
To complete the task, the object in the image should have {{CHOICE: [upward, downward, no]}} linear motion along the Z-axis with magnitude {{PNUM}} meters.
The red axis representing the world X-axis corresponds to right (positive) and left (negative) motion in the world, relative to the robot. 
To complete the task, the object in the image should have {{CHOICE: [leftward, rightward, no]}} linear motion along the X-axis with magnitude {{PNUM}} meters.
The green axis representing the world Y-axis corresponds to forward (positive) and backward (negative) motion in the world, relative to the robot. 
To complete the task, the object in the image should have {{CHOICE: [backward, forward, no]}} linear motion along the Y-axis with magnitude {{PNUM}} meters.
To accomplish the task in the world frame, the object must be moved {{DESCRIPTION: the object's required motion in the world frame to accomplish the task}}.

Understanding Robot-Applied Forces and Torques to Move Object in the World Frame:
To estimate the forces and torques required to accomplish {task} while grasping the {obj}, we must consider the following:
- Object Properties: {{DESCRIPTION: Think very carefully about the estimated mass, material, stiffness, friction coefficient of the object based off the visual information and semantic knowledge about the object. If object is articulated, do the same reasoning for whatever joint / degree of freedom enables motion. }}.
- Environmental Factors: {{DESCRIPTION: Think very carefully about the various environmental factors in task like gravity, surface friction, damping, hinge resistance that would interact with the object over the course of the task}}.
- The relevant object is {{DESCRIPTION: describe the object and its properties}} has mass {{NUM}} kg and, with the robot gripper, has a static friction coefficient of {{NUM}}.
- The surface of interaction is {{DESCRIPTION: describe the surface and its properties}} has a static friction coefficient of {{NUM}} with the object.
- Contact Types: {{DESCRIPTION: consideration of various contacts such as edge contact, maintaining surface contact, maintaining a pinch grasp, etc.}}.
- Motion Type: {{DESCRIPTION: consideration of forceful motion(s) involved in accomplishing task such as pushing forward while pressing down, rotating around hinge by pulling up and out, or sliding while maintaining contact}}.
- Contact Considerations: {{DESCRIPTION: explicitly consider whether additional axes of force are required to maintain contact with the object, robot, and environmen and accomplish the motion goal}}.
- Motion along axes: {{DESCRIPTION: e.g., the robot exerts motion in a “linear,” “rotational,” “some combination” fashion along the [x, y, z, rx, ry, rz] axes}}.
- Task duration: {{DESCRIPTION: reasoning about the task motion, forces, and other properties to determine an approximate time duration of the task, which must be positive}}.

Physical Model Computations:
- Relevant quantities and estimates: {{DESCRIPTION: include any relevant quantities and estimates used in the calculations}}.
- Relevant equations: {{DESCRIPTION: include any relevant equations used in the calculations}}.
- Relevant assumptions: {{DESCRIPTION: include any relevant assumptions made in the calculations}}.
- Computations: {{DESCRIPTION: include in full detail any relevant calculations using the above information}}.
- Grasping force computations: {{DESCRIPTION: typically, using the estimated mass m and estimated gripper-object friction mu, a good grasping force is (m*g)/mu. Use this calculation first and only modify it if deemed appropriate}}.
- Force/torque motion computations with object of mass {{NUM}} kg and static friction coefficient of {{NUM}} along the surface: {{DESCRIPTION: for the derived or estimated motion, compute the surface friction using appropriate formulae and quantities}}.

Force/Torque Motion Estimation:
Linear X-axis:  To complete the task and based upon {{DESCRIPTION: reasoning about and estimation of task physical properties}}, the object in the image must exert {{CHOICE: [leftward, rightward, no]}} force along the X-axis with magnitude {{PNUM}} N.
Linear Y-axis:  To complete the task and based upon {{DESCRIPTION: reasoning about and estimation of task physical properties}}, the object in the image must exert {{CHOICE: [backward, forward, no]}} force along the Y-axis with magnitude {{PNUM}} N.
Linear Z-axis:  To complete the task and based upon {{DESCRIPTION: reasoning about and estimation of task physical properties}}, the object in the image must exert {{CHOICE: linear [upward, downward, no]}} force along the Z-axis with magnitude {{PNUM}} N.
Angular X-axis: To complete the task and based upon {{DESCRIPTION: reasoning about and estimation of task physical properties}}, the object in the image must exert {{CHOICE: angular [counterclockwise, clockwise, no]}} torque about the X-axis with magnitude {{PNUM}} N-m.
Angular Y-axis: To complete the task and based upon {{DESCRIPTION: reasoning about and estimation of task physical properties}}, the object in the image must exert {{CHOICE: angular [counterclockwise, clockwise, no]}} torque about the Y-axis with magnitude {{PNUM}} N-m.
Angular Z-axis: To complete the task and based upon {{DESCRIPTION: reasoning about and estimation of task physical properties}}, the object in the image must exert {{CHOICE: angular [counterclockwise, clockwise, no]}} torque about the Z-axis with magnitude {{PNUM}} N-m.
Grasping force:  {{DESCRIPTION: estimated force range and justification based on friction, mass, resistance}}, thus {{PNUM}} to {{PNUM}} N .


Python Code with Final Motion Plan:
```python
# succinct text description of the explicit estimated physical properties of the object, including mass, material, friction coefficients, etc.
property_description = "{{DESCRIPTION: describe succinctly the object and its properties}}"
# succinct text description of the motion plan along the world axes
world_motion_description = "{{DESCRIPTION: the object's required position motion in the world frame to accomplish the task}}"
# describe the motion along the [x, y, z] axes as either positive, negative, or no motion, based on the mapping of world-relative motion to positive/negative motion provided in the direction guide
world_motion_direction = [{{CHOICE: [-1, 0, 1]}}, {{CHOICE: [-1, 0, 1]}}, {{CHOICE: [-1, 0, 1]}}]
# the magnitude of motion across the motion direction axes [x, y ,z]
world_motion_magnitude = [{{PNUM}}, {{PNUM}}, {{PNUM}}]
# the vector (sign of direction * magnitude) of motion across the motion direction axes [x, y ,z]. 
world_motion_vector = [{{NUM}}, {{NUM}}, {{NUM}}]
# succinct text description of the planned forces and torques on the object in the world frame
ft_description = "{{DESCRIPTION: describe succinctly the forces and torques required in the world frame to accomplish the task}}"
# the magnitudes of the forces and torques along the [x, y, z, rx, ry, rz] axes
ft_magnitude = [{{PNUM}}, {{PNUM}}, {{PNUM}}, {{PNUM}}, {{PNUM}}, {{PNUM}}]
# the vector (sign of direction * magnitude) of the forces and torques along the [x, y, z, rx, ry, rz] axes
ft_vector = [{{NUM}}, {{NUM}}, {{NUM}}, {{NUM}}, {{NUM}}, {{NUM}}]
# the grasping force, which must be positive
grasp_force = {{PNUM}}
# the task duration, which must be positive
duration = {{PNUM}}
```

[end of motion plan]

Rules:
1. Replace all {{DESCRIPTION: ...}}, {{PNUM}}, {{NUM}}, and {{CHOICE: ...}} entries with specific values or statements. For example, {{PNUM}} should be replaced with a number like 0.5. This is very important for downstream parsing!!
2. Use best physical reasoning based on known robot/environmental capabilities. Remember that the robot may have to exert forces in additional axes compared to the motion direction axes in order to maintain contacts between the object, robot, and environment.
3. Always include motion for all axes of motion, even if it's "No motion required."
4. Keep the explanation concise but physically grounded. Prioritize interpretability and reproducibility.
5. Use common sense where exact properties are ambiguous, and explain assumptions.
6. Do not include any sections outside the start/end blocks or add non-specified bullet points.
7. Make sure to provide the final python code for each requested force in a code block. Remember to fully replace the placeholder text with the actual values!
8. Do not abbreviate the prompt when generating the response. Fully reproduce the template, but filled in with your reasoning.
9. Make sure to refer to the provided correspondence in the direction guide between motion in the world frame and positive/negative motion in the respective axes.
"""

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

[start of motion plan]
Aligning Image With Motion:
The task is to {task} while grasping the {obj}.
The world frame motion to accomplish this task is {world_motion_vector} (x, y, z in meters) which resolves to the following positional motion along wrist frame: {wrist_motion_vector}.
In the right image with the labeled wrist axes, the center blue dot into the page represents motion along the wrist Z-axis. That is why, based off knowledge of the task and motion in the world frame the the motion along the wrist Z-axis is {wrist_motion_vector[2]}, since {{DESCRIPTION: the object's required motion in the wrist frame to accomplish the task}}.
Then, the red axis represents motion along the wrist's X-axis. That is why, based off knowledge of the task and motion in the world frame the the motion along the wrist X-axis is {wrist_motion_vector[0]}, since {{DESCRIPTION: the object's required motion in the wrist frame to accomplish the task}}.
Finally, the green axis represents motion along the wrist's Y-axis. That is why, based off knowledge of the task and motion in the world frame the the motion along the wrist Y-axis is {wrist_motion_vector[1]}, since {{DESCRIPTION: the object's required motion in the wrist frame to accomplish the task}}.
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
scrap = """

Based off knowledge of the task and motion, the object must be moved {{DESCRIPTION: the object's required motion in the wrist frame to accomplish the task}}.
Thus, in order to complete the task, the required linear wrist motion along the red axis representing the positive X-axis is {{DESCRIPTION: the potential linear motion or lack thereof of the object in the image to accomplish the task}}.
Thus, in order to complete the task, the required linear wrist motion along the green axis representing positive Y-axis is {{DESCRIPTION: the potential linear motion or lack thereof of the object in the image to accomplish the task}}.
Thus, in order to complete the task, the required linear wrist motion along the blue dot representing the positive Z-axis (into the page) is {{DESCRIPTION: the potential linear motion or lack thereof of the object in the image to accomplish the task}}.
Thus, in order to complete the task, the required angular wrist motion about the red axis representing the positive X-axis is {{DESCRIPTION: the potential angular motion or lack thereof of the object in the image to accomplish the task}}.
Thus, in order to complete the task, the required angular wrist motion about the green axis representing positive Y-axis is {{DESCRIPTION: the potential angular motion or lack thereof of the object in the image to accomplish the task}}.
Thus, in order to complete the task, the required angular wrist motion about the blue dot representing the positive Z-axis (into the page) is {{DESCRIPTION: the potential angular motion or lack thereof of the object in the image to accomplish the task}}.
Succinct motion plan: {{DESCRIPTION: describe succinctly the motion required along which wrist axes of motion}}.

Wrist Motion Required:
X-axis: There should be {{CHOICE: [positive, negative, no motion]}} along the specified wrist axis, with approximate magnitude {{NUM}}.
Y-axis: There should be {{CHOICE: [positive, negative, no motion]}} along the specified wrist axis, with approximate magnitude {{NUM}}.
Z-axis: There should be {{CHOICE: [positive, negative, no motion]}} along the specified wrist axis, with approximate magnitude {{NUM}}.

This is because upward and positive or downward and negative motion along the world Z-axis corresponds to wrist-relative motion along {{DESCRIPTION: the wrist axes which align with the world Z-axis}}.
This is because leftward and positive or rightward and negative motion along the world X-axis corresponds to wrist-relative motion along {{DESCRIPTION: the wrist axes which align with the world X-axis}}.
This is because backward and positive or forward and negative motion along the world Y-axis corresponds to wrist-relative motion along {{DESCRIPTION: the wrist axes which align with the world Y-axis}}.
In the right image with the labeled wrist axes, the center blue dot represents (into the image and positive) or (out of the image and negative) motion along the wrist Z-axis. That is why, based off knowledge of the task and motion in the world frame the the motion along the wrist Z-axis is {wrist_motion_vector[2]}, since {{DESCRIPTION: the object's required motion in the wrist frame to accomplish the task}}.
Then, the red axis represents (down in the image and positive) and (up the image and negative) motion along the wrist's X-axis. That is why, based off knowledge of the task and motion in the world frame the the motion along the wrist X-axis is {wrist_motion_vector[0]}, since {{DESCRIPTION: the object's required motion in the wrist frame to accomplish the task}}.
Finally, the green axis represents (left in the image and positive) and (right in the image and negative) motion along the wrist's Y-axis. That is why, based off knowledge of the task and motion in the world frame the the motion along the wrist Y-axis is {wrist_motion_vector[1]}, since {{DESCRIPTION: the object's required motion in the wrist frame to accomplish the task}}.
"""
import re
import sys
import ast

import magpie_prompts.safe_executor as safe_executor
import magpie_prompts.llm_prompt as llm_prompt
import magpie_prompts.process_code as process_code
import magpie_prompts.magpie_execution as magpie_execution

class PromptForceThinker(llm_prompt.LLMPrompt):
  """Prompt with both Motion Descriptor and Motion Coder."""

  def __init__(
      self,
  ):
    self.name = "LanguageAndVision2StructuredForceMotionParameters"

    self.num_llms = 1
    self.prompts = [prompt_motion_thinker]

    # The coder doesn't need to keep the history as it only serves a purpose for
    # translating to code
    self.keep_message_history = [True]
    self.response_processors = [
        self.process_thinker_response,
    ]

  # process the response from thinker, the output will be used as input to coder
  def process_thinker_response(self, response: str) -> str:
    try:
      # remove strings from list that begin with # or are empty
      force_plan_string = str(response).split("python")[-1].split("```")[0].split('\n')
      force_plan_string = [x for x in force_plan_string if x and not x.startswith("#")]
      force_plan_string = [x.strip() for x in force_plan_string]
      # separate variable names and values from strings, make motion_plan dict
      force_plan = {x.split("=")[0].strip(): ast.literal_eval(x.split("=")[1]) for x in force_plan_string}
      return force_plan
    except Exception as _:  # pylint: disable=broad-exception-caught
      print("Error processing response from thinker: ", _)
      return response