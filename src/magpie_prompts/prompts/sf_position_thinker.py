prompt_position_thinker = """
Given the user instruction and two-part image containing a wrist-image view on the left, a third-person view on the right, generate a structured physical plan for a robot end-effector interacting with the environment.
The task is to {task} while grasping the {obj}.

The robot is controlled using position and torque-based control, with access to contact feedback and 6D motion capabilities. 
Motions can include grasping, lifting, pushing, tapping, sliding, rotating, or any interaction with objects or surfaces.

Reason about the provided and implicit information in the images and task description to generate a structured plan for the robot's positional motion. Think about:
- Object geometry and contact points (from the image)
- Prior knowledge of object material types and mass estimates
- Environmental knowledge (table, gravity, hinge resistance, etc.)

The left image is labeled with the axes of motion relative to the base frame of the robot, as in the canonical world-axes (for example, the red positive Z-axis will always represent upward direction in the world).
The right image is a third-person view of the robot, which may be used to help with the mapping of the axes and understanding the environment
We must use the provided image data and physical reasoning to carefully map the true motion in the world frame to accomplish the task.

[start of position motion plan]
The task is to {task} while grasping the {obj}.

Aligning Images With World Frame Motion:
The provided images in the two-part image confirm {{DESCRIPTION: the object and environment in the image and their properties, such as color, shape, and material, and their correspondence to the requested task}}.
The red axis representing the world Z-axis corresponds to upward (positive) and downward (negative) motion in the world. 
To complete the task, the object in the image must perform {{CHOICE: [upward and positive, downward and negative, no]}} motion along the Z-axis with magnitude {{PNUM: 0.0}} meters.
The green axis representing the world X-axis corresponds to left (positive) and right (negative) motion in the world, relative to the robot. 
To complete the task, the object in the image must perform {{CHOICE: [leftward and positive, rightward and negative, no]}} motion along the X-axis with magnitude {{PNUM: 0.0}} meters.
The blue axis representing the world Y-axis corresponds to backward (positive) and forward (negative) motion in the world, relative to the robot. 
To complete the task, the object in the image must perform {{CHOICE: [backward and positive, forward and negative, no]}} motion along the Y-axis with magnitude {{PNUM: 0.0}} meters.
To accomplish the task in the world frame, the object must be moved {{DESCRIPTION: the object's required motion in the world frame to accomplish the task}}.

Python Code with Final Motion Plan:
```python
# succinct text description of the motion plan along the world axes
world_motion_description = "{{DESCRIPTION: the object's required motion in the world frame to accomplish the task}}"
# describe the motion along the [x, y, z] axes as either positive, negative, or no motion
world_motion_direction = [{{CHOICE: [-1, 0, 1}}, {{CHOICE: [-1, 0, 1}}, {{CHOICE: [-1, 0, 1}}]
# the magnitude of motion across the motion direction axes [x, y ,z]
world_motion_magnitude = [{{PNUM: 0.0}}, {{PNUM: 0.0}}, {{PNUM: 0.0}}]
# the vector (sign of direction * magnitude) of motion across the motion direction axes [x, y ,z]
world_motion_vector = [{{NUM: 0.0}}, {{NUM: 0.0}}, {{NUM: 0.0}}]
```

[end of position motion plan]

Rules:
1. Replace all {{DESCRIPTION: ...}}, {{PNUM: ...}}, {{NUM: ...}}, and {{CHOICE}} entries with specific values or statements.
2. Always include motion for all three axes, even if it's "No motion required."
3. Keep the explanation concise but physically grounded. 
4. Use common sense where exact properties are ambiguous, and explain assumptions.
5. Do not include any sections outside the start/end blocks or add non-specified bullet points.
6. Make sure to provide the final python code for each requested force in a code block.
7. Remember that for the Y-axis, backward motion is positive and forward motion is negative, while for the X-axis, leftward motion is positive and rightward motion is negative.
"""

