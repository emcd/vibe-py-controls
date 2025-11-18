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
**Question:** What should the module structure look like?

**Proposed:**
```
sources/vibecontrols/
├── __/                      # Common imports hub
│   └── imports.py
├── exceptions.py            # Exception hierarchy
├── protocols.py             # ControlDefinition, Control protocols
├── validation.py            # Validator framework
├── types/                   # Control type implementations
│   ├── __init__.py
│   ├── boolean.py
│   ├── text.py
│   ├── interval.py
│   ├── options.py
│   └── array.py
├── hints.py                 # UI hint classes
├── descriptors.py           # TOML parsing, BUILTIN_TYPES
└── serialization.py         # JSON serialization utilities
```

**Need confirmation:** Is this structure aligned with project conventions?

### 2. Import Conventions
**Observation:** Architecture doc mentions `__.typx.Any` pattern.

**Question:** Should I review `sources/vibecontrols/__/imports.py` first to understand the import hub pattern, or is there a template/example to follow?

### 3. Frigid DataclassProtocol Usage
**Understanding:** From architecture, frigid.DataclassProtocol provides:
- Immutability
- Concealment (private attributes)
- Keyword-only init

**Question:** Are there specific patterns or gotchas I should be aware of when combining:
- Protocol (structural typing)
- DataclassProtocol (immutability)
- ABC abstractmethod (enforcement)

The architecture shows this hybrid approach for Array types. Should all Definition and Control classes use this pattern?

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
**Architecture shows:**
- Validator protocol (callable)
- CompositeValidator (chains validators)
- Specific validators (TypeValidator, RangeValidator)

**Question:** Should validators be:
- Reusable instances? `type_validator = TypeValidator(bool)`
- Factory functions? `def type_validator(expected_type): ...`
- Classes with `__call__`? (as shown in architecture)

**Preference:** Classes seem most flexible and testable.

### 6. Default Values and Initialization
**From ai-experiments:** Definitions have `produce_default()` method.

**Architecture shows:** Each definition has a `get_default()` method.

**Question:** Should we auto-generate sensible defaults if not specified?
- Boolean → False
- Text → ""
- Interval → minimum value
- Options → first choice
- Array → empty sequence

Or require explicit defaults always?

### 7. Serialization Scope
**Architecture mentions two layers:**
1. Value Layer (just current values)
2. Definition Layer (full schema)

**For Phase 1, focusing on:**
- Control → JSON value serialization
- Definition → dict serialization (for introspection)

**Deferred:**
- TOML descriptor parsing (Phase 2)
- Full roundtrip Definition serialization

**Is this correct?**

## Implementation Approach (Based on Handoff)

### Session 1: Foundation (This Session)

Following the recommended approach from handoff:

#### Step 1: Core Infrastructure (Quick Wins)
- [x] Environment setup complete
- [ ] Create exception hierarchy
  - ControlError (base)
  - ValidationError
  - ConfigurationError
  - ConstraintError
- [ ] Define base protocols
  - ControlDefinition protocol
  - Control protocol
  - Document abstractmethod requirements

#### Step 2: Validation Framework
- [ ] Validator protocol
- [ ] CompositeValidator implementation
- [ ] Common validators:
  - TypeValidator
  - RangeValidator
  - LengthValidator
  - PatternValidator (for Text)
  - ChoiceValidator (for Options)
- [ ] Unit tests for validators

#### Step 3: Boolean Type (Proof of Concept)
**Why Boolean first?** Simplest type, validates entire pattern works.

- [ ] BooleanHints dataclass
- [ ] BooleanDefinition (DataclassProtocol)
  - validate_value()
  - create_control()
  - serialize_value()
  - get_default()
- [ ] Boolean control (DataclassProtocol)
  - update()
  - toggle() [type-specific method]
  - serialize()
- [ ] Comprehensive tests:
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
