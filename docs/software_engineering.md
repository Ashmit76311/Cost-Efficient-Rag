# Software Engineering

Software engineering is the systematic application of engineering principles to the design, development, testing, deployment, and maintenance of software systems. It emphasizes structured processes, quality assurance, and collaboration.

## Software Development Life Cycle (SDLC)

The SDLC describes the stages of software development:

1. **Requirements Gathering**: Understanding what the software should do. Functional requirements describe features; non-functional requirements cover performance, security, and scalability.
2. **Design**: Architectural decisions, data models, interface design, and component interactions. High-level design defines the overall system architecture; low-level design specifies module-level details.
3. **Implementation**: Writing the actual code based on the design specifications.
4. **Testing**: Verifying the software works correctly and meets requirements.
5. **Deployment**: Releasing the software to production.
6. **Maintenance**: Bug fixes, updates, and feature additions after deployment.

Common SDLC models include Waterfall (sequential, rigid), Agile (iterative, flexible), and Spiral (risk-driven, iterative).

## Design Patterns

Design patterns are reusable solutions to common software design problems. They are categorized into three types:

**Creational Patterns**: Deal with object creation mechanisms.
- Singleton: Ensures a class has only one instance. Used for database connections, configuration managers.
- Factory Method: Creates objects without specifying the exact class. Useful when the creation logic is complex.
- Builder: Constructs complex objects step by step.

**Structural Patterns**: Deal with object composition and relationships.
- Adapter: Converts one interface to another. Useful for integrating legacy systems.
- Decorator: Adds behavior to objects dynamically without modifying their class.
- Facade: Provides a simplified interface to a complex subsystem.

**Behavioral Patterns**: Deal with object interaction and responsibility.
- Observer: Defines a one-to-many dependency where multiple objects are notified of state changes. Used in event systems and reactive programming.
- Strategy: Defines a family of algorithms and makes them interchangeable.
- Iterator: Provides sequential access to elements without exposing the underlying structure.

## Testing

Software testing ensures quality and correctness at different levels:

**Unit Testing** tests individual functions or methods in isolation. Tests should be fast, independent, and repeatable. Frameworks include JUnit (Java), pytest (Python), and Jest (JavaScript). Unit tests typically follow the Arrange-Act-Assert pattern.

**Integration Testing** tests how multiple components work together. This includes testing API endpoints, database interactions, and service communication.

**End-to-End (E2E) Testing** tests the complete application flow from the user's perspective. Tools include Selenium, Cypress, and Playwright.

**Test-Driven Development (TDD)** writes tests before implementation code. The cycle is: write a failing test, write minimal code to pass, refactor. TDD encourages modular design and comprehensive test coverage.

## Version Control

Version control systems track changes to code over time. Git is the most widely used VCS. Key Git concepts include commits (snapshots of code), branches (parallel development lines), merging (combining branches), and rebasing (replaying commits onto a different base).

Common branching strategies include Git Flow (feature branches, develop, release, hotfix branches), GitHub Flow (main branch + feature branches with pull requests), and trunk-based development (frequent small commits to main).

## Code Quality

Code quality practices include:
- **Code reviews**: Peers review code changes before merging. Catches bugs, enforces standards, and spreads knowledge.
- **Linting**: Automated tools (ESLint, Pylint, Flake8) check code style and catch common errors.
- **Refactoring**: Restructuring existing code without changing its behavior. Common refactorings include extracting methods, renaming variables, and removing dead code.
- **Documentation**: Comments for complex logic, docstrings for API documentation, and README files for project overview. Over-documentation is as bad as under-documentation.
- **SOLID Principles**: Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion. These principles guide object-oriented design toward maintainable and extensible code.
