# PoI SDK Utility Scripts

This folder contains utility scripts to help you set up and work with the PoI SDK.

## 🚀 Quick Start

For a complete one-stop setup, run:

```bash
python utils/setup_environment.py
```

This will install the package, generate certificates, and create configuration files automatically.

## 📁 Available Scripts

### 1. **`setup_environment.py`** - Complete Environment Setup
**One-stop solution for setting up the entire PoI SDK environment.**

**What it does:**
- ✅ Installs the `poi-sdk` package from PyPI
- ✅ Generates test RSA and ECDSA keys
- ✅ Creates self-signed test certificates
- ✅ Generates configuration files
- ✅ Validates the complete setup

**Usage:**
```bash
python utils/setup_environment.py
```

**Output:**
- `test_keys/` - Private and public keys
- `test_certs/` - Self-signed certificates
- `.env.test` - Environment variables
- `poi_config_test.yaml` - YAML configuration

---

### 2. **`install_package.py`** - Package Installation Only
**Installs or upgrades the PoI SDK package from PyPI.**

**What it does:**
- ✅ Checks Python version compatibility
- ✅ Verifies pip availability
- ✅ Installs or upgrades `poi-sdk`
- ✅ Validates installation
- ✅ Provides installation feedback

**Usage:**
```bash
python utils/install_package.py
```

**Features:**
- Automatic dependency resolution
- Fallback to `--user` installation if needed
- Upgrade prompts for existing installations
- Installation verification

---

### 3. **`generate_certificates.py`** - Certificate Generation Only
**Generates test certificates and keys for development.**

**What it does:**
- ✅ Generates RSA 2048-bit key pairs
- ✅ Generates ECDSA secp256r1 key pairs
- ✅ Creates self-signed certificates
- ✅ Generates PKCS#12 bundles
- ✅ Creates configuration files

**Usage:**
```bash
python utils/generate_certificates.py
```

**Requirements:**
- OpenSSL must be installed
- Python 3.8+

### 4. **`generate_certificates_simple.py`** - Simple Certificate Generator
**Simplified, reliable certificate generation script.**

**What it does:**
- ✅ Same functionality as generate_certificates.py
- ✅ Simplified subprocess handling
- ✅ More reliable execution
- ✅ Better error reporting

**Usage:**
```bash
python utils/generate_certificates_simple.py
```

**Recommended for:**
- First-time users
- Troubleshooting certificate generation issues
- Reliable certificate generation

---

## 🔧 Prerequisites

### **Required Software:**
- **Python 3.8+** - For running the scripts
- **pip** - For package installation
- **OpenSSL** - For certificate generation

### **Installation:**
```bash
# macOS (using Homebrew)
brew install openssl

# Ubuntu/Debian
sudo apt-get install openssl

# CentOS/RHEL
sudo yum install openssl

# Windows
# Download from https://slproweb.com/products/Win32OpenSSL.html
```

---

## 📋 Generated Files

### **Keys Directory (`test_keys/`)**
```
test_keys/
├── private_key.pem          # RSA private key
├── public_key.pem           # RSA public key
├── ec_private_key.pem       # ECDSA private key
├── ec_public_key.pem        # ECDSA public key
├── rsa_bundle.p12           # RSA PKCS#12 bundle
└── ecdsa_bundle.p12         # ECDSA PKCS#12 bundle
```

### **Certificates Directory (`test_certs/`)**
```
test_certs/
├── certificate.pem           # RSA certificate
└── ec_certificate.pem        # ECDSA certificate
```

### **Configuration Files**
- **`.env.test`** - Environment variables for testing
- **`poi_config_test.yaml`** - YAML configuration for testing

---

## 🎯 Use Cases

### **Development Setup**
```bash
# Complete development environment
python utils/setup_environment.py

# Load environment variables
source .env.test

# Test the setup
python -c "from poi_sdk import PoIGenerator; print('Ready!')"
```

### **CI/CD Integration**
```bash
# Install package only
python utils/install_package.py

# Generate certificates for testing
python utils/generate_certificates.py
```

### **Production Preparation**
```bash
# Install production package
pip install poi-sdk

# Generate production certificates (modify scripts first)
python utils/generate_certificates.py
```

---

## ⚠️ Important Notes

### **Security Warnings:**
- **TEST CERTIFICATES ONLY** - Do not use in production
- **Self-signed certificates** - Not trusted by default
- **Default passwords** - Change for production use
- **Key permissions** - Secure private keys properly

### **Production Considerations:**
- Use proper CA-signed certificates
- Implement proper key management
- Set secure file permissions
- Use strong passwords
- Enable certificate validation

---

## 🐛 Troubleshooting

### **Common Issues:**

#### **1. OpenSSL Not Found**
```bash
# Check if OpenSSL is installed
openssl version

# Install if missing
# macOS: brew install openssl
# Ubuntu: sudo apt-get install openssl
```

#### **2. Permission Denied**
```bash
# Check file permissions
ls -la test_keys/
ls -la test_certs/

# Fix permissions if needed
chmod 600 test_keys/*.pem
chmod 644 test_certs/*.pem
```

#### **3. Package Installation Fails**
```bash
# Try with user flag
pip install --user poi-sdk

# Check Python environment
python --version
pip --version
```

#### **4. Certificate Generation Errors**
```bash
# Check OpenSSL version
openssl version

# Verify working directory
pwd
ls -la
```

---

## 📚 Related Documentation

- **Main README**: Overview and PyPI package information
- **QUICKSTART**: Detailed setup and usage instructions
- **PACKAGE_README**: Package building and distribution
- **CONTRIBUTING**: Development guidelines

---

## 🤝 Contributing

Found an issue or have an improvement? Please:

1. Check existing issues
2. Create a new issue with details
3. Submit a pull request with fixes
4. Follow the contribution guidelines

---

**Happy coding with PoI SDK!** 🚀✨
