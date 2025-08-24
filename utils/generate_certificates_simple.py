#!/usr/bin/env python3
"""
Simple Test Certificate Generator for PoI SDK

This script generates test certificates and keys for development.
"""

import subprocess
import sys
from pathlib import Path


def run_cmd(cmd, description):
    """Run a command and provide feedback."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stderr:
            print(f"   Error: {e.stderr}")
        return False


def main():
    """Generate test certificates and keys."""
    print("🔐 PoI SDK Test Certificate Generator (Simple)")
    print("=" * 50)
    
    # Check OpenSSL
    try:
        result = subprocess.run(["openssl", "version"], capture_output=True, text=True, check=True)
        print(f"✅ OpenSSL available: {result.stdout.strip()}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ OpenSSL not available")
        sys.exit(1)
    
    # Create directories
    keys_dir = Path("test_keys")
    certs_dir = Path("test_certs")
    
    keys_dir.mkdir(exist_ok=True)
    certs_dir.mkdir(exist_ok=True)
    
    print(f"📁 Working directories created")
    
    # Generate RSA keys
    print("\n🔐 Generating RSA keys...")
    if not run_cmd("openssl genrsa -out test_keys/private_key.pem 2048", "Generating RSA private key"):
        sys.exit(1)
    
    if not run_cmd("openssl rsa -in test_keys/private_key.pem -pubout -out test_keys/public_key.pem", "Generating RSA public key"):
        sys.exit(1)
    
    # Generate ECDSA keys
    print("\n🔐 Generating ECDSA keys...")
    if not run_cmd("openssl ecparam -genkey -name secp256r1 -out test_keys/ec_private_key.pem", "Generating ECDSA private key"):
        sys.exit(1)
    
    if not run_cmd("openssl ec -in test_keys/ec_private_key.pem -pubout -out test_keys/ec_public_key.pem", "Generating ECDSA public key"):
        sys.exit(1)
    
    # Generate certificates
    print("\n📜 Generating certificates...")
    
    # RSA certificate
    rsa_subj = "/C=US/ST=TestState/L=TestCity/O=TestOrganization/OU=TestUnit/CN=test-rsa-certificate/emailAddress=test@example.com"
    if not run_cmd(f"openssl req -new -x509 -key test_keys/private_key.pem -out test_certs/certificate.pem -days 365 -subj '{rsa_subj}'", "Generating RSA certificate"):
        sys.exit(1)
    
    # ECDSA certificate
    ecdsa_subj = "/C=US/ST=TestState/L=TestCity/O=TestOrganization/OU=TestUnit/CN=test-ecdsa-certificate/emailAddress=test@example.com"
    if not run_cmd(f"openssl req -new -x509 -key test_keys/ec_private_key.pem -out test_certs/ec_certificate.pem -days 365 -subj '{ecdsa_subj}'", "Generating ECDSA certificate"):
        sys.exit(1)
    
    # Generate PKCS#12 bundles
    print("\n📦 Generating PKCS#12 bundles...")
    if not run_cmd("openssl pkcs12 -export -out test_keys/rsa_bundle.p12 -inkey test_keys/private_key.pem -in test_certs/certificate.pem -passout pass:test123", "Generating RSA PKCS#12 bundle"):
        sys.exit(1)
    
    if not run_cmd("openssl pkcs12 -export -out test_keys/ecdsa_bundle.p12 -inkey test_keys/ec_private_key.pem -in test_certs/ec_certificate.pem -passout pass:test123", "Generating ECDSA PKCS#12 bundle"):
        sys.exit(1)
    
    # Create config files
    print("\n📝 Creating configuration files...")
    
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

# PKCS#12 Bundles
POI_RSA_BUNDLE_PATH=test_keys/rsa_bundle.p12
POI_ECDSA_BUNDLE_PATH=test_keys/ecdsa_bundle.p12

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
    
    # PKCS#12 Bundles
    rsa_bundle_path: test_keys/rsa_bundle.p12
    ecdsa_bundle_path: test_keys/ecdsa_bundle.p12
  
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
    
    print("✅ Configuration files created")
    
    # Show results
    print(f"\n🎉 Certificate generation completed!")
    print(f"📁 Keys: {keys_dir}")
    print(f"📁 Certificates: {certs_dir}")
    print(f"📝 Config files: .env.test, poi_config_test.yaml")
    print(f"\n⚠️  IMPORTANT: TEST certificates only!")
    print(f"   Do not use in production!")
    print(f"   Key password: test123")


if __name__ == "__main__":
    main()
