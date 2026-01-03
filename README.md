# Sketchmap

A Python project set up with GitHub Spec Kit for specification-driven development.

## Overview

This project follows a spec-driven development approach using [GitHub Spec Kit](https://github.com/github/spec-kit), which provides a structured workflow for:

1. Defining requirements and user stories
2. Creating technical implementation plans
3. Generating actionable task lists
4. Implementing features systematically

## Project Structure

```
sketchmap/
├── .claude/
│   └── commands/          # Spec Kit slash commands
│       ├── speckit.constitution.md
│       ├── speckit.specify.md
│       ├── speckit.plan.md
│       ├── speckit.tasks.md
│       └── speckit.implement.md
├── memory/
│   └── constitution.md    # Project governance principles
├── specs/                 # Feature specifications
├── templates/             # Document templates
│   ├── spec-template.md
│   ├── plan-template.md
│   └── tasks-template.md
├── src/
│   └── sketchmap/         # Python package source code
└── tests/                 # Test files
```

## Development Workflow

### 1. Define Requirements
Use `/speckit.specify` to create a feature specification:
```
/speckit.specify
[Describe your feature requirements]
```

This creates a specification in `specs/` with:
- User stories and acceptance criteria
- Functional requirements
- Success criteria
- Data models

### 2. Create Implementation Plan
Use `/speckit.plan` to design the technical approach:
```
/speckit.plan
```

This generates a plan with:
- Architecture decisions
- Data model design
- API contracts
- Testing strategy

### 3. Generate Task List
Use `/speckit.tasks` to break down the work:
```
/speckit.tasks
```

This creates an ordered task list ready for implementation.

### 4. Implement Feature
Use `/speckit.implement` to execute the tasks:
```
/speckit.implement
```

This systematically implements each task following TDD and constitutional principles.

## Constitutional Principles

This project follows strict development principles defined in `/memory/constitution.md`:

- **Simplicity Over Complexity**: Clear, maintainable code
- **Test-Driven Development**: Tests before implementation
- **Clear Documentation**: Self-documenting code with docstrings
- **Type Safety**: Type hints throughout
- **Modularity and Reusability**: Loosely coupled components

## Getting Started

### Prerequisites
- Python 3.11 or higher
- uv or pip for package management

### Installation

```bash
# Using uv (recommended)
uv pip install -e ".[dev]"

# Or using pip
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=sketchmap --cov-report=term-missing

# Run type checking
mypy src/

# Run linting
ruff check src/ tests/
```

### Code Quality

```bash
# Format code
black src/ tests/

# Type checking
mypy src/ --strict

# Linting
ruff check src/ tests/

# Run all quality checks
pytest && mypy src/ --strict && ruff check src/ tests/
```

## Contributing

1. Start with `/speckit.constitution` to understand project principles
2. Use `/speckit.specify` to define new features
3. Follow the spec-driven workflow for all changes
4. Ensure all quality gates pass before committing

## License

[Add your license here]

## Resources

- [GitHub Spec Kit Documentation](https://github.com/github/spec-kit)
- [Spec-Driven Development Guide](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/)
