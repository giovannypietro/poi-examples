# PoI Python SDK

[![PyPI version](https://badge.fury.io/py/poi-sdk.svg)](https://badge.fury.io/py/poi-sdk)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

> **From Permissions to Proof-of-Intent: A Python SDK for creating trustworthy AI agent transactions**

## 🚀 Quick Start

```bash
pip install poi-sdk
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

A PoI receipt is a cryptographically signed document that proves an agent's intent before taking action. It contains fields for agent identification, action details, target resources, declared objectives, risk context, and expiration times.

### 2. PoI Generator

Creates and cryptographically signs receipts using RSA or ECDSA algorithms. It can load private keys and certificates from files or generate temporary keys for development purposes.

### 3. PoI Validator

Verifies receipt authenticity and validity by checking cryptographic signatures, expiration times, and structural integrity. It supports both RSA and ECDSA signature verification.

## 🔧 Usage Examples

**📚 For comprehensive usage examples including basic usage, LangGraph integration, N8N workflows, and advanced patterns, see our [QUICKSTART Guide](QUICKSTART.md).**

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

The SDK supports configuration via environment variables for key paths, expiration times, risk thresholds, and signature algorithms.

### Configuration File

The SDK can load configuration from YAML files, with support for hierarchical configuration and environment variable overrides.

## 🧪 Testing

**💡 For testing your certificate setup and running examples, see our [QUICKSTART Guide](QUICKSTART.md).**

### Run Tests

The SDK includes a comprehensive test suite that can be run with pytest, including coverage reporting and specific test file execution.

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

The project includes development tools for code formatting, linting, type checking, and pre-commit hooks. See the [Contributing Guide](CONTRIBUTING.md) for detailed setup instructions.

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
2. **Follow** the [QUICKSTART Guide](QUICKSTART.md) for examples
3. **Integrate** with your agentic systems
4. **Join** the conversation about building trustworthy AI

This is just the beginning—your input will shape where we go next!
