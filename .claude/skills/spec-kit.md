# Spec Kit Skill

This skill enables specification-driven development using the GitHub Spec Kit workflow. Use this skill when working on feature development in this repository.

## When to Use This Skill

Activate this skill when:
- Starting a new feature or component
- Breaking down a complex task into specifications
- Following a structured development approach
- Ensuring alignment with project constitutional principles

## Constitutional Principles

This project follows strict development standards defined in `/memory/constitution.md`:

- **Simplicity Over Complexity**: Clear, maintainable code
- **Test-Driven Development**: Tests before implementation
- **Clear Documentation**: Self-documenting code with docstrings
- **Type Safety**: Type hints throughout (Python 3.11+)
- **Modularity and Reusability**: Loosely coupled components

### Quality Standards
- Maximum function complexity: 10 (McCabe)
- Maximum function length: 50 lines
- Test coverage target: 80% minimum
- All public functions need type hints and docstrings
- Follow PEP 8 and use Black formatter (88 char line length)

## Spec-Driven Workflow

The spec kit provides a five-stage development workflow:

### Stage 1: Constitution
**Purpose**: Review and maintain project governance principles

**When to use**:
- At project start to understand principles
- When updating development standards
- When clarifying technical direction

**Actions**:
1. Read `/memory/constitution.md`
2. Ensure all development aligns with constitutional principles
3. Update constitution if project standards change (bump version, update date)

### Stage 2: Specify
**Purpose**: Define WHAT to build (requirements and user stories)

**When to use**:
- Starting a new feature
- User describes a feature request
- Breaking down a complex requirement

**Actions**:
1. Parse user requirements
2. Generate descriptive branch name: `feature/<short-name>-<number>`
3. Create spec directory: `specs/<number>-<short-name>/`
4. Write `spec.md` using template at `/templates/spec-template.md`:
   - Overview and goals
   - User stories (P1, P2, P3 prioritized)
   - Functional requirements (FR-001, FR-002...)
   - Key entities (data models)
   - Success criteria (measurable)
   - Edge cases and error scenarios
   - Acceptance scenarios (Given-When-Then)
   - Out of scope items
5. Create `checklists/requirements.md` for validation
6. Mark unclear items with `[NEEDS CLARIFICATION]` (max 3)

**Focus**: WHAT not HOW - describe desired behavior, stay technology-agnostic

### Stage 3: Plan
**Purpose**: Design HOW to implement (technical approach)

**When to use**:
- After specification is complete
- Before breaking down into tasks
- When making architecture decisions

**Prerequisites**:
- Specification exists and is complete
- All `[NEEDS CLARIFICATION]` markers resolved
- Requirements checklist passes

**Actions**:
1. Read spec from `specs/<number>-<name>/spec.md`
2. Review constitution and plan template
3. Create `plan.md` in spec directory using `/templates/plan-template.md`:
   - Technical context (stack, framework, tools)
   - Architecture decisions with rationale
   - Data model design (detailed entities)
   - API contracts (if applicable)
   - Implementation phases (Setup, Core, Integration)
   - Testing strategy (unit, integration, E2E)
   - Quality gates
   - File structure
4. Create `data-model.md` with detailed entity definitions
5. Create API contracts in `contracts/` if needed
6. Ensure alignment with constitutional principles

**Focus**: HOW to implement with concrete technical decisions

### Stage 4: Tasks
**Purpose**: Generate actionable, ordered task list

**When to use**:
- After implementation plan is complete
- Before starting implementation
- When breaking down work into executable steps

**Prerequisites**:
- Plan exists and is complete
- All design decisions made
- No unresolved clarifications

**Actions**:
1. Load plan, spec, data model, and constitution
2. Create `tasks.md` using `/templates/tasks-template.md`
3. Generate tasks in strict format:
   ```markdown
   - [ ] [T001] [P] [US1] Clear action with file path
   ```
   - `[T###]`: Sequential task ID
   - `[P]`: Optional parallel execution marker
   - `[US#]`: Optional user story reference
4. Organize by phases:
   - **Phase 1: Setup** (environment, dependencies, config)
   - **Phase 2: Foundation** (base models, utilities)
   - **Phase 3-N: User Stories** (tests first, then implementation)
   - **Final Phase: Polish** (docs, cleanup, optimization)
5. Ensure tasks are:
   - Atomic and focused
   - Dependency-ordered
   - Include specific file paths
   - Have clear success criteria
   - Executable by an LLM without additional context

**Focus**: Actionable, ordered tasks following TDD principles

### Stage 5: Implement
**Purpose**: Execute tasks systematically

**When to use**:
- After task list is complete
- Ready to write code
- Following test-driven development

