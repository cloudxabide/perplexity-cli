"""
Tests for the config module.
"""

import os
import tempfile
from unittest import mock
from pathlib import Path

import pytest

from perplexity_cli.config import load_config, get_api_key, save_config


@mock.patch('perplexity_cli.config.CONFIG_FILE')
def test_load_config_file_not_exists(mock_config_file):
    """Test loading config when file doesn't exist."""
    # Set mock to a non-existent file
    mock_config_file.exists.return_value = False
    
    # Call the function
    config = load_config()
    
    # Check that an empty dict is returned
    assert config == {}


@mock.patch('perplexity_cli.config.CONFIG_FILE')
def test_load_config_file_exists(mock_config_file, tmp_path):
    """Test loading config when file exists."""
    # Create a temporary config file
    config_file = tmp_path / "config"
    with open(config_file, 'w') as f:
        f.write("[perplexity]\n")
        f.write("api_key = test_key\n")
        f.write("default_model = test_model\n")
        f.write("max_tokens = 1000\n")
    
    # Set mock to use our temporary file
    mock_config_file.exists.return_value = True
    mock_config_file.return_value = config_file
    
    # Mock configparser to read our file
    with mock.patch('configparser.ConfigParser.read') as mock_read:
        def side_effect(file_path):
            parser = mock.MagicMock()
            parser.__contains__.return_value = True
            parser.__getitem__.return_value = {
                "api_key": "test_key",
                "default_model": "test_model",
                "max_tokens": "1000"
            }
            return parser
        
        mock_read.side_effect = side_effect
        
        # Call the function
        config = load_config()
    
    # Check that the config is loaded correctly
    assert config == {
        "api_key": "test_key",
        "default_model": "test_model",
        "max_tokens": "1000"
    }


@mock.patch('os.getenv')
@mock.patch('perplexity_cli.config.load_config')
def test_get_api_key_from_env(mock_load_config, mock_getenv):
    """Test getting API key from environment variable."""
    # Set up mocks
    mock_getenv.return_value = "test_key_from_env"
    
    # Call the function
    api_key = get_api_key()
    
    # Check that the API key is from the environment
    assert api_key == "test_key_from_env"
    # Check that load_config was not called
    mock_load_config.assert_not_called()


@mock.patch('os.getenv')
@mock.patch('perplexity_cli.config.load_config')
def test_get_api_key_from_config(mock_load_config, mock_getenv):
    """Test getting API key from config file."""
    # Set up mocks
    mock_getenv.return_value = None
    mock_load_config.return_value = {"api_key": "test_key_from_config"}
    
    # Call the function
    api_key = get_api_key()
    
    # Check that the API key is from the config
    assert api_key == "test_key_from_config"
    # Check that load_config was called
    mock_load_config.assert_called_once()


@mock.patch('os.getenv')
@mock.patch('perplexity_cli.config.load_config')
def test_get_api_key_not_found(mock_load_config, mock_getenv):
    """Test getting API key when not found."""
    # Set up mocks
    mock_getenv.return_value = None
    mock_load_config.return_value = {}
    
    # Call the function and check that it raises an error
    with pytest.raises(EnvironmentError):
        get_api_key()


@mock.patch('perplexity_cli.config.CONFIG_FILE')
def test_save_config(mock_config_file, tmp_path):
    """Test saving config."""
    # Create a temporary config file
    config_file = tmp_path / "config"
    
    # Set mock to use our temporary file
    mock_config_file.return_value = config_file
    
    # Call the function
    save_config(api_key="new_key", default_model="new_model", max_tokens=2000)
    
    # Check that the config file was created
    assert config_file.exists()
    
    # Check the contents of the config file
    config = configparser.ConfigParser()
    config.read(config_file)
    
    assert "perplexity" in config
    assert config["perplexity"]["api_key"] == "new_key"
    assert config["perplexity"]["default_model"] == "new_model"
    assert config["perplexity"]["max_tokens"] == "2000"
