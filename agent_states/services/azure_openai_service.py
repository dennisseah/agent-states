from dataclasses import dataclass
from typing import Any

from azure.identity import DefaultAzureCredential
from lagom.environment import Env
from langchain_openai import AzureChatOpenAI

from agent_states.protocols.i_azure_openai_service import (
    IAzureOpenAIService,
)


class AzureOpenAIServiceEnv(Env):
    azure_openai_endpoint: str
    azure_openai_api_key: str | None = None
    azure_openai_api_version: str
    azure_openai_deployed_model_name: str


@dataclass
class AzureOpenAIService(IAzureOpenAIService):
    env: AzureOpenAIServiceEnv

    def get_model(self, temperature: float = 0.5) -> AzureChatOpenAI:
        params: dict[str, Any] = {
            "azure_endpoint": self.env.azure_openai_endpoint,
            "api_version": self.env.azure_openai_api_version,
            "model": self.env.azure_openai_deployed_model_name,
            "temperature": temperature,
        }

        if self.env.azure_openai_api_key is None:
            params["azure_ad_token"] = (
                DefaultAzureCredential()
                .get_token("https://cognitiveservices.azure.com/.default")
                .token
            )
        else:
            params["openai_api_key"] = self.env.azure_openai_api_key

        return AzureChatOpenAI(**params)
