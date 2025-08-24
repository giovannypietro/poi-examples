# PoI SDK Repository Structure

This document provides an overview of the repository structure and organization.

## 📁 Root Directory

```
poi-examples/
├── .gitignore              # Git ignore rules
├── LICENSE                 # MIT License
├── README.md               # Main documentation and API reference
├── QUICKSTART.md           # Getting started guide
├── CHANGELOG.md            # Version history and changes
├── CONTRIBUTING.md         # Contribution guidelines
├── REPOSITORY_STRUCTURE.md # This file
├── pyproject.toml          # Modern Python project configuration
├── setup.py                # Legacy setup configuration
├── requirements.txt        # Python dependencies
├── poi_config_example.yaml # Example configuration file
└── demo.py                 # Simple demonstration script
```

## 📦 Source Code (`src/poi_sdk/`)

```
src/poi_sdk/
├── __init__.py             # Package initialization and exports
├── receipt.py              # Core PoIReceipt class
├── generator.py             # PoIGenerator for creating receipts
├── validator.py             # PoIValidator for receipt validation
├── config.py                # Configuration management
├── exceptions.py            # Custom exception classes
└── cli.py                  # Command-line interface
```

## 📚 Examples (`examples/`)

```
examples/
├── basic_usage.py          # Basic SDK functionality demonstration
└── langgraph_integration.py # LangGraph workflow integration example
```

## 🧪 Tests (`tests/`)

```
tests/
├── __init__.py             # Test package initialization
└── test_receipt.py         # Unit tests for PoIReceipt class
```

## 🔧 Configuration Files

- **`pyproject.toml`**: Modern Python project configuration with build system, dependencies, and tool configurations
- **`setup.py`**: Legacy setup configuration for backward compatibility
- **`requirements.txt`**: Python package dependencies
- **`poi_config_example.yaml`**: Example configuration file showing available options

## 📖 Documentation

- **`README.md`**: Comprehensive documentation, API reference, and usage examples
- **`QUICKSTART.md`**: Step-by-step getting started guide
- **`CONTRIBUTING.md`**: Guidelines for contributors
- **`CHANGELOG.md`**: Version history and changes
- **`REPOSITORY_STRUCTURE.md`**: This file explaining the repository organization

## 🚀 Getting Started

1. **Clone the repository**
   ```bash
   git clone https://github.com/giovannypietro/poi.git
   cd poi
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install the SDK**
   ```bash
   pip install -e .
   ```

4. **Try the examples**
   ```bash
   python demo.py
   python examples/basic_usage.py
   ```

## 🔍 Key Files Explained

### Core SDK Files
- **`src/poi_sdk/receipt.py`**: Main PoIReceipt class with all receipt functionality
- **`src/poi_sdk/generator.py`**: Handles receipt creation and cryptographic signing
- **`src/poi_sdk/validator.py`**: Manages receipt validation and verification
- **`src/poi_sdk/config.py`**: Configuration management with environment variables and YAML

### Example Files
- **`demo.py`**: Simple demonstration of core functionality
- **`examples/basic_usage.py`**: Comprehensive usage examples
- **`examples/langgraph_integration.py`**: LangGraph workflow integration

### Configuration Files
- **`pyproject.toml`**: Modern Python packaging configuration
- **`poi_config_example.yaml`**: Example configuration showing all available options

## 🎯 Development Workflow

1. **Make changes** in the `src/poi_sdk/` directory
2. **Add tests** in the `tests/` directory
3. **Update examples** if adding new features
4. **Update documentation** in markdown files
5. **Run tests** to ensure everything works
6. **Commit changes** with descriptive messages

## 📋 File Naming Conventions

- **Python files**: snake_case (e.g., `receipt.py`, `basic_usage.py`)
- **Configuration files**: kebab-case (e.g., `poi-config.yaml`)
- **Documentation**: kebab-case (e.g., `README.md`, `QUICKSTART.md`)
- **Test files**: `test_*.py` prefix

## 🔒 Security Considerations

- **Configuration files**: Never commit actual cryptographic keys
- **Environment variables**: Use for sensitive configuration
- **Example files**: Use dummy data for demonstrations
- **Dependencies**: Keep security-related packages updated

## 📚 Additional Resources

- **GitHub Issues**: For bug reports and feature requests
- **GitHub Discussions**: For questions and community discussion
- **Documentation**: Start with README.md and QUICKSTART.md
- **Examples**: Check the examples/ directory for usage patterns
