prompt_motion_reflection = """
The robot has executed the initially provided motion plan, and now we need to analyze the ground-truth positions and forces during this interaction.
The feedback is as follows: 
- a three-part image containing a wrist view with world-frame labeled axes on the left, third-person view in the middle, and a wrist view with wrist-frame labeled axes on the right
- the change in position relative to the wrist
- the change in position relative to the robot base, or the world frame
- The duration of the task
- A summary of the wrenches in the base-frame downsampled to 2Hz
- A summary of the wrist wrenches downsampled to 2Hz
- A summary of the gripper contact forces downsampled to 2Hz
- Optionally, human feedback on the robot's performance, which takes priority over the robot's feedback
The task was to {task} while grasping the {obj}.

The goal is to analyze the robot's performance, given the feedback, and modify the motion plan if necessary or to improve task performance:
- You should consider the visual feedback from the three-part image, the change in position, and the forces to determine if the task was successful.
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
- Modify the required forces, torques, positions, and task duration to improve the robot's performance. If it is safe and appropriate to do so, try to speed up the task.  

Here are the results of the robot's interaction with the environment. 
{motion_report}

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

prompt_base_frame_reflector = """
The robot has executed the initially provided motion plan, and now we need to analyze the ground-truth positions and forces during this interaction.
The feedback is as follows: 
-Two two-part images each containing a wrist-image view on the left, a third-person view on the right. One is from prior to the robot's motion and the other is from after the robot's motion.
- the change in position relative to the wrist
- the change in position relative to the robot base, or the world frame
- The duration of the task
- A summary of the wrenches in the base-frame downsampled to 2Hz
- A summary of the wrist wrenches downsampled to 2Hz
- A summary of the gripper contact forces downsampled to 2Hz
- Optionally, human feedback on the robot's performance, which takes priority over the robot's feedback

The task was to {task} while grasping the {obj}.

The goal is to analyze the robot's performance, given the feedback, and modify the motion plan if necessary or to improve task performance:
- You should consider the visual feedback from the two-part image, the change in position, the forces, and potentially and especially the human feedback to determine if the task was successful.
- A potential cause of inconsistency with the motion plan and task failure is that the initial motion plan was incorrect, particularly if the robot was not able to move in the desired direction.
- Refer to the world-frame axes labeled on the prior and current image to help map the ground-truth motion history in the world frame.
- Note that some positional changes may be due to slip in the gripper, which can be observed visually and in the contact force history, and can be counteracted by increasing the grasping force. 
- After doing this analysis, you should be able to determine if the robot was able to accomplish the task of {task} while grasping the {obj} via close analysis of the provided feedback.
- Modify the required forces, torques, positions, and task duration to improve the robot's performance. If it is safe and appropriate to do so, try to speed up the task.  

The robot is controlled using position and torque-based control, with access to contact feedback and 6D motion capabilities. 
Motions can include grasping, lifting, pushing, tapping, sliding, rotating, or any interaction with objects or surfaces.

Reason about the provided and implicit information in the images, feedback, and desired task behavior to modify or create a structured plan for the robot's motion. Think about:
- Object geometry and contact points (from the image)
- Prior knowledge of object material types and mass estimates
- Force/torque sensing at the wrist
- Environmental knowledge (table, gravity, hinge resistance, etc.)

The left image is labeled with the axes of motion relative to the base frame of the robot, as in the canonical world-axes (for example, the red positive Z-axis will always represent upward direction in the world).
The right image is a third-person view of the robot, which may be used to help with the mapping of the axes and understanding the environment
Use the provided image data and physical reasoning to carefully map the true motion in the world frame to accomplish the task.
We want to reason about forces and torques relative to the world frame.

[start of motion plan]
The task is to {task} while grasping the {obj}.

