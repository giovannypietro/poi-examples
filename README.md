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

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Install from PyPI

```bash
pip install poi-sdk
```

### Install from Source

```bash
git clone https://github.com/giovannypietro/poi.git
cd poi/python-sdk
pip install -e .
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

### Advanced Usage with Custom Fields

```python
from poi_sdk import PoIReceipt, PoIGenerator
from datetime import datetime, timedelta, timezone

generator = PoIGenerator()

# Custom receipt with additional context
receipt = generator.generate_receipt(
    agent_id="n8n_workflow_001",
    action="file_upload",
    target_resource="s3://bucket/documents/",
    declared_objective="Upload processed documents to cloud storage",
    risk_context="medium",
    additional_context={
        "workflow_id": "wf_123",
        "trigger_source": "webhook",
        "data_sensitivity": "internal"
    },
    expiration_time=(datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
)
```

### Batch Processing

```python
from poi_sdk import PoIGenerator, PoIValidator

generator = PoIGenerator()
validator = PoIValidator()

# Generate multiple receipts
receipts = []
actions = [
    ("database_read", "user_profiles", "Read user profile data"),
    ("api_call", "payment_gateway", "Process payment transaction"),
    ("file_access", "financial_reports", "Generate monthly report")
]

for action, resource, objective in actions:
    receipt = generator.generate_receipt(
        agent_id="multi_agent_system",
        action=action,
        target_resource=resource,
        declared_objective=objective
    )
    receipts.append(receipt)

# Validate all receipts
valid_receipts = []
for receipt in receipts:
    if validator.validate_receipt(receipt):
        valid_receipts.append(receipt)

print(f"Valid receipts: {len(valid_receipts)}/{len(receipts)}")
```

## 🔌 Integration Examples

### LangGraph Integration

```python
from langgraph.graph import StateGraph, END
from poi_sdk import PoIGenerator

class PoILangGraphState:
    def __init__(self):
        self.poi_generator = PoIGenerator()
        self.current_receipt = None

def generate_poi(state):
    """Generate PoI receipt before taking action"""
    receipt = state.poi_generator.generate_receipt(
        agent_id="langgraph_agent",
        action="llm_inference",
        target_resource="openai_api",
        declared_objective="Generate response to user query"
    )
    state.current_receipt = receipt
    return state

def take_action(state):
    """Take action with PoI receipt"""
    if state.current_receipt:
        print(f"Action taken with PoI receipt: {state.current_receipt.receipt_id}")
    return state

# Build workflow
workflow = StateGraph(PoILangGraphState)
workflow.add_node("generate_poi", generate_poi)
workflow.add_node("take_action", take_action)
workflow.add_edge("generate_poi", "take_action")
workflow.add_edge("take_action", END)

# Run workflow
app = workflow.compile()
result = app.invoke({})
```

### N8N Integration

```python
# N8N Python Code Node
from poi_sdk import PoIGenerator, PoIValidator
import json

def main():
    # Get input from previous node
    input_data = json.loads(input_data)
    
    # Initialize PoI
    generator = PoIGenerator()
    
    # Generate receipt for this workflow step
    receipt = generator.generate_receipt(
        agent_id="n8n_workflow",
        action=input_data.get("action", "unknown"),
        target_resource=input_data.get("resource", "unknown"),
        declared_objective=input_data.get("objective", "Workflow execution")
    )
    
    # Add receipt to output
    output = {
        "poi_receipt": receipt.to_dict(),
        "original_data": input_data,
        "timestamp": receipt.timestamp
    }
    
    return json.dumps(output)

# Execute
result = main()
```

### Custom Agent Framework

```python
from poi_sdk import PoIGenerator, PoIValidator
from typing import Dict, Any

class PoIAgent:
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.poi_generator = PoIGenerator()
        self.poi_validator = PoIValidator()
        self.action_history = []
    
    def execute_with_poi(self, action: str, resource: str, objective: str, **kwargs) -> Dict[str, Any]:
        """Execute action with Proof-of-Intent"""
        
        # Generate receipt
        receipt = self.poi_generator.generate_receipt(
            agent_id=self.agent_id,
            action=action,
            target_resource=resource,
            declared_objective=objective,
            **kwargs
        )
        
        # Execute action (your custom logic here)
        result = self._execute_action(action, resource, **kwargs)
        
        # Record action with receipt
        action_record = {
            "receipt": receipt,
            "result": result,
            "timestamp": receipt.timestamp
        }
        self.action_history.append(action_record)
        
        return action_record
    
    def _execute_action(self, action: str, resource: str, **kwargs):
        """Override this method with your custom action logic"""
        return {"status": "success", "action": action, "resource": resource}

# Usage
agent = PoIAgent("custom_agent_001")
result = agent.execute_with_poi(
    action="data_processing",
    resource="customer_database",
    objective="Process customer data for analytics"
)
```

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
