import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="flaskauth",
    version="0.0.1",
    author="Dan Jones",
    author_email="dan.jones@lunarfish.co.uk",
    description="Authentication decorators and helpers for flask apps",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alphagov/cybersecuritytools",
    packages=setuptools.find_packages(),
    package_data={
        "flaskauth": ["templates/*"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "boto3",
        "flask",
        "oic",
        "pyjwt",
        "requests",
        "serverless_wsgi",
        "jsonlogger @ git+https://github.com/lunarfish/json-logger.git",
    ],
    extras_require={
        "dev": [
            "pytest",
            "isort",
            "pytest-env",
            "pytest-flake8",
            "pytest-isort",
            "pytest-mock",
            "requests-mock",
        ]
    },
    python_requires=">=3.6",
)
