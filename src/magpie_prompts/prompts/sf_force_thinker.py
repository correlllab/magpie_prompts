prompt_motion_thinker = """
Given the user instruction and image, generate a structured physical plan for a robot end-effector interacting with the environment.

The robot is controlled using position and torque-based control, with access to contact feedback and 6D motion capabilities. 
Motions can include grasping, lifting, pushing, tapping, sliding, rotating, or any interaction with objects or surfaces.

Assume the robot has access to:
- Object geometry and contact points (from the image)
- Force/torque sensing at the wrist
- Prior knowledge of object material types and mass estimates
- Environmental knowledge (table, gravity, hinge resistance, etc.)

Use physical reasoning to complete the following plan in a structured format.

[start of motion plan]
The right image is labeled with the axes of motion, which do not necessarily correspond with the world axes.
The task is to {task} while grasping the {obj}.
The provided image confirms {{DESCRIPTION: the object and environment in the image and their properties, such as color, shape, and material, and their correspondence to the requested task}}.
The green axis pointing to the right of the image is the positive X-axis, corresponding {{DESCRIPTION: the potential motion or lack thereof of the object in the image to accomplish the task}}.
The blue axis pointing up the image is the negative Y-axis, corresponding {{DESCRIPTION: the potential motion or lack thereof of the object in the image to accomplish the task}}.
The red dot pointing into the image is the positive Z-axis, corresponding {{DESCRIPTION: the potential motion or lack thereof of the object in the image to accomplish the task}}.

Position Motion Required:
X-axis: {{DESCRIPTION: describe if movement is required and in which direction along the labeled axis}}.

Y-axis: {{DESCRIPTION: describe if movement is required and in which direction along the labeled axis}}.

Z-axis: {{DESCRIPTION: describe if movement is required and in which direction along the labeled axis}}.

To estimate the forces required to accomplish {task} while grasping the {obj}, we must consider the following:
- {{DESCRIPTION: describe the forces required to accomplish the task for a specific subcomponent or subtask, including any resistances or forces acting on the object}}.
- {{DESCRIPTION: describe the forces required to accomplish the task for a specific subcomponent or subtask, including any resistances or forces acting on the object}}.
- ... {{DESCRIPTION: continue as many descriptions as needed}}

Force Motion Estimation:
X-axis: {{DESCRIPTION: estimated force range and justification based on friction, mass, resistance}}.

Y-axis: {{DESCRIPTION: estimated force range and justification based on friction, mass, resistance}}.

Z-axis: {{DESCRIPTION: estimated force range and justification based on friction, mass, resistance}}.

Grasping force: {{DESCRIPTION: estimated force range and justification based on friction, mass, resistance}}.

Detailed Force Reasoning:
- Object Properties: {{DESCRIPTION: estimated mass, material, stiffness, friction coefficient, if object is articulated, do the same reasoning for whatever joint / degree of freedom enables motion}}.
- Environmental Factors: {{DESCRIPTION: consideration of various environmental factors in task like gravity, surface friction, damping, hinge resistance}}.
- Contact Types: {{DESCRIPTION: consideration of various contacts such as edge contact, maintaining surface contact, maintaining a pinch grasp, etc.}}.
- Motion Type: {{DESCRIPTION: consideration of forceful motion(s) involved in accomplishing task such as pushing forward while pressing down, rotating around hinge by pulling up and out, or sliding while maintaining contact}}.
- Contact Considerations: {{DESCRIPTION: explicitly consider whether additional axes of force are required to maintain contact with the object, robot, and environmen and accomplish the motion goal}}.
- Motion along axes: {{DESCRIPTION: e.g., the robot exerts motion in a “linear,” “rotational,” “some combination” fashion along the [x, y, z] axes}}.

Physical Model (if applicable):
- Use Newton’s laws, torque estimates, or friction models if relevant.
- Show your math or approximations clearly.
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