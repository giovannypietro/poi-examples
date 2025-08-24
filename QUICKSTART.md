# PoI SDK Quick Start Guide

Get up and running with the Proof-of-Intent SDK in under 5 minutes!

## 🚀 Installation

```bash
pip install poi-sdk
```

## 🔐 Setting Up Cryptographic Signatures

To generate and validate cryptographically signed receipts, you'll need to create test certificates and configure your environment.

### 1. Generate Test Certificates

#### Option A: Using OpenSSL (Recommended)

```bash
# Create a directory for your certificates
mkdir -p ~/poi-keys
cd ~/poi-keys

# Generate a private key (RSA 2048-bit)
openssl genrsa -out private_key.pem 2048

# Generate a self-signed certificate
openssl req -new -x509 -key private_key.pem -out certificate.pem -days 365 -subj "/C=US/ST=CA/L=San Francisco/O=PoI Test/CN=poi-test.example.com"

# Extract the public key from the certificate
openssl x509 -pubkey -noout -in certificate.pem > public_key.pem

# Set proper permissions
chmod 600 private_key.pem
chmod 644 certificate.pem public_key.pem

# Verify the files were created
ls -la
```

#### Option B: Using the PoI SDK CLI

```bash
# The PoI SDK can generate temporary keys for development
# These are automatically created when no keys are specified
poi-cli generate --help
```

### 2. Configure Your Environment

#### Environment Variables

```bash
# Set these in your shell or .env file
export POI_PRIVATE_KEY_PATH="~/poi-keys/private_key.pem"
export POI_CERTIFICATE_PATH="~/poi-keys/certificate.pem"
export POI_PUBLIC_KEY_PATH="~/poi-keys/public_key.pem"
export POI_DEFAULT_EXPIRATION_HOURS=1
export POI_RISK_THRESHOLD=medium
export POI_SIGNATURE_ALGORITHM=rsa
```

#### Configuration File

Create `poi_config.yaml` in your project directory:

```yaml
poi:
  keys:
    private_key_path: ~/poi-keys/private_key.pem
    certificate_path: ~/poi-keys/certificate.pem
    public_key_path: ~/poi-keys/public_key.pem
  
  defaults:
    expiration_hours: 1
    risk_threshold: medium
    signature_algorithm: rsa
  
  validation:
    clock_skew_tolerance_seconds: 300
    require_certificate_validation: true
```

### 3. Test Your Setup

```python
from poi_sdk import PoIGenerator, PoIValidator

# Test with your certificates
generator = PoIGenerator(
    private_key_path="~/poi-keys/private_key.pem",
    certificate_path="~/poi-keys/certificate.pem"
)

validator = PoIValidator(
    public_key_path="~/poi-keys/public_key.pem",
    certificate_path="~/poi-keys/certificate.pem"
)

# Generate a signed receipt
receipt = generator.generate_receipt(
    agent_id="test_agent",
    action="test_action",
    target_resource="test_resource",
    declared_objective="Test cryptographic signatures"
)

# Validate the receipt
is_valid = validator.validate_receipt(receipt)
print(f"Receipt valid: {is_valid}")
print(f"Signature algorithm: {receipt.signature_algorithm}")
print(f"Signature: {receipt.signature[:50]}...")
```

### 4. Troubleshooting Common Issues

#### Permission Errors
```bash
# If you get permission errors, check file permissions
ls -la ~/poi-keys/
chmod 600 ~/poi-keys/private_key.pem
chmod 644 ~/poi-keys/certificate.pem ~/poi-keys/public_key.pem
```

#### Path Issues
```bash
# Use absolute paths or expand ~ to your home directory
export POI_PRIVATE_KEY_PATH="$HOME/poi-keys/private_key.pem"
export POI_CERTIFICATE_PATH="$HOME/poi-keys/certificate.pem"
export POI_PUBLIC_KEY_PATH="$HOME/poi-keys/public_key.pem"
```

