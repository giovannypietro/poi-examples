# PoI SDK Quick Start Guide

Get up and running with the Proof-of-Intent SDK in under 5 minutes!

## 🚀 Installation

```bash
pip install poi-sdk
```

## 📝 Your First PoI Receipt

### 1. Basic Example

```python
from poi_sdk import PoIGenerator, PoIValidator

# Create a generator
generator = PoIGenerator()

# Generate your first receipt
receipt = generator.generate_receipt(
    agent_id="my_first_agent",
    action="data_read",
    target_resource="user_database",
    declared_objective="Read user profile for authentication"
)

print(f"Generated receipt: {receipt.receipt_id}")
```

### 2. Validate the Receipt

```python
# Create a validator
validator = PoIValidator()

# Check if receipt is valid
is_valid = validator.validate_receipt(receipt)
print(f"Receipt valid: {is_valid}")
```

## Common Use Cases

### Database Access

```python
receipt = generator.generate_receipt(
    agent_id="db_agent",
    action="database_query",
    target_resource="customer_records",
    declared_objective="Fetch customer data for billing",
    risk_context="medium"
)
```

### API Calls

```python
receipt = generator.generate_receipt(
    agent_id="api_agent",
    action="http_request",
    target_resource="https://api.payment.com/transactions",
    declared_objective="Process payment transaction",
    risk_context="high"
)
```

### File Operations

```python
receipt = generator.generate_receipt(
    agent_id="file_agent",
    action="file_read",
    target_resource="/var/log/system.log",
    declared_objective="Analyze system performance",
    risk_context="low"
)
```

## Integration Examples

### LangGraph

```python
from langgraph.graph import StateGraph, END
from poi_sdk import PoIGenerator

def generate_poi(state):
    generator = PoIGenerator()
    receipt = generator.generate_receipt(
        agent_id="langgraph_agent",
        action="llm_inference",
        target_resource="openai_api",
        declared_objective="Generate response to user query"
    )
    state.poi_receipt = receipt
    return state

def take_action(state):
    if hasattr(state, 'poi_receipt'):
        print(f"Action taken with PoI: {state.poi_receipt.receipt_id}")
    return state

# Build workflow
workflow = StateGraph()
workflow.add_node("generate_poi", generate_poi)
workflow.add_node("take_action", take_action)
workflow.add_edge("generate_poi", "take_action")
workflow.add_edge("take_action", END)

app = workflow.compile()
result = app.invoke({})
```

### N8N

```python
# N8N Python Code Node
from poi_sdk import PoIGenerator
import json

def main():
    input_data = json.loads(input_data)
    
    generator = PoIGenerator()
    receipt = generator.generate_receipt(
        agent_id="n8n_workflow",
        action=input_data.get("action", "workflow_execution"),
        target_resource=input_data.get("resource", "unknown"),
        declared_objective=input_data.get("objective", "Process workflow data")
    )
    
    return json.dumps({
        "poi_receipt": receipt.to_dict(),
        "original_data": input_data
    })

result = main()
```

### Custom Agent

```python
from poi_sdk import PoIGenerator, PoIValidator

class PoIAgent:
    def __init__(self, agent_id):
        self.agent_id = agent_id
        self.generator = PoIGenerator()
        self.validator = PoIValidator()
    
    def execute_with_poi(self, action, resource, objective):
        receipt = self.generator.generate_receipt(
            agent_id=self.agent_id,
            action=action,
            target_resource=resource,
            declared_objective=objective
        )
        
        # Your custom logic here
        result = self._execute_action(action, resource)
        
        return {"receipt": receipt, "result": result}
    
    def _execute_action(self, action, resource):
        return {"status": "success", "action": action, "resource": resource}

# Usage
agent = PoIAgent("my_custom_agent")
result = agent.execute_with_poi(
    action="data_processing",
    resource="analytics_database",
    objective="Process customer analytics data"
)
```

## Configuration

### Environment Variables

```bash
export POI_PRIVATE_KEY_PATH="/path/to/private_key.pem"
export POI_CERTIFICATE_PATH="/path/to/certificate.pem"
export POI_PUBLIC_KEY_PATH="/path/to/public_key.pem"
export POI_DEFAULT_EXPIRATION_HOURS=1
```

### Custom Expiration

```python
from datetime import datetime, timedelta, timezone

receipt = generator.generate_receipt(
    agent_id="time_sensitive_agent",
    action="critical_operation",
    target_resource="sensitive_data",
    declared_objective="Perform critical system update",
    expiration_time=(datetime.now(timezone.utc) + timedelta(minutes=30)).isoformat()
)
```

## Receipt Inspection

### View Receipt Details

```python
# Convert to dictionary
receipt_dict = receipt.to_dict()
print(f"Receipt ID: {receipt_dict['receipt_id']}")
print(f"Agent: {receipt_dict['agent_id']}")
print(f"Action: {receipt_dict['action']}")
print(f"Objective: {receipt_dict['declared_objective']}")
print(f"Expires: {receipt_dict['expiration_time']}")

# Check if expired
if receipt.is_expired():
    print("⚠️ Receipt has expired!")
else:
    print("✅ Receipt is still valid")
```

### JSON Output

```python
# Get JSON representation
receipt_json = receipt.to_json()
print(receipt_json)
```

## Testing

### Basic Validation Test

```python
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
    assert receipt.agent_id == "test_agent"
    assert receipt.action == "test_action"

# Run test
test_receipt_validation()
print("✅ Basic validation test passed!")
```

## Error Handling

### Handle Validation Errors

```python
try:
    is_valid = validator.validate_receipt(receipt)
    if is_valid:
        print("✅ Receipt is valid")
    else:
        print("❌ Receipt validation failed")
except Exception as e:
    print(f"🚨 Validation error: {e}")
```

### Handle Generation Errors

```python
try:
    receipt = generator.generate_receipt(
        agent_id="my_agent",
        action="my_action",
        target_resource="my_resource",
        declared_objective="My objective"
    )
    print(f"✅ Receipt generated: {receipt.receipt_id}")
except Exception as e:
    print(f"🚨 Generation error: {e}")
```

## 📚 Next Steps

1. **Explore Advanced Features**: Check out the full [README](README.md) for detailed documentation
2. **Customize Your Implementation**: Adapt the examples to your specific use case
3. **Join the Community**: Visit [GitHub Discussions](https://github.com/giovannypietro/poi/discussions) to share your experience
4. **Contribute**: Help improve the SDK by submitting issues or pull requests

## Need Help?

- **Documentation**: [Full README](README.md)
- **Issues**: [GitHub Issues](https://github.com/giovannypietro/poi/issues)
- **Discussions**: [GitHub Discussions](https://github.com/giovannypietro/poi/discussions)
- **Examples**: Check the `examples/` directory for more use cases

---

**🎉 Congratulations! You've successfully generated your first Proof-of-Intent receipt.**

You're now ready to build trustworthy AI agents with cryptographic proof of their intentions!
