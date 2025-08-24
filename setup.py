#!/usr/bin/env python3
"""
Setup script for the Proof-of-Intent (PoI) Python SDK.
"""

from setuptools import setup, find_packages

# Read the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

# Development requirements
dev_requirements = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "pytest-mock>=3.10.0",
    "black>=23.0.0",
    "isort>=5.12.0",
    "flake8>=6.0.0",
    "mypy>=1.0.0",
    "pre-commit>=3.0.0",
    "tox>=4.0.0",
]

setup(
    name="poi-sdk",
    version="0.1.0",
    author="Aldo Pietropaolo",
    author_email="tbd@tbd.com",
    description="Proof-of-Intent Python SDK for creating trustworthy AI agent transactions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/giovannypietro/poi",
    project_urls={
        "Bug Tracker": "https://github.com/giovannypietro/poi/issues",
        "Documentation": "https://poi-sdk.readthedocs.io",
        "Source Code": "https://github.com/giovannypietro/poi",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Security",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Systems Administration",
        "Topic :: System :: Monitoring",
        "Topic :: System :: Logging",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": dev_requirements,
        "test": ["pytest>=7.0.0", "pytest-cov>=4.0.0", "pytest-mock>=3.10.0"],
        "docs": ["sphinx>=6.0.0", "sphinx-rtd-theme>=1.2.0", "myst-parser>=1.0.0"],
    },
    entry_points={
        "console_scripts": [
            "poi-cli=poi_sdk.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "poi_sdk": ["py.typed"],
    },
    keywords=[
        "ai", "agents", "security", "iam", "cryptography", 
        "proof-of-intent", "trust", "authentication", "authorization"
    ],
    zip_safe=False,
)
