# PoI SDK Quick Start Guide

Get up and running with the Proof-of-Intent SDK in under 5 minutes!

## 🚀 Installation

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

**💡 After installation, continue below for certificate setup and first steps.**

## 🛠️ Automated Setup with Utils Scripts

The PoI SDK includes utility scripts to automate the entire setup process. These scripts handle package installation, certificate generation, and environment configuration automatically.

### 📋 Utils Scripts Quick Reference

| Script | Purpose | Use Case | Complexity |
|--------|---------|----------|------------|
| `setup_environment.py` | Complete setup | 🚀 One-stop solution | 🟢 Easy |
| `install_package.py` | Package installation | 📦 Install SDK only | 🟢 Easy |
| `generate_certificates_simple.py` | Certificate generation | 🔐 Generate keys/certs | 🟢 Easy |
| `generate_certificates.py` | Advanced certificate generation | 🎨 Custom settings | 🟡 Medium |
| `README.md` | Utils documentation | 📚 Complete guide | 📖 Reference |

### 🚀 One-Stop Setup (Recommended)

For the fastest setup experience, use the comprehensive setup script:

```bash
# Run the complete environment setup
python utils/setup_environment.py
```

This script will:
- ✅ Install the `poi-sdk` package from PyPI
- ✅ Generate test certificates and keys
- ✅ Create configuration files
- ✅ Validate your setup

### 📦 Package Installation Only

If you just need to install the package:

```bash
# Install poi-sdk from PyPI
python utils/install_package.py
```

### 🔐 Certificate Generation Only

If you need to generate test certificates:

```bash
# Generate test certificates and keys
python utils/generate_certificates_simple.py
```

**💡 The simple version is recommended for most users. For advanced options, see `utils/generate_certificates.py`**

### 📋 What the Utils Scripts Generate

The utils scripts automatically create:

```
test_keys/
├── private_key.pem          # RSA private key
├── public_key.pem           # RSA public key
├── rsa_bundle.p12           # PKCS#12 bundle
├── ec_private_key.pem       # ECDSA private key
├── ec_public_key.pem        # ECDSA public key
└── ecdsa_bundle.p12         # ECDSA PKCS#12 bundle

test_certs/
├── certificate.pem           # RSA certificate
└── ec_certificate.pem       # ECDSA certificate

Configuration Files:
├── .env.test                # Environment variables
└── poi_config_test.yaml     # SDK configuration
```

### 🔧 Manual Setup vs Utils Scripts

| Setup Method | Speed | Customization | Complexity |
|--------------|-------|---------------|------------|
| **Utils Scripts** | ⚡ Fast | 🎯 Good | 🟢 Easy |
| **Manual Setup** | 🐌 Slow | 🎨 Full | 🟡 Medium |

**💡 For beginners and quick development, use the utils scripts. For production, consider manual setup with proper key management.**

## Test Your Installation

Let's verify that your PoI SDK installation is working correctly:

### Quick Installation Test

```python
from poi_sdk import PoIGenerator, PoIValidator

# Test basic import and initialization
generator = PoIGenerator()
validator = PoIValidator()

print("✅ PoI SDK imported successfully!")
print("✅ Generator initialized:", generator)
print("✅ Validator initialized:", validator)
```

**💡 If the above test works, continue to the next section for certificate setup. If you get errors, check your Python version and installation.**

## 🔐 Setting Up Cryptographic Signatures

To generate and validate cryptographically signed receipts, you'll need to create test certificates and configure your environment.

### 1. Generate Test Certificates

#### Option A: Using Utils Scripts (Recommended for Quick Start)

```bash
# Use the automated certificate generation
python utils/generate_certificates_simple.py

# Or for complete setup including package installation
python utils/setup_environment.py
```

**💡 This is the fastest way to get started. The scripts automatically generate all necessary files and set proper permissions.**

#### Option B: Using OpenSSL (Manual Setup)

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

#### Option A: Using Generated Configuration Files (Recommended)

If you used the utils scripts, configuration files are automatically created:

```bash
# Source the generated environment file
source .env.test

# Or use the generated config file
export POI_CONFIG_PATH="poi_config_test.yaml"
```

**💡 The utils scripts create these files with the correct paths and settings for your test environment.**

The generated `.env.test` file contains:

```bash
# Test environment configuration
POI_PRIVATE_KEY_PATH=./test_keys/private_key.pem
POI_CERTIFICATE_PATH=./test_certs/certificate.pem
POI_PUBLIC_KEY_PATH=./test_keys/public_key.pem
POI_DEFAULT_EXPIRATION_HOURS=1
POI_RISK_THRESHOLD=medium
POI_SIGNATURE_ALGORITHM=rsa
```

And `poi_config_test.yaml` contains:

```yaml
poi:
  keys:
    private_key_path: ./test_keys/private_key.pem
    certificate_path: ./test_certs/certificate.pem
    public_key_path: ./test_keys/public_key.pem
  
  defaults:
    expiration_hours: 1
    risk_threshold: medium
    signature_algorithm: rsa
  
  validation:
    clock_skew_tolerance_seconds: 300
    require_certificate_validation: true
```

#### Option B: Manual Environment Configuration

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

#### Option A: Using Utils-Generated Files (Recommended)

If you used the utils scripts, test with the generated files:

```python
from poi_sdk import PoIGenerator, PoIValidator

# Test with utils-generated certificates
generator = PoIGenerator(
    private_key_path="./test_keys/private_key.pem",
    certificate_path="./test_certs/certificate.pem"
)

validator = PoIValidator(
    public_key_path="./test_keys/public_key.pem",
    certificate_path="./test_certs/certificate.pem"
)
```

