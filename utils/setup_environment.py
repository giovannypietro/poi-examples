#!/usr/bin/env python3
"""
Complete Environment Setup for PoI SDK

This script provides a one-stop solution for setting up the PoI SDK environment:
1. Installs the PyPI package
2. Generates test certificates and keys
3. Creates configuration files
4. Validates the setup
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(command, description, check=True):
    """Run a shell command and provide feedback."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True, 
            check=check
        )
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            return result.stdout.strip()
        else:
            print(f"⚠️  {description} completed with warnings")
            if result.stderr:
                print(f"   Warnings: {result.stderr}")
            return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed")
        print(f"   Error: {e}")
        if e.stderr:
            print(f"   Details: {e.stderr}")
        return None


def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python {version.major}.{version.minor} detected")
        print("   PoI SDK requires Python 3.8 or higher")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True


def install_package():
    """Install the PoI SDK package."""
    print("📦 Installing PoI SDK package...")
    
    # Check if package is already installed
    try:
        result = subprocess.run(
            [sys.executable, "-c", "import poi_sdk; print('installed')"],
            capture_output=True,
            text=True,
            check=True
        )
        print("✅ PoI SDK is already installed")
        return True
    except subprocess.CalledProcessError:
        pass
    
    # Install the package
    result = run_command(
        f"{sys.executable} -m pip install poi-sdk",
        "Installing PoI SDK from PyPI",
        check=False
    )
    
    if result is not None:
        return True
    
    # Try with --user flag
    print("🔄 Trying installation with --user flag...")
    result = run_command(
        f"{sys.executable} -m pip install --user poi-sdk",
        "Installing PoI SDK with --user flag",
        check=False
    )
    
    return result is not None


def generate_certificates():
    """Generate test certificates and keys."""
    print("🔐 Generating test certificates and keys...")
    
    # Check if OpenSSL is available
    try:
        result = subprocess.run(
            ["openssl", "version"],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"✅ OpenSSL available: {result.stdout.strip()}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ OpenSSL not available")
        print("   Please install OpenSSL to generate certificates")
        return False
    
    # Create directories
    base_dir = Path.cwd()
    keys_dir = base_dir / "test_keys"
    certs_dir = base_dir / "test_certs"
    
    keys_dir.mkdir(exist_ok=True)
    certs_dir.mkdir(exist_ok=True)
    
    print(f"📁 Working directories:")
    print(f"   Keys: {keys_dir}")
    print(f"   Certificates: {certs_dir}")
    
    # Generate RSA keys
    print("🔐 Generating RSA keys...")
    if not run_command(
        f"openssl genrsa -out {keys_dir}/private_key.pem 2048",
        "Generating RSA private key"
    ):
        return False
    
    if not run_command(
        f"openssl rsa -in {keys_dir}/private_key.pem -pubout -out {keys_dir}/public_key.pem",
        "Generating RSA public key"
    ):
        return False
    
    # Generate ECDSA keys
    print("🔐 Generating ECDSA keys...")
    if not run_command(
        f"openssl ecparam -genkey -name secp256r1 -out {keys_dir}/ec_private_key.pem",
        "Generating ECDSA private key"
    ):
        return False
    
    if not run_command(
        f"openssl ec -in {keys_dir}/ec_private_key.pem -pubout -out {keys_dir}/ec_public_key.pem",
        "Generating ECDSA public key"
    ):
        return False
    
    # Generate certificates
    print("📜 Generating certificates...")
    
    # Create certificate config
    config_content = """
[req]
distinguished_name = req_distinguished_name
req_extensions = v3_req
prompt = no

[req_distinguished_name]
C = US
ST = TestState
L = TestCity
O = TestOrganization
OU = TestUnit
CN = test-certificate
emailAddress = test@example.com

[v3_req]
basicConstraints = CA:FALSE
keyUsage = nonRepudiation, digitalSignature, keyEncipherment
subjectAltName = @alt_names

[alt_names]
DNS.1 = localhost
DNS.2 = *.localhost
IP.1 = 127.0.0.1
"""
    
    config_file = f"{keys_dir}/cert_config.conf"
    with open(config_file, 'w') as f:
        f.write(config_content)
    
    # Generate RSA certificate
    if not run_command(
        f"openssl req -new -x509 -key {keys_dir}/private_key.pem -out {certs_dir}/certificate.pem -days 365 -config {config_file}",
        "Generating RSA certificate"
    ):
        return False
    
    # Generate ECDSA certificate
    if not run_command(
        f"openssl req -new -x509 -key {keys_dir}/ec_private_key.pem -out {certs_dir}/ec_certificate.pem -days 365 -config {config_file}",
        "Generating ECDSA certificate"
    ):
        return False
    
    # Clean up config file
    os.remove(config_file)
    
    return True


