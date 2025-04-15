from typing import Protocol

from langchain_openai import AzureChatOpenAI


class IAzureOpenAIService(Protocol):
    def get_model(self, temperature: float = 0.5) -> AzureChatOpenAI:
        """
        Return the Azure OpenAI model with the given temperature.

        The parameters for constructing the model are read from the environment
        variables.

        :param temperature: The temperature to use for the model.
        :return: The Azure OpenAI model with the given temperature
        """
        ...
