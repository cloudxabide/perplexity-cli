"""
Tests for the CLI module.
"""

import sys
from unittest import mock

import pytest

from perplexity_cli.cli import parse_args, main


def test_parse_args_defaults():
    """Test parsing arguments with defaults."""
    # Mock load_config to return empty dict
    with mock.patch('perplexity_cli.cli.load_config', return_value={}):
        # Call the function with no arguments
        args = parse_args([])
        
        # Check default values
        assert args.model == "sonar-pro"
        assert args.tokens == 4000
        assert not args.list_models
        assert args.query is None
        assert not args.verbose
        assert not args.debug
        assert args.set_api_key is None
        assert args.set_default_model is None
        assert args.set_max_tokens is None


def test_parse_args_custom():
    """Test parsing arguments with custom values."""
    # Mock load_config to return empty dict
    with mock.patch('perplexity_cli.cli.load_config', return_value={}):
        # Call the function with custom arguments
        args = parse_args([
            "-m", "sonar",
            "-t", "1000",
            "-q", "test query",
            "-v",
            "-d"
        ])
        
        # Check custom values
        assert args.model == "sonar"
        assert args.tokens == 1000
        assert not args.list_models
        assert args.query == "test query"
        assert args.verbose
        assert args.debug
        assert args.set_api_key is None
        assert args.set_default_model is None
        assert args.set_max_tokens is None


def test_parse_args_config():
    """Test parsing arguments with config values."""
    # Mock load_config to return custom values
    with mock.patch('perplexity_cli.cli.load_config', return_value={
        "default_model": "sonar",
        "max_tokens": "1000"
    }):
        # Call the function with no arguments
        args = parse_args([])
        
        # Check config values
        assert args.model == "sonar"
        assert args.tokens == 1000


@mock.patch('perplexity_cli.cli.save_config')
def test_main_set_config(mock_save_config):
    """Test main function with set config arguments."""
    # Call the function with set config arguments
    result = main(["--set-api-key", "test_key"])
    
    # Check that save_config was called
    mock_save_config.assert_called_once_with("test_key", None, None)
    # Check that the function returned 0
    assert result == 0


@mock.patch('perplexity_cli.cli.list_models')
def test_main_list_models(mock_list_models):
    """Test main function with list models argument."""
    # Call the function with list models argument
    result = main(["-l"])
    
    # Check that list_models was called
    mock_list_models.assert_called_once()
    # Check that the function returned 0
    assert result == 0


@mock.patch('perplexity_cli.cli.call_api')
@mock.patch('perplexity_cli.cli.parse_response')
def test_main_query(mock_parse_response, mock_call_api):
    """Test main function with query argument."""
    # Set up mocks
    mock_call_api.return_value = {"test": "response"}
    
    # Call the function with query argument
    result = main(["-q", "test query"])
    
    # Check that call_api was called
    mock_call_api.assert_called_once_with("sonar-pro", 4000, "test query")
    # Check that parse_response was called
    mock_parse_response.assert_called_once_with({"test": "response"}, False)
    # Check that the function returned 0
    assert result == 0


def test_main_no_query():
    """Test main function with no query argument."""
    # Call the function with no query argument
    result = main([])
    
    # Check that the function returned 1
    assert result == 1


def test_main_invalid_model():
    """Test main function with invalid model."""
    # Call the function with invalid model
    result = main(["-m", "invalid_model", "-q", "test query"])
    
    # Check that the function returned 1
    assert result == 1


@mock.patch('perplexity_cli.cli.call_api')
def test_main_api_error(mock_call_api):
    """Test main function with API error."""
    # Set up mocks
    mock_call_api.side_effect = Exception("API error")
    
    # Call the function with query argument
    result = main(["-q", "test query"])
    
    # Check that the function returned 1
    assert result == 1
