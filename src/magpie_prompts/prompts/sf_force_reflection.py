prompt_motion_reflection = """
The robot has executed the initially provided motion plan, and now we need to analyze the ground-truth positions and forces during this interaction.
The feedback is as follows: 
- a three-part image containing a wrist view with world-frame labeled axes on the left, third-person view in the middle, and a wrist view with wrist-frame labeled axes on the right
- the change in position relative to the wrist
- the change in position relative to the robot base, or the world frame
- The duration of the task
- A summary of the wrist wrenches downsampled to 2Hz
- A summary of the gripper contact forces downsampled to 2Hz

Remember that the force feedback is inverted from the applied forces, as the F/T sensor measures environmental forces reacting to the robot's motion.
As in, the robot applying a motion and force along a positive axis will result in a negative force reading from the F/T sensor, and vice-versa.
Remember that as the robot moves, the wrist-frame axes will change from the initial wrist-frame axes. 
Refer to the world-frame axes labeled on the left of the three-part images to help map the ground-truth motion history along original wrist-frame axes in the first three-part image.

Here are the results of the robot's interaction with the environment. 
{results}

[beginning of reflection]
Reflection on Task Completion:
- The provided three-part image and change in position confirms the robot {{CHOICE: [was, was not}} able to accomplish the task of {task} while grasping the {obj}.
- This is because, based on the following observations: {{DESCRIPTION: describe the visual (labeled axes in wrist and base frames) and position observations that explain and confirm or deny task completion}}.
- If the task was incomplete, describe the task state: {{DESCRIPTION: describe the task state, partially completed, bad position, or complete failure, utilizing the provided details}}.
- The estimated task duration was {{CHOICE: [sufficient, insufficient}} with the actual task duration.

Reflection on Motion:
- The provided two-part image and change in position confirms the robot {{CHOICE: [was, was not}} able to exert the estimated forces or move to the correct positions required to accomplish the task of {task} while grasping the {obj}.
- The change in position relative to the wrist was {{CHOICE: [consistent, inconsistent}} with the estimated position because {{DESCRIPTION: describe the reasoning about the visual, position, and force observations that to reach this conclusion }}.
- The change in the wrist X-axis position was {{CHOICE: [consistent, inconsistent}} with the estimated position because {{DESCRIPTION: describe the reasoning about the visual, position, and force observations that to reach this conclusion }}.
- The change in the wrist Y-axis position was {{CHOICE: [consistent, inconsistent}} with the estimated position because {{DESCRIPTION: describe the reasoning about the visual, position, and force observations that to reach this conclusion }}.
- The change in the wrist Z-axis position was {{CHOICE: [consistent, inconsistent}} with the estimated position because {{DESCRIPTION: describe the reasoning about the visual, position, and force observations that to reach this conclusion }}.
- The robot's wrist wrenches and gripper contact forces were {{CHOICE: [consistent, inconsistent}} with the estimated forces because {{DESCRIPTION: describe the reasoning about the visual, position, and force observations that confirm to reach this conclusion.}}
- The robot's wrist X-axis force was {{CHOICE: [consistent, inconsistent}} with the estimated forces because {{DESCRIPTION: describe the reasoning about the visual, position, and force observations that to reach this conclusion }}.
- The robot's wrist Y-axis force was {{CHOICE: [consistent, inconsistent}} with the estimated forces because {{DESCRIPTION: describe the reasoning about the visual, position, and force observations that to reach this conclusion }}.
- The robot's wrist Z-axis force was {{CHOICE: [consistent, inconsistent}} with the estimated forces because {{DESCRIPTION: describe the reasoning about the visual, position, and force observations that to reach this conclusion }}.
- The robot's grasping force was {{CHOICE: [consistent, inconsistent}} with the estimated forces because {{DESCRIPTION: describe the reasoning about the visual, position, and force observations that to reach this conclusion }}.

Proposed Changes to Motion Plan:
- The task {{CHOICE: [is, is not]}} either fully completed or failed beyond recovery, so the task {{CHOICE: [should, should not}} be reset to try again.
- The plan {{CHOICE: [is, is not]}} is partially incorrect or incomplete, thus the robot {{CHOICE: [should, should not}} change the motion plan by {{DESCRIPTION: describe the changes to the motion plan, such as changing the direction of motion or adjusting the forces}}.
- The wrist X-axis position should be {{CHOICE: [increased, decreased, no change]}} by {{NUM: 0.0}} because {{DESCRIPTIOn: brief concluding thought based on prior reasoning}}
- The wrist Y-axis position should be {{CHOICE: [increased, decreased, no change]}} by {{NUM: 0.0}} because {{DESCRIPTIOn: brief concluding thought based on prior reasoning}}
- The wrist Z-axis position should be {{CHOICE: [increased, decreased, no change]}} by {{NUM: 0.0}} because {{DESCRIPTIOn: brief concluding thought based on prior reasoning}}
- The wrist X-axis force should be {{CHOICE: [increased, decreased, no change]}} by {{NUM: 0.0}} because {{DESCRIPTIOn: brief concluding thought based on prior reasoning}}
- The wrist Y-axis force should be {{CHOICE: [increased, decreased, no change]}} by {{NUM: 0.0}} because {{DESCRIPTIOn: brief concluding thought based on prior reasoning}}
- The wrist Z-axis force should be {{CHOICE: [increased, decreased, no change]}} by {{NUM: 0.0}} because {{DESCRIPTIOn: brief concluding thought based on prior reasoning}}
- The grasping force should be {{CHOICE: [increased, decreased, no change]}} by {{NUM: 0.0}} because {{DESCRIPTIOn: brief concluding thought based on prior reasoning}}

Python Code with Updated Motion Plan after Reflection:
```python
# describe whether or not to reset the task completely and whether it was a complete failure (False) or complete success (True). In the case of failure, the motion plan described will be executed only after the reset
reset_task_info = [{{CHOICE: [True, False]}}, {{CHOICE: [True, False]}}]
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
[end of reflection]

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


# only to be used in conjunction with sf_force_thinker.py, after robot execution of initial robot plan
class PromptForceReflection(llm_prompt.LLMPrompt):
  """Prompt with both Motion Descriptor and Motion Coder."""

  def __init__(
      self,
  ):
    self.name = "LanguageAndVisionFeedback2ImprovedStructuredForceMotionParameters"

    self.num_llms = 1
    self.prompts = [prompt_motion_reflection]

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