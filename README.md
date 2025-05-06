# 🧪 RESTful API with Python 3 and FastAPI

## Status

[![Python CI](https://github.com/nanotaboada/python-samples-fastapi-restful/actions/workflows/python-app.yml/badge.svg)](https://github.com/nanotaboada/python-samples-fastapi-restful/actions/workflows/python-app.yml)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=nanotaboada_python-samples-fastapi-restful&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=nanotaboada_python-samples-fastapi-restful)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/8f9bab37f6f444c895a8b25d5df772fc)](https://app.codacy.com/gh/nanotaboada/python-samples-fastapi-restful/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
[![codecov](https://codecov.io/gh/nanotaboada/python-samples-fastapi-restful/branch/master/graph/badge.svg?token=A1WNZPRQEJ)](https://codecov.io/gh/nanotaboada/python-samples-fastapi-restful)
[![CodeFactor](https://www.codefactor.io/repository/github/nanotaboada/python-samples-fastapi-restful/badge)](https://www.codefactor.io/repository/github/nanotaboada/python-samples-fastapi-restful)
[![codebeat badge](https://codebeat.co/badges/4c4f7c08-3b35-4b57-a875-bf2043efe515)](https://codebeat.co/projects/github-com-nanotaboada-python-samples-fastapi-restful-master)

## About

Proof of Concept for a RESTful API made with [Python 3](https://www.python.org/) and [FastAPI](https://fastapi.tiangolo.com/).

## Structure

![Simplified, conceptual project structure and main application flow](assets/images/structure.svg)

_Figure: Simplified, conceptual project structure and main application flow. Not all dependencies are shown._

## Install

```console
pip install -r requirements.txt
pip install -r requirements-lint.txt
pip install -r requirements-test.txt
```

## Start

```console
uvicorn main:app --reload --port 9000
```

## Docs

```console
http://localhost:9000/docs
```

![API Documentation](assets/images/swagger.png)

## Docker

This project includes a multi-stage `Dockerfile` for local development and production builds.

### Build the image

```bash
docker build -t python-samples-fastapi-restful .
```

### Run the container

```bash
docker run -p 9000:9000 python-samples-fastapi-restful:latest
```

## Credits

The solution has been coded using [Visual Studio Code](https://code.visualstudio.com/) with the official [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python) extension.

## Terms

All trademarks, registered trademarks, service marks, product names, company names, or logos mentioned on this repository are the property of their respective owners. All usage of such terms herein is for identification purposes only and constitutes neither an endorsement nor a recommendation of those items. Furthermore, the use of such terms is intended to be for educational and informational purposes only.
