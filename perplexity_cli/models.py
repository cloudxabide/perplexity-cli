"""
Models module for Perplexity CLI.

This module contains information about available Perplexity AI models.
"""

# List of available models (as of May 2025)
# Reference: https://docs.perplexity.ai/guides/model-cards
AVAILABLE_MODELS = [
    "sonar-reasoning-pro",
    "sonar-reasoning",
    "sonar-pro", 
    "sonar",
    "llama-3.1-sonar-small-128k-online",
    "llama-3.1-sonar-large-128k-online",
    "llama-3.1-sonar-huge-128k-online"
]


def list_models() -> None:
    """
    Display a list of the available models.
    """
    print("\nAvailable Perplexity AI models:")
    print("-------------------------------")
    for model in AVAILABLE_MODELS:
        print(f"- {model}")
    print("\nNote: This list is maintained within the script and not dynamically retrieved from Perplexity AI.")
    print("For the most up-to-date list, visit: https://docs.perplexity.ai/guides/model-cards")
