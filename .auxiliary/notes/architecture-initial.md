# Controls Layer Architecture

**Date:** 2025-11-16
**Status:** Design phase - refinements incorporated
**Version:** 2.1 (refined)

## Executive Summary

This document captures the architectural design for the **vibe-py-controls** project, which provides an abstract controls layer mediating between data-driven UI layout and backend systems (LLM specifications, prompt templates, etc.).

This consolidated document incorporates:
- Initial architecture analysis
- Review feedback responses
- Clarifications and elaborations

---

## Analysis of Existing Architecture (ai-experiments)

### Core Patterns Identified

#### 1. **Definition/Control Split Pattern**
The existing architecture uses a clear separation:
- **Definitions**: Templates that know how to validate, create controls, and serialize
- **Controls**: Pair a definition with current state

**Terminology Decision:** Using "Control" instead of "Instance" or "Value" for simplicity and clarity.

This pattern enables:
- Reusability (one definition, many controls)
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

#### 4. **Type Routing via Registry**
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

## Architectural Principles

### Must-Have Requirements

1. **UI Framework Agnostic** - Core must work with any UI framework
2. **Immutable Definitions** - Using `frigid.DataclassProtocol`
3. **No External Validation Dependencies** - No Pydantic or attrs
4. **Exception-Based Error Handling** - Not Result types
5. **Correctness Over Performance** - Optimize only if proven bottleneck

### Project Integration

**External Layers:**
- **LLM Provider Clients**: Separate project nativizes control values to API parameters
- **Prompt Templates**: Consume values from controls
- **UI Frameworks**: Adapters map control definitions to framework widgets

**This Library's Scope:**
- Control abstractions (definitions and controls)
- Validation framework
- JSON-compatible serialization
- TOML descriptor parsing

---

## Core Architecture

### Terminology: Control (not Instance or Value)

**Chosen Term:** `Control` (replaces `ControlInstance` and `ControlValue`)

**Rationale:**
- Simple and intuitive - "a control" is the thing the user interacts with
- Avoids redundancy - "control" already implies it has state
- Clean pairing with "Definition"
- Natural language: "BooleanDefinition creates a Boolean control"

**Naming Convention:**
- Base classes: `ControlDefinition`, `Control`
- Concrete types: `BooleanDefinition` creates `Boolean`
- Methods: `create_control()`, `update_control()`, etc.

**Alternatives Considered (and rejected):**
- `ControlValue` - Redundant, controls already have values
- `ControlState` - Emphasizes state but verbose
- `ControlInstance` - Confusing with Python class instances

### Architecture Layers

```
┌─────────────────────────────────────────────────┐
│     Prompt Template Layer (external)            │  ← Consumes controls
│     (Jinja2, template expansion)                │
└─────────────────┬───────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────┐
│     LLM Provider Clients (external)             │  ← Nativizes to APIs
│     (Anthropic, OpenAI, etc.)                   │
└─────────────────┬───────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────┐
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
│          Core Controls Layer (THIS LIBRARY)     │
│  - Definition base classes                      │
│  - Value management                             │
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

---

## Type System Design

### Base Protocols with DataclassProtocol

Using `Protocol` + `__.immut.DataclassProtocol` with `abc.abstractmethod`:

```python
from abc import abstractmethod
from typing import Protocol, Any, Self
import frigid as immut

class ControlDefinition(Protocol):
    """Protocol for control definitions.

    Uses both structural (Protocol) and nominal (ABC) typing.
    """

    @abstractmethod
    def validate_value(self, value: __.typx.Any) -> __.typx.Any:
        """Validate and normalize a value for this control."""
        ...

    @abstractmethod
    def create_control(self, initial: __.typx.Any = None) -> 'Control':
        """Create a control from this definition."""
        ...

    @abstractmethod
    def serialize_value(self, value: __.typx.Any) -> __.typx.Any:
        """Serialize a value to JSON-compatible format."""
        ...

    @abstractmethod
    def get_default(self) -> __.typx.Any:
        """Get the default value for this control."""
        ...


