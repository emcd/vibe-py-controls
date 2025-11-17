# Controls Layer Architecture

**Date:** 2025-11-16
**Status:** Design phase - incorporating review feedback
**Version:** 2.0 (consolidated)

## Executive Summary

This document captures the architectural design for the **vibe-py-controls** project, which provides an abstract controls layer mediating between data-driven UI layout and backend systems (LLM specifications, prompt templates, etc.).

This consolidated document incorporates:
- Initial architecture analysis
- Review feedback responses
- Clarifications and elaborations

---

## Analysis of Existing Architecture (ai-experiments)

### Core Patterns Identified

#### 1. **Definition/Value Split Pattern**
The existing architecture uses a clear separation:
- **Definitions**: Templates that know how to validate, create values, and serialize
- **Values**: Pair a definition with current state

**Terminology Decision:** Replacing "Instance" with "Value" to avoid confusion with Python class instances.

This pattern enables:
- Reusability (one definition, many values)
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
- **LLM Provider Clients**: Separate project nativizes controls to API parameters
- **Prompt Templates**: Consume this library's control values
- **UI Frameworks**: Adapters map controls to framework widgets

**This Library's Scope:**
- Generic control abstractions
- Validation framework
- JSON-compatible serialization
- TOML descriptor parsing

---

## Core Architecture

### Terminology: Value (not Instance)

**Chosen Term:** `ControlValue` (replaces `ControlInstance`)

**Rationale:**
- Intuitive - users think "I'm setting the value"
- Matches UI conventions (e.g., `<input value="...">`)
- Concise and unambiguous
- Pairs well with "Definition"

**Naming Convention:**
- Base classes: `ControlDefinition`, `ControlValue`
- Concrete types: `BooleanDefinition`, `BooleanValue`

**Alternatives Considered:**
- `ControlState` - Emphasizes state management
- `ControlBinding` - Data binding concept
- `ControlModel` - MVC terminology

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
    def create_value(self, initial: __.typx.Any = None) -> 'ControlValue':
        """Create a value holder for this control."""
        ...

    @abstractmethod
    def serialize_value(self, value: __.typx.Any) -> __.typx.Any:
        """Serialize a value to JSON-compatible format."""
        ...

    @abstractmethod
    def get_default(self) -> __.typx.Any:
        """Get the default value for this control."""
        ...


class ControlValue(Protocol):
    """Protocol for control values.

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
    """

    default: bool = False
    validation_message: str = "Value must be a boolean"

    def validate_value(self, value: __.typx.Any) -> bool:
        """Validate boolean value with strict type checking."""
        if not isinstance(value, bool):
            raise ValidationError(self.validation_message)
        return value

    def create_value(self, initial: __.typx.Any = None) -> 'BooleanValue':
        """Create boolean value holder."""
        validated = self.validate_value(
            initial if initial is not None else self.default
        )
        return BooleanValue(definition=self, current=validated)

    def serialize_value(self, value: bool) -> bool:
        """Boolean serializes as-is."""
        return value

    def get_default(self) -> bool:
        """Return default value."""
        return self.default


class BooleanValue(DataclassProtocol):
    """Boolean control value holder.

    Attributes:
        definition: The boolean definition
        current: Current boolean value
    """

    definition: BooleanDefinition
    current: bool

    def update(self, new_value: __.typx.Any) -> Self:
        """Create new value with updated state."""
        validated = self.definition.validate_value(new_value)
        return BooleanValue(definition=self.definition, current=validated)

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
        container_hints: UI hints for layout
    """

    element_definition: ControlDefinition
    min_size: int = 0
    max_size: int | None = None
    default_elements: Sequence[__.typx.Any] = ()
    allow_duplicates: bool = True
    container_hints: 'ContainerHints' = field(default_factory=lambda: ContainerHints())

    def validate_value(self, value: Sequence[__.typx.Any]) -> tuple:
        """Validate array value."""
        # Validate sequence type, size constraints, elements, uniqueness
        ...

    def create_value(self, initial: Sequence[__.typx.Any] | None = None) -> 'ArrayValue':
        """Create array value."""
        ...


class ArrayValue(DataclassProtocol, Generic[T]):
    """Array control value holder.

    All operations return new ArrayValue (immutable).
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

### Container UI Hints

```python
from typing import Literal

@dataclass
class ContainerHints:
    """UI hints for container controls.

    Attributes:
        orientation: Layout direction
        collapsible: Can be collapsed/expanded
        initially_collapsed: Start collapsed
        border: Show border
        title: Container title/header
    """

    orientation: Literal["horizontal", "vertical", "grid"] = "vertical"
    collapsible: bool = False
    initially_collapsed: bool = False
    border: bool = False
    title: str | None = None
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

### Hybrid Approach

Global default registry for convenience + custom registries for testing:

```python
class ControlRegistry:
    """Control type registry."""

    def __init__(self, parent: 'ControlRegistry | None' = None):
        self._types: dict[str, type[ControlDefinition]] = {}
        self._parent = parent

    def register(self, name: str, definition_class: type[ControlDefinition]):
        """Register a control type."""
        self._types[name] = definition_class

    def get(self, name: str) -> type[ControlDefinition]:
        """Get control type."""
        if name in self._types:
            return self._types[name]
        if self._parent:
            return self._parent.get(name)
        raise ConfigurationError(f"Unknown control type: {name}")


