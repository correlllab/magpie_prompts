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
- After doing this analysis, you should be able to determine if the robot was able to accomplish the task via close analysis of the provided feedback.
- Modify the required forces, torques, positions, and task duration to improve the robot's performance. If it is safe and appropriate to do so, try to speed up the task.  
- Given the observed position motion, time duration, and average force and torque applied, reassess whether the original physical estimates and equation-based computations of motion based upon the prescribed equations of motion were sufficient to explain the result. 
- In the case of inconsistency or incompletion, update any properties that may have been over- or under-estimated (such as mass, surface friction, hinge stiffness, or rotational inertia). Often times there will be multiple confounding and related variables, such as mass and friction. 
- Consider either computation in which the only mass should be adjusted or only the friction should be adjusted. Then, using your physical and visual reasoning about your knowledge of the environment, estimate the new values of the physical properties, which will probably be between either extreme of only changing friction or mass.
- In cases where there is large error, you may have to drastically change the estimates of the physical properties of the object and surface and/or the forces required.
- Then recompute the forces and torques required to accomplish the task, and update the motion plan accordingly.
- Note that there will always be some noise in the wrench data and position data resulting from real-world motion and contact. 

The left image is labeled with the axes of motion relative to the base frame of the robot, as in the canonical world-axes (for example, the red positive Z-axis will always represent upward direction in the world).
The right image is a third-person view of the robot, which may be used to help with the mapping of the axes and understanding the environment
Use the provided image data and physical reasoning to carefully reason about the requisite motion and forces in the world frame to accomplish the task.
Reason about the provided and implicit information in the images, feedback, and desired task behavior to modify or create a structured plan for the robot's motion. 
Think about object and environment geometry, material, contact points, and physical properties (friction, dynamics, degrees of freedom) obtained from the image and prior knowledge

[beginning of reflection]
The task is to {task} while grasping the {obj}.

