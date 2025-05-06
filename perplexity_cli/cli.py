"""
Command-line interface module for Perplexity CLI.

This module handles command-line argument parsing and execution.
"""

import sys
import logging
import argparse
from typing import List, Optional

from perplexity_cli import __version__
from perplexity_cli.config import load_config, save_config, DEFAULT_MODEL, DEFAULT_MAX_TOKENS
from perplexity_cli.models import list_models, AVAILABLE_MODELS
from perplexity_cli.api import call_api, parse_response

# Configure logging
logger = logging.getLogger(__name__)


def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """
    Parse command line arguments.
    
    Args:
        args (Optional[List[str]]): Command line arguments to parse
        
    Returns:
        argparse.Namespace: Parsed arguments
    """
    # Load config for default values
    config = load_config()
    default_model = config.get("default_model", DEFAULT_MODEL)
    default_max_tokens = int(config.get("max_tokens", DEFAULT_MAX_TOKENS))
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Perplexity AI CLI Client - Interact with Perplexity AI API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  List available models:
    %(prog)s -l
  
  Query using default model:
    %(prog)s -q "What is the distance between the Sun and Earth?"
  
  Query using specific model:
    %(prog)s -m sonar-pro -q "What is the distance between the Sun and Earth?"
  
  Set API key in config file:
    %(prog)s --set-api-key YOUR_API_KEY
  
  Set default model in config file:
    %(prog)s --set-default-model sonar-pro
        """
    )
    
    parser.add_argument("-t", "--tokens", type=int, default=default_max_tokens,
                        help=f"Maximum number of tokens (default: {default_max_tokens})")
    parser.add_argument("-m", "--model", type=str, default=default_model,
                        help=f"Model to use (default: {default_model})")
    parser.add_argument("-l", "--list-models", action="store_true",
                        help="List available models")
    parser.add_argument("-q", "--query", type=str,
                        help="Query to send to the API")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Enable verbose output")
    parser.add_argument("-d", "--debug", action="store_true",
                        help="Enable debug logging")
    parser.add_argument("--set-api-key", type=str,
                        help="Set API key in config file")
    parser.add_argument("--set-default-model", type=str,
                        help="Set default model in config file")
    parser.add_argument("--set-max-tokens", type=int,
                        help="Set default max tokens in config file")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    
    return parser.parse_args(args)


def main(args: Optional[List[str]] = None) -> int:
    """
    Main function to parse arguments and execute commands.
    
    Args:
        args (Optional[List[str]]): Command line arguments
        
    Returns:
        int: Exit code
    """
    # Configure basic logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # Parse arguments
    parsed_args = parse_args(args)
    
    # Set debug logging if requested
    if parsed_args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Debug logging enabled")
    
    # Handle configuration settings
    if parsed_args.set_api_key or parsed_args.set_default_model or parsed_args.set_max_tokens:
        save_config(parsed_args.set_api_key, parsed_args.set_default_model, parsed_args.set_max_tokens)
        return 0
    
    # List models if requested
    if parsed_args.list_models:
        list_models()
        return 0
    
    # Validate query parameter
    if not parsed_args.query:
        parser = argparse.ArgumentParser()
        parser.print_help()
        print("\nError: A query must be provided unless listing models (-l) or setting configuration.")
        return 1
    
    # Validate model parameter
    if parsed_args.model not in AVAILABLE_MODELS:
        print(f"Error: Invalid model '{parsed_args.model}'.")
        list_models()
        return 1
    
    try:
        # Call API and parse response
        response = call_api(parsed_args.model, parsed_args.tokens, parsed_args.query)
        parse_response(response, parsed_args.verbose)
        return 0
    except Exception as e:
        logger.error(str(e))
        return 1


if __name__ == "__main__":
    sys.exit(main())
