# PR Review Tool

A powerful CLI tool for analyzing GitHub pull requests with detailed review information, built with Python and following hexagonal architecture principles.

## Features

- 🔍 **Comprehensive PR Analysis**: Fetch pull requests, reviews, and comments
- 📊 **Rich Reports**: Console and Excel output with detailed metrics
- ⏱️ **Duration Tracking**: See how long PRs stayed open
- 👥 **Reviewer Information**: Track who reviewed each PR
- 📅 **Date Filtering**: Filter PRs by creation date range
- 🚀 **Async Performance**: Fast concurrent API calls
- 🏗️ **Clean Architecture**: Hexagonal architecture for maintainability

## Installation

### Option 1: Install from GitHub Packages (Recommended)

```bash
pip install pr-review-tool --index-url https://npm.pkg.github.com/yourusername
```

### Option 2: Install from PyPI

```bash
pip install pr-review-tool
```

### Option 3: Install from Source

```bash
git clone https://github.com/yourusername/pr-review-tool.git
cd pr-review-tool
pip install -e .
```

## Usage

### Basic Usage

```bash
# Console output
pr-review owner/repo

# Excel output
pr-review owner/repo --excel

# With authentication (recommended for large repos)
pr-review owner/repo --token <your_github_token>
```

### Advanced Usage

```bash
# Date range filtering
pr-review owner/repo --since 2024-01-01 --until 2024-12-31

# Custom Excel filename
pr-review owner/repo --excel --filename my_report.xlsx

# Complete example
pr-review freeCodeCamp/freeCodeCamp --token <token> --excel --since 2024-12-01 --until 2024-12-31
```

## Report Columns

The tool generates reports with the following information:

- **PR Title**: Title of the pull request
- **Author**: GitHub username of the PR author
- **State**: Current state (open/closed)
- **Created At**: Date when PR was created
- **Close Date**: Date when PR was closed (or "Still open")
- **Days Open**: Number of days the PR was open
- **Duration**: Human-readable duration (e.g., "2 weeks, 3 days")
- **# Reviews**: Number of reviews received
- **Reviewers**: List of reviewers (comma-separated)
- **# Review Comments**: Number of review comments
- **# PR Comments**: Number of general PR comments

## Authentication

For large repositories or to avoid rate limits, use a GitHub Personal Access Token:

1. Go to [GitHub Settings > Tokens](https://github.com/settings/tokens)
2. Generate a new token with `repo` scope
3. Use the token with the `--token` option

## Examples

### Analyze a Public Repository

```bash
pr-review tiangolo/typer --excel
```

### Analyze Your Private Repository

```bash
pr-review yourusername/your-repo --token ghp_your_token_here --excel
```

### Filter by Date Range

```bash
pr-review facebook/react --token <token> --since 2024-12-01 --until 2024-12-31
```

## Architecture

This tool follows hexagonal architecture principles:

- **Domain Layer**: Business logic and models
- **Application Layer**: Use case orchestration
- **Adapters**: CLI interface and GitHub API client
- **Ports**: Abstract interfaces for external dependencies

## Development

### Setup Development Environment

```bash
git clone https://github.com/yourusername/pr-review-tool.git
cd pr-review-tool
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e .
```

### Run Tests

```bash
pytest
```

### Build Package

```bash
python -m build
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

- 📧 Email: your.email@example.com
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/pr-review-tool/issues)
- 📖 Documentation: [GitHub Wiki](https://github.com/yourusername/pr-review-tool/wiki) 