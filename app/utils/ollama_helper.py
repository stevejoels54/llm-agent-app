"""Ollama client helper functions"""
from openai import OpenAI
from .container_utils import is_running_in_container


def get_ollama_client():
    """
    Get configured Ollama client based on environment
    
    Returns:
        OpenAI: Configured OpenAI client pointing to Ollama
    """
    # Determine Ollama endpoint based on container status
    if is_running_in_container():
        ollama_api_endpoint = "http://ollama.ollama.svc.cluster.local:11434"
    else:
        ollama_api_endpoint = "http://localhost:11434"
    
    return OpenAI(
        base_url=ollama_api_endpoint + '/v1',
        api_key='forced_key',  # required, but unused
    )