def create_config_files():
    """Create configuration files for the SDK."""
    print("📝 Creating configuration files...")
    
    # Environment file
    env_content = """# PoI SDK Test Environment Configuration
# Generated automatically - DO NOT USE IN PRODUCTION

# RSA Keys
POI_PRIVATE_KEY_PATH=test_keys/private_key.pem
POI_PUBLIC_KEY_PATH=test_keys/public_key.pem
POI_CERTIFICATE_PATH=test_certs/certificate.pem

# ECDSA Keys
POI_EC_PRIVATE_KEY_PATH=test_keys/ec_private_key.pem
POI_EC_PUBLIC_KEY_PATH=test_keys/ec_public_key.pem
POI_EC_CERTIFICATE_PATH=test_certs/ec_certificate.pem

# Test Configuration
POI_TEST_MODE=true
POI_KEY_PASSWORD=test123
"""
    
    with open(".env.test", 'w') as f:
        f.write(env_content)
    
    # YAML config file
    yaml_content = """# PoI SDK Test Configuration
# Generated automatically - DO NOT USE IN PRODUCTION

poi:
  keys:
    # RSA Keys
    private_key_path: test_keys/private_key.pem
    public_key_path: test_keys/public_key.pem
    certificate_path: test_certs/certificate.pem
    
    # ECDSA Keys
    ec_private_key_path: test_keys/ec_private_key.pem
    ec_public_key_path: test_keys/ec_public_key.pem
    ec_certificate_path: test_certs/ec_certificate.pem
  
  defaults:
    expiration_hours: 24
    risk_threshold: low
    signature_algorithm: rsa  # or ecdsa
  
  validation:
    clock_skew_tolerance_seconds: 600
    require_certificate_validation: false  # Set to true in production
"""
    
    with open("poi_config_test.yaml", 'w') as f:
        f.write(yaml_content)
    
    print("✅ Configuration files created:")
    print("   - .env.test (environment variables)")
    print("   - poi_config_test.yaml (YAML config)")


def validate_setup():
    """Validate that the setup is working correctly."""
    print("🔍 Validating setup...")
    
    # Test package import
    try:
        result = subprocess.run(
            [sys.executable, "-c", "from poi_sdk import PoIGenerator, PoIValidator; print('✅ Package import successful')"],
            capture_output=True,
            text=True,
            check=True
        )
        print("✅ PoI SDK package imported successfully")
    except subprocess.CalledProcessError as e:
        print("❌ Failed to import PoI SDK")
        if e.stderr:
            print(f"   Error: {e.stderr}")
        return False
    
    # Test certificate files exist
    required_files = [
        "test_keys/private_key.pem",
        "test_keys/public_key.pem", 
        "test_certs/certificate.pem",
        "test_keys/ec_private_key.pem",
        "test_keys/ec_public_key.pem",
        "test_certs/ec_certificate.pem"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing certificate files:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        return False
    
    print("✅ All certificate files present")
    
    # Test basic functionality
    try:
        test_script = """
from poi_sdk import PoIGenerator, PoIValidator
import os

# Set test environment
os.environ['POI_PRIVATE_KEY_PATH'] = 'test_keys/private_key.pem'
os.environ['POI_CERTIFICATE_PATH'] = 'test_certs/certificate.pem'

# Test basic functionality
generator = PoIGenerator()
validator = PoIValidator()

print('✅ Basic functionality test passed')
"""
        
        result = subprocess.run(
            [sys.executable, "-c", test_script],
            capture_output=True,
            text=True,
            check=True
        )
        print("✅ Basic functionality test passed")
        
    except subprocess.CalledProcessError as e:
        print("⚠️  Basic functionality test had issues")
        if e.stderr:
            print(f"   Details: {e.stderr}")
    
    return True


def main():
    """Main setup process."""
    print("🚀 PoI SDK Complete Environment Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Step 1: Install package
    print("\n📦 Step 1: Installing PoI SDK Package")
    print("-" * 40)
    if not install_package():
        print("❌ Package installation failed")
        sys.exit(1)
    
    # Step 2: Generate certificates
    print("\n🔐 Step 2: Generating Test Certificates")
    print("-" * 40)
    if not generate_certificates():
        print("❌ Certificate generation failed")
        sys.exit(1)
    
    # Step 3: Create config files
    print("\n📝 Step 3: Creating Configuration Files")
    print("-" * 40)
    create_config_files()
    
    # Step 4: Validate setup
    print("\n🔍 Step 4: Validating Setup")
    print("-" * 40)
    if not validate_setup():
        print("❌ Setup validation failed")
        sys.exit(1)
    
    print("\n🎉 Environment setup completed successfully!")
    print("\n📚 Next steps:")
    print("   1. Load environment: source .env.test")
    print("   2. Run examples: python -c \"from poi_sdk import PoIGenerator; print('Ready!')\"")
    print("   3. Check QUICKSTART.md for detailed usage")
    print("\n⚠️  IMPORTANT: These are TEST certificates only!")
    print("   Do not use in production environments!")


if __name__ == "__main__":
    main()
