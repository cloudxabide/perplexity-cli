"""
Setup script for the Perplexity CLI package.
"""

from setuptools import setup, find_packages
import re

# Read version from __init__.py
with open('perplexity_cli/__init__.py', 'r') as f:
    version_match = re.search(r"__version__\s*=\s*['\"]([^'\"]*)['\"]", f.read())
    if version_match:
        version = version_match.group(1)
    else:
        raise RuntimeError("Unable to find version string.")

# Read long description from README.md
with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name="perplexity-cli",
    version=version,
    author="cloudxabide",
    author_email="author@example.com",  # Replace with actual email
    description="A command-line interface for interacting with the Perplexity AI API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cloudxabide/perplexity-cli",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
    ],
    entry_points={
        "console_scripts": [
            "perplexity-cli=perplexity_cli.cli:main",
        ],
    },
)