class Control(Protocol):
    """Protocol for controls.

    Represents the current state of a control paired with its definition.
    """

    definition: ControlDefinition
    current: __.typx.Any

    @abstractmethod
    def update(self, new_value: __.typx.Any) -> Self:
        """Update to a new value (immutable operation)."""
        ...

    @abstractmethod
    def serialize(self) -> __.typx.Any:
        """Serialize current value."""
        ...
```

### Concrete Implementation Pattern

Using `immut.DataclassProtocol` for concrete types:

```python
from frigid import DataclassProtocol

class BooleanDefinition(DataclassProtocol):
    """Boolean control definition.

    Attributes:
        default: Default boolean value
        validation_message: Custom error message
        hints: UI hints for rendering
    """

    default: bool = False
    validation_message: str = "Value must be a boolean"
    hints: 'BooleanHints' = field(default_factory=lambda: BooleanHints())

    def validate_value(self, value: __.typx.Any) -> bool:
        """Validate boolean value with strict type checking."""
        if not isinstance(value, bool):
            raise ValidationError(self.validation_message)
        return value

    def create_control(self, initial: __.typx.Any = None) -> 'Boolean':
        """Create boolean control."""
        validated = self.validate_value(
            initial if initial is not None else self.default
        )
        return Boolean(definition=self, current=validated)

    def serialize_value(self, value: bool) -> bool:
        """Boolean serializes as-is."""
        return value

    def get_default(self) -> bool:
        """Return default value."""
        return self.default


class Boolean(DataclassProtocol):
    """Boolean control.

    Attributes:
        definition: The boolean definition
        current: Current boolean value
    """

    definition: BooleanDefinition
    current: bool

    def update(self, new_value: __.typx.Any) -> Self:
        """Create new control with updated state."""
        validated = self.definition.validate_value(new_value)
        return Boolean(definition=self.definition, current=validated)

    def toggle(self) -> Self:
        """Toggle the boolean value."""
        return self.update(not self.current)

    def serialize(self) -> bool:
        """Serialize current value."""
        return self.definition.serialize_value(self.current)
```

### Key Benefits

1. **Protocol**: Structural typing for flexibility
2. **DataclassProtocol**: Immutability, concealment, keyword-only init
3. **abstractmethod**: Enforces implementation of required methods
4. **Hybrid typing**: Both nominal (ABC) and structural (Protocol) subtyping

---

## Validation Framework

### Custom Lightweight Validation

No Pydantic or attrs - custom composable validators:

```python
from typing import Callable

class Validator(Protocol):
    """Protocol for value validators."""

    def __call__(self, value: __.typx.Any) -> __.typx.Any:
        """Validate value, returning validated/transformed value."""
        ...


class CompositeValidator:
    """Chains multiple validators."""

    def __init__(self, *validators: Validator):
        self._validators = validators

    def __call__(self, value: __.typx.Any) -> __.typx.Any:
        """Apply validators in sequence."""
        result = value
        for validator in self._validators:
            result = validator(result)
        return result


class TypeValidator:
    """Validates value type."""

    def __init__(self, expected_type: type, message: str | None = None):
        self.expected_type = expected_type
        self.message = message or f"Value must be {expected_type.__name__}"

    def __call__(self, value: __.typx.Any) -> __.typx.Any:
        if not isinstance(value, self.expected_type):
            raise ValidationError(self.message)
        return value


class RangeValidator:
    """Validates numeric range."""

    def __init__(self, minimum: float, maximum: float):
        self.minimum = minimum
        self.maximum = maximum

    def __call__(self, value: __.typx.Any) -> __.typx.Any:
        if not self.minimum <= value <= self.maximum:
            raise ValidationError(
                f"Value must be between {self.minimum} and {self.maximum}"
            )
        return value
```

### Usage in Controls

```python
class IntervalDefinition(DataclassProtocol):
    """Numeric interval control."""

    minimum: float
    maximum: float
    default: float

    def __post_init__(self):
        """Build validator pipeline."""
        self._validator = CompositeValidator(
            TypeValidator((int, float), "Value must be numeric"),
            RangeValidator(self.minimum, self.maximum)
        )

    def validate_value(self, value: __.typx.Any) -> float:
        """Validate using validator pipeline."""
        return self._validator(value)
