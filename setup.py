from setuptools import setup, find_packages
from pathlib import Path

setup(
    name="nexus_ai",
    version="0.1.0",
    author="Shri",
    description="Modular AI copilot engine for cross-industry applications",
    long_description=Path("README.md").read_text(encoding="utf-8") if Path("README.md").exists() else "",
    long_description_content_type="text/markdown",
    license="MIT",
    python_requires=">=3.10",
    packages=find_packages(include=["nexus_ai", "nexus_ai.*"]),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "fastapi",
        "pydantic",
        "uvicorn",
        "transformers",
        "numpy",
        "scikit-learn",
        "httpx",
        "loguru"
    ],
    entry_points={
      "console_scripts": [
        "plugin = nexus_ai.cli.plugin_commands:main"
      ]
     }
      
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License"
    ],
)