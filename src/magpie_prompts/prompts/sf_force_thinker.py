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
The green axis representing the positive X-axis along the wrist corresponds to {{DESCRIPTION: the world-frame axes and motion, as described in the left and middle images, that best match the task}}.
The blue axis representing negative Y-axis along the wrist corresponds to {{DESCRIPTION: the world-frame axes and motion, as described in the left and middle images, that best match the task}}.
The red dot representing the positive Z-axis (into the page) along the wrist corresponds {{DESCRIPTION: the world-frame axes and motion, as described in the left and middle images, that best match the task}}.}}
Thus, in order to complete the task, the required linear wrist motion along the green axis representing the positive X-axis is {{DESCRIPTION: the potential linear motion or lack thereof of the object in the image to accomplish the task}}.
Thus, in order to complete the task, the required linear wrist motion along the blue axis representing positive Y-axis is {{DESCRIPTION: the potential linear motion or lack thereof of the object in the image to accomplish the task}}.
Thus, in order to complete the task, the required linear wrist motion along the red dot representing the positive Z-axis (into the page) is {{DESCRIPTION: the potential linear motion or lack thereof of the object in the image to accomplish the task}}.
Thus, in order to complete the task, the required angular wrist motion about the green axis representing the positive X-axis is {{DESCRIPTION: the potential angular motion or lack thereof of the object in the image to accomplish the task}}.
Thus, in order to complete the task, the required angular wrist motion about the blue axis representing positive Y-axis is {{DESCRIPTION: the potential angular motion or lack thereof of the object in the image to accomplish the task}}.
Thus, in order to complete the task, the required angular wrist motion about the red dot representing the positive Z-axis (into the page) is {{DESCRIPTION: the potential angular motion or lack thereof of the object in the image to accomplish the task}}.

Position Motion Required:
X-axis: {{DESCRIPTION: describe if movement is required and in which direction along the labeled axis}}.
Y-axis: {{DESCRIPTION: describe if movement is required and in which direction along the labeled axis}}.
Z-axis: {{DESCRIPTION: describe if movement is required and in which direction along the labeled axis}}.

To estimate the forces and torques required to accomplish {task} while grasping the {obj}, we must consider the following:
- The relevant object is {{DESCRIPTION: describe the object and its properties}} has mass {{NUM: 0.0}} kg and, with the robot gripper, has a static friction coefficient of {{NUM: 0.0}}.
- The surface of interaction is {{DESCRIPTION: describe the surface and its properties}} has a static friction coefficient of {{NUM: 0.0}} with the object.
- Object Properties: {{DESCRIPTION: estimated mass, material, stiffness, friction coefficient, if object is articulated, do the same reasoning for whatever joint / degree of freedom enables motion}}.
- Environmental Factors: {{DESCRIPTION: consideration of various environmental factors in task like gravity, surface friction, damping, hinge resistance}}.
- Contact Types: {{DESCRIPTION: consideration of various contacts such as edge contact, maintaining surface contact, maintaining a pinch grasp, etc.}}.
- Motion Type: {{DESCRIPTION: consideration of forceful motion(s) involved in accomplishing task such as pushing forward while pressing down, rotating around hinge by pulling up and out, or sliding while maintaining contact}}.
- Contact Considerations: {{DESCRIPTION: explicitly consider whether additional axes of force are required to maintain contact with the object, robot, and environmen and accomplish the motion goal}}.
- Motion along axes: {{DESCRIPTION: e.g., the robot exerts motion in a “linear,” “rotational,” “some combination” fashion along the [x, y, z] axes}}.

Force/Torque Motion Estimation:
Linear X-axis: {{DESCRIPTION: estimated force range and justification based on friction, mass, resistance}}.
Linear Y-axis: {{DESCRIPTION: estimated force range and justification based on friction, mass, resistance}}.
Linear Z-axis: {{DESCRIPTION: estimated force range and justification based on friction, mass, resistance}}.
Angular X-axis: {{DESCRIPTION: estimated torque range and justification based on friction, mass, resistance}}.
Angular Y-axis: {{DESCRIPTION: estimated torque range and justification based on friction, mass, resistance}}.
Angular Z-axis: {{DESCRIPTION: estimated torque range and justification based on friction, mass, resistance}}.
Grasping force: {{DESCRIPTION: estimated force range and justification based on friction, mass, resistance}}.

Physical Model (if applicable):
- Relevant quantities and estimates: {{DESCRIPTION: include any relevant quantities and estimates used in the calculations}}.
- Relevant equations: {{DESCRIPTION: include any relevant equations used in the calculations}}.
- Relevant assumptions: {{DESCRIPTION: include any relevant assumptions made in the calculations}}.
- Computations: {{DESCRIPTION: include in full detail any relevant calculations using the above information}}.
- Force/torque motion computations with object of mass {{NUM: 0.0}} kg and static friction coefficient of {{NUM: 0.0}} along the surface: {{DESCRIPTION: for the derived or estimated motion, compute the surface friction using appropriate formulae and quantities}}.

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
# explicitly state the forces along the [x, y, z] axes
force = [{{NUM: 0.0}}, {{NUM: 0.0}}, {{NUM: 0.0}}, {{NUM: 0.0}}, {{NUM: 0.0}}, {{NUM: 0.0}}]
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

