#!/usr/bin/env python3
"""
Automated PyPI Package Installer for PoI SDK

This script automatically downloads and installs the poi-sdk package from PyPI.
It handles dependency resolution and provides installation status feedback.
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


def check_pip():
    """Check if pip is available and working."""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "--version"],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"✅ pip available: {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ pip not available")
        return False


def check_package_installed(package_name):
    """Check if a package is already installed."""
    try:
        result = subprocess.run(
            [sys.executable, "-c", f"import {package_name}; print('installed')"],
            capture_output=True,
            text=True,
            check=True
        )
        return True
    except subprocess.CalledProcessError:
        return False


def install_package(package_name, version=None):
    """Install a package using pip."""
    if version:
        package_spec = f"{package_name}=={version}"
    else:
        package_spec = package_name
    
    print(f"📦 Installing {package_spec}...")
    
    # Try to install the package
    result = run_command(
        f"{sys.executable} -m pip install {package_spec}",
        f"Installing {package_spec}",
        check=False
    )
    
    if result is not None:
        return True
    
    # If direct install fails, try with --user flag
    print("🔄 Trying installation with --user flag...")
    result = run_command(
        f"{sys.executable} -m pip install --user {package_spec}",
        f"Installing {package_spec} with --user flag",
        check=False
    )
    
    return result is not None


def upgrade_package(package_name):
    """Upgrade an existing package."""
    print(f"🔄 Upgrading {package_name}...")
    
    result = run_command(
        f"{sys.executable} -m pip install --upgrade {package_name}",
        f"Upgrading {package_name}",
        check=False
    )
    
    return result is not None


def verify_installation(package_name):
    """Verify that a package was installed correctly."""
    print(f"🔍 Verifying {package_name} installation...")
    
    try:
        # Try to import the package
        import_name = package_name.replace('-', '_')
        result = subprocess.run(
            [sys.executable, "-c", f"import {import_name}; print('✅ Import successful')"],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"✅ {package_name} imported successfully")
        
        # Try to get version info
        try:
            version_result = subprocess.run(
                [sys.executable, "-c", f"import {package_name}; print(getattr({package_name}, '__version__', 'version unknown'))"],
                capture_output=True,
                text=True,
                check=True
            )
            version = version_result.stdout.strip()
            if version and version != 'version unknown':
                print(f"📋 {package_name} version: {version}")
        except:
            pass
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to import {package_name}")
        if e.stderr:
            print(f"   Error: {e.stderr}")
        return False


def main():
    """Main installation process."""
    print("🚀 PoI SDK Package Installer")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check pip availability
    if not check_pip():
        print("❌ Cannot proceed without pip")
        sys.exit(1)
    
    package_name = "poi-sdk"
    
    # Check if package is already installed
    if check_package_installed(package_name):
        print(f"📦 {package_name} is already installed")
        
        # Ask if user wants to upgrade
        response = input("🔄 Would you like to upgrade to the latest version? (y/N): ").strip().lower()
        if response in ['y', 'yes']:
            if upgrade_package(package_name):
                verify_installation(package_name)
            else:
                print(f"❌ Failed to upgrade {package_name}")
        else:
            print("✅ Keeping current version")
            verify_installation(package_name)
    else:
        print(f"📦 {package_name} is not installed")
        
        # Install the package
        if install_package(package_name):
            verify_installation(package_name)
        else:
            print(f"❌ Failed to install {package_name}")
            sys.exit(1)
    
    print("\n🎉 Installation process completed!")
    print(f"📚 You can now use: from {package_name.replace('-', '_')} import PoIGenerator, PoIValidator")
    print(f"🖥️  Or run: {package_name.replace('-', '_')}-cli --help")


if __name__ == "__main__":
    main()