Assessing Object-Centric Motion in the World Frame:
The provided images in the two-part image confirm {{DESCRIPTION: the object and environment in the image and their properties, such as color, shape, and material, and their correspondence to completion of the requested task}}.
The blue axis representing the world Z-axis corresponds to upward and downward motion in the world. 
The change in the world Z-axis position was {{CHOICE: [correct, incorrect]}} relative to the estimated position goal because {{DESCRIPTION: describe the reasoning about the visual, position, and force observations that to reach this conclusion }}.
The red axis representing the world X-axis corresponds to left and right motion in the world, relative to the robot. 
The change in the world X-axis position was {{CHOICE: [correct, incorrect]}} relative to the estimated position goal because {{DESCRIPTION: describe the reasoning about the visual, position, and force observations that to reach this conclusion }}.
The green axis representing the world Y-axis corresponds to backward and forward motion in the world, relative to the robot. 
The change in the world Y-axis position was {{CHOICE: [correct, incorrect]}} relative to the estimated position goal because {{DESCRIPTION: describe the reasoning about the visual, position, and force observations that to reach this conclusion }}.
To complete the task, the object should additionally {{DESCRIPTION: the object's required motion in the world frame to complete the task, if required}}.

The robot {{CHOICE: [was, was not]}} able to accomplish the task because {{DESCRIPTION: succinctly describe the reasoning about visual, positional, and force/torque feedback that confirms or denies task completion}}.
If the task was incomplete, describe the task state: {{DESCRIPTION: describe the task state, partially completed, bad position, or complete failure, utilizing the provided details}}.
The estimated task duration was {{CHOICE: [sufficient, insufficient]}} to complete the desired task.

Proposed Changes to Motion Plan:
- The task {{CHOICE: [is, is not]}} either fully completed or failed beyond recovery, so the task {{CHOICE: [should, should not]}} be reset to try again.
- The plan {{CHOICE: [is, is not]}} is partially incorrect or incomplete, thus the robot {{CHOICE: [should, should not]}} change the motion plan by {{DESCRIPTION: describe the changes to the motion plan, such as changing the direction and/or magnitudes of positional and/or force/torque goals}}.
- The world X-axis goal position should be {{CHOICE: [increased, decreased, no change]}} by {{NUM}} because {{DESCRIPTION: describe the reasoning about the visual, position, and force observations that to reach this conclusion}}
- The world Y-axis goal position should be {{CHOICE: [increased, decreased, no change]}} by {{NUM}} because {{DESCRIPTION: describe the reasoning about the visual, position, and force observations that to reach this conclusion}}
- The world Z-axis goal position should be {{CHOICE: [increased, decreased, no change]}} by {{NUM}} because {{DESCRIPTION: describe the reasoning about the visual, position, and force observations that to reach this conclusion}}
- The new task duration should be {{CHOICE: [increased, decreased, no change]}} by {{NUM}} because {{DESCRIPTION: describe the additional time required, if at all, to complete the task given the prior motion and new motion plan}}

Recomputing Physical Model and Force Plan :
The previous motion plan, using the physical property estimates of {{DESCRIPTION: describe the previously estimated object and surface properties}} computed the motion plan using the following equations of motion to model the task {{DESCRIPTION: redescribe in full the equations of motion used to compute the task previously and their results}}.
Now, recomputing these computations using the provided true ground-truth position change, the updated position plan, the updated task duration, and average net forces and torques, {{DESCRIPTION: recompute the same motion and equations with the ground truth information about net forces and position change, which should yield information on the object properties like mass and friction}}
Based off what was and was not understood about the various physical properties, the previously estimated physical properties of the object and surface are approximately {{DESCRIPTION: describe the updated estimates for the physical properties such as mass and friction based off of the ground-truth information and understanding of the properties from previous visual and semantic cues}}.
To accomplish the task, using the updated physical properties, the forces and motion required are {{DESCRIPTION: fully describe the computations for motion using the ground truth data}}.

Proposed Changes to Motion Plan:
- The world linear X-axis force should be {{CHOICE: [increased, decreased, no change]}} by {{NUM}} because {{DESCRIPTION: describe the reasoning about the visual, position, and force observations that to reach this conclusion}}
- The world linear Y-axis force should be {{CHOICE: [increased, decreased, no change]}} by {{NUM}} because {{DESCRIPTION: describe the reasoning about the visual, position, and force observations that to reach this conclusion}}
- The world linear Z-axis force should be {{CHOICE: [increased, decreased, no change]}} by {{NUM}} because {{DESCRIPTION: describe the reasoning about the visual, position, and force observations that to reach this conclusion}}
- The world angular X-axis torque should be {{CHOICE: [increased, decreased, no change]}} by {{NUM}} because {{DESCRIPTION: describe the reasoning about the visual, position, and force observations that to reach this conclusion}}
- The world angular Y-axis torque should be {{CHOICE: [increased, decreased, no change]}} by {{NUM}} because {{DESCRIPTION: describe the reasoning about the visual, position, and force observations that to reach this conclusion}}
- The world angular Z-axis torque should be {{CHOICE: [increased, decreased, no change]}} by {{NUM}} because {{DESCRIPTION: describe the reasoning about the visual, position, and force observations that to reach this conclusion}}
- The grasping force should be {{CHOICE: [increased, decreased, no change]}} by {{NUM}} because {{DESCRIPTION: describe the reasoning about the visual, position, and force observations that to reach this conclusion}}

Python Code with Updated Motion Plan after Reflection:
```python
# succinct text description of the motion plan along the world axes
world_motion_reflection = "{{DESCRIPTION: describe succinctly the reasoning about visual, positional, and forces/torque feedback that explains task completion and the proposed changes}}"
# boolean flag on whether to reset the task
reset_task = {{CHOICE: [True, False]}}
# the vector (sign of direction * magnitude) of relative motion across the motion direction axes [x, y ,z] (relative as in additional motion required to accomplish the task from prior motion)
world_motion_vector = [{{NUM}}, {{NUM}}, {{NUM}}]
# the vector (sign of direction * magnitude) of the forces and torques along the [x, y, z, rx, ry, rz] axes
ft_vector = [{{NUM}}, {{NUM}}, {{NUM}}, {{NUM}}, {{NUM}}, {{NUM}}]
# the grasping force, which must be positive
grasp_force = {{PNUM}}
# the task duration, which must be positive
duration = {{PNUM}}
```

[end of motion reflection]

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
9. If the task is either fully completed or failed beyond recovery, the task should be reset to try again. The motion plan should be updated to reflect starting from the beginning of the task.
"""

scraps = '''
Here are the results of the robot's interaction with the environment. 
{motion_report}

Human Feedback: {human_feedback}

# succinct text description, updated with reflection over feedback, of the explicit estimated physical properties of the object, including mass, material, friction coefficients, etc.
property_description = "{{DESCRIPTION: describe succinctly the object and its properties}}"
# describe the motion along the [x, y, z] axes as either positive, negative, or no motion
world_motion_direction = [{{CHOICE: [-1, 0, 1]}}, {{CHOICE: [-1, 0, 1]}}, {{CHOICE: [-1, 0, 1]}}]
# the magnitude of motion across the motion direction axes [x, y ,z]
world_motion_magnitude = [{{PNUM}}, {{PNUM}}, {{PNUM}}]
# succinct text description of the planned forces and torques on the object in the world frame
ft_description = "{{DESCRIPTION: describe succinctly the forces and torques required in the world frame to accomplish the task}}"
# the magnitudes of the forces and torques along the [x, y, z, rx, ry, rz] axes
ft_magnitude = [{{PNUM}}, {{PNUM}}, {{PNUM}}, {{PNUM}}, {{PNUM}}, {{PNUM}}]

The robot is controlled using position and torque-based control, with access to contact feedback and 6D motion capabilities. 
Motions can include grasping, lifting, pushing, tapping, sliding, rotating, or any interaction with objects or surfaces.

The force applied along the linear X-axis force was {{CHOICE: [correct, incorrect]}} relative to the estimated forces because {{DESCRIPTION: describe the reasoning about the visual, position, and force observations that to reach this conclusion }}.
The force applied along the linear Y-axis force was {{CHOICE: [correct, incorrect]}} relative to the estimated forces because {{DESCRIPTION: describe the reasoning about the visual, position, and force observations that to reach this conclusion }}.
The force applied along the linear Z-axis force was {{CHOICE: [correct, incorrect]}} relative to the estimated forces because {{DESCRIPTION: describe the reasoning about the visual, position, and force observations that to reach this conclusion }}.
The torque applied about the angular X-axis torque was {{CHOICE: [correct, incorrect]}} relative to the estimated torque because {{DESCRIPTION: describe the reasoning about the visual, position, and force observations that to reach this conclusion }}.
The torque applied about the angular Y-axis torque was {{CHOICE: [correct, incorrect]}} relative to the estimated torque because {{DESCRIPTION: describe the reasoning about the visual, position, and force observations that to reach this conclusion }}.
The torque applied about the angular Z-axis torque was {{CHOICE: [correct, incorrect]}} relative to the estimated torque because {{DESCRIPTION: describe the reasoning about the visual, position, and force observations that to reach this conclusion }}.
The robot's grasping force was {{CHOICE: [sufficient, insufficient]}} with the estimated forces because {{DESCRIPTION: describe the reasoning about the visual, position, and force observations that to reach this conclusion }}.
'''

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