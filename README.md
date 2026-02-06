# Study Planner CLI

[![Coverage Status](https://img.shields.io/badge/coverage-99%25-brightgreen)](#tests-and-code-coverage)

## Introduction

An offline, dependency-free Python CLI application built to practice Clean Architecture, SOLID principles, and type annotations.  
The app stores data locally in a JSON file and includes unit, integration, and end-to-end tests.  

## Architecture

- `src/domain`: Entities, value objects, domain errors  
- `src/application`: Use cases, ports (interfaces), application errors  
- `src/adapters`: Repository implementations (in-memory + JSON file)  
- `src/cli`: Command-line interface  
- `tests/unit`: Unit tests  
- `tests/integration`: Integration tests  
- `tests/e2e`: End-to-end tests  

## Development Environment

At the bare minimum you'll need the following:

1. [Python 3.11+](https://www.python.org/)

Recommended:

1. [virtualenv](https://virtualenv.pypa.io/)
2. [ruff](https://github.com/astral-sh/ruff)
3. [mypy](https://mypy-lang.org/)

## Local Setup

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -U pip
pip install -r requirements.txt
```

## CLI Usage

```bash
python -m src.cli --help
python -m src.cli add-course "Algorithms"
python -m src.cli list-courses
python -m src.cli add-topic <course_id> "Graphs"
python -m src.cli plan-session <topic_id> 2026-02-08 45
python -m src.cli complete-session <session_id>
python -m src.cli list-sessions
python -m src.cli weekly-report 2026-02-03
```

## Tests and Code Coverage

Install testing dependencies:

```bash
pip install pytest pytest-cov
```

### Unit Tests + Coverage
```bash
pytest -vv --cov --cov-report=term-missing tests/unit
```

### Integration Tests + Coverage
```bash
pytest -vv --cov --cov-report=term-missing tests/integration
```

### End-to-End Tests + Coverage
```bash
pytest -vv --cov --cov-report=term-missing tests/e2e
```

### Full Test Suite + Coverage
```bash
pytest -vv --cov --cov-report=term-missing
```

Current coverage target: **99%** (maintained).

## Linting

```bash
pip install ruff
ruff check .
```

## Type Checking

```bash
pip install mypy
mypy .
```

## Working Features

Feature | Type | Command | Access
------------ | ------------- | ------------- | -------------
Add a course | CLI | `add-course` | Local
List courses | CLI | `list-courses` | Local
Delete course | CLI | `delete-course` | Local
Add topic | CLI | `add-topic` | Local
List topics | CLI | `list-topics` | Local
Remove topic | CLI | `remove-topic` | Local
Plan session | CLI | `plan-session` | Local
Complete session | CLI | `complete-session` | Local
List sessions | CLI | `list-sessions` | Local
Weekly report | CLI | `weekly-report` | Local

## Highlights
 - [x] Clean Architecture
 - [x] SOLID Principles
 - [x] Type Annotations
 - [x] Unit Testing
 - [x] Integration Testing
 - [x] End2End Testing
 - [x] Ruff Linting
 - [x] MyPy Typing
 - [x] High Code Coverage Target (99%)

## Roadmap
 - [ ] Add CLI output formatting
 - [ ] Add richer reporting (streaks, per-topic charts)
 - [ ] Add config file support
 - [ ] Add CI pipeline
