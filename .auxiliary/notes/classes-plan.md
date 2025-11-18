# Phase 1 Implementation Plan: Classes and Core Infrastructure

**Date:** 2025-11-18
**Session:** Setup and Planning
**Status:** Ready to begin implementation

## Setup Complete

Environment setup completed successfully:
- GitHub CLI installed (v2.83.1)
- Python tools installed (hatch, copier, emcd-agents)
- Project agents populated
- Language servers installed (mcp-language-server, pyright, ruff)
- Bash tool bypass wrapper configured

## Architecture Review Summary

The architecture document (architecture-initial.md) provides a solid foundation:

**Key Strengths:**
1. Clean Definition/Control split pattern from ai-experiments
2. Clear scope boundaries (no LLM client code, no template expansion)
3. Lightweight custom validation (no Pydantic/attrs dependency)
4. Immutable controls using frigid.DataclassProtocol
5. UI framework agnostic design
6. Simple dictionary-based type registry for Phase 1

**Core Patterns Identified from ai-experiments:**
- Descriptor-driven instantiation (TOML → Definition → Control)
- Species polymorphism (string type names → classes)
- Serialization/deserialization support
- Manager pattern for GUI integration (separate project concern)

## Initial Questions & Clarifications

### 1. Project Structure

**Implemented Structure** (per your feedback):
```
sources/vibecontrols/
├── __/                      # Common imports hub
│   ├── __init__.py
│   ├── imports.py           # Package-wide imports (abc, cabc, typx, immut, etc.)
│   └── nomina.py
├── __init__.py
├── exceptions.py            # Exception hierarchy (ControlError, ValidationError, etc.)
├── protocols.py             # ControlDefinition, Control base protocols
├── validation.py            # Validator framework (composable validators)
├── vulturefood.py           # Whitelist for dead code detection
└── controls/                # Control type implementations
    ├── __/                  # Subpackage imports hub
    │   └── __init__.py      # from ..__ import * + parent imports
    ├── __init__.py          # Public API exports
    ├── boolean.py           # BooleanHints, BooleanDefinition, Boolean (all together)
    ├── text.py              # (future) TextHints, TextDefinition, Text
    ├── interval.py          # (future) IntervalHints, IntervalDefinition, Interval
    ├── options.py           # (future) OptionsHints, OptionsDefinition, Options
    └── array.py             # (future) ArrayHints, ArrayDefinition, Array
```

**Key Decisions from Your Feedback:**
- Use `controls/` subdirectory (not `types/`)
- Keep Definition, Control, and Hints classes together per module
- Each control type is self-contained in its own file
- Protocols and validation stay at package level

### 2. Import Conventions

**Resolved:** Import pattern understood and implemented.
- Package-wide imports in `sources/vibecontrols/__/imports.py`
- Includes: `abc`, `cabc` (collections.abc), `typx` (typing_extensions), `immut` (frigid), `absent`/`is_absent`
- Subpackages do `from ..__ import *` in their `__/__init__.py`
- Pattern: `__.typx.Any`, `__.abc.abstractmethod`, `__.immut.DataclassObject`

### 3. Frigid DataclassProtocol Usage

**Resolved:** Pattern established per your guidance.
- **Abstract base protocols**: `__.immut.DataclassProtocol, __.typx.Protocol` with `@__.abc.abstractmethod`
- **Concrete implementations**: `__.immut.DataclassObject`
- DataclassProtocol already provides ABC functionality, no need for separate ABC inheritance
- Works with Generic types (confirmed for future Array implementation)

### 4. Testing Strategy
**Proposed Test Structure:**
```
tests/
├── unit/
│   ├── test_exceptions.py
│   ├── test_validation.py
│   ├── types/
│   │   ├── test_boolean.py
│   │   ├── test_text.py
│   │   ├── test_interval.py
│   │   ├── test_options.py
│   │   └── test_array.py
├── integration/
│   ├── test_serialization.py
│   └── test_descriptors.py
└── fixtures/
    └── toml_examples/
```

**Question:** Is Hypothesis already a project dependency for property-based testing?

### 5. Validation Framework Design

