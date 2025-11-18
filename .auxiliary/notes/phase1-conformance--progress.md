# Phase 1 Code Conformance Refactoring

## Context and References

**Implementation Title**: Conform Phase 1 implementation to project coding standards
**Start Date**: 2025-11-18
**Reference Files**:
- `.auxiliary/instructions/practices.rst` - General development practices
- `.auxiliary/instructions/practices-python.rst` - Python-specific practices
- `sources/vibecontrols/controls/boolean.py` - Example implementation to conform
- `sources/vibecontrols/protocols.py` - To be renamed to interfaces.py
- `sources/vibecontrols/validation.py` - Validator framework to conform

**Design Documents**: N/A (conformance to existing practices)

**Session Notes**: TodoWrite tracking active

## Design and Style Conformance Checklist

- [x] Module organization follows practices guidelines
- [ ] Function signatures use wide parameter, narrow return patterns
- [ ] Type annotations use __.ddoc.Doc on Annotated (not docstring params)
- [ ] Exception handling follows Omniexception → Omnierror hierarchy
- [x] Naming follows nomenclature conventions (updating to match)
- [ ] Immutability preferences applied (all DataclassObject)
- [x] Code style follows formatting guidelines (spaces, quotes, etc.)

## Implementation Progress Checklist

### Structural Changes
- [x] Move vulturefood.py to .auxiliary/configuration/
- [x] Rename controls/__/__init__.py to controls/__.py
- [x] Remove __all__ from controls/__init__.py
- [x] Add dataclasses import to __/imports.py as dcls

### Exception Naming
- [x] ValidationError → ControlInvalidity
- [x] ConstraintError → ConstraintViolation
- [x] ConfigurationError → DefinitionInvalidity
- [x] Update all references in validation.py
- [ ] Update references in interfaces.py (formerly protocols.py)
- [ ] Update references in boolean.py
- [ ] Update .auxiliary/configuration/vulturefood.py

### File and Class Renaming
- [ ] protocols.py → interfaces.py
- [ ] Update all imports of protocols module
- [ ] TypeValidator → ClassValidator
- [ ] RangeValidator → IntervalValidator
- [ ] LengthValidator → SizeValidator
- [ ] ChoiceValidator → SelectionValidator

### Method Renaming
- [ ] create_control() → produce_control()
- [ ] update() → copy()
- [ ] Update all implementations and calls

### Validator Framework
- [ ] Make Validator inherit from DataclassProtocol + Protocol
- [ ] Make Validator.__call__ abstract
- [ ] Make all validators inherit from Validator
- [ ] Update validator implementations

### BooleanHints
- [ ] Change from @dataclass(frozen=True) to DataclassObject
- [ ] Remove dataclass import from boolean.py

### Documentation Conversion
- [ ] Convert boolean.py docstrings to __.ddoc.Doc on Annotated
- [ ] Convert validation.py docstrings to __.ddoc.Doc on Annotated
- [ ] Convert interfaces.py docstrings to __.ddoc.Doc on Annotated
- [ ] Ensure narrative mood (third person) in all docstrings

## Quality Gates Checklist

- [ ] Linters pass (`hatch --env develop run linters`)
- [ ] Type checker passes
- [ ] Tests pass (`hatch --env develop run testers`)
- [ ] Manual testing confirms Boolean still works
- [ ] Code review ready

## Decision Log

- **2025-11-18**: Following user feedback to conform to project standards
  - Using __.ddoc.Doc instead of Google/NumPy docstrings
  - Exception naming follows nomenclature guide (-Invalidity, -Violation)
  - Validators as proper protocol with DataclassProtocol inheritance
  - Method naming: produce not create, copy not update

## Handoff Notes

**Current State**:
- Structural changes complete (file moves, __all__ removal, imports)
- Exception renaming in progress (exceptions.py and validation.py done)
- Still need: file renaming, method renaming, validator framework changes, documentation conversion

**Next Steps**:
1. Rename protocols.py → interfaces.py and update all imports
2. Rename validator classes (Type→Class, Range→Interval, etc.)
3. Make validators inherit from Validator protocol
4. Rename methods (create_control→produce_control, update→copy)
5. Fix BooleanHints to use DataclassObject
6. Convert all docstrings to __.ddoc.Doc on Annotated
7. Run linters and tests
8. Commit all changes

**Known Issues**: None yet

**Context Dependencies**:
- Must maintain backwards compatibility with existing Boolean implementation tests
- Pattern established by Boolean type serves as template for future types