**Prerequisites**:
- All checklists complete (or user override)
- Tasks well-defined
- Development environment ready

**Actions**:
1. Load tasks, plan, spec, and constitution
2. For each task in order:
   - Read task description and requirements
   - **If test task**: Write failing test first
   - **If implementation task**: Write minimal code to pass tests
   - Follow constitutional principles (TDD, type hints, docstrings)
   - Run relevant tests
   - Mark task as `[X]` when complete
   - Report progress
3. Follow implementation rules:
   - **TDD**: Tests before implementation, red-green-refactor
   - **Type hints**: All functions typed
   - **Docstrings**: All public APIs documented
   - **PEP 8/Black**: Consistent formatting
   - **Small functions**: Max 50 lines, complexity ≤ 10
4. Progress tracking:
   - Update `tasks.md` with `[X]` for completed tasks
   - Stop on errors and explain
   - Ask for guidance if unclear
5. Quality validation:
   - Run tests after each task
   - Check type hints with mypy
   - Run ruff linting
   - Verify coverage targets (80%+)
6. Completion:
   - All tasks marked complete
   - Full test suite passing
   - Generate summary report

**Focus**: Systematic, test-driven implementation following all quality gates

## Automatic Workflow Detection

When the user asks you to build a feature or implement functionality, automatically guide them through the spec-driven workflow:

1. **If no spec exists**: Start with Stage 2 (Specify)
2. **If spec exists but no plan**: Move to Stage 3 (Plan)
3. **If plan exists but no tasks**: Move to Stage 4 (Tasks)
4. **If tasks exist**: Execute Stage 5 (Implement)

## Key Artifacts and Locations

- **Constitution**: `/memory/constitution.md` - Project principles
- **Templates**: `/templates/` - Spec, plan, and task templates
- **Specs**: `specs/<number>-<name>/` - Feature specifications
  - `spec.md` - Requirements and user stories
  - `plan.md` - Technical implementation plan
  - `data-model.md` - Detailed entity definitions
  - `tasks.md` - Actionable task list
  - `checklists/` - Validation checklists
  - `contracts/` - API contracts (if applicable)

## Quality Gates

### Before Each Commit
- [ ] All tests pass
- [ ] Type checking passes (mypy --strict)
- [ ] Linting passes (ruff)
- [ ] Code formatted (black)
- [ ] Test coverage ≥ 80%

### Before Merge
- [ ] Code reviewed
- [ ] Documentation updated
- [ ] No security vulnerabilities
- [ ] Performance benchmarks met

## Best Practices

1. **Always read the constitution first** to understand project principles
2. **Complete each stage** before moving to the next
3. **Resolve all clarifications** before planning
4. **Follow TDD** - write tests before implementation
5. **Keep tasks atomic** - one clear action per task
6. **Update checklists** as you complete tasks
7. **Report progress** to the user regularly
8. **Stop on errors** - don't skip broken tests
9. **Ask for guidance** when requirements are unclear
10. **Validate quality** after every task

## Example Usage Flow

**User**: "Add a feature to parse markdown files and extract metadata"

**Your response**:
1. Recognize this is a new feature request
2. Start with Stage 2 (Specify):
   - Generate branch name: `feature/markdown-parser-001`
   - Create `specs/001-markdown-parser/`
   - Write `spec.md` with user stories, requirements, entities
   - Create requirements checklist
   - Ask for any clarifications
3. Move to Stage 3 (Plan):
   - Design data model for metadata
   - Choose parsing library
   - Define API contracts
   - Create testing strategy
   - Write `plan.md`
4. Move to Stage 4 (Tasks):
   - Break down into atomic tasks
   - Order by dependencies
   - Include test tasks before implementation tasks
   - Write `tasks.md`
5. Execute Stage 5 (Implement):
   - Work through tasks in order
   - Write tests first (TDD)
   - Implement functionality
   - Validate quality gates
   - Update task checklist

## Common Patterns

### New Feature Development
```
User request → Specify → Plan → Tasks → Implement
```

### Extending Existing Feature
```
Read existing spec → Update spec → Update plan → Add tasks → Implement
```

### Bug Fix with Unclear Cause
```
Specify bug behavior → Plan investigation → Create debug tasks → Implement fix
```

### Refactoring
```
Specify desired improvements → Plan approach → Break into tasks → Implement incrementally
```

## Remember

- **WHAT before HOW**: Specify requirements before technical design
- **HOW before DO**: Plan implementation before writing code
- **DO incrementally**: Execute tasks one at a time with validation
- **Quality always**: Never skip tests, type checking, or linting
- **Constitution rules**: All decisions must align with project principles

This workflow ensures systematic, testable, and maintainable development aligned with project governance.