**Implemented:** Classes with `__call__` pattern (as you confirmed).
- `Validator` protocol (callable interface - can be class or function)
- `CompositeValidator` for chaining
- `TypeValidator`, `RangeValidator`, `LengthValidator`, `ChoiceValidator`
- All validators are reusable, composable, and testable

### 6. Default Values and Initialization

**Resolved:** Using `produce_default()` (per your guidance on etymology).
- Method name follows project convention (Germanic "produce" not Latin "get")
- Boolean implementation provides sensible default: `default: bool = False`
- Future types should also provide sensible defaults per ai-experiments pattern

### 7. Serialization Scope

**Implemented:** Focus on control creation first (per your guidance).
- `serialize_value()` method on Definition
- `serialize()` method on Control
- Boolean demonstrates pattern: booleans serialize as-is (JSON-compatible)
- TOML descriptor parsing deferred to Phase 2
- Current focus: proving the Definition → Control pattern works

## Implementation Approach (Based on Handoff)

### Session 1: Foundation (This Session)

Following the recommended approach from handoff:

#### Step 1: Core Infrastructure (Quick Wins) ✅
- [x] Environment setup complete
- [x] Create exception hierarchy
  - ControlError (base)
  - ValidationError
  - ConstraintError
  - ConfigurationError
- [x] Define base protocols
  - ControlDefinition protocol
  - Control protocol
  - All abstractmethod requirements documented

#### Step 2: Validation Framework ✅
- [x] Validator protocol
- [x] CompositeValidator implementation
- [x] Common validators:
  - TypeValidator
  - RangeValidator
  - LengthValidator
  - ChoiceValidator
  - (PatternValidator deferred - can be added when needed for Text)
- [x] Unit tests for validators (deferred per your guidance on testing)

#### Step 3: Boolean Type (Proof of Concept) ✅
**Why Boolean first?** Simplest type, validates entire pattern works.

- [x] BooleanHints dataclass (frozen=True)
- [x] BooleanDefinition (DataclassObject)
  - validate_value()
  - create_control()
  - serialize_value()
  - produce_default()
- [x] Boolean control (DataclassObject)
  - update()
  - toggle() [type-specific method]
  - serialize()
- [x] Manual testing verified:
  - Creation with valid/invalid parameters
  - Validation (valid/invalid values)
  - Default values
  - Immutable updates (returns new instance)
  - Serialization roundtrips
  - toggle() behavior

#### Success Criteria for Step 3:
If Boolean type works perfectly with 100% test coverage, the pattern is validated and we can confidently implement remaining types.

### Session 2: Remaining Core Types

#### Text Type
- TextHints (multiline, placeholder)
- TextDefinition (optional pattern validation, length constraints)
- Text control
- Tests

#### Interval Type
- IntervalHints (widget_preference, orientation)
- IntervalDefinition (minimum, maximum, step/grade)
- Interval control (increment/decrement methods?)
- Tests

#### Options Type
- OptionsHints
- OptionsDefinition (choices, allow_multiple?)
- Options control
- Tests

#### Array Type (Most Complex)
- ArrayHints (orientation, collapsible)
- ArrayDefinition (element_definition, size constraints)
  - Generic type support
- Array control
  - append(), remove_at(), insert_at(), reorder()
- Tests for:
  - Nested arrays
  - Size constraints
  - Element validation
  - Immutable operations

### Session 3: Serialization & Registry

- [ ] BUILTIN_TYPES dictionary
- [ ] descriptor_to_definition() function
- [ ] JSON serialization helpers
- [ ] Roundtrip tests
- [ ] TOML parser integration (if time permits)

## Initial Thoughts & Design Notes

### On Immutability
The immutable update pattern is elegant:
```python
control = boolean_def.create_control(True)
updated = control.update(False)  # returns new instance
toggled = control.toggle()       # returns new instance
```

This prevents accidental state mutations and makes controls safe to share.

### On Validation Composition
The composable validator pattern is powerful:
```python
validator = CompositeValidator(
    TypeValidator(float),
    RangeValidator(0.0, 1.0)
)
# Apply both validations in sequence
value = validator(0.7)  # passes both
```