# Global default registry
_DEFAULT_REGISTRY = ControlRegistry()

def register_type(name: str, definition_class: type[ControlDefinition],
                  registry: ControlRegistry | None = None):
    """Register type in registry (default if not specified)."""
    (registry or _DEFAULT_REGISTRY).register(name, definition_class)

def get_type(name: str, registry: ControlRegistry | None = None) -> type[ControlDefinition]:
    """Get type from registry (default if not specified)."""
    return (registry or _DEFAULT_REGISTRY).get(name)


# Register built-ins at module import
register_type("boolean", BooleanDefinition)
register_type("text", TextDefinition)
register_type("interval", IntervalDefinition)
register_type("options", OptionsDefinition)
register_type("array", ArrayDefinition)
```

**Usage:**
```python
# Simple case - use default
definition = get_type("interval")

# Advanced case - custom registry
custom = ControlRegistry()
register_type("email", EmailDefinition, registry=custom)
definition = get_type("email", registry=custom)
```

**Rationale:**
- Simple 90% case: just use defaults
- Advanced 10% case: custom registries available
- No global state pollution when testing (use custom registry)
- Matches Python conventions (like `warnings.filterwarnings`)

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

### Framework-Agnostic Hints (Phase 1)

```python
@dataclass
class UIHints:
    """Framework-agnostic UI hints."""
    widget: str | None = None
    label: str | None = None
    help_text: str | None = None
    placeholder: str | None = None
    # ... other agnostic hints
```

### Per-Framework Hints (Phase 2+)

```python
@dataclass
class ControlMetadata:
    """Control metadata."""
    ui_hints: UIHints
    framework_hints: dict[str, dict[str, __.typx.Any]] = field(default_factory=dict)
    # framework_hints example:
    # {
    #     "panel": {"sizing_mode": "stretch_width"},
    #     "streamlit": {"help": "Additional help"}
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
                   current_value: __.typx.Any) -> ControlValue:
    """Reload control definition, preserving value if possible."""
    new_definition = descriptor_to_definition(new_descriptor)

    try:
        # Try to use current value
        return new_definition.create_value(current_value)
    except ValidationError:
        # Fall back to default if current value incompatible
        return new_definition.create_value()
```

**Advanced Approach (If Needed):**
- Versioned descriptors
- Migration registry with transform functions
- Multi-version migration paths

**Complexity Assessment:**
- Low: Versioning and registration
- Medium: Migration path finding
- High: Automatic migration generation

### Value History Tracking - Phase 2+

**Future Enhancement:**

```python
class ControlValue(DataclassProtocol):
    """Control value with state tracking (future)."""

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
| **Terminology** | Value (not Instance) | Intuitive, matches UI conventions |
| **Base Classes** | Protocol + DataclassProtocol + abstractmethod | Hybrid typing, immutability |
| **Validation** | Custom lightweight framework | No external dependencies, composable |
| **Array Design** | Inheritance from DataclassProtocol + ABC | ABC enforcement, generics support |
| **Error Handling** | Exceptions | Project standard |
| **Registry** | Global default + custom option | Convenience + testability |
| **UI Framework** | Must be agnostic | Core requirement |
| **LLM Integration** | External layer | Separate provider client project |
| **Template Expansion** | External consumer | Not this library's responsibility |
| **Value History** | Defer to Phase 2+ | Presentation layer can't persist |
| **Scale** | Handful of controls (< 20) | Correctness over performance |
| **i18n** | Message keys + optional catalog | Non-intrusive, deferred |
| **Schema Evolution** | Defer or simple reload | Complex, not MVP |
| **Imports** | `__.typx.Any` pattern | Project convention |
| **Immutability** | Via frigid.DataclassProtocol | Project standard |

---

## Implementation Roadmap

### Phase 1: Foundation (MVP)

**Goal:** Core functionality with 5 basic types

1. Base abstractions (ControlDefinition, ControlValue protocols)
2. Custom validation framework (Validator, CompositeValidator, etc.)
3. Five core types: Boolean, Text, Interval, Options, Array
4. JSON serialization/deserialization
5. Basic exception hierarchy
6. Initial test suite

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
4. **Generalizes** to support multiple UI frameworks
5. **Separates concerns** cleanly (controls vs LLM clients vs templates)
6. **Defers complexity** to later phases (i18n, evolution, computed controls)
7. **Prioritizes correctness** over premature optimization

Ready to proceed with Phase 1 implementation!
