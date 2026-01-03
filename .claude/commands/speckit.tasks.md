# Spec Kit: Tasks Command

Generate an actionable task list from the implementation plan.

## Your Task

1. **Load Required Documents**:
   - Implementation plan: `specs/<number>-<name>/plan.md`
   - Feature spec: `specs/<number>-<name>/spec.md`
   - Data model: `specs/<number>-<name>/data-model.md` (if exists)
   - Constitution: `/memory/constitution.md`

2. **Validate Prerequisites**:
   - Plan must exist and be complete
   - All design decisions must be made
   - No unresolved clarifications

3. **Generate Task List**: Create `tasks.md` with dependency-ordered tasks:

   **Format** (strict):
   ```markdown
   - [ ] [T001] [P] [US1] Create User model in src/models/user.py
   - [ ] [T002] Add email validation to User model
   - [ ] [T003] [P] Write tests for User model in tests/test_user.py
   ```

   Where:
   - `[T###]`: Sequential task ID
   - `[P]`: Optional, marks tasks that can run in parallel
   - `[US#]`: Optional, links to user story
   - Description: Clear action with file path

4. **Organize by Phases**:

   **Phase 1: Setup**
   - Development environment setup
   - Install dependencies
   - Initialize configuration files

   **Phase 2: Foundation**
   - Create base models/entities
   - Set up database migrations (if applicable)
   - Implement core utilities

   **Phase 3-N: User Stories** (in priority order)
   - Tests first (if TDD)
   - Models and business logic
   - API endpoints/interfaces
   - Integration points

   **Final Phase: Polish**
   - Documentation
   - Code cleanup
   - Performance optimization
   - Final testing

5. **Task Properties**:
   - Each task is independently executable
   - Clear success criteria
   - Includes specific file paths
   - Respects dependencies
   - Can be completed by an LLM without context

6. **Testing Integration**:
   - Follow constitutional TDD requirements
   - Test tasks before implementation tasks
   - Include unit, integration, and E2E tests as appropriate

7. **Report**: Provide user with:
   - Tasks file location
   - Total task count
   - Estimated phases
   - Ready for implementation

## Quality Standards

- Tasks are atomic and focused
- Dependencies are explicit
- File paths are specific
- Success criteria are clear
- Aligned with constitution and plan
