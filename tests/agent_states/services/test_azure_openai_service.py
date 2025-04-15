from pytest_mock import MockerFixture

from agent_states.services.azure_openai_service import (
    AzureOpenAIService,
    AzureOpenAIServiceEnv,
)


def test_get_model_with_key(mocker: MockerFixture):
    mocked_chat_openai = mocker.patch(
        "agent_states.services.azure_openai_service.AzureChatOpenAI"
    )
    svc = AzureOpenAIService(
        env=AzureOpenAIServiceEnv(
            azure_openai_endpoint="https://api.openai.com",
            azure_openai_api_key="test_key",
            azure_openai_api_version="2020-08-04",
            azure_openai_deployed_model_name="test_model",
        )
    )
    assert svc.get_model() is not None
    assert mocked_chat_openai.call_count == 1
    assert "azure_ad_token" not in mocked_chat_openai.call_args.kwargs
    assert "openai_api_key" in mocked_chat_openai.call_args.kwargs


def test_get_model_without_key(mocker: MockerFixture):
    mocked_chat_openai = mocker.patch(
        "agent_states.services.azure_openai_service.AzureChatOpenAI"
    )
    mocked_default_azure_credential = mocker.patch(
        "agent_states.services.azure_openai_service.DefaultAzureCredential"
    )
    svc = AzureOpenAIService(
        env=AzureOpenAIServiceEnv(
            azure_openai_endpoint="https://api.openai.com",
            azure_openai_api_version="2020-08-04",
            azure_openai_deployed_model_name="test_model",
        )
    )
    assert svc.get_model() is not None
    assert mocked_chat_openai.call_count == 1
    assert mocked_default_azure_credential.call_count == 1
    assert "azure_ad_token" in mocked_chat_openai.call_args.kwargs
