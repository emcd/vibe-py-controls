# Controls Layer Architecture - Initial Analysis & Design Notes

**Date:** 2025-11-16
**Status:** Initial architectural exploration

## Executive Summary

This document captures the initial architectural analysis for the **vibe-py-controls** project, which aims to provide an abstract controls layer mediating between data-driven UI layout and backend systems (LLM specifications, prompt templates, etc.).

---

## Analysis of Existing Architecture (ai-experiments)

### Core Patterns Identified

#### 1. **Definition/Instance Split Pattern**
The existing architecture uses a clear separation:
- **Definitions**: Templates that know how to validate, create instances, and serialize values
- **Instances**: Pair a definition with a current value, providing state management

This is a solid pattern that enables:
- Reusability (one definition, many instances)
- Type safety through validation
- Clean separation of concerns

#### 2. **Descriptor-Based Configuration**
The system uses descriptors (dict/TOML) to declaratively define controls:
```python
descriptor_to_definition(variable) → Definition object
```

This enables:
- Data-driven configuration
- Versioning and serialization
- Separation from implementation details

#### 3. **Manager Pattern for UI Mapping**
GUI integration uses managers that:
- Map control definitions to specific UI widgets
- Handle bidirectional synchronization
- Manage callbacks and state updates

#### 4. **Type Routing via Species**
A registry pattern maps control type names to implementation classes:
```python
_species_to_class(species_name) → ControlClass
```

### Existing Control Types

From the reference implementation:

1. **Boolean** - True/false values
2. **DiscreteInterval** - Numeric ranges with min/max/grade (step)
3. **FlexArray** - Dynamic sequences with capacity constraints
4. **Options** - Enumerated choices
5. **Text** - String values

---

## Proposed Architecture for vibe-py-controls

### Core Type System

#### Fundamental Types

| Type | Purpose | UI Mappings | Key Features |
|------|---------|-------------|--------------|
| **Boolean** | Binary choices | Checkbox, Toggle, Radio | Simple true/false |
| **Text** | String input | TextInput, TextArea, Label | Multi-line support, validation patterns |
| **Interval** | Numeric ranges | Slider, SpinBox, RangeSlider | Min/max/step, continuous vs discrete |
| **Options** | Enumerated choices | Select, RadioGroup, Dropdown | Single/multi-select variants |
| **Array** | Recursive containers | List, Grid, Accordion | Size constraints, homogeneous/heterogeneous |

#### Additional Types to Consider

1. **Integer** - Distinct from Interval for cases needing exact integer semantics
2. **Float** - Continuous numeric values
3. **Date/Time** - Temporal values with timezone support
4. **Color** - RGB/HSL color specifications
5. **File** - File/path references with validation
6. **Composite/Struct** - Named field groupings (like a dict but typed)
7. **Union/Variant** - Sum types for alternatives (e.g., "manual entry OR file upload")
8. **Reference** - Cross-references to other controls (for dependencies)

### Architecture Layers

```
┌─────────────────────────────────────────────────┐
│          Application / UI Framework             │
│    (Panel, Streamlit, Web Forms, etc.)         │
└─────────────────┬───────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────┐
│          UI Adapter Layer                       │
│  - Framework-specific managers                  │
│  - Widget mapping & synchronization             │
│  - Event handling                               │
└─────────────────┬───────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────┐
│          Core Controls Layer                    │
│  - Definition base classes                      │
│  - Instance management                          │
│  - Validation & serialization                   │
│  - Type registry                                │
└─────────────────┬───────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────┐
│          Configuration Layer                    │
│  - Descriptor parsing (TOML, JSON, YAML)       │
│  - Schema validation                            │
│  - Metadata handling                            │
└─────────────────────────────────────────────────┘
```

### Key Design Decisions

#### 1. **Type System: Nominal vs Structural**

**Question:** Should we use a class hierarchy or a more flexible protocol-based approach?

**Recommendation:** Hybrid approach
- Use ABC (Abstract Base Classes) for core contracts
- Support Protocol types for extensibility
- Enable custom validators without inheritance

```python
from typing import Protocol

class ControlDefinition(Protocol):
    def validate_value(self, value: Any) -> Any: ...
    def create_instance(self, value: Any = None) -> ControlInstance: ...
    def serialize_value(self, value: Any) -> JSONSerializable: ...
```

#### 2. **Validation Strategy**

**Options:**
- A. Built-in validation in each control type
- B. Pluggable validator pattern
- C. Schema-based validation (Pydantic, attrs, etc.)

**Recommendation:** Option C with customization hooks
- Use Pydantic v2 for core validation
- Allow custom validators via hooks
- Support composition of validation rules