```

### Validator Benefits

- Reusable validator components
- Composable validation logic
- Type-agnostic (any control can use any validator)
- Extensible (users can add custom validators)
- Testable (validators are isolated units)
- No complex framework, just callable Protocol

---

## Core Control Types (Phase 1)

### Fundamental Types

| Type | Purpose | UI Mappings | Key Features |
|------|---------|-------------|--------------|
| **Boolean** | Binary choices | Checkbox, Toggle, Radio | Simple true/false |
| **Text** | String input | TextInput, TextArea, Label | Multi-line support, validation patterns |
| **Interval** | Numeric ranges | Slider, SpinBox, RangeSlider | Min/max/step, continuous vs discrete |
| **Options** | Enumerated choices | Select, RadioGroup, Dropdown | Single/multi-select variants |
| **Array** | Recursive containers | List, Grid, Accordion | Size constraints, homogeneous/heterogeneous |

### Array Type Design

Per review feedback, use inheritance for ABC abstract method enforcement:

```python
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Sequence

T = TypeVar('T')

class ArrayDefinition(DataclassProtocol, ABC, Generic[T]):
    """Array container control definition.

    Attributes:
        element_definition: Definition for array elements
        min_size: Minimum number of elements (0 = no minimum)
        max_size: Maximum number of elements (None = no maximum)
        default_elements: Default elements on creation
        allow_duplicates: Whether duplicate values are allowed
        hints: UI hints for layout
    """

    element_definition: ControlDefinition
    min_size: int = 0
    max_size: int | None = None
    default_elements: Sequence[__.typx.Any] = ()
    allow_duplicates: bool = True
    hints: 'ArrayHints' = field(default_factory=lambda: ArrayHints())

    def validate_value(self, value: Sequence[__.typx.Any]) -> tuple:
        """Validate array value."""
        # Validate sequence type, size constraints, elements, uniqueness
        ...

    def create_control(self, initial: Sequence[__.typx.Any] | None = None) -> 'Array':
        """Create array control."""
        ...


class Array(DataclassProtocol, Generic[T]):
    """Array control.

    All operations return new Array (immutable).
    """

    definition: ArrayDefinition[T]
    current: tuple[T, ...]

    def update(self, new_value: Sequence[__.typx.Any]) -> Self:
        """Replace entire array."""
        ...

    def append(self, element: __.typx.Any) -> Self:
        """Append element to array."""
        ...

    def remove_at(self, index: int) -> Self:
        """Remove element at index."""
        ...

    def insert_at(self, index: int, element: __.typx.Any) -> Self:
        """Insert element at index."""
        ...

    def reorder(self, new_order: Sequence[int]) -> Self:
        """Reorder elements by indices."""
        ...
```

### Deferred Types (Phase 2+)

- Integer (distinct from Interval)
- Float (continuous numeric)
- Date/Time
- Color
- File/Path
- Composite/Struct
- Union/Variant
- Reference

---

## Type Registry

### Simple Dictionary Approach (Phase 1)

For Phase 1, use a simple dictionary to map type names to definition classes:

```python
# In descriptors.py or similar module
from .types import (
    BooleanDefinition,
    TextDefinition,
    IntervalDefinition,
    OptionsDefinition,
    ArrayDefinition,
)

# Simple type name to class mapping
BUILTIN_TYPES: dict[str, type[ControlDefinition]] = {
    "boolean": BooleanDefinition,
    "text": TextDefinition,
    "interval": IntervalDefinition,
    "options": OptionsDefinition,
    "array": ArrayDefinition,
}


