prompt_position_thinker = """
Given the user instruction and two-part image containing a wrist-image view on the left, a third-person view on the right, generate a structured physical plan for a robot end-effector interacting with the environment.
The task is to {task} while grasping the {obj}.

The robot is controlled using position and torque-based control, with access to contact feedback and 6D motion capabilities. 
Motions can include grasping, lifting, pushing, tapping, sliding, rotating, or any interaction with objects or surfaces.

Reason about the provided and implicit information in the images and task description to generate a structured plan for the robot's positional motion. Think about:
- Object geometry and contact points (from the image)
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

prompt_position_reflection = """
The robot has executed the initially provided motion plan, and now we need to analyze the ground-truth positional motion during this interaction.
The feedback is as follows: 
- a three-part image containing a wrist view with world-frame labeled axes on the left, third-person view in the middle, and a wrist view with wrist-frame labeled axes on the right
- the change in position relative to the wrist
- the change in position relative to the robot base, or the world frame
- The duration of the task

The goal is to analyze the robot's performance and modify the motion plan if necessary or to improve task performance:
- You should consider the visual feedback from the three-part image and the change in position to determine if the task was successful.
- Remember that as the robot moves, the labeled wrist-frame does not change, but the world-frame does. This is because motion is relative to the robot's wrist-frame, which is fixed to the robot, while the world-frame is fixed to the environment.
- Thus, refer to both the prior and current three-part images, which show world-frame axes before and after the robot's motion.
- A potential cause of inconsistency with the motion plan and task failure is that the initial motion plan was incorrect, particularly if the robot was not able to move in the desired direction.
- Refer to the world-frame axes labeled on the prior and current image to help map the ground-truth motion history in the world frame.
- Then, refer to the wrist-frame axes labeled on the prior image to map the ground-truth motion history from the world frame to ground-truth wrist motion relative to the prior wrist-frame.
- If this ground-truth motion history does not match the desired motion in the task, then the axes of motion may be incorrect.
- Note that some positional changes may be due to slip in the gripper, which can be observed visually and in the contact force history, and can be counteracted by increasing the grasping force. 
- However, make sure to not increase the grasping force too much, as this can cause damage to the object or gripper.
- After doing this analysis, you should be able to determine if the robot was able to accomplish the task of {task} while grasping the {obj} via close analysis of the provided feedback.
- If the robot and object moved in the correct direction and the forces relative to the prior wrist-frame were sufficient with the task, then the task was successful.
- You may not have had all the information about the scene and object for the initial plan. If possible, use the feedback and experience to better understand the physical properties of the object and environment.

Here are the results of the robot's interaction with the environment. 
{positional_motion_results}