prompt_position_reflection = """
The robot has executed the initially provided motion plan, and now we need to analyze the ground-truth positional motion during this interaction.
The feedback is as follows: 
- a two-part image containing a wrist view on the left and a third-person view on the right, both with world-frame labeled axes
- the change in position relative to the wrist
- the change in position relative to the robot base, or the world frame

The goal is to analyze the robot's positional motion and modify the motion plan if necessary or to correct, improve, or completely retry the task:
- You should consider the visual feedback from the two-part image and the positional motion to determine whether the robot was able to accomplish the task.
- Thus, refer to both the prior and current two-part images, which show wrist-view and third-person view images labeled with world-frame axes before and after the robot's motion.
- A potential cause of inconsistency with the motion plan and/or task failure is that the initial motion plan was incorrect, particularly if the robot moved in a direction that did not match the task.
- Refer to the world-frame axes labeled on the prior and current image, the visual differences between the images, and position motion results to help understand the ground-truth motion history in the world frame and task results.
- If this ground-truth motion history does not match the desired motion in the task, then the axes of motion may be incorrect.
- After doing this analysis, you should be able to determine if the robot was able to accomplish the task of {task} while grasping the {obj} via close analysis of the provided feedback.
- Modify the required position motion to improve the robot's performance.

Here are the results of the robot's positional motion interaction with the environment. 
{position_motion_report}

[beginning of postional motion reflection]
Reflection on Task:
The red axis representing the world Z-axis corresponds to upward (positive) and downward (negative) motion in the world. 
The green axis representing the world X-axis corresponds to left (positive) and right (negative) motion in the world, relative to the robot. 
The blue axis representing the world Y-axis corresponds to backward (positive) and forward (negative) motion in the world, relative to the robot. 
The overall position motion plan in the world frame was {{CHOICE: [sufficient, insufficient]}} to accomplish the task.
The change in the world Z-axis position was {{CHOICE: [sufficient, insufficient]}} with the estimated position because {{DESCRIPTION: describe the reasoning about the visual and position observations that to reach this conclusion, including incorrect sign of direction, magnitude of motion, or incorrect selection of motion axis altogether }}.
The change in the world X-axis position was {{CHOICE: [sufficient, insufficient]}} with the estimated position because {{DESCRIPTION: describe the reasoning about the visual and position observations that to reach this conclusion, including incorrect sign of direction, magnitude of motion, or incorrect selection of motion axis altogether }}.
The change in the world Y-axis position was {{CHOICE: [sufficient, insufficient]}} with the estimated position because {{DESCRIPTION: describe the reasoning about the visual and position observations that to reach this conclusion, including incorrect sign of direction, magnitude of motion, or incorrect selection of motion axis altogether }}.
The provided two-part image and change in position confirms the robot {{CHOICE: [was, was not]}} able to accomplish the task of {task} while grasping the {obj} becase {{DESCRIPTION: describe the visual (labeled axes in wrist and base frames) and position observations that explain and confirm or deny task completion}}.
If the task was incomplete, describe the task state: {{DESCRIPTION: describe the task state, partially completed, bad position, or complete failure, utilizing the provided details}}.

Proposed Changes to Motion Plan:
If the task is either fully completed or or if it is failed beyond recovery, then the task should be reset. Otherwise, the task is partially complete and/or can be corrected, and does not need to be reset.
Thus, the task {{CHOICE: [should, should not]}} be reset because {{DESCRIPTION: summarize the reasoning about observations to determine task completion }}
The positional motion plan {{CHOICE: [should, should not]}} be changed by {{DESCRIPTION: describe the changes to the motion plan, such as changing the directions or axes of motion}}.

Python Code with Updated Motion Plan after Reflection:
```python
# succinct text description of the positional motion reflection
position_motion_reflection = "{{DESCRIPTION: describe the task state, partially completed, bad position, or complete failure, utilizing the provided details}}"
# describe whether or not to reset the task (True/False) completely and whether it was a complete failure (False) or complete success (True). In the case of failure, the motion plan described will be executed only after the reset
reset_task_info = {{CHOICE: [True, False]}}
# the magnitude of motion across the motion direction axes [x, y ,z]
world_motion_magnitude = [{{PNUM: 0.0}}, {{PNUM: 0.0}}, {{PNUM: 0.0}}]
# the vector (sign of direction * magnitude) of motion across the motion direction axes [x, y ,z]
world_motion_vector = [{{NUM: 0.0}}, {{NUM: 0.0}}, {{NUM: 0.0}}]
```
[end of positional motion reflection]

Rules:
1. Replace all {{DESCRIPTION: ...}}, {{PNUM: ...}}, {{NUM: ...}}, and {{CHOICE}} entries with specific values or statements.
2. Always include motion for all three axes, even if it's "No motion required."
3. Keep the explanation concise but physically grounded. Prioritize interpretability and reproducibility.
4. Use common sense where exact properties are ambiguous, and explain assumptions.
5. Do not include any sections outside the start/end blocks or add non-specified bullet points.
6. Make sure to provide the final python code for each requested force in a code block.
7. Make sure to update and change the final motion plan according to the proposed changes in the reflection.
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