def descriptor_to_definition(descriptor: dict) -> ControlDefinition:
    """Create a control definition from a descriptor dictionary.

    Args:
        descriptor: Dictionary with 'type' key and type-specific parameters

    Returns:
        Control definition instance

    Raises:
        ConfigurationError: If type is unknown or descriptor is invalid
    """
    type_name = descriptor.get("type")
    if not type_name:
        raise ConfigurationError("Descriptor must have 'type' field")

    definition_class = BUILTIN_TYPES.get(type_name)
    if not definition_class:
        raise ConfigurationError(
            f"Unknown control type: {type_name}. "
            f"Valid types: {', '.join(BUILTIN_TYPES.keys())}"
        )

    # Remove 'type' from descriptor before passing to constructor
    params = {k: v for k, v in descriptor.items() if k != "type"}

    return definition_class(**params)
```

**Usage:**
```python
# From TOML descriptor
descriptor = {
    "type": "interval",
    "minimum": 0.0,
    "maximum": 1.0,
    "default": 0.7
}
definition = descriptor_to_definition(descriptor)
```

**Rationale:**
- **Simple**: Just a dictionary, no registry pattern needed
- **Sufficient**: Handles the string → class lookup use case
- **Clear**: Easy to understand and maintain
- **Extensible**: Can add custom types later if needed

**Future Consideration (Phase 2+):**
If we need extensibility for custom types, we can add:
```python
def register_custom_type(name: str, definition_class: type[ControlDefinition]):
    """Register a custom control type."""
    if name in BUILTIN_TYPES:
        raise ValueError(f"Cannot override builtin type: {name}")
    CUSTOM_TYPES[name] = definition_class

# Then check CUSTOM_TYPES in descriptor_to_definition()
```

---

## Serialization & Configuration

### TOML Descriptor Format

```toml
format-version = "1.0"

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

**Note:** `format-version` must be outside the tables (per review feedback).

### JSON Value Serialization

```json
{
  "temperature": 0.7,
  "model": "claude-3-sonnet"
}
```

### Serialization Layers

1. **Value Layer**: Just current values (lightweight, for state save/restore)
2. **Definition Layer**: Full schema (for transmission, documentation)

---

## UI Metadata & Hints

### Control-Specific Hint Classes (Phase 1)

Each control type has its own hint class with relevant attributes:

```python
from dataclasses import dataclass, field
from typing import Literal

@dataclass
class BooleanHints:
    """UI hints for boolean controls."""
    widget_preference: Literal["checkbox", "toggle", "radio"] | None = None
    label: str | None = None
    help_text: str | None = None


@dataclass
class TextHints:
    """UI hints for text controls."""
    widget_preference: Literal["input", "textarea"] | None = None
    multiline: bool = False
    placeholder: str | None = None
    label: str | None = None
    help_text: str | None = None


@dataclass
class IntervalHints:
    """UI hints for interval controls."""
    widget_preference: Literal["slider", "spinbox"] | None = None
    orientation: Literal["horizontal", "vertical"] | None = None
    show_ticks: bool = False
    show_value: bool = True
    label: str | None = None
    help_text: str | None = None


@dataclass
class OptionsHints:
    """UI hints for options controls."""
    widget_preference: Literal["select", "radio", "dropdown"] | None = None
    label: str | None = None
    help_text: str | None = None


@dataclass
class ArrayHints:
    """UI hints for array/container controls."""
    orientation: Literal["horizontal", "vertical", "grid"] = "vertical"
    collapsible: bool = False
    initially_collapsed: bool = False
    border: bool = False
    title: str | None = None
    label: str | None = None
    help_text: str | None = None
```

**Rationale:**
- Each control type has exactly the hints it needs
- No forced common structure that doesn't fit all types
- Type-safe: Can't set invalid hints for a control type
- Extensible: Easy to add new hints to specific types

### Per-Framework Hints (Phase 2+)

Optional framework-specific hints can be added later:

```python
@dataclass
class BooleanHints:
    """UI hints for boolean controls."""
    widget_preference: Literal["checkbox", "toggle", "radio"] | None = None
    label: str | None = None
    help_text: str | None = None

    # Optional per-framework hints (Phase 2+)
    framework_hints: dict[str, dict[str, __.typx.Any]] = field(default_factory=dict)
    # Example:
    # {
    #     "panel": {"sizing_mode": "stretch_width"},
    #     "streamlit": {"custom_css": "..."}
    # }
```