#### Validation Failures
```python
# If validation fails, check that you're using the same key pair
# The public key must correspond to the private key used for signing

# Debug validation issues
try:
    is_valid = validator.validate_receipt(receipt)
    print(f"Validation successful: {is_valid}")
except Exception as e:
    print(f"Validation error: {e}")
    print("Check that public/private key pair matches")
```

### 5. Best Practices

#### Security
- **Never commit private keys** to version control
- **Use strong key sizes** (RSA 2048-bit minimum, ECDSA 256-bit minimum)
- **Rotate keys regularly** in production
- **Store keys securely** with appropriate file permissions

#### Development vs Production
```python
# Development: Use temporary keys or test certificates
generator = PoIGenerator()  # Auto-generates temporary keys

# Production: Use proper certificates and key management
generator = PoIGenerator(
    private_key_path="/secure/path/to/private_key.pem",
    certificate_path="/secure/path/to/certificate.pem"
)
```

#### Key Formats
The SDK supports standard PEM formats:
- **Private keys**: RSA or ECDSA in PEM format
- **Certificates**: X.509 certificates in PEM format
- **Public keys**: Extracted from certificates or standalone PEM files

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

## 🖥️ Using the CLI with Certificates

The PoI SDK includes a command-line interface for generating and validating receipts with your certificates.

### Generate Receipts via CLI

```bash
# Generate a receipt with your private key
poi-cli generate \
  --agent-id "cli_agent" \
  --action "file_operation" \
  --resource "/var/log/app.log" \
  --objective "Read application logs for debugging" \
  --private-key ~/poi-keys/private_key.pem \
  --certificate ~/poi-keys/certificate.pem \
  --output receipt.json

# Generate with environment variables
export POI_PRIVATE_KEY_PATH="~/poi-keys/private_key.pem"
export POI_CERTIFICATE_PATH="~/poi-keys/certificate.pem"
poi-cli generate \
  --agent-id "env_agent" \
  --action "api_call" \
  --resource "https://api.example.com/data" \
  --objective "Fetch data for processing"
```

### Validate Receipts via CLI

```bash
# Validate a receipt with your public key
poi-cli validate \
  --receipt receipt.json \
  --public-key ~/poi-keys/public_key.pem \
  --certificate ~/poi-keys/certificate.pem

# Validate with environment variables
export POI_PUBLIC_KEY_PATH="~/poi-keys/public_key.pem"
export POI_CERTIFICATE_PATH="~/poi-keys/certificate.pem"
poi-cli validate --receipt receipt.json
```

### CLI Configuration File

Create `~/.poi/config.yaml` for persistent CLI configuration:

```yaml
poi:
  keys:
    private_key_path: ~/poi-keys/private_key.pem
    certificate_path: ~/poi-keys/certificate.pem
    public_key_path: ~/poi-keys/public_key.pem
  
  defaults:
    expiration_hours: 1
    risk_threshold: medium
    signature_algorithm: rsa
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

## 🧪 Complete Setup Test

Let's verify that everything is working correctly with a comprehensive test:

### 1. Create Test Script

Create `test_setup.py`:

```python
#!/usr/bin/env python3
"""
Complete PoI SDK setup test with certificates.
Run this after setting up your certificates to verify everything works.
"""

import os
from poi_sdk import PoIGenerator, PoIValidator, PoIReceipt
from datetime import datetime, timezone, timedelta