#### 3. **Metadata & UI Hints**

**Proposal:** Structured metadata system

```python
@dataclass
class UIHints:
    """UI customization hints"""
    widget_type: Optional[str] = None  # Preferred widget
    label: Optional[str] = None
    help_text: Optional[str] = None
    placeholder: Optional[str] = None
    css_classes: List[str] = field(default_factory=list)
    layout_hints: Dict[str, Any] = field(default_factory=dict)
    validation_message: Optional[str] = None
```

Metadata should be:
- Optional (sensible defaults)
- Framework-agnostic
- Extensible (custom keys allowed)
- Serializable

#### 4. **Dependency & Relationship Handling**

**Use Cases:**
- Conditional visibility (show field B only if A is checked)
- Value constraints (max of B depends on value of A)
- Cascading updates (changing A updates options in B)

**Recommendation:** Declarative dependency system

```python
@dataclass
class ControlDependency:
    source_control: str  # Name/path of source
    dependency_type: Literal["visibility", "constraint", "cascade"]
    predicate: Callable[[Any], bool]  # When to apply
    effect: Callable[[Any, ControlInstance], None]  # What to do
```

#### 5. **Array Type Enhancements**

The existing `FlexArray` is good, but consider:

**Homogeneous vs Heterogeneous:**
- `Array[T]` - all elements same type
- `Tuple[T1, T2, ...]` - fixed types per position
- `Sequence[Union[T1, T2]]` - mixed types from set

**Operations:**
- Append/Remove
- Reorder (drag-and-drop support)
- Bulk edit
- Search/filter

**Constraints:**
- Min/max size
- Unique elements
- Custom validation per element

---

## Serialization Architecture

### Requirements

1. **Roundtrip Fidelity**: `deserialize(serialize(x)) == x`
2. **Human Readability**: Prefer TOML/YAML for configs
3. **API Compatibility**: Support JSON for web APIs
4. **Versioning**: Schema evolution support

### Proposed Format

**Control Definition (TOML):**
```toml
[controls.temperature]
type = "interval"
value_type = "float"
minimum = 0.0
maximum = 1.0
step = 0.1
default = 0.7

[controls.temperature.ui]
widget = "slider"
label = "Temperature"
help = "Controls randomness in responses"

[controls.model]
type = "options"
choices = ["claude-3-opus", "claude-3-sonnet", "claude-3-haiku"]
default = "claude-3-sonnet"

[controls.model.ui]
widget = "dropdown"
label = "Model Selection"
```

**Instance State (JSON):**
```json
{
  "temperature": 0.7,
  "model": "claude-3-sonnet"
}
```

### Serialization Layers

1. **Value Layer**: Just the current values (lightweight, for state save/restore)
2. **Instance Layer**: Values + metadata (for debugging, introspection)
3. **Definition Layer**: Full schema (for transmission, documentation)

---

## Questions for Clarification

### 1. **Scope & Boundaries**

- **Q1:** Should this library be UI-framework-agnostic, or optimized for specific frameworks?
  - **Suggestion:** Core should be agnostic, with optional adapter modules for Panel, Streamlit, etc.

- **Q2:** Do we need runtime schema evolution (changing control definitions while app is running)?
  - **Use case:** Hot-reloading prompt templates

- **Q3:** Should we support internationalization (i18n) for labels and help text?

### 2. **Integration Points**

- **Q4:** How should controls integrate with LLM APIs?
  - **Idea:** Controls could serialize to LLM parameter dicts directly
  - **Example:** `IntervalControl("temperature") → {"temperature": 0.7}`

- **Q5:** Should we support prompt template expansion here?
  - **Or:** Keep it in a separate layer that consumes control values?

- **Q6:** How should validation errors propagate?
  - **Options:** Exceptions, Result types, error accumulation

### 3. **Advanced Features**

- **Q7:** Do we need undo/redo support for control values?
  - **Implementation:** Command pattern with history stack

- **Q8:** Should we support computed/derived controls?
  - **Example:** Control C always equals A + B

- **Q9:** Do we need access control (read-only, disabled, hidden based on permissions)?

### 4. **Performance**

- **Q10:** What are expected scale parameters?
  - Number of controls per form: 10? 100? 1000?
  - Update frequency: Real-time, on-change, manual commit?

- **Q11:** Should we optimize for:
  - Memory efficiency (many instances)
  - Serialization speed
  - Validation performance

---

## Implementation Roadmap Suggestions

### Phase 1: Core Foundation
1. Define base abstractions (Definition, Instance, Registry)
2. Implement fundamental types (Boolean, Text, Interval, Options)
3. Basic serialization (JSON round-trip)
4. Validation framework