---

## Exception Hierarchy

```python
class ControlError(Exception):
    """Base exception for control errors."""

class ValidationError(ControlError):
    """Value validation failed."""

class ConfigurationError(ControlError):
    """Control configuration invalid."""

class ConstraintError(ValidationError):
    """Constraint violation."""
```

---

## Advanced Features (Deferred)

### Internationalization (i18n) - Phase 2

**Non-Intrusive Message Key Pattern:**

```python
class BooleanDefinition(DataclassProtocol):
    """Boolean control with i18n support."""

    default: bool = False

    # Message keys (not literal text)
    label_key: str = "control.boolean.label"
    help_key: str = "control.boolean.help"

    # Optional literal overrides
    label: str | None = None
    help_text: str | None = None
```

**Optional Message Catalog:**

```python
class MessageCatalog(Protocol):
    """Protocol for message resolution."""

    def get(self, key: str, locale: str = "en",
            default: str | None = None) -> str:
        """Resolve message key to localized text."""
        ...
```

**Fallback Chain:** literal → catalog → key → default

**Deferred:** Translation formats, pluralization, format strings

### Runtime Schema Evolution - Phase 2+

**Simplified Approach (Lower Complexity):**

```python
def reload_control(name: str, new_descriptor: dict,
                   current_value: __.typx.Any) -> Control:
    """Reload control definition, preserving value if possible."""
    new_definition = descriptor_to_definition(new_descriptor)

    try:
        # Try to use current value
        return new_definition.create_control(current_value)
    except ValidationError:
        # Fall back to default if current value incompatible
        return new_definition.create_control()
```

**Advanced Approach (If Needed):**
- Versioned descriptors
- Migration registry with transform functions
- Multi-version migration paths

**Complexity Assessment:**
- Low: Versioning and registration
- Medium: Migration path finding
- High: Automatic migration generation

### State History Tracking - Phase 2+

**Future Enhancement:**

```python
class Control(DataclassProtocol):
    """Control with state tracking (future)."""

    definition: ControlDefinition
    current: __.typx.Any           # Current value
    initial: __.typx.Any           # Initial value when created
    previous: __.typx.Any | None   # Previous value (for change detection)

    def reset(self) -> Self:
        """Reset to initial value."""
        return self.update(self.initial)

    def has_changed(self) -> bool:
        """Check if value differs from initial."""
        return self.current != self.initial
```

**Rationale:** Presentation layer can't persist this state, so deferred initially.

### Computed/Derived Controls - Phase 3+

Deferred until constraints and cascades work (possibly using `param` machinery).

### Access Control - Phase 3+

Future enhancement for read-only, disabled, hidden controls based on permissions.

---

## Design Decisions Summary

| Aspect | Decision | Rationale |
|--------|----------|-----------|
| **Terminology** | Control (not Instance/Value) | Simple, intuitive, avoids redundancy |
| **Base Classes** | Protocol + DataclassProtocol + abstractmethod | Hybrid typing, immutability |
| **Validation** | Custom lightweight framework | No external dependencies, composable |
| **Array Design** | Inheritance from DataclassProtocol + ABC | ABC enforcement, generics support |
| **Error Handling** | Exceptions | Project standard |
| **Type Lookup** | Simple dictionary | Sufficient, clear, extensible later |
| **UI Hints** | Control-specific hint classes | Each type has exactly what it needs |
| **UI Framework** | Must be agnostic | Core requirement |
| **LLM Integration** | External layer | Separate provider client project |
| **Template Expansion** | External consumer | Not this library's responsibility |
| **State History** | Defer to Phase 2+ | Presentation layer can't persist |
| **Scale** | Handful of controls (< 20) | Correctness over performance |
| **i18n** | Message keys + optional catalog | Non-intrusive, deferred |
| **Schema Evolution** | Defer or simple reload | Complex, not MVP |
| **Imports** | `__.typx.Any` pattern | Project convention |
| **Immutability** | Via frigid.DataclassProtocol | Project standard |

