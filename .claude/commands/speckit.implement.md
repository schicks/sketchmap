# Spec Kit: Implement Command

Execute the implementation based on the task list.

## Your Task

1. **Load Context**:
   - Task list: `specs/<number>-<name>/tasks.md`
   - Implementation plan: `specs/<number>-<name>/plan.md`
   - Feature spec: `specs/<number>-<name>/spec.md`
   - Constitution: `/memory/constitution.md`

2. **Validate Readiness**:
   - All checklists must be complete (or user override)
   - Tasks must be well-defined
   - Development environment must be ready

3. **Execute Tasks by Phase**:

   For each task:
   - Read task description and requirements
   - Implement the change
   - Follow constitutional principles (TDD, type hints, documentation)
   - Run relevant tests
   - Mark task as `[X]` when complete
   - Report progress

4. **Implementation Rules**:

   **Test-Driven Development**:
   - Write tests before implementation
   - Ensure tests fail before implementing
   - Implement minimal code to pass tests
   - Refactor while keeping tests green

   **Code Quality**:
   - Add type hints to all functions
   - Include docstrings for public APIs
   - Follow PEP 8 / Black formatting
   - Keep functions small and focused

   **Error Handling**:
   - Validate inputs appropriately
   - Provide meaningful error messages
   - Log errors for debugging
   - Handle edge cases from spec

5. **Progress Tracking**:
   - Update tasks.md with `[X]` for completed tasks
   - Report completion after each task
   - Stop on errors and explain issue
   - Ask for guidance if task is unclear

6. **Quality Validation**:
   - Run tests after each task
   - Check type hints with mypy
   - Verify linting passes
   - Ensure code coverage targets met

7. **Completion**:
   - Verify all tasks marked complete
   - Run full test suite
   - Generate summary report
   - Check that spec requirements are met

## Important Notes

- Follow the constitutional principles throughout
- Test frequently and incrementally
- Keep commits focused and atomic
- Document as you go
- Stop and ask if requirements are unclear
- Respect the spec-driven workflow
