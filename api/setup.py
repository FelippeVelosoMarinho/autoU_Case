from setuptools import setup, find_packages

setup(
    name="autoU_case",
    version="0.1.0",
    description="Uma aplicação FastAPI de exemplo",
    author="Felippe Veloso",
    author_email="felippe.veloso15@gmail.com",
    packages=find_packages(),  # Inclui automaticamente os pacotes no diretório
    install_requires=[
        "fastapi==0.115.7",
        "uvicorn==0.34.0",
        "requests",
        "python-multipart",
        "transformers==4.48.1",
        "torch==2.6.0",
        "datasets==3.2.0",
        "python-dotenv==1.0.1",
        "PyPDF2==3.0.1",
        "huggingface_hub==0.28.1",
        "hypercorn==0.13.1 ",
        "pytest==7.1.2"
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
