"""
Tests for the API module.
"""

import json
from unittest import mock

import pytest
import requests

from perplexity_cli.api import call_api, parse_response


@mock.patch('perplexity_cli.api.get_api_key')
@mock.patch('requests.post')
def test_call_api_success(mock_post, mock_get_api_key):
    """Test successful API call."""
    # Set up mocks
    mock_get_api_key.return_value = "test_key"
    mock_response = mock.MagicMock()
    mock_response.json.return_value = {"test": "response"}
    mock_post.return_value = mock_response
    
    # Call the function
    response = call_api("sonar-pro", 1000, "test query")
    
    # Check that the API key was retrieved
    mock_get_api_key.assert_called_once()
    
    # Check that requests.post was called with the correct arguments
    mock_post.assert_called_once()
    args, kwargs = mock_post.call_args
    assert args[0] == "https://api.perplexity.ai/chat/completions"
    assert kwargs["headers"]["Authorization"] == "Bearer test_key"
    assert kwargs["json"]["model"] == "sonar-pro"
    assert kwargs["json"]["max_tokens"] == 1000
    assert kwargs["json"]["messages"][1]["content"] == "test query"
    
    # Check that the response was returned
    assert response == {"test": "response"}


@mock.patch('perplexity_cli.api.get_api_key')
@mock.patch('requests.post')
def test_call_api_error(mock_post, mock_get_api_key):
    """Test API call with error."""
    # Set up mocks
    mock_get_api_key.return_value = "test_key"
    mock_response = mock.MagicMock()
    mock_response.status_code = 400
    mock_response.text = "Error message"
    mock_response.json.return_value = {"error": {"message": "API error"}}
    mock_post.side_effect = requests.exceptions.RequestException(response=mock_response)
    
    # Call the function and check that it raises an exception
    with pytest.raises(Exception) as excinfo:
        call_api("sonar-pro", 1000, "test query")
    
    # Check the exception message
    assert "API call failed with status code 400: API error" in str(excinfo.value)


@mock.patch('builtins.print')
def test_parse_response_basic(mock_print):
    """Test parsing a basic API response."""
    # Create a test response
    response = {
        "model": "sonar-pro",
        "choices": [
            {
                "message": {
                    "content": "Test content"
                }
            }
        ],
        "usage": {
            "prompt_tokens": 10,
            "completion_tokens": 20,
            "total_tokens": 30
        }
    }
    
    # Call the function
    parse_response(response)
    
    # Check that print was called with the correct arguments
    assert mock_print.call_count >= 6
    # Check that the model was printed
    assert any("sonar-pro" in args[0] for args, _ in mock_print.call_args_list)
    # Check that the content was printed
    assert any("Test content" in args[0] for args, _ in mock_print.call_args_list)
    # Check that the usage was printed
    assert any("prompt_tokens" in args[0] for args, _ in mock_print.call_args_list)


@mock.patch('builtins.print')
def test_parse_response_verbose(mock_print):
    """Test parsing an API response with verbose output."""
    # Create a test response
    response = {
        "model": "sonar-pro",
        "choices": [
            {
                "message": {
                    "content": "Test content",
                    "tool_calls": [
                        {
                            "function": {
                                "name": "test_function",
                                "arguments": "test_arguments"
                            }
                        }
                    ]
                }
            }
        ],
        "usage": {
            "prompt_tokens": 10,
            "completion_tokens": 20,
            "total_tokens": 30
        }
    }
    
    # Call the function with verbose=True
    parse_response(response, verbose=True)
    
    # Check that print was called with the correct arguments
    assert mock_print.call_count >= 10
    # Check that the tool calls were printed
    assert any("Tool Calls" in args[0] for args, _ in mock_print.call_args_list)
    assert any("test_function" in args[0] for args, _ in mock_print.call_args_list)
    # Check that the full response was printed
    assert any("Full Response" in args[0] for args, _ in mock_print.call_args_list)
