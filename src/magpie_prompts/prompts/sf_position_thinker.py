prompt_position_thinker = """
Given the user instruction and two-part image containing a wrist-image view on the left, a third-person view on the right, generate a structured physical plan for a robot end-effector interacting with the environment.
The task is to {task} while grasping the {obj}.

The robot is controlled using position and torque-based control, with access to contact feedback and 6D motion capabilities. 
Motions can include grasping, lifting, pushing, tapping, sliding, rotating, or any interaction with objects or surfaces.

Reason about the provided and implicit information in the images and task description to generate a structured plan for the robot's motion. Think about:
- Object geometry and contact points (from the image)
- Force/torque sensing at the wrist
- Prior knowledge of object material types and mass estimates
- Environmental knowledge (table, gravity, hinge resistance, etc.)

The left image is labeled with the positive axes of motion relative to the base frame of the robot, as in the canonical world-axes (for example, the red positive Z-axis will always represent upward direction in the world).
The right image is a third-person view of the robot, which may be used to help with the mapping of the axes and understanding the environment
We must use the provided image data and physical reasoning to carefully map the true motion in the world frame to accomplish the task.

[start of motion plan]
The task is to {task} while grasping the {obj}.

Aligning Images With World Frame Motion:
The provided images in the two-part image confirm {{DESCRIPTION: the object and environment in the image and their properties, such as color, shape, and material, and their correspondence to the requested task}}.
The red axis representing the positive world Z-axis corresponds to upward motion in the world. The object in the image is {{DESCRIPTION: the object's alignment with the upward world Z-axis, based upon its placement and orientation}}.
The green axis representing the positive world X-axis corresponds to left-ward motion in the world. The object in the image is {{DESCRIPTION: the object's alignment with the left-ward world X-axis, based upon its placement and orientation}}.
The blue axis representing the positive world Y-axis corresponds to backward motion in the world. The object in the image is {{DESCRIPTION: the object's alignment with the backward world Y-axis, based upon its placement and orientation}}.
To accomplish the task in the world frame, the object must be moved {{DESCRIPTION: the object's required motion in the world frame to accomplish the task}}.

Python Code with Final Motion Plan:
```python
# succinct text description of the motion plan along the world axes
world_motion_description = "{{DESCRIPTION: the object's required motion in the world frame to accomplish the task}}"
# describe the motion along the [x, y, z] axes as either positive, negative, or no motion
world_motion_direction = [{{CHOICE: [-1, 0, 1}}, {{CHOICE: [-1, 0, 1}}, {{CHOICE: [-1, 0, 1}}]
# resolve the magnitude of motion across the motion direction axes [x, y ,z]
world_motion_goal = [{{NUM: 0.0}}, {{NUM: 0.0}}, {{NUM: 0.0}}]
```

[end of motion plan]

Rules:
1. Replace all {{DESCRIPTION: ...}}, {{PNUM: ...}}, {{NUM: ...}}, and {{CHOICE}} entries with specific values or statements.
3. Always include motion for all three axes, even if it's "No motion required."
4. Keep the explanation concise but physically grounded. 
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

class PromptPositionThinker(llm_prompt.LLMPrompt):
  """Prompt with both Motion Descriptor and Motion Coder."""

  def __init__(
      self,
  ):
    self.name = "LanguageAndVision2StructuredPositionMotionParameters"

    self.num_llms = 1
    self.prompts = [prompt_position_thinker]

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