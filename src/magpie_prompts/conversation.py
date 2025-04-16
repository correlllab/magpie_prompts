# Copyright 2023 DeepMind Technologies Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""A class which manages a chat session using a prompt."""

import time
from typing import Any

from openai import OpenAI

client = OpenAI()
# import termcolor

# from language_to_reward_2023.platforms import llm_prompt
# import llm_prompt
from magpie_prompts import llm_prompt

def _open_ai_call_with_retry(
    model: str, messages: list[Any]
):
  """Call OpenAI API with retry."""
  reset_trigger_phrases = ["CHOICE", "NUM"]
  success = False
  completion = None
  while not success:
    try:
      completion = client.chat.completions.create(model=model,
      messages=messages,
      temperature=0.3)
      success = True
      for reset_trigger_phrase in reset_trigger_phrases:
        if reset_trigger_phrase in completion.choices[0].message.content:
          success = False
    except Exception as e:  # pylint: disable=broad-exception-caught
      print("OpenAI API call issue, re-trying..." + str(e) + "\n")
      time.sleep(5)
  return completion

def openai_encode_image(image):
    '''
    @param image PIL image to convet to a base64 string for OpenAI API.
    '''
    import base64
    import io
    buffer = io.BytesIO()
    img = image.save(buffer, format="JPEG") # image is PIL image
    return base64.b64encode(buffer.getvalue()).decode("utf-8")

def build_messages(text=None, image=None, messages=[], model_type="gemini", role="user"):
    '''
    @param text (str): text to be sent to the model
    @param image (PIL.Image): image to be sent to the model
    '''
    if model_type == "gemini":
        if text is not None:
          messages.append(text)
        if image is not None:
          messages.append(image)
    elif model_type == "openai":
        content = []
        if text is not None:
            content_type = "input_text"
            if role != "user":
                content_type = "output_text"
            content.append({"type": content_type, "text": text})
        if image is not None:
            content.append({
                "type": "input_image",
                "image_url": f"data:image/jpeg;base64,{openai_encode_image(image)}",
            })
        message = {
            "role": role,
            "content": content
        }
        messages.append(message)
    return messages

def send_message(client, model, messages=[], model_type="gemini"):
    '''
    Sends a list of messages to the specified client and model.

    @param client: The initialized OpenAI or Gemini client.
    @param model (str): The model ID to use.
    @param messages (list): A list of message dictionaries (for OpenAI) or content parts (for Gemini).
    @param model_type (str): Either "openai" or "gemini".
    @return: The response from the model.
    '''
    text = ""
    if model_type == "gemini":
        response = client.models.generate_content(
            model=model,
            contents=messages,
        )
        text = response.text
    elif model_type == "openai":
        response = client.responses.create(
            model=model,
            input=messages,
        )
        text = response.output_text
    else:
        raise ValueError("Invalid model type. Choose either 'gemini' or 'openai'.")
    return text

class Conversation:
  """Manages the state of a conversation with a language model."""

  def __init__(
      self,
      prompt_model: llm_prompt.LLMPrompt,
      model: str,
      print_responses: bool = True,
      vision_model: bool = False,
  ):
    self._prompt_model = prompt_model
    self._model = model
    self._print_responses = print_responses
    number_of_llms = prompt_model.num_llms
    self._message_queues = [[] for _ in range(number_of_llms)]
    self._llm_responses = [None for _ in range(number_of_llms)]
    self._vision_model = vision_model
    # Add general prompt to the message queue.
    for llm_id in range(number_of_llms):
      message = [{"role": "user", "content": prompt_model.prompts[llm_id]}]
      self._message_queues[llm_id].append(message[0])

  def send_command(self, user_command: str, encoded_image=None, vision=False, debug=False) -> str:
    """Sends a user command to the LLMs, returns final processed response."""
    if user_command == "reset":
      self.reset()
      print("Resetting the conversation history.")
      return "reset"
    upstream_message = user_command + " Make sure to ignore irrelevant options."
    if self._vision_model and vision and encoded_image is not None:
      upstream_message = [
          {
            "type": "text",
            "text": f"{user_command} Make sure to ignore irrelevant options."
          },
          {
            "type": "image_url",
            "image_url": {
              "url": f"data:image/jpeg;base64,{encoded_image}"
            }
          }]
    for llm_id in range(self._prompt_model.num_llms):
      start = time.time()
      completion = _open_ai_call_with_retry(
          self._model,
          self._message_queues[llm_id]
          + [{"role": "user", "content": upstream_message}],
      )
      if debug:
        print(f"LLM{llm_id} took {time.time() - start:.2f}s")
      if self._prompt_model.keep_message_history[llm_id]:
        self._message_queues[llm_id].append(
            {"role": "user", "content": upstream_message}
        )
        self._message_queues[llm_id].append(completion.choices[0].message)
      print(f"LLM{llm_id} queried")
      response = completion.choices[0].message.content
      self._llm_responses[llm_id] = response
      if self._print_responses:
        # print(termcolor.colored(response + "\n", "cyan", attrs=["bold"]))
        print(response + "\n")
      try:
        upstream_message = self._prompt_model.response_processors[llm_id](
            response
        )
      except Exception:
        if self._prompt_model.keep_message_history[llm_id]:
          self._message_queues[llm_id].pop(-1)
          self._message_queues[llm_id].pop(-1)
        raise
    return upstream_message

  def reset(self) -> None:
    for i in range(self._prompt_model.num_llms):
      while len(self._message_queues[i]) > 1:
        self._message_queues[i].pop(-1)
