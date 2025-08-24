# PoI Python SDK

[![PyPI version](https://badge.fury.io/py/poi-sdk.svg)](https://badge.fury.io/py/poi-sdk)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

> **From Permissions to Proof-of-Intent: A Python SDK for creating trustworthy AI agent transactions**

## 🚀 Quick Start

```bash
pip install poi-sdk
```

```python
from poi_sdk import PoIReceipt, PoIGenerator, PoIValidator

# Generate a proof of intent
generator = PoIGenerator()
receipt = generator.generate_receipt(
    agent_id="agent_123",
    action="database_query",
    target_resource="user_data",
    declared_objective="Fetch user profile for authentication"
)

# Validate a proof of intent
validator = PoIValidator()
is_valid = validator.validate_receipt(receipt)
print(f"Receipt valid: {is_valid}")
```

**📚 For detailed setup instructions, examples, and troubleshooting, see our [QUICKSTART Guide](QUICKSTART.md).**

## 📖 What is Proof-of-Intent (PoI)?

Proof-of-Intent (PoI) is a cryptographic framework that moves beyond traditional IAM by providing **provable trust** for AI agents. Instead of just asking "Does this agent have permission?", PoI answers "Why is it doing this, right now, on whose behalf, and with what justification?"

### Key Benefits

- 🔐 **Cryptographic Proof**: Tamper-evident receipts for every privileged action
- 🎯 **Intent Transparency**: Clear declaration of agent objectives and justifications
- 🔗 **Agent Lineage**: Complete chain of responsibility from human to sub-agents
- ⏰ **Temporal Security**: Time-boxed permissions with expiration
- 📋 **Audit Trail**: Immutable records for compliance and security

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Intent        │    │   Receipt       │    │   Verification  │
│   Declaration   │───▶│   Generation    │───▶│   & Audit       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🛠️ Installation

**📚 For complete installation instructions, prerequisites, and setup steps, see our [QUICKSTART Guide](QUICKSTART.md).**

```bash
pip install poi-sdk
```

## 📚 Core Concepts

### 1. PoI Receipt

A PoI receipt is a cryptographically signed document that proves an agent's intent before taking action:

```python
from poi_sdk import PoIReceipt

receipt = PoIReceipt(
    receipt_id="receipt_abc123",
    timestamp="2024-01-15T10:30:00Z",
    agent_id="agent_123",
    action="database_query",
    target_resource="user_data",
    declared_objective="Fetch user profile for authentication",
    risk_context="low",
    expiration_time="2024-01-15T11:30:00Z"
)
```

### 2. PoI Generator

Creates and cryptographically signs receipts:

```python
from poi_sdk import PoIGenerator

generator = PoIGenerator(
    private_key_path="path/to/private_key.pem",
    certificate_path="path/to/certificate.pem"
)

receipt = generator.generate_receipt(
    agent_id="agent_123",
    action="database_query",
    target_resource="user_data",
    declared_objective="Fetch user profile for authentication"
)
```

### 3. PoI Validator

Verifies receipt authenticity and validity:

```python
from poi_sdk import PoIValidator

validator = PoIValidator(
    public_key_path="path/to/public_key.pem",
    certificate_path="path/to/certificate.pem"
)

is_valid = validator.validate_receipt(receipt)
if is_valid:
    print("Receipt is valid and authentic")
else:
    print("Receipt validation failed")
```

## 🔧 Usage Examples

### Basic Usage

```python
from poi_sdk import PoIGenerator, PoIValidator

# Initialize
generator = PoIGenerator()
validator = PoIValidator()

# Generate receipt
receipt = generator.generate_receipt(
    agent_id="langchain_agent_001",
    action="api_call",
    target_resource="https://api.example.com/users",
    declared_objective="Retrieve user information for customer support"
)

# Validate receipt
is_valid = validator.validate_receipt(receipt)
print(f"Receipt valid: {is_valid}")
```

**💡 For more examples including LangGraph integration, N8N workflows, and advanced usage patterns, see our [QUICKSTART Guide](QUICKSTART.md).**

## 🔌 Integration Examples

**📚 For detailed integration examples with LangGraph, N8N, and custom agent frameworks, see our [QUICKSTART Guide](QUICKSTART.md).**

## 🔐 Security Features

### Cryptographic Signatures

- **RSA/ECDSA Support**: Multiple signature algorithms
- **Certificate-based**: X.509 certificate validation
- **Tamper Detection**: Any modification invalidates signatures

### Agent Lineage Binding

- **Chain of Trust**: Complete agent hierarchy tracking
- **Parent-Child Relationships**: Sub-agent accountability
- **Signature Inheritance**: Capability delegation with proof

### Temporal Security

- **Expiration Times**: Time-boxed permissions
- **Clock Skew Protection**: Tolerance for time differences
- **Replay Attack Prevention**: One-time use receipts

## 📋 Configuration

**💡 For detailed configuration instructions including certificate generation and environment setup, see our [QUICKSTART Guide](QUICKSTART.md).**

### Environment Variables

```bash
# PoI Configuration
POI_PRIVATE_KEY_PATH=/path/to/private_key.pem
POI_CERTIFICATE_PATH=/path/to/certificate.pem
POI_PUBLIC_KEY_PATH=/path/to/public_key.pem
POI_DEFAULT_EXPIRATION_HOURS=1
POI_RISK_THRESHOLD=medium
```

### Configuration File

```yaml
# poi_config.yaml
poi:
  keys:
    private_key_path: /path/to/private_key.pem
    certificate_path: /path/to/certificate.pem
    public_key_path: /path/to/public_key.pem
  
  defaults:
    expiration_hours: 1
    risk_threshold: medium
    signature_algorithm: rsa
  
  validation:
    clock_skew_tolerance_seconds: 300
    require_certificate_validation: true
```

## 🧪 Testing

**💡 For testing your certificate setup and running examples, see our [QUICKSTART Guide](QUICKSTART.md).**

### Run Tests

```bash
# Install test dependencies
pip install -e ".[test]"

# Run all tests
pytest

# Run with coverage
pytest --cov=poi_sdk --cov-report=html

# Run specific test file
pytest tests/test_generator.py
```

### Test Examples

```python
import pytest
from poi_sdk import PoIGenerator, PoIValidator

def test_basic_receipt_generation():
    generator = PoIGenerator()
    receipt = generator.generate_receipt(
        agent_id="test_agent",
        action="test_action",
        target_resource="test_resource",
        declared_objective="Test objective"
    )
    
    assert receipt.agent_id == "test_agent"
    assert receipt.action == "test_action"
    assert receipt.receipt_id is not None

def test_receipt_validation():
    generator = PoIGenerator()
    validator = PoIValidator()
    
    receipt = generator.generate_receipt(
        agent_id="test_agent",
        action="test_action",
        target_resource="test_resource",
        declared_objective="Test objective"
    )
    
    assert validator.validate_receipt(receipt) == True
```

## 📚 API Reference

### Core Classes

#### `PoIReceipt`

Main receipt class containing all intent information.

**Attributes:**
- `receipt_id`: Unique identifier for the receipt
- `timestamp`: Creation timestamp (ISO 8601)
- `agent_id`: Identifier of the agent taking action
- `action`: Type of action being performed
- `target_resource`: Resource being accessed
- `declared_objective`: Stated purpose of the action
- `risk_context`: Risk level assessment
- `expiration_time`: When the receipt expires
- `signature`: Cryptographic signature

**Methods:**
- `to_dict()`: Convert to dictionary
- `to_json()`: Convert to JSON string
- `is_expired()`: Check if receipt has expired

#### `PoIGenerator`

Generates and signs PoI receipts.

**Methods:**
- `generate_receipt(**kwargs)`: Create new receipt
- `sign_receipt(receipt)`: Cryptographically sign receipt
- `validate_receipt_structure(receipt)`: Validate receipt format

#### `PoIValidator`

Validates receipt authenticity and validity.

**Methods:**
- `validate_receipt(receipt)`: Validate receipt signature and format
- `verify_signature(receipt)`: Verify cryptographic signature
- `check_expiration(receipt)`: Check if receipt is expired

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Clone repository
git clone https://github.com/giovannypietro/poi.git
cd poi/python-sdk

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Code Style

- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting
- **mypy**: Type checking

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

Thanks to all contributors who are helping build a more trustworthy AI future. See the [AUTHORS](AUTHORS) file for a complete list of contributors.

## 🔗 Links

- **GitHub Repository**: [https://github.com/giovannypietro/poi](https://github.com/giovannypietro/poi)
- **Documentation**: [https://poi-sdk.readthedocs.io](https://poi-sdk.readthedocs.io)
- **PyPI Package**: [https://pypi.org/project/poi-sdk](https://pypi.org/project/poi-sdk)
- **Issues**: [https://github.com/giovannypietro/poi/issues](https://github.com/giovannypietro/poi/issues)
- **Discussions**: [https://github.com/giovannypietro/poi/discussions](https://github.com/giovannypietro/poi/discussions)

---

**Ready to build provable trust for your AI agents?**

1. **Install** the SDK: `pip install poi-sdk`
2. **Try** the quick start examples
3. **Integrate** with your agentic systems
4. **Join** the conversation about building trustworthy AI

This is just the beginning—your input will shape where we go next!
