# Business rules package
This package contains business logic and doesn't depend on any framework or
representation implementation (web, cli)

## Structure
- commands: contains commands classes
- entities: contains business entities (Note)
- interfaces: contains abstract base classes for commands, processors and repository
- processors: contains commands processors implementations

## Note on location
It must be on the root level, but if we place it in root, import from it will not work