**💡 The utils scripts generate files in the current directory, so use relative paths like `./test_keys/`**

#### Option B: Using Manual Setup Files

If you generated certificates manually:

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

#### Utils Script Issues

If you encounter problems with the utils scripts:

```bash
# Check Python version (requires 3.8+)
python --version

# Check if OpenSSL is installed
openssl version

# Verify the utils directory exists
ls -la utils/

# Check script permissions
ls -la utils/*.py
chmod +x utils/*.py  # Make scripts executable if needed
```

**💡 If the comprehensive setup script fails, try the individual scripts: `install_package.py` then `generate_certificates_simple.py`**

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

## 🔧 Advanced Utils Usage

### Customizing Certificate Generation

The utils scripts support customization for different use cases:

```bash
# View available options for certificate generation
python utils/generate_certificates.py --help

# Generate certificates with custom settings
python utils/generate_certificates.py --key-size 4096 --curve secp384r1

# Use specific output directories
python utils/generate_certificates.py --output-dir ~/my-custom-keys
```

### Batch Operations

For multiple environments or testing scenarios:

```bash
# Generate certificates for different environments
mkdir -p ~/poi-keys/dev ~/poi-keys/staging ~/poi-keys/test

# Generate dev certificates
python utils/generate_certificates_simple.py --output-dir ~/poi-keys/dev

# Generate staging certificates  
python utils/generate_certificates_simple.py --output-dir ~/poi-keys/staging

# Generate test certificates
python utils/generate_certificates_simple.py --output-dir ~/poi-keys/test
```

### Integration with CI/CD

The utils scripts can be integrated into automated workflows:

```bash
# In your CI/CD pipeline
python utils/install_package.py --quiet --no-interaction
python utils/generate_certificates_simple.py --output-dir /tmp/poi-keys

# Use generated keys for testing
export POI_PRIVATE_KEY_PATH="/tmp/poi-keys/private_key.pem"
export POI_CERTIFICATE_PATH="/tmp/poi-keys/certificate.pem"
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

### Testing with Utils-Generated Certificates

If you used the utils scripts, test with the generated certificates:

```python
def test_with_utils_certificates():
    generator = PoIGenerator(
        private_key_path="./test_keys/private_key.pem",
        certificate_path="./test_certs/certificate.pem"
    )
    
    validator = PoIValidator(
        public_key_path="./test_keys/public_key.pem",
        certificate_path="./test_certs/certificate.pem"
    )
    
    receipt = generator.generate_receipt(
        agent_id="utils_test_agent",
        action="test_action",
        target_resource="test_resource",
        declared_objective="Test with utils-generated certificates"
    )
    
    is_valid = validator.validate_receipt(receipt)
    print(f"Utils certificate test: {'✅ PASSED' if is_valid else '❌ FAILED'}")
    
    return is_valid

# Run utils certificate test
test_with_utils_certificates()
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

### Utils Script Error Handling

If you encounter errors with the utils scripts:

```python
import subprocess
import sys

def run_utils_with_error_handling():
    try:
        # Try the simple certificate generation first
        result = subprocess.run(
            ["python", "utils/generate_certificates_simple.py"],
            capture_output=True,
            text=True,
            check=True
        )
        print("✅ Utils script completed successfully")
        print(result.stdout)
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Utils script failed with exit code {e.returncode}")
        print(f"Error output: {e.stderr}")
        print(f"Standard output: {e.stdout}")
        
        # Fallback to manual setup
        print("🔄 Falling back to manual setup...")
        return False
        
    except FileNotFoundError:
        print("❌ Utils scripts not found. Make sure you're in the correct directory.")
        return False

# Run with error handling
run_utils_with_error_handling()
```









## 📚 Next Steps

1. **Explore Advanced Features**: Check out the full [README](README.md) for detailed documentation
2. **Customize Your Implementation**: Adapt the examples to your specific use case
3. **Master the Utils**: Explore the `utils/` directory for automation scripts and advanced features
4. **Join the Community**: Visit [GitHub Discussions](https://github.com/giovannypietro/poi/discussions) to share your experience
5. **Contribute**: Help improve the SDK by submitting issues or pull requests

## Need Help?

- **Documentation**: [Full README](README.md)
- **Utils Scripts**: [Utils README](utils/README.md) - Complete guide to automation scripts
- **Issues**: [GitHub Issues](https://github.com/giovannypietro/poi/issues)
- **Discussions**: [GitHub Discussions](https://github.com/giovannypietro/poi/discussions)
- **Examples**: Check the `examples/` directory for more use cases

---

**🎉 Congratulations! You've successfully generated your first Proof-of-Intent receipt.**

You're now ready to build trustworthy AI agents with cryptographic proof of their intentions!

## 🚀 Complete Utils Workflow

Here's the complete workflow using the utils scripts:

```bash
# 1. Clone the repository
git clone https://github.com/giovannypietro/poi-examples.git
cd poi-examples

# 2. Run the complete setup (recommended)
python utils/setup_environment.py

# 3. Test your setup
python -c "
from poi_sdk import PoIGenerator, PoIValidator
generator = PoIGenerator('./test_keys/private_key.pem', './test_certs/certificate.pem')
validator = PoIValidator('./test_keys/public_key.pem', './test_certs/certificate.pem')
receipt = generator.generate_receipt('test_agent', 'test_action', 'test_resource', 'Test objective')
print(f'✅ Receipt generated: {receipt.receipt_id}')
print(f'✅ Validation: {validator.validate_receipt(receipt)}')
"

# 4. Start building your AI agents!
```

**💡 The utils scripts handle everything automatically - from package installation to certificate generation to configuration setup. You can focus on building your AI agents instead of managing infrastructure!**
