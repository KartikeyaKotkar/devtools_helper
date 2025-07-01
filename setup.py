from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [
        line.strip() for line in fh if line.strip() and not line.startswith("#")
    ]

setup(
    name="devtools-helper",
    version="0.1.0",
    author="DevTools Helper Contributors",
    author_email="devtools-helper@example.com",
    description="A comprehensive developer productivity toolkit for Python projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/KartikeyaKotkar/devtools-helper",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "devtools=devtools_helper.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "devtools_helper": ["templates/**/*", "*.yaml", "*.json"],
    },
)