### Phase 2: Container & Composition
1. Array type with constraints
2. Composite/Struct type
3. Dependency system
4. Metadata/UI hints

### Phase 3: Configuration & Formats
1. TOML descriptor parsing
2. JSON Schema generation
3. YAML support
4. Versioning/migration

### Phase 4: UI Integration
1. Panel adapter (based on existing code)
2. Generic adapter interface
3. Bidirectional sync
4. Event handling

### Phase 5: Advanced Features
1. Conditional logic
2. Computed controls
3. Validation message customization
4. Undo/redo

---

## Technical Considerations

### 1. **Type Safety**

Use modern Python typing:
- `typing.Protocol` for structural typing
- `typing.Generic` for parameterized types
- Runtime type checking (beartype, typeguard) for validation

### 2. **Immutability vs Mutability**

**Recommendation:**
- Definitions: Immutable (frozen dataclasses)
- Instances: Mutable state, immutable definition reference
- Values: Depends on type (primitives immutable, containers may be mutable)

### 3. **Error Handling**

Create custom exception hierarchy:
```python
class ControlError(Exception): ...
class ValidationError(ControlError): ...
class SerializationError(ControlError): ...
class ConfigurationError(ControlError): ...
```

### 4. **Testing Strategy**

- Property-based testing for serialization (Hypothesis)
- Roundtrip tests for all types
- UI integration tests with mocking
- Performance benchmarks

### 5. **Documentation**

- Type stubs (.pyi files) for IDE support
- Comprehensive docstrings (Google/NumPy style)
- Example gallery (Jupyter notebooks)
- Architecture Decision Records (ADRs)

---

## Open Design Questions

### Naming Conventions

- **Current:** `DefinitionBase`, `Instance`, `FlexArray`
- **Alternative:** `ControlSchema`, `ControlState`, `ArrayControl`
- **Question:** Should we use a consistent suffix? (`*Control`, `*Definition`, `*Schema`)

### Inheritance vs Composition

**Example:** Should `Array` inherit from `Definition` or compose it?

```python
# Option A: Inheritance
class ArrayDefinition(DefinitionBase):
    element_definition: DefinitionBase

# Option B: Composition
class ArrayDefinition:
    _definition_base: DefinitionBase
    element_definition: DefinitionBase
```

**Recommendation:** Inheritance for "is-a", composition for "has-a". Arrays ARE definitions, so inheritance seems appropriate.

### Registry Pattern

Should the type registry be:
- Global singleton
- Contextual (per-application)
- Explicit (passed around)

**Recommendation:** Start with global, add contextual later if needed.

---

## References & Prior Art

### Similar Projects
- **Param** (HoloViz) - Parameter framework for Python
- **Pydantic** - Data validation using type annotations
- **attrs** - Classes without boilerplate
- **Traitlets** (Jupyter) - Configuration system
- **Marshmallow** - Serialization library

### Relevant Patterns
- Descriptor pattern
- Builder pattern
- Visitor pattern (for serialization)
- Strategy pattern (for validation)
- Observer pattern (for UI sync)

---

## Next Steps

1. **Review & Discuss** this document
2. **Clarify** open questions
3. **Define** initial API surface
4. **Prototype** core abstractions
5. **Iterate** based on feedback

---

## Notes & Ideas

### Potential Extensions

1. **Control Groups/Sections**
   - Organize related controls
   - Collapsible sections in UI
   - Validation at group level

2. **Presets/Profiles**
   - Save/load control value sets
   - "Beginner" vs "Advanced" presets
   - Share configurations

3. **Control State History**
   - Track changes over time
   - Audit trail
   - A/B testing support

4. **Reactive Programming**
   - Use Rx-style observables
   - Declarative data flow
   - Automatic dependency tracking

5. **Schema Generation**
   - JSON Schema from definitions
   - OpenAPI specs
   - GraphQL schemas

### Implementation Tools

- **Dataclasses/attrs**: For immutable definitions
- **Pydantic**: For validation and serialization
- **typing_extensions**: For advanced type features
- **beartype/typeguard**: Runtime type checking
- **Hypothesis**: Property-based testing

---

## Conclusion

The vibe-py-controls architecture should build upon the solid foundation of the ai-experiments reference implementation while:

1. **Generalizing** to support more use cases and UI frameworks
2. **Modernizing** with current Python best practices (Pydantic, Protocols, etc.)
3. **Extending** with advanced features (dependencies, composition, etc.)
4. **Documenting** thoroughly for adoption

The layered architecture with clear separation of concerns (definition/instance/UI) should enable flexible integration with various backends (LLM APIs, prompt templates) and frontends (Panel, Streamlit, web forms).

I'm excited to collaborate on refining this design and implementing it!
