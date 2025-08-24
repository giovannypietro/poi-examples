# Contributing to PoI SDK

Thank you for your interest in contributing to the Proof-of-Intent (PoI) SDK! This document provides guidelines and information for contributors.

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- pip or conda

### Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/poi.git
   cd poi
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install development dependencies**
   ```bash
   pip install -e ".[dev]"
   ```

4. **Install pre-commit hooks**
   ```bash
   pre-commit install
   ```

## 🧪 Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=poi_sdk --cov-report=html

# Run specific test file
pytest tests/test_receipt.py -v
```

## 📝 Code Style

We use several tools to maintain code quality:

- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting
- **mypy**: Type checking

### Formatting Code

```bash
# Format code with Black
black src/ tests/

# Sort imports with isort
isort src/ tests/

# Check code style
flake8 src/ tests/

# Type checking
mypy src/
```

## 🔧 Development Workflow

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow the coding standards
   - Add tests for new functionality
   - Update documentation as needed

3. **Run tests and checks**
   ```bash
   pytest
   flake8 src/ tests/
   mypy src/
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

5. **Push and create a pull request**
   ```bash
   git push origin feature/your-feature-name
   ```

## 📚 Documentation

- **README.md**: Main documentation and API reference
- **QUICKSTART.md**: Getting started guide
- **examples/**: Code examples and integration guides
- **docstrings**: Inline documentation for all classes and methods

### Adding Documentation

- Update docstrings for any new or modified functions/classes
- Add examples to the examples/ directory
- Update README.md if adding new features
- Include type hints for all function parameters and return values

## 🧪 Testing Guidelines

- **Test coverage**: Aim for at least 80% test coverage
- **Test types**: Include unit tests, integration tests, and edge cases
- **Test naming**: Use descriptive test names that explain what is being tested
- **Fixtures**: Use pytest fixtures for common test data and setup

### Example Test Structure

```python
def test_receipt_creation_with_valid_data():
    """Test that receipt creation works with valid input data."""
    receipt = PoIReceipt.create(
        agent_id="test_agent",
        action="test_action",
        target_resource="test_resource",
        declared_objective="Test objective"
    )
    
    assert receipt.agent_id == "test_agent"
    assert receipt.action == "test_action"
    assert receipt.receipt_id.startswith("poi_")
```

## 🐛 Bug Reports

When reporting bugs, please include:

- **Description**: Clear description of the bug
- **Steps to reproduce**: Detailed steps to reproduce the issue
- **Expected behavior**: What you expected to happen
- **Actual behavior**: What actually happened
- **Environment**: Python version, OS, SDK version
- **Code example**: Minimal code that reproduces the issue

## 💡 Feature Requests

For feature requests, please:

- **Describe the feature**: What functionality you'd like to see
- **Use case**: Explain why this feature would be useful
- **Implementation ideas**: If you have ideas on how to implement it
- **Examples**: Provide examples of how the feature would be used

## 🔒 Security

If you discover a security vulnerability, please:

- **DO NOT** open a public issue
- **DO** email security@example.com (replace with actual security contact)
- **DO** provide a detailed description of the vulnerability
- **DO** include steps to reproduce if possible

## 📋 Pull Request Guidelines

### Before submitting a PR:

1. **Ensure tests pass**: All tests should pass locally
2. **Check code style**: Run formatting and linting tools
3. **Update documentation**: Add/update docstrings and examples
4. **Add tests**: Include tests for new functionality
5. **Update CHANGELOG**: Document any user-facing changes

### PR Description should include:

- **Summary**: Brief description of changes
- **Motivation**: Why these changes are needed
- **Changes**: Detailed list of changes made
- **Testing**: How the changes were tested
- **Breaking changes**: Any breaking changes and migration steps

## 🏷️ Commit Message Format

We use conventional commit messages:

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, etc.)
- **refactor**: Code refactoring
- **test**: Adding or updating tests
- **chore**: Maintenance tasks

Examples:
```
feat: add support for ECDSA signatures
fix: resolve timestamp validation issue
docs: update API documentation
style: format code with Black
```

## 🤝 Code Review

All contributions require code review:

- **Be respectful**: Provide constructive feedback
- **Be thorough**: Review for functionality, style, and security
- **Be responsive**: Respond to review comments promptly
- **Be patient**: Code review takes time

## 📞 Getting Help

- **Issues**: Use GitHub issues for bug reports and feature requests
- **Discussions**: Use GitHub Discussions for questions and general discussion
- **Documentation**: Check README.md and examples/ first

## 🙏 Recognition

Contributors will be recognized in:

- **AUTHORS** file
- **GitHub contributors** page
- **Release notes** for significant contributions

Thank you for contributing to making AI agents more trustworthy and auditable!