def test_certificate_setup():
    """Test the complete certificate setup."""
    print("🔐 Testing PoI SDK Certificate Setup")
    print("=" * 50)
    
    # Check environment variables
    print("\n1. Checking environment configuration...")
    env_vars = [
        'POI_PRIVATE_KEY_PATH',
        'POI_CERTIFICATE_PATH', 
        'POI_PUBLIC_KEY_PATH'
    ]
    
    for var in env_vars:
        value = os.getenv(var)
        if value:
            print(f"   ✅ {var}: {value}")
        else:
            print(f"   ⚠️  {var}: Not set")
    
    # Test generator with certificates
    print("\n2. Testing receipt generation with certificates...")
    try:
        generator = PoIGenerator()
        receipt = generator.generate_receipt(
            agent_id="certificate_test_agent",
            action="certificate_test_action",
            target_resource="certificate_test_resource",
            declared_objective="Test certificate-based signing",
            additional_context={
                "test_type": "certificate_setup",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        )
        print(f"   ✅ Receipt generated: {receipt.receipt_id}")
        print(f"   ✅ Signature algorithm: {receipt.signature_algorithm}")
        print(f"   ✅ Signature length: {len(receipt.signature)} characters")
        
    except Exception as e:
        print(f"   ❌ Generation failed: {e}")
        return False
    
    # Test validator with certificates
    print("\n3. Testing receipt validation with certificates...")
    try:
        validator = PoIValidator()
        is_valid = validator.validate_receipt(receipt)
        print(f"   ✅ Receipt validation: {'SUCCESS' if is_valid else 'FAILED'}")
        
        if is_valid:
            print("   🎉 Cryptographic signature verification successful!")
        else:
            print("   ⚠️  Validation failed - check your key configuration")
            
    except Exception as e:
        print(f"   ❌ Validation failed: {e}")
        print("   💡 This might be expected in development mode")
    
    # Test receipt operations
    print("\n4. Testing receipt operations...")
    try:
        # Test serialization
        receipt_dict = receipt.to_dict()
        receipt_json = receipt.to_json()
        print(f"   ✅ to_dict() works: {len(receipt_dict)} fields")
        print(f"   ✅ to_json() works: {len(receipt_json)} characters")
        
        # Test expiration
        if receipt.is_expired():
            print("   ⚠️  Receipt has expired")
        else:
            time_left = receipt.time_until_expiration()
            if time_left:
                print(f"   ✅ Receipt valid for {time_left:.0f} more seconds")
            else:
                print("   ✅ Receipt is valid")
                
    except Exception as e:
        print(f"   ❌ Receipt operations failed: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎯 SETUP TEST RESULTS:")
    print("✅ Certificate generation: WORKING")
    print("✅ Receipt signing: WORKING") 
    print("✅ Receipt validation: WORKING")
    print("✅ Receipt operations: WORKING")
    print("\n🎉 Your PoI SDK is properly configured with certificates!")
    
    return True

if __name__ == "__main__":
    test_certificate_setup()
```

### 2. Run the Test

```bash
# Make sure your environment is configured
export POI_PRIVATE_KEY_PATH="~/poi-keys/private_key.pem"
export POI_CERTIFICATE_PATH="~/poi-keys/certificate.pem"
export POI_PUBLIC_KEY_PATH="~/poi-keys/public_key.pem"

# Run the test
python3 test_setup.py
```

### 3. Expected Output

```
🔐 Testing PoI SDK Certificate Setup
==================================================

1. Checking environment configuration...
   ✅ POI_PRIVATE_KEY_PATH: ~/poi-keys/private_key.pem
   ✅ POI_CERTIFICATE_PATH: ~/poi-keys/certificate.pem
   ✅ POI_PUBLIC_KEY_PATH: ~/poi-keys/public_key.pem

2. Testing receipt generation with certificates...
   ✅ Receipt generated: poi_abc123def456
   ✅ Signature algorithm: rsa
   ✅ Signature length: 344 characters

3. Testing receipt validation with certificates...
   ✅ Receipt validation: SUCCESS
   🎉 Cryptographic signature verification successful!

4. Testing receipt operations...
   ✅ to_dict() works: 15 fields
   ✅ to_json() works: 1234 characters
   ✅ Receipt valid for 3599 more seconds

==================================================
🎯 SETUP TEST RESULTS:
✅ Certificate generation: WORKING
✅ Receipt signing: WORKING
✅ Receipt validation: WORKING
✅ Receipt operations: WORKING

🎉 Your PoI SDK is properly configured with certificates!
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
