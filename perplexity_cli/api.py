"""
API module for Perplexity CLI.

This module handles API calls to the Perplexity AI API.
"""

import json
import logging
import requests
from typing import Dict, Any

from perplexity_cli.config import get_api_key

# Configure logging
logger = logging.getLogger(__name__)

# Constants
BASE_URL = "https://api.perplexity.ai/chat/completions"


def call_api(model: str, max_tokens: int, query: str) -> Dict[str, Any]:
    """
    Submit an API call to the Perplexity.ai API endpoint.
    
    Args:
        model (str): The model to use for the query
        max_tokens (int): Maximum number of tokens for the response
        query (str): The query to send to the API
        
    Returns:
        Dict[str, Any]: The API response as a dictionary
        
    Raises:
        Exception: If the API call fails
    """
    api_key = get_api_key()
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are an AI assistant."},
            {"role": "user", "content": query}
        ],
        "max_tokens": max_tokens
    }

    try:
        logger.debug("Sending request to Perplexity AI API")
        response = requests.post(BASE_URL, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        if hasattr(e, 'response') and e.response:
            status_code = e.response.status_code
            error_text = e.response.text
            try:
                error_json = e.response.json()
                error_message = error_json.get('error', {}).get('message', error_text)
            except:
                error_message = error_text
                
            raise Exception(f"API call failed with status code {status_code}: {error_message}")
        else:
            raise Exception(f"API call failed: {str(e)}")


def parse_response(response: Dict[str, Any], verbose: bool = False) -> None:
    """
    Parse the API response into variables and print them.
    
    Args:
        response (Dict[str, Any]): The API response dictionary
        verbose (bool): Whether to print additional details
    """
    # Extract key parts of the response
    model_used = response.get("model", "N/A")
    choices = response.get("choices", [])
    usage = response.get("usage", {})

    # Print results with headers
    print("\n--- Model Used ---")
    print(model_used)

    print("\n--- Choices ---")
    for choice in choices:
        message = choice.get('message', {})
        content = message.get('content', 'N/A')
        print(f"{content}")
        
        # Print additional message details if verbose
        if verbose and 'tool_calls' in message:
            print("\n--- Tool Calls ---")
            for tool_call in message['tool_calls']:
                print(f"Tool: {tool_call.get('function', {}).get('name', 'N/A')}")
                print(f"Arguments: {tool_call.get('function', {}).get('arguments', 'N/A')}")

    print("\n--- Usage ---")
    for key, value in usage.items():
        print(f"{key}: {value}")
    
    if verbose:
        print("\n--- Full Response ---")
        print(json.dumps(response, indent=2))