[beginning of reflection]
Reflection on Task:
- The change in the world X-axis position corresponds to the prior wrist frame motion as such {{DESCRIPTION: describe the reasoning about the visual, position, and force observations that to map the world frame motion to the prior wrist frame's motion axes }}.
- The change in the world Y-axis position corresponds to the prior wrist frame motion as such {{DESCRIPTION: describe the reasoning about the visual, position, and force observations that to map the world frame motion to the prior wrist frame's motion axes }}.
- The change in the world Z-axis position corresponds to the prior wrist frame motion as such {{DESCRIPTION: describe the reasoning about the visual, position, and force observations that to map the world frame motion to the prior wrist frame's motion axes }}.
- The change in the prior wrist X-axis position was {{CHOICE: [sufficient, insufficient]}} with the estimated position because {{DESCRIPTION: describe the reasoning about the visual, position, and force observations that to reach this conclusion }}.
- The change in the prior wrist Y-axis position was {{CHOICE: [sufficient, insufficient]}} with the estimated position because {{DESCRIPTION: describe the reasoning about the visual, position, and force observations that to reach this conclusion }}.
- The change in the prior wrist Z-axis position was {{CHOICE: [sufficient, insufficient]}} with the estimated position because {{DESCRIPTION: describe the reasoning about the visual, position, and force observations that to reach this conclusion }}.
- The robot's wrist linear X-axis force was {{CHOICE: [sufficient, insufficient]}} with the estimated forces because {{DESCRIPTION: describe the reasoning about the visual, position, and force observations that to reach this conclusion }}.
- The robot's wrist linear Y-axis force was {{CHOICE: [sufficient, insufficient]}} with the estimated forces because {{DESCRIPTION: describe the reasoning about the visual, position, and force observations that to reach this conclusion }}.
- The robot's wrist linear Z-axis force was {{CHOICE: [sufficient, insufficient]}} with the estimated forces because {{DESCRIPTION: describe the reasoning about the visual, position, and force observations that to reach this conclusion }}.
- The robot's wrist angular X-axis torque was {{CHOICE: [sufficient, insufficient]}} with the estimated forces because {{DESCRIPTION: describe the reasoning about the visual, position, and force observations that to reach this conclusion }}.
- The robot's wrist angular Y-axis torque was {{CHOICE: [sufficient, insufficient]}} with the estimated forces because {{DESCRIPTION: describe the reasoning about the visual, position, and force observations that to reach this conclusion }}.
- The robot's wrist angular Z-axis torque was {{CHOICE: [sufficient, insufficient]}} with the estimated forces because {{DESCRIPTION: describe the reasoning about the visual, position, and force observations that to reach this conclusion }}.
- The robot's grasping force was {{CHOICE: [sufficient, insufficient}} with the estimated forces because {{DESCRIPTION: describe the reasoning about the visual, position, and force observations that to reach this conclusion }}.
- Based on the provided feedback, the object and surface properties are {{CHOICE: [consistent, inconsistent]}} with the estimated properties because {{DESCRIPTION: describe the reasoning about the visual, position, and force observations that to reach this conclusion }}.
- Thus, the object properties are {{DESCRIPTION: explicitly describe the object properties, such as mass, friction, and stiffness}}.
- Thus, the surface properties are {{DESCRIPTION: explicitly describe the surface properties, such as mass, friction, and stiffness}}.
- The provided three-part image and change in position confirms the robot {{CHOICE: [was, was not]}} able to accomplish the task of {task} while grasping the {obj}.
- This is because, based on the following observations: {{DESCRIPTION: describe the visual (labeled axes in wrist and base frames) and position observations that explain and confirm or deny task completion}}.
- If the task was incomplete, describe the task state: {{DESCRIPTION: describe the task state, partially completed, bad position, or complete failure, utilizing the provided details}}.
- The estimated task duration was {{CHOICE: [sufficient, insufficient]}} to complete the desired task
- The provided three-part image and change in position confirms the robot {{CHOICE: [was, was not]}} able to exert the estimated forces or move to the correct positions required to accomplish the task of {task} while grasping the {obj}.

Proposed Changes to Motion Plan:
- The task {{CHOICE: [is, is not]}} either fully completed or failed beyond recovery, so the task {{CHOICE: [should, should not]}} be reset to try again.
- The plan {{CHOICE: [is, is not]}} is partially incorrect or incomplete, thus the robot {{CHOICE: [should, should not]}} change the motion plan by {{DESCRIPTION: describe the changes to the motion plan, such as changing the direction of motion or adjusting the forces}}.
- The task duration should be {{CHOICE: [increased, decreased, no change]}} by {{NUM: 0.0}} because {{DESCRIPTION: brief concluding thought based on prior reasoning on reached position and forces applied}}
- The overall force and torque magnitudes should be {{CHOICE: [increased, decreased, no change]}} by {{NUM: 0.0}} because {{DESCRIPTION: brief concluding thought based on prior reasoning related to task completion given the motion plan}}
- The overall magnitude of motion to specified goal positions should be {{CHOICE: [increased, decreased, no change]}} by {{NUM: 0.0}} because {{DESCRIPTION: brief concluding thought based on prior reasoning related to task completion given the motion plan}}
- The wrist X-axis goal position should be {{CHOICE: [increased, decreased, no change]}} by {{NUM: 0.0}} because {{DESCRIPTION: brief concluding thought based on prior reasoning}}
- The wrist Y-axis goal position should be {{CHOICE: [increased, decreased, no change]}} by {{NUM: 0.0}} because {{DESCRIPTION: brief concluding thought based on prior reasoning}}
- The wrist Z-axis goal position should be {{CHOICE: [increased, decreased, no change]}} by {{NUM: 0.0}} because {{DESCRIPTION: brief concluding thought based on prior reasoning}}
- The wrist linear X-axis force should be {{CHOICE: [increased, decreased, no change]}} by {{NUM: 0.0}} because {{DESCRIPTION: brief concluding thought based on prior reasoning}}
- The wrist linear Y-axis force should be {{CHOICE: [increased, decreased, no change]}} by {{NUM: 0.0}} because {{DESCRIPTION: brief concluding thought based on prior reasoning}}
- The wrist linear Z-axis force should be {{CHOICE: [increased, decreased, no change]}} by {{NUM: 0.0}} because {{DESCRIPTION: brief concluding thought based on prior reasoning}}
- The wrist angular X-axis torque should be {{CHOICE: [increased, decreased, no change]}} by {{NUM: 0.0}} because {{DESCRIPTION: brief concluding thought based on prior reasoning}}
- The wrist angular Y-axis torque should be {{CHOICE: [increased, decreased, no change]}} by {{NUM: 0.0}} because {{DESCRIPTION: brief concluding thought based on prior reasoning}}
- The wrist angular Z-axis torque should be {{CHOICE: [increased, decreased, no change]}} by {{NUM: 0.0}} because {{DESCRIPTION: brief concluding thought based on prior reasoning}}
- The grasping force should be {{CHOICE: [increased, decreased, no change]}} by {{NUM: 0.0}} because {{DESCRIPTION: brief concluding thought based on prior reasoning}}

Python Code with Updated Motion Plan after Reflection:
```python
# describe whether or not to reset the task (True/False) completely and whether it was a complete failure (False) or complete success (True). In the case of failure, the motion plan described will be executed only after the reset
reset_task_info = [{{CHOICE: [True, False]}}, {{CHOICE: [True, False]}}]
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
[end of reflection]

Rules:
1. Replace all {{DESCRIPTION: ...}}, {{PNUM: ...}}, {{NUM: ...}}, and {{CHOICE}} entries with specific values or statements.
2. Use best physical reasoning based on known robot/environmental capabilities. Remember that the robot may have to exert forces in additional axes compared to the motion direction axes in order to maintain contacts between the object, robot, and environment.
3. Always include motion for all three axes, even if it's "No motion required."
4. Keep the explanation concise but physically grounded. Prioritize interpretability and reproducibility.
5. Use common sense where exact properties are ambiguous, and explain assumptions.
6. Do not include any sections outside the start/end blocks or add non-specified bullet points.
7. Make sure to provide the final python code for each requested force in a code block.
8. Make sure to update and change the final motion plan according to the proposed changes in the reflection.
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