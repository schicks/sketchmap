# Spec Kit: Plan Command

Create a technical implementation plan for an existing feature specification.

## Your Task

1. **Load Context**:
   - Read the feature spec from `specs/<number>-<name>/spec.md`
   - Review constitution at `/memory/constitution.md`
   - Check the plan template at `/templates/plan-template.md`

2. **Validate Prerequisites**:
   - Specification must exist and be complete
   - All `[NEEDS CLARIFICATION]` markers must be resolved
   - Requirements checklist must pass

3. **Create Implementation Plan**: Generate `plan.md` in the spec directory with:

   **Technical Context**:
   - Tech stack and framework choices
   - Architecture decisions with rationale
   - Dependencies and tools needed

   **Data Model Design**:
   - Entity definitions with attributes and types
   - Relationships and constraints
   - Database schema if applicable

   **API Contracts** (if applicable):
   - Endpoint definitions
   - Request/response formats
   - Error handling strategy

   **Implementation Phases**:
   - Phase 1: Setup and infrastructure
   - Phase 2: Core functionality
   - Phase 3: Integration and polish

   **Testing Strategy**:
   - Unit tests approach
   - Integration tests plan
   - E2E tests if needed

   **Quality Gates**:
   - Type checking requirements
   - Linting standards
   - Code coverage targets
   - Performance benchmarks

4. **Align with Constitution**: Ensure plan follows:
   - Code quality standards
   - Testing requirements
   - Documentation expectations
   - Architectural principles

5. **Generate Artifacts**:
   - Create `data-model.md` with detailed entity definitions
   - Create API contracts in `contracts/` directory if needed
   - Update plan checklist

6. **Report**: Provide user with:
   - Plan file location
   - Key technical decisions made
   - Estimated complexity
   - Ready for task generation

## Important Notes

- Focus on HOW to implement, not WHAT to build
- Make concrete technical decisions
- Consider maintainability and testing
- Document tradeoffs and alternatives
- Ensure alignment with constitutional principles
