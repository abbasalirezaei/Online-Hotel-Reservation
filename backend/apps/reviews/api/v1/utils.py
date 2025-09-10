import json
from azure.core.credentials import AzureKeyCredential
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from django.conf import settings
from decouple import config


def _call_text_summarizer(prompt_messages):
    """
    Wrapper to call the Azure/GitHub inference endpoint configured via env.
    Expects prompt_messages: list of SystemMessage/UserMessage
    Returns parsed JSON if model returns JSON, otherwise raw text.
    """
    endpoint = getattr(
        settings, "AZURE_INFERENCE_ENDPOINT", "https://models.github.ai/inference"
    )
    model = getattr(settings, "AZURE_INFERENCE_MODEL", "xai/grok-3-mini")
    api_token = config("GITHUB_TOKEN")
    if not api_token:
        raise RuntimeError("Inference API token not configured")

    client = ChatCompletionsClient(
        endpoint=endpoint, credential=AzureKeyCredential(api_token)
    )
    resp = client.complete(
        messages=prompt_messages, model=model, temperature=0.2, top_p=1.0
    )
    content = resp.choices[0].message.content

    def validate_summary_output(data):
        required_keys = {"summary", "pros", "cons", "top_mentions"}
        return isinstance(data, dict) and required_keys.issubset(data.keys())

    try:
        parsed = json.loads(content)
        if validate_summary_output(parsed):
            return parsed
    except Exception:
        pass

    return {"text": content}
