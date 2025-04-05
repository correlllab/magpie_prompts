prompt_motion_thinker = """
Given the user instruction and image, generate a structured physical plan for a robot end-effector interacting with the environment.

The robot is controlled using position and torque-based control, with access to contact feedback and 6D motion capabilities. Motions can include grasping, lifting, pushing, tapping, sliding, rotating, or any interaction with objects or surfaces.

Assume the robot has access to:
- Object geometry and contact points (from the image)
- Force/torque sensing at the wrist
- Prior knowledge of object material types and mass estimates
- Environmental knowledge (table, gravity, hinge resistance, etc.)

Use physical reasoning to complete the following plan in a structured format.

[start of motion plan]
The right image is labeled with the axes of motion, which do not necessarily correspond with the world axes.
The task is to {task} while grasping the {obj}.
The green axis pointing to the right of the image is the positive X-axis, corresponding [DESCRIPTION: the potential motion or lack thereof of the object in the image to accomplish the task].
The blue axis pointing up the image is the negative Y-axis, corresponding [DESCRIPTION: the potential motion or lack thereof of the object in the image to accomplish the task].
The red dot pointing into the image is the positive Z-axis, corresponding [DESCRIPTION: the potential motion or lack thereof of the object in the image to accomplish the task].

Motion Required:
X-axis: [DESCRIPTION: describe if movement is required and in which direction (e.g., "Move positive to push the lid closed")].

Y-axis: [DESCRIPTION: describe if movement is required and in which direction].

Z-axis: [DESCRIPTION: describe if movement is required and in which direction].

To estimate the forces required to accomplish {task} while grasping the {obj}, we must consider the following:
- [DESCRIPTION: describe the forces required to accomplish the task for a specific subcomponent or subtask, including any resistances or forces acting on the object].
- [DESCRIPTION: describe the forces required to accomplish the task for a specific subcomponent or subtask, including any resistances or forces acting on the object].
- ... [DESCRIPTION: continue as many descriptions as needed]

Qualitative Force Estimation:
X-axis: [DESCRIPTION: estimated force range and justification based on friction, mass, resistance].

Y-axis: [DESCRIPTION: estimated force range and justification based on friction, mass, resistance].

Z-axis: [DESCRIPTION: estimated force range and justification based on friction, mass, resistance].

Grasping force: [DESCRIPTION: estimated force range and justification based on friction, mass, resistance].

Detailed Force Estimation Reasoning:
- Object Properties: [DESCRIPTION: estimated mass, material, stiffness, friction coefficient, if object is articulated, do the same reasoning for whatever joint / degree of freedom enables motion].
- Contact Type: [DESCRIPTION: e.g., “edge contact,” “surface press,” “pinch grip,” etc.].
- Motion Type: [DESCRIPTION: e.g., “push while pressing down,” “rotate around hinge,” “slide while maintaining contact”].
- Motion along axes: [DESCRIPTION: e.g., the robot exerts motion in a “linear,” “rotational,” “some combination” fashion along the [x, y, z] axes].
- Environmental Factors: [DESCRIPTION: e.g., gravity, table friction, damping, hinge resistance].

Physical Model (if applicable):
- Use Newton’s laws, torque estimates, or friction models if relevant.
- Show your math or approximations clearly. For example:
  "Torque τ = I * α, with I = 1/3 M L² for rectangular lid rotating on hinge..."
  "Force F = τ / r, where r is distance from hinge to contact."

Final Computed Estimated Forces:
X-axis: [PNUM: 0.0–0.0] N  
Y-axis: [PNUM: 0.0–0.0] N  
Z-axis: [PNUM: 0.0–0.0] N  
Grasp: [PNUM: 0.0–0.0] N  
[end of motion plan]

Rules:
1. Replace all [DESCRIPTION: ...] and [PNUM: ...] entries with specific values or short, clear statements.
2. Use best physical reasoning based on known robot/environmental capabilities.
3. Always include motion for all three axes, even if it's "No motion required."
4. Keep the explanation concise but physically grounded. Prioritize interpretability and reproducibility.
5. Use common sense where exact properties are ambiguous, and explain assumptions.
6. Do not include any sections outside the start/end blocks or add non-specified bullet points.
"""

