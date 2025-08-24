#!/usr/bin/env python3
"""
Test Certificate Generator for PoI SDK

This script automatically generates test certificates and keys for development
and testing purposes. It creates RSA and ECDSA key pairs with self-signed
certificates.
"""

import subprocess
import sys
import os
from pathlib import Path
import secrets
import string


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


def check_openssl():
    """Check if OpenSSL is available."""
    try:
        result = subprocess.run(
            ["openssl", "version"],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"✅ OpenSSL available: {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ OpenSSL not available")
        print("   Please install OpenSSL to generate certificates")
        return False


def generate_random_string(length=16):
    """Generate a random string for certificate details."""
    chars = string.ascii_letters + string.digits
    return ''.join(secrets.choice(chars) for _ in range(length))


def create_directory(path):
    """Create a directory if it doesn't exist."""
    Path(path).mkdir(parents=True, exist_ok=True)
    print(f"📁 Created directory: {path}")


def generate_rsa_key_pair(key_path, key_size=2048):
    """Generate RSA private key and public key."""
    print(f"🔐 Generating RSA {key_size}-bit key pair...")
    
    # Generate private key
    private_key_cmd = f"openssl genrsa -out {key_path}/private_key.pem {key_size}"
    if not run_command(private_key_cmd, "Generating RSA private key"):
        return False
    
    # Generate public key from private key
    public_key_cmd = f"openssl rsa -in {key_path}/private_key.pem -pubout -out {key_path}/public_key.pem"
    if not run_command(public_key_cmd, "Generating RSA public key"):
        return False
    
    return True


def generate_ecdsa_key_pair(key_path, curve="secp256r1"):
    """Generate ECDSA private key and public key."""
    print(f"🔐 Generating ECDSA key pair with curve {curve}...")
    
    # Generate private key
    private_key_cmd = f"openssl ecparam -genkey -name {curve} -out {key_path}/ec_private_key.pem"
    if not run_command(private_key_cmd, "Generating ECDSA private key"):
        return False
    
    # Generate public key from private key
    public_key_cmd = f"openssl ec -in {key_path}/ec_private_key.pem -pubout -out {key_path}/ec_public_key.pem"
    if not run_command(public_key_cmd, "Generating ECDSA public key"):
        return False
    
    return True


def generate_self_signed_certificate(key_path, cert_path, key_type="rsa"):
    """Generate a self-signed certificate."""
    print(f"📜 Generating self-signed certificate for {key_type.upper()}...")
    
    # Create certificate configuration
    config_content = f"""
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
CN = test-{key_type}-certificate
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
    
    config_file = f"{key_path}/cert_config.conf"
    with open(config_file, 'w') as f:
        f.write(config_content)
    
    # Generate certificate
    if key_type == "rsa":
        private_key = f"{key_path}/private_key.pem"
        cert_file = f"{cert_path}/certificate.pem"
    else:
        private_key = f"{key_path}/ec_private_key.pem"
        cert_file = f"{cert_path}/ec_certificate.pem"
    
    cert_cmd = f"openssl req -new -x509 -key {private_key} -out {cert_file} -days 365 -config {config_file}"
    if not run_command(cert_cmd, f"Generating {key_type.upper()} certificate"):
        return False
    
    # Clean up config file
    os.remove(config_file)
    
    return True


def generate_pkcs12_bundle(key_path, cert_path, key_type="rsa"):
    """Generate PKCS#12 bundle for easy import."""
    print(f"📦 Generating PKCS#12 bundle for {key_type.upper()}...")
    
    if key_type == "rsa":
        private_key = f"{key_path}/private_key.pem"
        certificate = f"{cert_path}/certificate.pem"
        output_file = f"{key_path}/rsa_bundle.p12"
    else:
        private_key = f"{key_path}/ec_private_key.pem"
        certificate = f"{cert_path}/ec_certificate.pem"
        output_file = f"{key_path}/ecdsa_bundle.p12"
    
    # Generate PKCS#12 bundle
    bundle_cmd = f"openssl pkcs12 -export -out {output_file} -inkey {private_key} -in {certificate} -passout pass:test123"
    if not run_command(bundle_cmd, f"Generating {key_type.upper()} PKCS#12 bundle"):
        return False
    
    return True


