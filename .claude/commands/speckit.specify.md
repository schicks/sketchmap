# Spec Kit: Specify Command

Create a feature specification based on the user's requirements.

## Your Task

1. **Parse Requirements**: Understand the feature description provided by the user

2. **Generate Branch Name**: Create a descriptive branch name using format `feature/<short-name>-<number>`
   - Short name: 2-4 words, action-noun format (e.g., "user-auth", "api-integration")
   - Number: Next sequential number based on existing specs

3. **Create Feature Directory**: Set up directory structure:
   ```
   specs/
   └── <number>-<short-name>/
       ├── spec.md
       └── checklists/
           └── requirements.md
   ```

4. **Write Specification**: Create `spec.md` following the template in `/templates/spec-template.md`:
   - **Overview**: Brief description and goals
   - **User Stories**: Prioritized (P1, P2, P3), independently testable
   - **Functional Requirements**: Specific, numbered (FR-001, FR-002, etc.)
   - **Key Entities**: Data models and relationships
   - **Success Criteria**: Measurable, technology-agnostic outcomes
   - **Edge Cases**: Boundary conditions and error scenarios
   - **Acceptance Scenarios**: Given-When-Then format

5. **Focus on WHAT, not HOW**:
   - Describe desired behavior and outcomes
   - Avoid implementation details
   - Write for business stakeholders
   - Use technology-agnostic language

6. **Mark Clarifications**: Use `[NEEDS CLARIFICATION]` only for:
   - Decisions with multiple reasonable interpretations
   - Significant scope/UX/security implications
   - Maximum 3 clarification markers

7. **Generate Requirements Checklist**: Create validation checklist at `checklists/requirements.md`

8. **Report**: Provide user with:
   - Branch name created
   - Spec file location
   - Summary of specification
   - Any clarifications needed

## Quality Standards

- All requirements must be testable
- Success criteria must be measurable
- No implementation details
- Scope must be clearly bounded
- User stories must be independently deliverable