prompt_motion_thinker_2image = """
Given the user instruction and two-part image containing a third-person view on the left and a wrist view on the right, generate a structured physical plan for a robot end-effector interacting with the environment.

The robot is controlled using position and torque-based control, with access to contact feedback and 6D motion capabilities. 
Motions can include grasping, lifting, pushing, tapping, sliding, rotating, or any interaction with objects or surfaces.

Assume the robot has access to:
- Object geometry and contact points (from the image)
- Force/torque sensing at the wrist
- Prior knowledge of object material types and mass estimates
- Environmental knowledge (table, gravity, hinge resistance, etc.)

Use physical reasoning to complete the following plan in a structured format.

[start of motion plan]
The task is to {task} while grasping the {obj}.

Aligning Image With Motion:
The right image is labeled with the axes of motion relative to the wrist of the robot. 
The wrist of the robot may be oriented differently from the canonical world-axes, and so the upward axis (-Y axis) in the image may not correspond to the upward axis in the world.
Thus, we must carefully map the motion axes of the wrist the true motion in the world. Use the left image, whis is a third-person view of the robot, to help with this mapping.

The provided image confirms {{DESCRIPTION: the object and environment in the image and their properties, such as color, shape, and material, and their correspondence to the requested task}}.
The green axis pointing to the right of the image is the positive X-axis, corresponding {{DESCRIPTION: the potential motion or lack thereof of the object in the image to accomplish the task}}.
The blue axis pointing up the image is the negative Y-axis, corresponding {{DESCRIPTION: the potential motion or lack thereof of the object in the image to accomplish the task}}.
The red dot pointing into the image is the positive Z-axis, corresponding {{DESCRIPTION: the potential motion or lack thereof of the object in the image to accomplish the task}}.

Position Motion Required:
X-axis: {{DESCRIPTION: describe if movement is required and in which direction along the labeled axis}}.

Y-axis: {{DESCRIPTION: describe if movement is required and in which direction along the labeled axis}}.

Z-axis: {{DESCRIPTION: describe if movement is required and in which direction along the labeled axis}}.

To estimate the forces required to accomplish {task} while grasping the {obj}, we must consider the following:
- The relevant object is {{DESCRIPTION: describe the object and its properties}} has mass {{NUM: 0.0}} kg and, with the robot gripper, has a static friction coefficient of {{NUM: 0.0}}.
- The surface of interaction is {{DESCRIPTION: describe the surface and its properties}} has a static friction coefficient of {{NUM: 0.0}} with the object.
- Object Properties: {{DESCRIPTION: estimated mass, material, stiffness, friction coefficient, if object is articulated, do the same reasoning for whatever joint / degree of freedom enables motion}}.
- Environmental Factors: {{DESCRIPTION: consideration of various environmental factors in task like gravity, surface friction, damping, hinge resistance}}.
- Contact Types: {{DESCRIPTION: consideration of various contacts such as edge contact, maintaining surface contact, maintaining a pinch grasp, etc.}}.
- Motion Type: {{DESCRIPTION: consideration of forceful motion(s) involved in accomplishing task such as pushing forward while pressing down, rotating around hinge by pulling up and out, or sliding while maintaining contact}}.
- Contact Considerations: {{DESCRIPTION: explicitly consider whether additional axes of force are required to maintain contact with the object, robot, and environmen and accomplish the motion goal}}.
- Motion along axes: {{DESCRIPTION: e.g., the robot exerts motion in a “linear,” “rotational,” “some combination” fashion along the [x, y, z] axes}}.

Force Motion Estimation:
X-axis: {{DESCRIPTION: estimated force range and justification based on friction, mass, resistance}}.

Y-axis: {{DESCRIPTION: estimated force range and justification based on friction, mass, resistance}}.

Z-axis: {{DESCRIPTION: estimated force range and justification based on friction, mass, resistance}}.

Grasping force: {{DESCRIPTION: estimated force range and justification based on friction, mass, resistance}}.

Physical Model (if applicable):
- Use Newton’s laws, torque estimates, or friction models if relevant, showing your math or approximations clearly.
- Relevant quantities and estimates: {{DESCRIPTION: include any relevant quantities and estimates used in the calculations}}.
- Relevant equations: {{DESCRIPTION: include any relevant equations used in the calculations}}.
- Relevant assumptions: {{DESCRIPTION: include any relevant assumptions made in the calculations}}.
- Computations: {{DESCRIPTION: include in full detail any relevant calculations using the above information}}.

Computed Forces with Estimate Ranges:
X-axis: {{NUM: 0.0}} to {{NUM: 0.0}} N  
Y-axis: {{NUM: 0.0}} to {{NUM: 0.0}} N  
Z-axis: {{NUM: 0.0}} to {{NUM: 0.0}} N  
Grasp: {{PNUM: 0.0}} to {{PNUM: 0.0}} N  

Python Code with Final Motion Plan:
```python
# describe the motion along the [x, y, z] axes as either positive, negative, or no motion
position_direction = [{{CHOICE: [-1, 0, 1}}, {{CHOICE: [-1, 0, 1}}, {{CHOICE: [-1, 0, 1}}]
# resolve the magnitude of motion across the motion direction axes [x, y ,z]
position_goal = [{{NUM: 0.0}}, {{NUM: 0.0}}, {{NUM: 0.0}}]
# explicitly state the forces along the [x, y, z] axes
force = [{{NUM: 0.0}}, {{NUM: 0.0}}, {{NUM: 0.0}}]
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