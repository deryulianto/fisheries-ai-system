from setuptools import setup, find_packages

setup(
    name="fisheries-ai-system",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.21.0",
        "pandas>=1.3.0", 
        "pyyaml>=5.4.0",
    ],
)
