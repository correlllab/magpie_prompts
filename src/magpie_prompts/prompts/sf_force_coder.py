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

class PromptMotionCoder(llm_prompt.LLMPrompt):
  """Prompt with both Motion Descriptor and Motion Coder."""

  def __init__(
      self,
      executor: safe_executor.SafeExecutor,
  ):
    # self._agent = client.agent()
    self._safe_executor = magpie_execution.MagpieSafeExecutor(executor)

    self.name = "LanguageAndVision2StructuredLang2GraspParameters"

    self.num_llms = 1
    self.prompts = [prompt_motion_coder]

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
