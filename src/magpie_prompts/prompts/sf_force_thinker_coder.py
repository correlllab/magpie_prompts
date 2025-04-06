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
We have a description of a robot's motion and force sensing and we want you to turn that into the corresponding program with following class functions of the robot:

Example answer code:
```
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
    motion_log = self._safe_executor.execute(code)
    print(motion_log)
    return motion_log
    # self._agent.set_task_parameters(mjpc_parameters.task_parameters)
    # self._agent.set_cost_weights(mjpc_parameters.cost_weights)
