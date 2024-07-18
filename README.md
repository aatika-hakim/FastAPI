# FastAPI App

## Introduction
FastAPI is a modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints.

## Installed Packages

- **FastAPI**: A web framework for building APIs with Python.
- **Uvicorn**: A lightning-fast ASGI server implementation, using uvloop and httptools.


## Setup and Installation

1. Install python
2. Install Poetry: If you haven't installed Poetry yet, you can do so by following the instructions here

`poetry install`

## Running the Application
To start the FastAPI server, use the following command:

`poetry run uvicorn main:app --reload`


### what are dependencies in fastapi?

Dependencies are the packages that are required to run the application. They are specified in the pyproject.toml
file. To install the dependencies, use the following command:
`poetry install`

### Dependency injection:
Dependency injection is a design pattern that allows you to pass dependencies to your application.
It is used to make your application more modular and testable.
# Depend 
 keyword is used to specify the dependencies that are required by the application.

### Dependencies:

- **uvicorn**: A lightning-fast ASGI server implementation, using uvloop and httptools
- **fastapi**: A web framework for building APIs with Python.
- **pydantic**: A library for validating input data. It bases on a Python type system
- **starlette**: A lightweight ASGI framework/toolkit
- **python-multipart**: A Python library for parsing multipart/form-data
- **python-jose**: A Python implementation of the JSON Object Signing and Encryption (JOSE)
- **pyjwt**: JSON Web Token implementation in Python

