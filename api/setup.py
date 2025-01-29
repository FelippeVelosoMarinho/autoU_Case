from setuptools import setup, find_packages

setup(
    name="autoU_case",
    version="0.1.0",
    description="Uma aplicação FastAPI de exemplo",
    author="Seu Nome",
    author_email="seu.email@example.com",
    packages=find_packages(),  # Inclui automaticamente os pacotes no diretório
    install_requires=[
        "fastapi==0.115.7",
        "uvicorn==0.34.0"
    ],
    entry_points={
        "console_scripts": [
            "autoU_case=autoU_case.main:app",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