prompt_motion_coder = """
We have a description of a gripper's motion and force sensing and we want you to turn that into the corresponding program with following class functions of the gripper:
The gripper has a measurable max force of 16N and min force of 0.15N, a maximum aperture of 105mm and a minimum aperture of 1mm.

```
def get_aperture(finger='both')
```
finger: which finger to get the aperture in mm, of, either 'left', 'right', or 'both'. If 'left' or 'right', returns aperture, or distance, from finger to center. If 'both', returns aperture between fingers.

```
def set_goal_aperture(aperture, finger='both', record_load=False)
```
aperture: the aperture to set the finger(s) to (in mm)
finger: which finger to set the aperture in mm, of, either 'left', 'right', or 'both'.
record_load: whether to record the load at the goal aperture. If true, will return array of (pos, load) tuples
This function will move the finger(s) to the specified goal aperture, and is used to close and open the gripper.
Returns a position-load data array of shape (2, n) --> [[positions], [loads]], average force, and max force after the motion.

```
def set_compliance(margin, flexibility, finger='both')
```
margin: the allowable error between the goal and present position (in mm)
flexibility: the compliance slope of motor torque (value 0-7, higher is more flexible) until it reaches the compliance margin
finger: which finger to set compliance for, either 'left', 'right', or 'both'

```
def set_force(force, finger='both')
```
force: the maximum force the finger is allowed to apply at contact with an object(in N), ranging from (0.1 to 16 N)
finger: which finger to set compliance for, either 'left', 'right', or 'both'

```
def deligrasp(goal_aperture, initial_force, additional_closure, additional_force, complete_grasp)
```
goal_aperture: the goal aperture to grasp the object (in mm)
initial_force: the initial force to apply to the object (in N)
additional_closure: the additional aperture to close if the gripper slips (in mm)
additional_force: the additional force to apply if the gripper slips (in N)
complete_grasp: whether the grasp is complete or incomplete (True or False)
This function will close the gripper to the goal aperture, apply the initial force, and adjust the force if the gripper slips. If the grasp is incomplete, the gripper will open after the slip check.

```
def poke(direction, speed, aperture)
```
direction: 'left' or 'right' to poke the left or right finger
speed of finger in m/s
aperture: distance to poke in mm (of one finger, not both)


Example answer code:
```
from magpie_control.gripper import Gripper # must import the gripper class
from magpie_control.ur5 import UR5_Interface # must import the robot interface
G = Gripper() # create a gripper object
import numpy as np  # import numpy because we are using it below

new_task = {CHOICE: [True, False]} # Whether or not the task is new
# Reset parameters to default since this is a new, delicate grasp to avoid crushing the raspberry.
if new_task:
    G.reset_parameters()

# [REASONING] 
goal_aperture = {PNUM: goal_aperture}
complete_grasp = {CHOICE: [True, False]} 
# Initial force. Convert mass (g) to (kg). The default value of object weight / friction coefficient.
initial_force = {PNUM: {CHOICE: [({PNUM: mass} * 9.81) / ({PNUM: mu} * 1000), {PNUM: different_inital_force}] }}}
# [REASONING for initial force choice]
additional_closure = {PNUM: additional_closure} 
# Additional force increase. The default value is the product of the object spring constant and the additional_closure, with a dampening constant 0.1.
additional_force = np.max([0.01, additional_closure * {PNUM: spring_constant} * 0.0001])

# Move quickly (without recording load) to a safe aperture that is wider than the goal aperture
G.set_goal_aperture(goal_aperture + additional_closure * 2, finger='both', record_load=False)

# [REASONING]
# [PREDICTION]
G.set_compliance(1, 3, finger='both')
G.set_force(initial_force, 'both')

G.deligrasp(goal_aperture, initial_force, additional_closure, additional_force, complete=complete_grasp, debug=True)
```

Remember:
1. Always format the code in code blocks. In your response all five functions above: get_aperture, set_goal_aperture, set_compliance, set_force, check_slip should be used.
2. Do not invent new functions or classes. The only allowed functions you can call are the ones listed above. Do not leave unimplemented code blocks in your response.
3. The only allowed library is numpy. Do not import or use any other library. If you use np, be sure to import numpy.
4. If you are not sure what value to use, just use your best judge. Do not use None for anything.
5. If you see phrases like [REASONING], replace the entire phrase with a code comment explaining the grasp strategy and its relation to the following gripper commands.
6. If you see phrases like [PREDICTION], replace the entire phrase with a prediction of the gripper's state after the following gripper commands are executed.
7. If you see phrases like {PNUM: default_value}, replace the value with the corresponding value from the grasp description.
8. If you see phrases like {CHOICE: [choice1, choice2, ...]}, it means you should replace the entire phrase with one of the choices listed. Be sure to replace all of them. If you are not sure about the value, just use your best judgement.
9. Remember to import the gripper class and create a Gripper at the beginning of your code.
"""
import re
import sys

import magpie_prompts.safe_executor as safe_executor
import magpie_prompts.llm_prompt as llm_prompt
import magpie_prompts.process_code as process_code
import magpie_prompts.magpie_execution as magpie_execution

class PromptMotionThinkerCoder(llm_prompt.LLMPrompt):
  """Prompt with both Motion Descriptor and Motion Coder."""

  def __init__(
      self,
      executor: safe_executor.SafeExecutor,
  ):
    # self._agent = client.agent()
    self._safe_executor = magpie_execution.MagpieSafeExecutor(executor)

    self.name = "LanguageAndVision2StructuredLang2GraspParameters"

    self.num_llms = 2
    self.prompts = [prompt_motion_thinker, prompt_motion_coder]

    # The coder doesn't need to keep the history as it only serves a purpose for
    # translating to code
    self.keep_message_history = [True, False]
    self.response_processors = [
        self.process_thinker_response,
        self.process_coder_response,
    ]
    self.code_executor = self.execute_code

  # process the response from thinker, the output will be used as input to coder
  def process_thinker_response(self, response: str) -> str:
    try:
      motion_description = (
          re.split(
              "end of description",
              re.split("start of description", response, flags=re.IGNORECASE)[
                  1
              ],
              flags=re.IGNORECASE,
          )[0]
          .strip("[")
          .strip("]")
          .strip()
          .strip("```")
      )
      return motion_description
    except Exception as _:  # pylint: disable=broad-exception-caught
      return response

  def process_coder_response(self, response):
    """Process the response from coder, the output will be the python code."""
    return process_code.process_code_block(response)

  def execute_code(self, code: str) -> None:
    print("ABOUT TO EXECUTE\n", code)
    grasp_log = self._safe_executor.execute(code)
    print(grasp_log)
    return grasp_log
    # self._agent.set_task_parameters(mjpc_parameters.task_parameters)
    # self._agent.set_cost_weights(mjpc_parameters.cost_weights)
