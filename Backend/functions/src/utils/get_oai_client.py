import os
from openai import AzureOpenAI

def get_oai_client()-> AzureOpenAI:
    api_k = os.environ.get("AZURE_OPENAI_API_KEY")
    endp = os.environ.get("AZURE_OPENAI_ENDPOINT")
    api_ver = os.environ.get("AZURE_OPENAI_API_VERSION")
    if not api_k or not endp or not api_ver:
        raise ValueError("Azure open ai definitions are not set up")
    try:
        return AzureOpenAI(
            api_key=api_k,
            azure_endpoint=endp,
            api_version=api_ver
        )
    except Exception as e:
        raise ValueError(f"Failed to create AzureOpenAI client: {e}")
