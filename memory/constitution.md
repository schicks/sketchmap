# Sketchmap Project Constitution

## Core Principles

### Simplicity Over Complexity
Code should be straightforward and maintainable. Avoid premature optimization and over-engineering. Choose the simplest solution that meets the requirements.

### Test-Driven Development
All features must be testable and include appropriate test coverage. Write tests before implementation when possible. Use pytest as the primary testing framework.

### Clear Documentation
Code should be self-documenting with clear naming conventions. Complex logic requires inline comments. Public APIs must include docstrings following PEP 257.

### Type Safety
Use Python type hints throughout the codebase. Run type checking with mypy to catch errors early. Types should be explicit and meaningful.

### Modularity and Reusability
Design components to be loosely coupled and highly cohesive. Favor composition over inheritance. Create reusable modules that can be tested independently.

## Technical Standards

### Python Standards
- Follow PEP 8 style guidelines
- Use Python 3.11+ features
- Type hints required for all public functions and methods
- Docstrings required for all public modules, classes, and functions

### Code Quality
- Maximum function complexity: 10 (McCabe)
- Maximum function length: 50 lines
- Line length: 88 characters (Black formatter)
- Test coverage target: 80% minimum

### Dependencies
- Minimize external dependencies
- Pin all dependency versions
- Regular security audits of dependencies
- Document rationale for each major dependency

## Development Workflow

### Specification-Driven Development
1. Define requirements in specs/ directory
2. Create implementation plan
3. Generate tasks checklist
4. Implement with tests
5. Validate against specification

### Code Review
- All changes require review
- Automated tests must pass
- Type checking must pass
- Code coverage must not decrease

### Version Control
- Descriptive commit messages
- Small, focused commits
- Branch naming: feature/, bugfix/, refactor/
- Never commit secrets or credentials

## Quality Gates

### Before Commit
- [ ] All tests pass
- [ ] Type checking passes (mypy)
- [ ] Linting passes (ruff)
- [ ] Code formatted (black)
- [ ] No security vulnerabilities

### Before Merge
- [ ] Code reviewed
- [ ] Documentation updated
- [ ] CHANGELOG updated
- [ ] Version bumped if needed

## Governance

This constitution governs all development activities in the Sketchmap project. Deviations from these principles require explicit justification and documentation.

**Version**: 1.0.0 | **Ratified**: 2026-01-03 | **Last Amended**: 2026-01-03
