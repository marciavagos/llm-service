from setuptools import setup, find_packages

setup(
    name="llm_inference_package",
    version="0.1.0",
    description="A package for loading LLMs, running inference, and displaying results via Streamlit.",
    author="Your Name",
    author_email="your.email@example.com",
    python_requires=">=3.8",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests",
        "streamlit",
        "pyyaml",
        "paramiko",
    ],
)
