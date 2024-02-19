import os
from typing import Type

from langchain_core.runnables import Runnable, RunnableParallel, RunnableLambda, chain

from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import HumanMessage

from pydantic import BaseModel

from game_utils import log
from controllers import controller_from_name

class Player:
    def __init__(
            self,
            name: str,
            controller: str,
            role: str,
            id: str = None,
            log_filepath: str = None
    ):
        self.name = name
        self.id = id

        if controller == "human":
            self.controller_type = "human"
        else:
            self.controller_type = "ai"

        self.controller = controller_from_name(controller)

        self.role = role
        self.messages = []

        self.log_filepath = log_filepath

        if log_filepath:
            player_info = {
                "id": self.id,
                "name": self.name,
                "role": self.role,
                "controller": {
                    "name": controller,
                    "type": self.controller_type
                }
            }
            log(player_info, log_filepath)

        # initialize the runnables
        self.generate = RunnableLambda(self._generate)
        self.format_output = RunnableLambda(self._output_formatter)

    async def respond_to(self, prompt: str, output_format: Type[BaseModel], max_retries=3):
        """Makes the player respond to a prompt. Returns the response in the specified format."""
        message = HumanMessage(content=prompt)
        output = await self.generate.ainvoke(message)
        if self.controller_type == "ai":
            retries = 0
            try:
                output = await self.format_output.ainvoke({"output_format": output_format})
            except ValueError as e:
                if retries < max_retries:
                    self.add_to_history(HumanMessage(content=f"Error formatting response: {e} \n\n Please try again."))
                    output = await self.format_output.ainvoke({"output_format": output_format})
                    retries += 1
                else:
                    raise e
        else:
            # Convert the human message to the pydantic object format
            field_name = output_format.model_fields.copy().popitem()[0]  # only works because current outputs have only 1 field
            output = output_format.model_validate({field_name: output.content})

        return output

    def add_to_history(self, message):
        self.messages.append(message)
        # log(message.model_dump_json(), self.log_filepath)

    def _generate(self, message: HumanMessage):
        """Entry point for the Runnable generating responses, automatically logs the message."""
        self.add_to_history(message)

        # AI's need to be fed the whole message history, but humans can just go back and look at it
        if self.controller_type == "human":
            response = self.controller.invoke(message.content)
        else:
            response = self.controller.invoke(self.messages)

        self.add_to_history(response)

        return response

    def _output_formatter(self, inputs: dict):
        """Formats the output of the response."""
        output_format: BaseModel = inputs["output_format"]

        prompt_template = PromptTemplate.from_template(
            "Please rewrite your previous response using the following format: \n\n{format_instructions}"
        )

        parser = PydanticOutputParser(pydantic_object=output_format)

        prompt = prompt_template.invoke({"format_instructions": parser.get_format_instructions()})

        message = HumanMessage(content=prompt.text)

        response = self.generate.invoke(message)

        return parser.invoke(response)
