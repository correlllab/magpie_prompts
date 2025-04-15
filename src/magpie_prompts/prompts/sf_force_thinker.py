prompt_motion_thinker = """
Given the user instruction and three-part image containing a wrist-image view on the left, a third-person view in the middle, and another wrist view on the right, generate a structured physical plan for a robot end-effector interacting with the environment.
The task is to {task} while grasping the {obj}.

The robot is controlled using position and torque-based control, with access to contact feedback and 6D motion capabilities. 
Motions can include grasping, lifting, pushing, tapping, sliding, rotating, or any interaction with objects or surfaces.

Reason about the provided and implicit information in the images and task description to generate a structured plan for the robot's motion. Think about:
- Object geometry and contact points (from the image)
- Force/torque sensing at the wrist
- Prior knowledge of object material types and mass estimates
- Environmental knowledge (table, gravity, hinge resistance, etc.)

The left image is labeled with the positive axes of motion relative to the base frame of the robot, as in the canonical world-axes (for example, the red positive Z-axis will always represent upward direction in the world).
The right image is labeled with the axes of motion relative to the wrist of the robot. The wrist of the robot may be oriented differently from the canonical world-axes.
The middle image is a third-person view of the robot, which may be used to help with the mapping of the axes and understanding the environment
Thus, in order to generate a structured motion plan in the wrist frame to accomplish the task, we must use the provided image data and physical reasoning to carefully map the true motion in the world to the motion axes of the wrist.

[start of motion plan]
The task is to {task} while grasping the {obj}.

Aligning Images With Wrist Motion:
The provided images in the three-part image confirm {{DESCRIPTION: the object and environment in the image and their properties, such as color, shape, and material, and their correspondence to the requested task}}.
The red axis representing the positive world Z-axis corresponds to upward motion in the world. The object in the image is {{DESCRIPTION: the object's alignment with the upward world Z-axis, based upon its placement and orientation}}.
The green axis representing the positive world X-axis corresponds to left-ward motion in the world. The object in the image is {{DESCRIPTION: the object's alignment with the left-ward world X-axis, based upon its placement and orientation}}.
The blue axis representing the positive world Y-axis corresponds to backward motion in the world. The object in the image is {{DESCRIPTION: the object's alignment with the backward world Y-axis, based upon its placement and orientation}}.
To accomplish the task in the world frame, the object must be moved {{DESCRIPTION: the object's required motion in the world frame to accomplish the task}}.
The red dot going into the page representing the positive wrist Z-axis corresponds to forward motion from the wrist and camera. Based off knowledge of the task and motion in the world frame, the object must be moved {{DESCRIPTION: the object's required motion in the wrist frame to accomplish the task}}.
The green axis representing the positive wrist X-axis does not have a strict correspondence. Based off knowledge of the task and motion in the world frame and the forward motion of the positive wrist Z-axis, the object must be moved {{DESCRIPTION: the object's required motion in the wrist frame to accomplish the task}}.
The blue axis representing positive wrist Y-axis does not have a strict correspondence. Based off knowledge of the task and motion in the world frame and the forward motion of the positive wrist Z-axis, the object must be moved {{DESCRIPTION: the object's required motion in the wrist frame to accomplish the task}}.
To accomplish the task in the wrist frame, the object must be moved {{DESCRIPTION: the object's required motion in the wrist frame to accomplish the task}}.
Thus, in order to complete the task, the required linear wrist motion along the green axis representing the positive X-axis is {{DESCRIPTION: the potential linear motion or lack thereof of the object in the image to accomplish the task}}.
Thus, in order to complete the task, the required linear wrist motion along the blue axis representing positive Y-axis is {{DESCRIPTION: the potential linear motion or lack thereof of the object in the image to accomplish the task}}.
Thus, in order to complete the task, the required linear wrist motion along the red dot representing the positive Z-axis (into the page) is {{DESCRIPTION: the potential linear motion or lack thereof of the object in the image to accomplish the task}}.
Thus, in order to complete the task, the required angular wrist motion about the green axis representing the positive X-axis is {{DESCRIPTION: the potential angular motion or lack thereof of the object in the image to accomplish the task}}.
Thus, in order to complete the task, the required angular wrist motion about the blue axis representing positive Y-axis is {{DESCRIPTION: the potential angular motion or lack thereof of the object in the image to accomplish the task}}.
Thus, in order to complete the task, the required angular wrist motion about the red dot representing the positive Z-axis (into the page) is {{DESCRIPTION: the potential angular motion or lack thereof of the object in the image to accomplish the task}}.
Succinct motion plan: {{DESCRIPTION: describe succinctly the motion required along which wrist axes of motion}}.

Wrist Motion Required:
X-axis: There should be {{CHOICE: [positive, negative, no motion]}} along the specified wrist axis, with approximate magnitude {{NUM: 0.0}}.
Y-axis: There should be {{CHOICE: [positive, negative, no motion]}} along the specified wrist axis, with approximate magnitude {{NUM: 0.0}}.
Z-axis: There should be {{CHOICE: [positive, negative, no motion]}} along the specified wrist axis, with approximate magnitude {{NUM: 0.0}}.

To estimate the forces and torques required to accomplish {task} while grasping the {obj}, we must consider the following:
- The relevant object is {{DESCRIPTION: describe the object and its properties}} has mass {{NUM: 0.0}} kg and, with the robot gripper, has a static friction coefficient of {{NUM: 0.0}}.
- The surface of interaction is {{DESCRIPTION: describe the surface and its properties}} has a static friction coefficient of {{NUM: 0.0}} with the object.
- Object Properties: {{DESCRIPTION: estimated mass, material, stiffness, friction coefficient, if object is articulated, do the same reasoning for whatever joint / degree of freedom enables motion}}.
- Environmental Factors: {{DESCRIPTION: consideration of various environmental factors in task like gravity, surface friction, damping, hinge resistance}}.
- Contact Types: {{DESCRIPTION: consideration of various contacts such as edge contact, maintaining surface contact, maintaining a pinch grasp, etc.}}.
- Motion Type: {{DESCRIPTION: consideration of forceful motion(s) involved in accomplishing task such as pushing forward while pressing down, rotating around hinge by pulling up and out, or sliding while maintaining contact}}.
- Contact Considerations: {{DESCRIPTION: explicitly consider whether additional axes of force are required to maintain contact with the object, robot, and environmen and accomplish the motion goal}}.
- Motion along axes: {{DESCRIPTION: e.g., the robot exerts motion in a “linear,” “rotational,” “some combination” fashion along the [x, y, z] axes}}.

Physical Model (if applicable):
- Relevant quantities and estimates: {{DESCRIPTION: include any relevant quantities and estimates used in the calculations}}.
- Relevant equations: {{DESCRIPTION: include any relevant equations used in the calculations}}.
- Relevant assumptions: {{DESCRIPTION: include any relevant assumptions made in the calculations}}.
- Computations: {{DESCRIPTION: include in full detail any relevant calculations using the above information}}.
- Force/torque motion computations with object of mass {{NUM: 0.0}} kg and static friction coefficient of {{NUM: 0.0}} along the surface: {{DESCRIPTION: for the derived or estimated motion, compute the surface friction using appropriate formulae and quantities}}.

Force/Torque Motion Estimation:
Linear X-axis: {{DESCRIPTION: estimated force range and justification based on friction, mass, resistance}}.
Linear Y-axis: {{DESCRIPTION: estimated force range and justification based on friction, mass, resistance}}.
Linear Z-axis: {{DESCRIPTION: estimated force range and justification based on friction, mass, resistance}}.
Angular X-axis: {{DESCRIPTION: estimated torque range and justification based on friction, mass, resistance}}.
Angular Y-axis: {{DESCRIPTION: estimated torque range and justification based on friction, mass, resistance}}.
Angular Z-axis: {{DESCRIPTION: estimated torque range and justification based on friction, mass, resistance}}.
Grasping force: {{DESCRIPTION: estimated force range and justification based on friction, mass, resistance}}.


Computed Forces with Estimate Ranges:
Linear X-axis: {{NUM: 0.0}} to {{NUM: 0.0}} N  
Linear Y-axis: {{NUM: 0.0}} to {{NUM: 0.0}} N  
Linear Z-axis: {{NUM: 0.0}} to {{NUM: 0.0}} N
Angular X-axis: {{NUM: 0.0}} to {{NUM: 0.0}} N-m
Angular Y-axis: {{NUM: 0.0}} to {{NUM: 0.0}} N-m
Angular Z-axis: {{NUM: 0.0}} to {{NUM: 0.0}} N-m
Grasp: {{PNUM: 0.0}} to {{PNUM: 0.0}} N  

Python Code with Final Motion Plan:
```python
# describe the motion along the [x, y, z] axes as either positive, negative, or no motion
position_direction = [{{CHOICE: [-1, 0, 1}}, {{CHOICE: [-1, 0, 1}}, {{CHOICE: [-1, 0, 1}}]
# resolve the magnitude of motion across the motion direction axes [x, y ,z]
position_goal = [{{NUM: 0.0}}, {{NUM: 0.0}}, {{NUM: 0.0}}]
# explicitly state the forces and torques along the [x, y, z, rx, ry, rz] axes
wrench= [{{NUM: 0.0}}, {{NUM: 0.0}}, {{NUM: 0.0}}, {{NUM: 0.0}}, {{NUM: 0.0}}, {{NUM: 0.0}}]
# explicitly state the grasping force, which must be positive
grasp_force = {{PNUM: 0.0}}
# explicitly state the task duration, which must be positive
duration = {{PNUM: 0.0}}
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

Use physical reasoning to complete the following plan in a structured format. Use the provided motion plans in the world and wrist frame to help understand the task's forces and torques.
We want to reason about forces and torques relative to the wrist frame because that is the frame of reference for the F/T sensor.
More importantly, as the wrist's end-effector is grasping the object, assuming no slip, the requisite applied forces and especially torques on the object to accomplish the task will be the same as the forces and torques on the wrist frame.

[start of motion plan]
Aligning Image With Motion:
The task is to {task} while grasping the {obj}.
The world frame motion to accomplish this task is {world_motion} (x, y, z in meters) because {world_motion_description}.
Using the robot pose data, this world motion resolves to the following positional motion along wrist frame: {wrist_motion}.
This is because, in the right image with the labeled wrist axes, the center red dot going into the page representing the positive wrist Z-axis corresponds to forward motion from the wrist and camera. Based off knowledge of the task and motion in the world frame, the object must be moved {{DESCRIPTION: the object's required motion in the wrist frame to accomplish the task}}.
Then, the green axis in the right image representing the positive wrist X-axis does not have a strict correspondence. Based off knowledge of the task and motion in the world frame and the forward motion of the positive wrist Z-axis, the object must be moved {{DESCRIPTION: the object's required motion in the wrist frame to accomplish the task}}.
Finally, the blue axis in the right image representing positive wrist Y-axis does not have a strict correspondence. Based off knowledge of the task and motion in the world frame and the forward motion of the positive wrist Z-axis, the object must be moved {{DESCRIPTION: the object's required motion in the wrist frame to accomplish the task}}.
Thus, to accomplish the task in the wrist frame, the object must be moved {{DESCRIPTION: describe succinctly the motion required along which wrist axes of motion to accomplish the task}}.

Understanding Forces and Torques Required for Motion:
To estimate the forces and torques required to accomplish {task} while grasping the {obj}, we must consider the following:
- The relevant object is {{DESCRIPTION: describe the object and its properties}} has mass {{NUM: 0.0}} kg and, with the robot gripper, has a static friction coefficient of {{NUM: 0.0}}.
- The surface of interaction is {{DESCRIPTION: describe the surface and its properties}} has a static friction coefficient of {{NUM: 0.0}} with the object.
- Object Properties: {{DESCRIPTION: estimated mass, material, stiffness, friction coefficient, if object is articulated, do the same reasoning for whatever joint / degree of freedom enables motion}}.
- Environmental Factors: {{DESCRIPTION: consideration of various environmental factors in task like gravity, surface friction, damping, hinge resistance}}.
- Contact Types: {{DESCRIPTION: consideration of various contacts such as edge contact, maintaining surface contact, maintaining a pinch grasp, etc.}}.
- Motion Type: {{DESCRIPTION: consideration of forceful motion(s) involved in accomplishing task such as pushing forward while pressing down, rotating around hinge by pulling up and out, or sliding while maintaining contact}}.
- Contact Considerations: {{DESCRIPTION: explicitly consider whether additional axes of force are required to maintain contact with the object, robot, and environmen and accomplish the motion goal}}.
- Motion along axes: {{DESCRIPTION: e.g., the robot exerts motion in a “linear,” “rotational,” “some combination” fashion along the [x, y, z] axes}}.

Physical Model (if applicable):
- Relevant quantities and estimates: {{DESCRIPTION: include any relevant quantities and estimates used in the calculations}}.
- Relevant equations: {{DESCRIPTION: include any relevant equations used in the calculations}}.
- Relevant assumptions: {{DESCRIPTION: include any relevant assumptions made in the calculations}}.
- Computations: {{DESCRIPTION: include in full detail any relevant calculations using the above information}}.
- Force/torque motion computations with object of mass {{NUM: 0.0}} kg and static friction coefficient of {{NUM: 0.0}} along the surface: {{DESCRIPTION: for the derived or estimated motion, compute the surface friction using appropriate formulae and quantities}}.

Force/Torque Motion Estimation:
Linear X-axis:   {{DESCRIPTION: estimated force range and justification based on friction, mass, resistance}}, thus {{NUM: 0.0}} to {{NUM: 0.0}}.
Linear Y-axis:   {{DESCRIPTION: estimated force range and justification based on friction, mass, resistance}}, thus {{NUM: 0.0}} to {{NUM: 0.0}}.
Linear Z-axis:   {{DESCRIPTION: estimated force range and justification based on friction, mass, resistance}}, thus {{NUM: 0.0}} to {{NUM: 0.0}} N.
Angular X-axis: {{DESCRIPTION: estimated torque range and justification based on friction, mass, resistance}}, thus {{NUM: 0.0}} to {{NUM: 0.0}} N-m.
Angular Y-axis: {{DESCRIPTION: estimated torque range and justification based on friction, mass, resistance}}, thus {{NUM: 0.0}} to {{NUM: 0.0}} N-m.
Angular Z-axis: {{DESCRIPTION: estimated torque range and justification based on friction, mass, resistance}}, thus {{NUM: 0.0}} to {{NUM: 0.0}} N-m.
Grasping force:  {{DESCRIPTION: estimated force range and justification based on friction, mass, resistance}}, thus {{PNUM: 0.0}} to {{PNUM: 0.0}} N .

Python Code with Final Motion Plan:
```python
# explicitly state the forces along the [x, y, z] axes
wrench_description = "{{DESCRIPTION: describe succinctly the forces and torques required along which wrist axes of motion to accomplish the task}}"
# explicitly state the forces and torques along the [x, y, z, rx, ry, rz] axes
wrench= [{{NUM: 0.0}}, {{NUM: 0.0}}, {{NUM: 0.0}}, {{NUM: 0.0}}, {{NUM: 0.0}}, {{NUM: 0.0}}]
# explicitly state the grasping force, which must be positive
grasp_force = {{PNUM: 0.0}}
# explicitly state the task duration, which must be positive
duration = {{PNUM: 0.0}}
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