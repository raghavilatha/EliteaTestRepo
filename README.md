# EliteA Pipeline

Automated Confluence documentation generation from GitHub repositories using Claude AI.

## Quick Start

```bash
# Clone
git clone https://github.com/your-org/elitea-pipeline.git
cd elitea-pipeline

# Setup
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env with your tokens

# Run
python main.py --repo https://github.com/owner/repo --dry-run -v

## team

Service_owner = Raghavi,
business_impact=high.

## Requirements

- Python 3.9+
- GitHub Token
- Claude API Key
- (Optional) Confluence API Token

## Usage

```bash
python main.py --repo <URL> [OPTIONS]

Options:
  --repo TEXT         GitHub repository URL (required)
  --template TEXT     Template name (default: Technical-App-Manifest-v1)
  --space TEXT        Confluence space (default: DOC)
  --dry-run          Run without creating page
  --output TEXT      Save to file instead
  --update           Update existing page
  --verbose, -v      Enable debug logging
```

## Example

```bash
# Dry run
python main.py --repo https://github.com/facebook/react --dry-run -v

# Create in Confluence
python main.py --repo https://github.com/owner/repo -v

# Save to file
python main.py --repo https://github.com/owner/repo --output result.md
```

## Docker

```bash
docker build -t elitea .
docker run -e GITHUB_TOKEN=xxx -e CLAUDE_API_KEY=yyy elitea \
  --repo https://github.com/owner/repo --dry-run
```

## License

MIT