Understanding Object-Centric Motion in the World Frame:
The provided images in the two-part image confirm {{DESCRIPTION: the object and environment in the image and their properties, such as color, shape, and material, and their correspondence to the requested task}}.
The red axis representing the world Z-axis corresponds to upward and downward motion in the world. 
To complete the task, the object in the image should have {{CHOICE: [upward, downward, no]}} linear motion along the Z-axis with magnitude {{PNUM}} meters.
The green axis representing the world X-axis corresponds to left and right motion in the world, relative to the robot. 
To complete the task, the object in the image should have {{CHOICE: [leftward, rightward, no]}} linear motion along the X-axis with magnitude {{PNUM}} meters.
The blue axis representing the world Y-axis corresponds to backward and forward motion in the world, relative to the robot. 
To complete the task, the object in the image should have {{CHOICE: [backward, forward, no]}} linear motion along the Y-axis with magnitude {{PNUM}} meters.
To accomplish the task in the world frame, the object must be moved {{DESCRIPTION: the object's required motion in the world frame to accomplish the task}}.

Understanding Robot-Applied Forces and Torques to Move Object in the World Frame:
To estimate the forces and torques required to accomplish {task} while grasping the {obj}, we must consider the following:
- The relevant object is {{DESCRIPTION: describe the object and its properties}} has mass {{NUM}} kg and, with the robot gripper, has a static friction coefficient of {{NUM}}.
- The surface of interaction is {{DESCRIPTION: describe the surface and its properties}} has a static friction coefficient of {{NUM}} with the object.
- Object Properties: {{DESCRIPTION: estimated mass, material, stiffness, friction coefficient, if object is articulated, do the same reasoning for whatever joint / degree of freedom enables motion}}.
- Environmental Factors: {{DESCRIPTION: consideration of various environmental factors in task like gravity, surface friction, damping, hinge resistance}}.
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
- Force/torque motion computations with object of mass {{NUM}} kg and static friction coefficient of {{NUM}} along the surface: {{DESCRIPTION: for the derived or estimated motion, compute the surface friction using appropriate formulae and quantities}}.

Force/Torque Motion Estimation:
Linear X-axis:  To complete the task and based upon {{DESCRIPTION: reasoning about and estimation of task physical properties}}, the object in the image must exert {{CHOICE: [leftward and positive, rightward and negative, no]}} force along the X-axis with magnitude {{PNUM}} N.
Linear Y-axis:  To complete the task and based upon {{DESCRIPTION: reasoning about and estimation of task physical properties}}, the object in the image must exert {{CHOICE: [backward and positive, forward and negative, no]}} force along the Y-axis with magnitude {{PNUM}} N.
Linear Z-axis:  To complete the task and based upon {{DESCRIPTION: reasoning about and estimation of task physical properties}}, the object in the image must exert {{CHOICE: linear [upward and positive, downward and negative, no]}} force along the Z-axis with magnitude {{PNUM}} N.
Angular X-axis: To complete the task and based upon {{DESCRIPTION: reasoning about and estimation of task physical properties}}, the object in the image must exert {{CHOICE: angular [counterclockwise and positive, clockwise and negative, no]}} torque about the X-axis with magnitude {{PNUM}} N-m.
Angular Y-axis: To complete the task and based upon {{DESCRIPTION: reasoning about and estimation of task physical properties}}, the object in the image must exert {{CHOICE: angular [counterclockwise and positive, clockwise and negative, no]}} torque about the Y-axis with magnitude {{PNUM}} N-m.
Angular Z-axis: To complete the task and based upon {{DESCRIPTION: reasoning about and estimation of task physical properties}}, the object in the image must exert {{CHOICE: angular [counterclockwise and positive, clockwise and negative, no]}} torque about the Z-axis with magnitude {{PNUM}} N-m.
Grasping force:  {{DESCRIPTION: estimated force range and justification based on friction, mass, resistance}}, thus {{PNUM}} to {{PNUM}} N .


Python Code with Final Motion Plan:
```python
# succinct text description of the motion plan along the world axes
world_motion_description = "{{DESCRIPTION: the object's required position motion in the world frame to accomplish the task}}"
# describe the motion along the [x, y, z] axes as either positive, negative, or no motion
world_motion_direction = [{{CHOICE: [-1, 0, 1]}}, {{CHOICE: [-1, 0, 1]}}, {{CHOICE: [-1, 0, 1]}}]
# the magnitude of motion across the motion direction axes [x, y ,z]
world_motion_magnitude = [{{PNUM}}, {{PNUM}}, {{PNUM}}]
# the vector (sign of direction * magnitude) of motion across the motion direction axes [x, y ,z]
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
0. The human feedback, if provided, takes priority over the robot's feedback. Use the human feedback to guide your analysis of the provided robot data and tailor the updated motion plan to the human's feedback.
1. Replace all {{DESCRIPTION: ...}}, {{PNUM}}, {{NUM}}, and {{CHOICE: ...}} entries with specific values or statements. For example, {{PNUM}} should be replaced with a number like 0.5. This is very important for downstream parsing!!
2. Use best physical reasoning based on known robot/environmental capabilities. Remember that the robot may have to exert forces in additional axes compared to the motion direction axes in order to maintain contacts between the object, robot, and environment.
3. Always include motion for all axes of motion, even if it's "No motion required."
4. Keep the explanation concise but physically grounded. Prioritize interpretability and reproducibility.
5. Use common sense where exact properties are ambiguous, and explain assumptions.
6. Do not include any sections outside the start/end blocks or add non-specified bullet points.
7. Make sure to provide the final python code for each requested force in a code block. Remember to fully replace the placeholder text with the actual values!
8. Do not abbreviate the prompt when generating the response. Fully reproduce the template, but filled in with your reasoning.
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