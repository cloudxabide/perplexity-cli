# Perplexity CLI

A command-line interface for interacting with the Perplexity AI API.

## Installation

### From PyPI (recommended)

```bash
pip install perplexity-cli
```

### From Source

```bash
git clone https://github.com/cloudxabide/perplexity-cli.git
cd perplexity-cli
pip install -e .
```

## Configuration

Before using the CLI, you need to set up your Perplexity API key. You can do this in one of two ways:

1. Set an environment variable:

```bash
export PERPLEXITY_API_KEY="your-api-key"
```

2. Save the API key to the configuration file:

```bash
perplexity-cli --set-api-key "your-api-key"
```

You can also configure default settings:

```bash
# Set default model
perplexity-cli --set-default-model "sonar-pro"

# Set default max tokens
perplexity-cli --set-max-tokens 2000
```

## Usage

### List Available Models

```bash
perplexity-cli -l
```

### Send a Query

Using the default model:

```bash
perplexity-cli -q "What is the distance between the Sun and Earth?"
```

Using a specific model:

```bash
perplexity-cli -m sonar-pro -q "What is the distance between the Sun and Earth?"
```

### Advanced Options

Set maximum tokens for the response:

```bash
perplexity-cli -t 2000 -q "Explain quantum computing in detail"
```

Enable verbose output:

```bash
perplexity-cli -v -q "What is the distance between the Sun and Earth?"
```

Enable debug logging:

```bash
perplexity-cli -d -q "What is the distance between the Sun and Earth?"
```

## Available Models

As of May 2025, the following models are available:

- sonar-reasoning-pro
- sonar-reasoning
- sonar-pro
- sonar
- llama-3.1-sonar-small-128k-online
- llama-3.1-sonar-large-128k-online
- llama-3.1-sonar-huge-128k-online

For the most up-to-date list, visit: https://docs.perplexity.ai/guides/model-cards

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/cloudxabide/perplexity-cli.git
cd perplexity-cli

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
```

## License

MIT License

## Author

cloudxabide
