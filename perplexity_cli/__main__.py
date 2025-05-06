"""
Main entry point for the Perplexity CLI package.

This allows the package to be run as a module:
python -m perplexity_cli
"""

import sys
from perplexity_cli.cli import main

if __name__ == "__main__":
    sys.exit(main())
