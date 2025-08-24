# PoI Python SDK

[![PyPI version](https://badge.fury.io/py/poi-sdk.svg)](https://badge.fury.io/py/poi-sdk)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

> **From Permissions to Proof-of-Intent: A Python SDK for creating trustworthy AI agent transactions**

**📚 For detailed setup instructions, examples, and troubleshooting, see our [QUICKSTART Guide](QUICKSTART.md).**

## What is Proof-of-Intent (PoI)?

Proof-of-Intent (PoI) is a cryptographic framework that moves beyond traditional IAM by providing **provable trust** for AI agents. Instead of just asking "Does this agent have permission?", PoI answers "Why is it doing this, right now, on whose behalf, and with what justification?" PoI also creates an end to end agent lineage that is auditable.

### Key Benefits

- **Cryptographic Proof**: Tamper-evident receipts for every privileged action
- **Intent Transparency**: Clear declaration of agent objectives and justifications
- **Agent Lineage**: Complete chain of responsibility from human to sub-agents
- **Temporal Security**: Time-boxed permissions with expiration
- **Audit Trail**: Immutable records for compliance and security

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Intent        │    │   Receipt       │    │   Verification  │
│   Declaration   │───▶│   Generation    │───▶│   & Audit       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Installation

**📚 For complete installation instructions, prerequisites, and setup steps, see our [QUICKSTART Guide](QUICKSTART.md).**

### Quick Install

```bash
pip install poi-sdk
```

**🎉 Package now available on [PyPI](https://pypi.org/project/poi-sdk/)!**
`
##  Core Concepts

### 1. PoI Receipt

A PoI receipt is a cryptographically signed document that proves an agent's intent before taking action. It contains fields for agent identification, action details, target resources, declared objectives, risk context, and expiration times.

### 2. PoI Generator

Creates and cryptographically signs receipts using RSA or ECDSA algorithms. It can load private keys and certificates from files or generate temporary keys for development purposes.

### 3. PoI Validator

Verifies receipt authenticity and validity by checking cryptographic signatures, expiration times, and structural integrity. It supports both RSA and ECDSA signature verification.

## Usage Examples

**📚 For comprehensive usage examples including basic usage, LangGraph integration, N8N workflows, and advanced patterns, see our [QUICKSTART Guide](QUICKSTART.md).**

### Agent Lineage Binding

- **Chain of Trust**: Complete agent hierarchy tracking
- **Parent-Child Relationships**: Sub-agent accountability
- **Signature Inheritance**: Capability delegation with proof

### Temporal Security

- **Expiration Times**: Time-boxed permissions
- **Clock Skew Protection**: Tolerance for time differences
- **Replay Attack Prevention**: One-time use receipts

## API Reference

**📚 For detailed API documentation, method signatures, and examples, see our [QUICKSTART Guide](QUICKSTART.md).**

The SDK provides three core classes:

- **`PoIReceipt`**: Main receipt class with all intent information
- **`PoIGenerator`**: Creates and cryptographically signs receipts
- **`PoIValidator`**: Verifies receipt authenticity and validity

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

Thanks to all contributors who are helping build a more trustworthy AI future. See the [AUTHORS](AUTHORS) file for a complete list of contributors.

## 🔗 Links

- **GitHub Repository**: [https://github.com/giovannypietro/poi](https://github.com/giovannypietro/poi)
- **PyPI Package**: [https://pypi.org/project/poi-sdk](https://pypi.org/project/poi-sdk)
- **Issues**: [https://github.com/giovannypietro/poi/issues](https://github.com/giovannypietro/poi/issues)
- **Discussions**: [https://github.com/giovannypietro/poi/discussions](https://github.com/giovannypietro/poi/discussions)

---

**Ready to build provable trust for your AI agents?**

1. **🚀 Install** the SDK: `pip install poi-sdk`
2. **📚 Follow** the [QUICKSTART Guide](QUICKSTART.md) for examples
3. **🔗 Integrate** with your agentic systems
4. **🌟 Join** the conversation about building trustworthy AI

**🎉 The PoI package is now live on [PyPI](https://pypi.org/project/poi-sdk/)!**

This is just the beginning—your input will shape where we go next!