---

## Implementation Roadmap

### Phase 1: Foundation (MVP)

**Goal:** Core functionality with 5 basic types

1. Base abstractions (ControlDefinition, Control protocols)
2. Custom validation framework (Validator, CompositeValidator, etc.)
3. Five core types with hint classes:
   - Boolean + BooleanHints
   - Text + TextHints
   - Interval + IntervalHints
   - Options + OptionsHints
   - Array + ArrayHints
4. Simple type name → class dictionary (BUILTIN_TYPES)
5. JSON serialization/deserialization
6. Basic exception hierarchy
7. Initial test suite

**Deliverables:**
- Working core library
- Comprehensive tests
- Basic examples

### Phase 2: Configuration Layer

**Goal:** Data-driven control creation

1. TOML descriptor parser
2. Descriptor → Definition conversion
3. UI hints structure
4. Container hints (collapsible, orientation, etc.)
5. Validation message customization
6. Schema validation
7. Optional: i18n message keys and catalog

**Deliverables:**
- TOML-based control definitions
- Configuration examples
- Validation for descriptors

### Phase 3: UI Integration

**Goal:** Framework adapters

1. Generic adapter interface
2. Panel adapter (based on ai-experiments code)
3. Bidirectional synchronization
4. Event handling
5. Callback system
6. UI hint mapping

**Deliverables:**
- Panel integration
- Example UIs
- Integration tests

### Phase 4: Advanced Features (If Needed)

**Goal:** Extended capabilities

1. Additional types based on real use cases
2. Composite types
3. Cross-control dependencies
4. Computed controls
5. Constraints and cascades (possibly using `param`)
6. Runtime schema evolution (if needed)
7. Per-framework hint dictionaries

### Phase 5: Production Readiness

**Goal:** Robustness and performance

1. Performance optimization (only if proven bottleneck)
2. Comprehensive documentation
3. Migration guides
4. Production examples
5. Benchmarks

---

## Testing Strategy

- Property-based testing for serialization (Hypothesis)
- Roundtrip tests for all types
- UI integration tests with mocking
- Performance benchmarks (Phase 5)
- Isolated registry tests with custom registries

---

## Documentation Strategy

- Type stubs (.pyi files) for IDE support
- Comprehensive docstrings (Google/NumPy style)
- Example gallery (Jupyter notebooks)
- Architecture Decision Records (ADRs)
- Project standards documentation

---

## Related Projects & Patterns

### Similar Projects
- **Param** (HoloViz) - Parameter framework (familiar, may reuse for constraints)
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

1. **Get final approval** on design decisions
2. **Prototype** Boolean type as proof-of-concept
3. **Create ADRs** for key architectural choices
4. **Implement** Phase 1 core types
5. **Test** the pattern with actual usage scenarios
6. **Iterate** based on findings

---

## Appendix: Import Conventions

Per project standards:

```python
from . import __ as __  # Common imports hub

# Use project conventions:
def validate_value(self, value: __.typx.Any) -> __.typx.Any:
    ...

# typing_extensions imported as typx
# collections.abc as cabc
# etc. (see sources/vibecontrols/__/imports.py)
```

---

## Conclusion

The vibe-py-controls architecture:

1. **Builds upon** the solid foundation from ai-experiments
2. **Modernizes** with frigid.DataclassProtocol and Protocol typing
3. **Simplifies** with custom lightweight validation (no Pydantic/attrs)
4. **Clarifies** with clean terminology (Control instead of Instance/Value)
5. **Customizes** UI hints per control type (no one-size-fits-all)
6. **Generalizes** to support multiple UI frameworks
7. **Separates concerns** cleanly (controls vs LLM clients vs templates)
8. **Defers complexity** to later phases (i18n, evolution, computed controls)
9. **Prioritizes correctness** over premature optimization
10. **Keeps it simple** with dictionary-based type lookup (Phase 1)

Ready to proceed with Phase 1 implementation!