This allows complex validation logic without inheritance.

### On Type-Specific Methods
Each control type can add convenience methods:
- Boolean: `toggle()`
- Interval: `increment()`, `decrement()`?
- Array: `append()`, `remove_at()`, etc.
- Options: `select_next()`, `select_previous()`?

These make controls more ergonomic while maintaining immutability.

### On Error Messages
Should validation errors include context?
```python
raise ValidationError(
    f"Invalid value for control '{name}': {message}",
    control_name=name,
    invalid_value=value
)
```

Or keep simple for Phase 1?

### On Hints Design
The per-type hint classes are excellent. They avoid the "common denominator" problem where every hint must work for every control type.

Each type gets exactly the hints it needs, nothing more.

## Potential Challenges

### 1. Frigid DataclassProtocol Learning Curve
Never used frigid before. Need to understand:
- How concealment works
- How to properly initialize immutable dataclasses
- How field() factory patterns work
- Whether frozen=True is automatic

**Mitigation:** Start simple with Boolean, learn incrementally.

### 2. Generic Array Type
The Array type uses `Generic[T]` which adds complexity:
```python
class ArrayDefinition(DataclassProtocol, ABC, Generic[T]):
    element_definition: ControlDefinition
```

**Question:** Does DataclassProtocol work with Generic? Need to test.

### 3. Circular Type References
Control has `definition: ControlDefinition`
ControlDefinition.create_control() returns `Control`

Need forward references and proper TYPE_CHECKING imports.

### 4. TOML Descriptor Parsing
The TOML format has nested structures:
```toml
[[variables]]
species = 'flex-array'
[variables.element]
species = 'text'
```

**Phase 2 concern**, but need to keep descriptor_to_definition() design in mind.

## Open Questions for Discussion

1. **Module structure:** Confirm proposed package layout
2. **Import conventions:** Review __.imports pattern before starting
3. **frigid patterns:** Any examples or docs to review?
4. **Test coverage target:** Aim for 100% for core types?
5. **Descriptor format:** Stick with ai-experiments format or evolve?
6. **Default auto-generation:** Auto-generate defaults or require explicit?
7. **Error context:** Rich error messages now or later?
8. **Array generics:** Confirm Generic[T] + DataclassProtocol compatibility

## Next Actions

### Immediate (This Session):
1. ✅ Complete environment setup
2. ✅ Review architecture document
3. ✅ Review reference implementations
4. ✅ Create this planning document
5. [ ] Commit planning document

### Next Session Start:
1. Review __.imports pattern in codebase
2. Check if frigid is already in dependencies
3. Create exception hierarchy
4. Define base protocols
5. Implement validation framework
6. Start Boolean type implementation

## References

- Architecture: `.auxiliary/notes/architecture-initial.md`
- AI Experiments Controls: `https://github.com/emcd/ai-experiments/blob/master/sources/aiwb/controls/core.py`
- AI Experiments GUI: `https://github.com/emcd/ai-experiments/blob/master/sources/aiwb/gui/controls.py`
- Descriptor Example: `https://github.com/emcd/ai-experiments/blob/master/data/prompts/descriptors/pair-programmer.toml`

## Success Metrics

**Phase 1 Complete When:**
- [ ] All 5 core types implemented
- [ ] All types have comprehensive tests (target: >90% coverage)
- [ ] All tests passing
- [ ] Serialization roundtrips work
- [ ] BUILTIN_TYPES registry functional
- [ ] descriptor_to_definition() works for basic cases
- [ ] Documentation strings complete
- [ ] At least one working example

**Quality Bar:**
- No shortcuts on immutability
- No Pydantic/attrs leakage
- Clean separation of concerns
- Each type fully tested before moving to next
- Boolean type serves as perfect template

## Notes from Handoff

Key advice from previous session:
> "Your instinct is right - implement classes and test control creation first, then serialization. Start with Boolean as the proof-of-concept. Once that's solid, the rest will follow the same pattern."

> "The architecture is in excellent shape: Clean and simple - No over-engineering, just what's needed for Phase 1"

This gives me confidence the design is sound. Time to implement!

---

**Ready to begin implementation.** 🚀