def create_environment_file(key_path, cert_path):
    """Create environment file with key paths."""
    env_content = f"""# PoI SDK Test Environment Configuration
# Generated automatically - DO NOT USE IN PRODUCTION

# RSA Keys
POI_PRIVATE_KEY_PATH={key_path}/private_key.pem
POI_PUBLIC_KEY_PATH={key_path}/public_key.pem
POI_CERTIFICATE_PATH={cert_path}/certificate.pem

# ECDSA Keys
POI_EC_PRIVATE_KEY_PATH={key_path}/ec_private_key.pem
POI_EC_PUBLIC_KEY_PATH={key_path}/ec_public_key.pem
POI_EC_CERTIFICATE_PATH={cert_path}/ec_certificate.pem

# PKCS#12 Bundles
POI_RSA_BUNDLE_PATH={key_path}/rsa_bundle.p12
POI_ECDSA_BUNDLE_PATH={key_path}/ecdsa_bundle.p12

# Test Configuration
POI_TEST_MODE=true
POI_KEY_PASSWORD=test123
"""
    
    env_file = ".env.test"
    with open(env_file, 'w') as f:
        f.write(env_content)
    
    print(f"📝 Created environment file: {env_file}")


def create_config_file(key_path, cert_path):
    """Create YAML configuration file."""
    config_content = f"""# PoI SDK Test Configuration
# Generated automatically - DO NOT USE IN PRODUCTION

poi:
  keys:
    # RSA Keys
    private_key_path: {key_path}/private_key.pem
    public_key_path: {key_path}/public_key.pem
    certificate_path: {cert_path}/certificate.pem
    
    # ECDSA Keys
    ec_private_key_path: {key_path}/ec_private_key.pem
    ec_public_key_path: {key_path}/ec_public_key.pem
    ec_certificate_path: {cert_path}/ec_certificate.pem
    
    # PKCS#12 Bundles
    rsa_bundle_path: {key_path}/rsa_bundle.p12
    ecdsa_bundle_path: {key_path}/ecdsa_bundle.p12
  
  defaults:
    expiration_hours: 24
    risk_threshold: low
    signature_algorithm: rsa  # or ecdsa
  
  validation:
    clock_skew_tolerance_seconds: 600
    require_certificate_validation: false  # Set to true in production
"""
    
    config_file = "poi_config_test.yaml"
    with open(config_file, 'w') as f:
        f.write(config_content)
    
    print(f"📝 Created configuration file: {config_file}")


def main():
    """Main certificate generation process."""
    print("🔐 PoI SDK Test Certificate Generator")
    print("=" * 50)
    
    # Check OpenSSL availability
    if not check_openssl():
        sys.exit(1)
    
    # Create directories
    base_dir = Path.cwd()
    keys_dir = base_dir / "test_keys"
    certs_dir = base_dir / "test_certs"
    
    create_directory(keys_dir)
    create_directory(certs_dir)
    
    print(f"\n📁 Working directories:")
    print(f"   Keys: {keys_dir}")
    print(f"   Certificates: {certs_dir}")
    
    # Generate RSA key pair and certificate
    print(f"\n🔐 Generating RSA keys and certificate...")
    if generate_rsa_key_pair(keys_dir):
        print("🔐 Generating RSA certificate...")
        if generate_self_signed_certificate(keys_dir, certs_dir, "rsa"):
            print("📦 Generating RSA PKCS#12 bundle...")
            generate_pkcs12_bundle(keys_dir, certs_dir, "rsa")
    
    # Generate ECDSA key pair and certificate
    print(f"\n🔐 Generating ECDSA keys and certificate...")
    if generate_ecdsa_key_pair(keys_dir):
        print("🔐 Generating ECDSA certificate...")
        if generate_self_signed_certificate(keys_dir, certs_dir, "ecdsa"):
            print("📦 Generating ECDSA PKCS#12 bundle...")
            generate_pkcs12_bundle(keys_dir, certs_dir, "ecdsa")
    
    # Create configuration files
    print(f"\n📝 Creating configuration files...")
    create_environment_file(keys_dir, certs_dir)
    create_config_file(keys_dir, certs_dir)
    
    print(f"\n🎉 Certificate generation completed!")
    print(f"📁 Keys stored in: {keys_dir}")
    print(f"📁 Certificates stored in: {certs_dir}")
    print(f"📝 Configuration files created:")
    print(f"   - .env.test (environment variables)")
    print(f"   - poi_config_test.yaml (YAML config)")
    print(f"\n⚠️  IMPORTANT: These are TEST certificates only!")
    print(f"   Do not use in production environments!")
    print(f"   Key password: test123")


if __name__ == "__main__":
    main()
