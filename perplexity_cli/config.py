"""
Configuration module for Perplexity CLI.

This module handles loading and saving configuration settings.
"""

import os
import logging
import configparser
from pathlib import Path
from typing import Dict, Optional

# Configure logging
logger = logging.getLogger(__name__)

# Constants
CONFIG_FILE = Path.home() / ".perplexity_cli_config"
DEFAULT_MAX_TOKENS = 4000
DEFAULT_MODEL = "sonar-pro"

def load_config() -> Dict[str, str]:
    """
    Load configuration from config file if it exists.
    
    Returns:
        Dict[str, str]: Configuration dictionary
    """
    config = {}
    config_file = Path(CONFIG_FILE)
    
    if config_file.exists():
        try:
            parser = configparser.ConfigParser()
            parser.read(config_file)
            
            if "perplexity" in parser:
                if "api_key" in parser["perplexity"]:
                    config["api_key"] = parser["perplexity"]["api_key"]
                if "default_model" in parser["perplexity"]:
                    config["default_model"] = parser["perplexity"]["default_model"]
                if "max_tokens" in parser["perplexity"]:
                    config["max_tokens"] = parser["perplexity"]["max_tokens"]
            
            logger.debug("Loaded configuration from %s", config_file)
        except Exception as e:
            logger.warning("Failed to load config file: %s", e)
    
    return config


def get_api_key() -> str:
    """
    Get the Perplexity API key from environment variable or config file.
    
    Returns:
        str: The API key
        
    Raises:
        EnvironmentError: If API key is not found
    """
    # First try environment variable
    api_key = os.getenv("PERPLEXITY_API_KEY")
    
    # If not in environment, try config file
    if not api_key:
        config = load_config()
        api_key = config.get("api_key")
    
    # If still not found, raise error
    if not api_key:
        raise EnvironmentError(
            "PERPLEXITY_API_KEY environment variable not set and no API key found in config file.\n"
            "Please set the environment variable or create a config file at ~/.perplexity_cli_config"
        )
    
    return api_key


def save_config(api_key: Optional[str] = None, default_model: Optional[str] = None, 
               max_tokens: Optional[int] = None) -> None:
    """
    Save configuration to config file.
    
    Args:
        api_key (Optional[str]): API key to save
        default_model (Optional[str]): Default model to save
        max_tokens (Optional[int]): Default max tokens to save
    """
    config = configparser.ConfigParser()
    
    # Load existing config if it exists
    if Path(CONFIG_FILE).exists():
        config.read(CONFIG_FILE)
    
    # Ensure perplexity section exists
    if "perplexity" not in config:
        config["perplexity"] = {}
    
    # Update values if provided
    if api_key:
        config["perplexity"]["api_key"] = api_key
    if default_model:
        config["perplexity"]["default_model"] = default_model
    if max_tokens:
        config["perplexity"]["max_tokens"] = str(max_tokens)
    
    # Write config file
    try:
        with open(CONFIG_FILE, 'w') as f:
            config.write(f)
        os.chmod(CONFIG_FILE, 0o600)  # Set permissions to user read/write only
        print(f"Configuration saved to {CONFIG_FILE}")
    except Exception as e:
        logger.error("Failed to save config file: %s", e)
