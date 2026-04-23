"""LeadFlow AI setup configuration."""

from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="leadflow-ai",
    version="1.0.0",
    author="LeadFlow AI",
    description="AI-powered lead generation tool for freelancers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/leadflow-ai",
    packages=find_packages(exclude=["tests*", "examples*"]),
    python_requires=">=3.11",
    install_requires=[
        "fastapi>=0.115.0",
        "uvicorn>=0.32.0",
        "requests>=2.32.0",
        "python-dotenv>=1.0.0",
        "pydantic>=2.10.0",
    ],
    extras_require={
        "openai": ["openai>=1.57.0"],
        "dev": ["pytest>=8.3.0"],
    },
    entry_points={
        "console_scripts": [
            "leadflow=cli.main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Office/Business",
    ],
)
