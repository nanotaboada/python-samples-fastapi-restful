# 🧪 RESTful API with Python 3 and FastAPI

## Status

[![Python CI](https://github.com/nanotaboada/python-samples-fastapi-restful/actions/workflows/python-app.yml/badge.svg)](https://github.com/nanotaboada/python-samples-fastapi-restful/actions/workflows/python-app.yml)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=nanotaboada_python-samples-fastapi-restful&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=nanotaboada_python-samples-fastapi-restful)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/8f9bab37f6f444c895a8b25d5df772fc)](https://app.codacy.com/gh/nanotaboada/python-samples-fastapi-restful/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
[![codecov](https://codecov.io/gh/nanotaboada/python-samples-fastapi-restful/branch/master/graph/badge.svg?token=A1WNZPRQEJ)](https://codecov.io/gh/nanotaboada/python-samples-fastapi-restful)
[![CodeFactor](https://www.codefactor.io/repository/github/nanotaboada/python-samples-fastapi-restful/badge)](https://www.codefactor.io/repository/github/nanotaboada/python-samples-fastapi-restful)
[![codebeat badge](https://codebeat.co/badges/4c4f7c08-3b35-4b57-a875-bf2043efe515)](https://codebeat.co/projects/github-com-nanotaboada-python-samples-fastapi-restful-master)

## Manifesto

> "Nobody should start to undertake a large project. You start with a small _trivial_ project, and you should never expect it to get large. If you do, you'll just overdesign and generally think it is more important than it likely is at that stage. Or worse, you might be scared away by the sheer size of the work you envision. So start small, and think about the details. Don't think about some big picture and fancy design. If it doesn't solve some fairly immediate need, it's almost certainly over-designed. And don't expect people to jump in and help you. That's not how these things work. You need to get something half-way _useful_ first, and then others will say "hey, that _almost_ works for me", and they'll get involved in the project." — [Linus Torvalds](https://web.archive.org/web/20050404020308/http://www.linuxtimes.net/modules.php?name=News&file=article&sid=145)

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

## Documentation

```console
http://localhost:9000/docs
```

![API Documentation](assets/images/swagger.png)

## Credits

The solution has been coded using [Visual Studio Code](https://code.visualstudio.com/) with the official [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python) extension.

## Terms

All trademarks, registered trademarks, service marks, product names, company names, or logos mentioned on this repository are the property of their respective owners. All usage of such terms herein is for identification purposes only and constitutes neither an endorsement nor a recommendation of those items. Furthermore, the use of such terms is intended to be for educational and informational purposes only.
