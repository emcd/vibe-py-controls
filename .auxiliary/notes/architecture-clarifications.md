# Architecture Clarifications - Round 2

**Date:** 2025-11-16
**Status:** Addressing reviewer questions and incorporating feedback

## Summary

This document addresses specific questions from the PR review and incorporates the clarifications provided.

---

## Questions Answered by Reviewer

### ✅ Q1: LLM API Integration

**My Question:** Should controls serialize directly to API parameters, or use a separate mapping layer?

**Answer (Comment #15):**
> "We have a separate project which implements LLM provider clients. These will handle nativizing our controls into the dicts that the LLM APIs expect."

**Implication:**
- This library provides generic control abstractions
- A separate LLM provider client layer handles conversion to API-specific formats
- Controls should serialize to generic JSON-compatible structures
- The provider client layer maps those to API parameters

**Updated Design:**
```python
# vibe-py-controls serializes to generic structure
controls = {
    "temperature": 0.7,
    "max_tokens": 1000,
    "stream": True
}

# Separate provider client layer nativizes for specific APIs
# Anthropic client:
api_params = {
    "temperature": 0.7,
    "max_tokens": 1000,
    "stream": True
}

# OpenAI client might map differently:
api_params = {
    "temperature": 0.7,
    "max_tokens": 1000,
    "stream": True
}
```

---

### ✅ Q2: Prompt Template Integration

**My Question:** Does this library handle template expansion (Jinja2, etc.)?

**Answer (Comment #16):**
> "Prompt templates are a consumer of this lower-level library. We should have no direct support for them here."

**Implication:**
- This library is lower-level infrastructure
- Prompt template libraries consume control values
- No Jinja2 or template engine integration here
- Focus on clean value serialization

**Updated Architecture:**
```
┌─────────────────────────────────┐
│   Prompt Template Layer         │  ← Consumes controls
│   (Jinja2, template expansion)  │
└────────────┬────────────────────┘
             │
┌────────────▼────────────────────┐
│   vibe-py-controls              │  ← This library
│   (Control definitions/values)  │
└─────────────────────────────────┘
```

---

### ✅ Q3: Error Handling Strategy

**My Question:** Exceptions vs Result types vs error accumulation?

**Answer (Comment #17):**
> "Exceptions."

**Design Decision:** Use exceptions for validation errors and control errors.

**Implementation:**
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

### ✅ Q4: Multiple Value Support (History/Previous/Default)

**My Question:** Should ControlValue track history (current, previous, default)?

**Answer (Comment #20):**
> "Good question. I think we can defer any internal tracking of this initially. We might need to provide some fields for this later since I doubt we can persist tracking of this kind of state at whatever layer is presenting the controls."

**Design Decision:**
- **Phase 1:** ControlValue holds only `current` value
- **Future:** May add `previous`, `default`, `initial` fields
- Rationale: Presentation layer can't persist this state

**Future Enhancement Structure:**
```python
class ControlValue(DataclassProtocol):
    """Control value with state tracking (future)."""

    definition: ControlDefinition
    current: Any           # Current value
    initial: Any           # Initial value when created
    previous: Any | None   # Previous value (for change detection)

    def reset(self) -> Self:
        """Reset to initial value."""
        return self.update(self.initial)

    def has_changed(self) -> bool:
        """Check if value differs from initial."""
        return self.current != self.initial
```

---

### ✅ Q5: Performance & Scale

**My Question:** What are expected scale parameters (number of controls, update frequency)?

**Answer (Comments #21-22):**
> "Does scale matter? In most cases, we are talking a handful of knobs to adjust or text areas to fill for prompt templates and a handful of sliders (temperature, top-k, etc...) and checkboxes (streaming, etc...) for models."
>
> "Correctness first and then we will worry about performance if it is proven to be a bottleneck."

**Design Decision:**
- **Expected Scale:** Handful of controls (< 20 per form typically)
- **Priority:** Correctness over performance
- **Optimization:** Only if proven bottleneck
- **Approach:** Simple, readable implementations first

---

### ✅ Q6: Deferred Features Confirmed

**Answers (Comments #18-19):**

- **Access Control** (Comment #18): "No... Good future enhancement."
- **Computed Controls** (Comment #19): "Yes, we should, but not initially... Would probably tackle this with the cascades and constraints work."

**Deferred to Future:**
- Access control (read-only, disabled, hidden)
- Computed/derived controls
- Constraints and cascades (possibly using `param` machinery)

---

### ✅ Q7: UI Framework Agnosticism

**Answer (Comments #12, #8):**
> "Must absolutely be UI-framework-agnostic. We can support a per-framework hints dictionary at some point. But not a necessary part of the implementation."
>
> "Some metadata should be framework agnostic. But, it might also be nice to have a per-framework dictionary too for even finer control. We will not need to support this initially though."

**Design Decision:**
- **Phase 1:** Framework-agnostic hints only
- **Future:** Optional per-framework hint dictionaries

**Structure:**
```python
@dataclass
class UIHints:
    """Framework-agnostic UI hints."""
    widget: str | None = None
    label: str | None = None
    help_text: str | None = None
    # ... other agnostic hints

@dataclass
class ControlMetadata:
    """Control metadata."""
    ui_hints: UIHints
    framework_hints: dict[str, dict[str, Any]] = field(default_factory=dict)
    # framework_hints example:
    # {
    #     "panel": {"sizing_mode": "stretch_width"},
    #     "streamlit": {"help": "Additional help"}
    # }
```

---

### ✅ Q8: TOML Format

**Answer (Comment #11):**
> "Proposed controls TOML format looks good. Should have `format-version` outside of the tables."

**Updated Format:**
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
help = "Controls randomness"
```

---

### ✅ Q9: Import Conventions

**Answer (Comment #23):**
> "We import `typing_extensions` as `typx` into a common imports hub. We will reference things like `Any` as `__.typx.Any`. This is per project standards."

**Convention:**
```python
from . import __ as __  # Common imports hub

# Use project conventions:
def validate_value(self, value: __.typx.Any) -> __.typx.Any:
    ...
```

---

### ✅ Q10: Code Standards

**Answer (Comment #24):**
> "Let's prescribe exceptions, immutability, etc.. here. We have project coding standards for all these things."

**Standards to Follow:**
- **Exceptions:** For error handling
- **Immutability:** Via `frigid.DataclassProtocol`
- **Concealment:** Non-public attributes hidden
- **Keyword-only:** Initialization
- Project standards apply (coders will handle details)

---

## Questions for Me to Answer

### Q1: Pluggable Validator Pattern - Elaboration

**Reviewer Question (Comment #6):**
> "What do you have in mind for a pluggable validator pattern?"

**Detailed Proposal:**

#### Core Concept
Allow validators to be composed and reused across control types without inheritance.

#### Implementation

**1. Validator Protocol:**
```python
class Validator(Protocol):
    """Protocol for value validators."""

    def __call__(self, value: __.typx.Any) -> __.typx.Any:
        """Validate value.

        Args:
            value: Value to validate

        Returns:
            Validated/transformed value

        Raises:
            ValidationError: If validation fails
        """
        ...
```

**2. Composable Validators:**
```python
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
```

**3. Validator Library:**
```python
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


class LengthValidator:
    """Validates sequence length."""

    def __init__(self, min_len: int = 0, max_len: int | None = None):
        self.min_len = min_len
        self.max_len = max_len

    def __call__(self, value: __.typx.Any) -> __.typx.Any:
        length = len(value)
        if length < self.min_len:
            raise ValidationError(f"Must have at least {self.min_len} items")
        if self.max_len is not None and length > self.max_len:
            raise ValidationError(f"Must have at most {self.max_len} items")
        return value
```

**4. Usage in Control Definitions:**
```python
class IntervalDefinition(DataclassProtocol):
    """Interval control with pluggable validation."""

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

**5. Custom Validators:**
```python
class EmailValidator:
    """Custom email validator."""

    def __call__(self, value: __.typx.Any) -> str:
        import re
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', str(value)):
            raise ValidationError("Invalid email format")
        return str(value)


# Usage
class EmailTextDefinition(DataclassProtocol):
    """Text control for email addresses."""

    def __post_init__(self):
        self._validator = CompositeValidator(
            TypeValidator(str),
            EmailValidator()
        )
```

**Benefits:**
- Reusable validator components
- Composable validation logic
- Type-agnostic (any control can use any validator)
- Extensible (users can add custom validators)
- Testable (validators are isolated units)

**Simplicity:**
- No complex framework
- Just callable objects following Protocol
- Straightforward composition pattern

---

### Q2: Runtime Schema Evolution - Ideas

**Reviewer Question (Comment #13):**
> "Great question. Would be nice to support this, but we need to explore the complexity cost. Do you have specific ideas in mind?"

**Proposal: Versioned Descriptors with Migration**

#### Use Case
Hot-reloading prompt templates with updated control schemas without restarting application.

#### Approach

**1. Versioned Descriptors:**
```toml
format-version = "1.0"
schema-version = "2"  # User-defined version

[controls.temperature]
type = "interval"
# ...
```

**2. Immutable Definition + Value Replacement:**
Since definitions are immutable, "evolution" means creating new definitions and migrating values.

```python
class ControlRegistry:
    """Manages control definitions with versioning."""

    def __init__(self):
        self._definitions: dict[str, ControlDefinition] = {}
        self._versions: dict[str, int] = {}

    def register(self, name: str, definition: ControlDefinition,
                 version: int = 1):
        """Register a control definition."""
        self._definitions[name] = definition
        self._versions[name] = version

    def update(self, name: str, new_definition: ControlDefinition,
               version: int, migrate: bool = True) -> ControlDefinition:
        """Update definition to new version.

        Args:
            name: Control name
            new_definition: New definition
            version: New version number
            migrate: Whether to attempt value migration

        Returns:
            The new definition
        """
        if version <= self._versions.get(name, 0):
            raise ConfigurationError(
                f"Version {version} must be greater than "
                f"current {self._versions[name]}"
            )

        old_definition = self._definitions.get(name)

        if migrate and old_definition is not None:
            # Store migration path
            self._register_migration(name, old_definition, new_definition)

        self._definitions[name] = new_definition
        self._versions[name] = version
        return new_definition

    def migrate_value(self, name: str, old_value: ControlValue,
                     to_version: int) -> ControlValue:
        """Migrate value to new version."""
        # Apply migration transformations
        ...
```

**3. Value Migration Callbacks:**
```python
@dataclass
class Migration:
    """Describes how to migrate from one definition to another."""

    from_version: int
    to_version: int
    transform: Callable[[Any], Any]


class MigrationRegistry:
    """Manages migrations between versions."""

    def __init__(self):
        self._migrations: dict[str, list[Migration]] = {}

    def register(self, control_name: str, migration: Migration):
        """Register a migration path."""
        if control_name not in self._migrations:
            self._migrations[control_name] = []
        self._migrations[control_name].append(migration)

    def migrate(self, control_name: str, value: Any,
                from_version: int, to_version: int) -> Any:
        """Migrate value across versions."""
        migrations = self._migrations.get(control_name, [])

        # Build migration path
        current_value = value
        current_version = from_version

        while current_version < to_version:
            # Find next migration
            migration = next(
                (m for m in migrations
                 if m.from_version == current_version),
                None
            )
            if migration is None:
                raise ConfigurationError(
                    f"No migration path from {current_version} "
                    f"to {to_version}"
                )

            current_value = migration.transform(current_value)
            current_version = migration.to_version

        return current_value
```

**4. Usage Example:**
```python
# Version 1: Simple interval
temp_v1 = IntervalDefinition(minimum=0.0, maximum=1.0, default=0.7)

# Version 2: Add step constraint
temp_v2 = IntervalDefinition(
    minimum=0.0, maximum=1.0, default=0.7, step=0.1
)

# Register migration
migrations.register("temperature", Migration(
    from_version=1,
    to_version=2,
    transform=lambda v: round(v, 1)  # Round to step precision
))

# Migrate existing value
old_value = temp_v1.create_value(0.73)
new_value_data = migrations.migrate("temperature",
                                     old_value.current,
                                     from_version=1,
                                     to_version=2)
new_value = temp_v2.create_value(new_value_data)
```

**Complexity Assessment:**
- **Low Complexity:** Versioning and registration
- **Medium Complexity:** Migration path finding
- **High Complexity:** Automatic migration generation

**Recommendation:**
- **Phase 1:** Skip (not needed for MVP)
- **Phase 2:** Add versioning and explicit migrations
- **Phase 3:** Consider automatic migration hints

**Simplified Alternative (Lower Complexity):**
Just support reloading with best-effort value preservation:

```python
def reload_control(name: str, new_descriptor: dict,
                   current_value: Any) -> ControlValue:
    """Reload control definition, preserving value if possible."""
    new_definition = descriptor_to_definition(new_descriptor)

    try:
        # Try to use current value
        return new_definition.create_value(current_value)
    except ValidationError:
        # Fall back to default if current value incompatible
        return new_definition.create_value()
```

---

### Q3: i18n Support - Non-Intrusive Recommendations

**Reviewer Question (Comment #14):**
> "Excellent question. I had not thought of this. Do you have any recommendations that are not too intrusive into our design?"

**Proposal: Message Key Pattern with Optional Catalog**

#### Core Idea
Store message keys instead of literal strings, with optional resolution to localized text.

#### Implementation

**1. Message Keys in Definitions:**
```python
class BooleanDefinition(DataclassProtocol):
    """Boolean control with i18n support."""

    default: bool = False

    # Message keys (not literal text)
    label_key: str = "control.boolean.label"
    help_key: str = "control.boolean.help"
    validation_error_key: str = "control.boolean.validation_error"

    # Optional literal overrides
    label: str | None = None
    help_text: str | None = None
```

**2. Optional Message Catalog:**
```python
class MessageCatalog(Protocol):
    """Protocol for message resolution."""

    def get(self, key: str, locale: str = "en",
            default: str | None = None) -> str:
        """Resolve message key to localized text."""
        ...


class SimpleMessageCatalog:
    """Simple dict-based catalog."""

    def __init__(self):
        self._messages: dict[str, dict[str, str]] = {
            "en": {},
            "es": {},
            "fr": {},
        }

    def register(self, key: str, locale: str, text: str):
        """Register a message."""
        if locale not in self._messages:
            self._messages[locale] = {}
        self._messages[locale][key] = text

    def get(self, key: str, locale: str = "en",
            default: str | None = None) -> str:
        """Get message."""
        return self._messages.get(locale, {}).get(key, default or key)
```

**3. Rendering with Locale:**
```python
def render_label(definition: ControlDefinition,
                 locale: str = "en",
                 catalog: MessageCatalog | None = None) -> str:
    """Render label with i18n support."""

    # If literal provided, use it
    if hasattr(definition, 'label') and definition.label:
        return definition.label

    # Otherwise resolve from catalog
    if catalog and hasattr(definition, 'label_key'):
        return catalog.get(definition.label_key, locale)

    # Fall back to key itself
    return getattr(definition, 'label_key', "")
```

**4. TOML Descriptor Format:**
```toml
[controls.temperature]
type = "interval"
minimum = 0.0
maximum = 1.0
default = 0.7

[controls.temperature.ui]
label-key = "prompts.params.temperature.label"
help-key = "prompts.params.temperature.help"

# OR provide literals directly
# label = "Temperature"
# help = "Controls randomness"
```

**5. Message Catalog Files:**
```toml
# messages/en.toml
[prompts.params.temperature]
label = "Temperature"
help = "Controls randomness in responses"

# messages/es.toml
[prompts.params.temperature]
label = "Temperatura"
help = "Controla la aleatoriedad en las respuestas"
```

**Non-Intrusive Aspects:**
1. **Optional:** Works without catalog (keys are self-documenting)
2. **Backward Compatible:** Literal strings still work
3. **Simple Protocol:** Just need `.get(key, locale)` method
4. **No Complex Framework:** No gettext, no babel required
5. **Lazy Resolution:** Only resolve when rendering UI
6. **Fallback Chain:** literal → catalog → key → default

**Usage Example:**
```python
# Without i18n (works fine)
temp_def = IntervalDefinition(
    minimum=0.0, maximum=1.0, default=0.7,
    label="Temperature"
)

# With i18n (optional)
temp_def = IntervalDefinition(
    minimum=0.0, maximum=1.0, default=0.7,
    label_key="params.temperature.label",
    help_key="params.temperature.help"
)

# UI layer resolves
catalog = load_catalog("en")
label = render_label(temp_def, locale="en", catalog=catalog)
```

**Deferred Complexity:**
- Translation file format (TOML vs JSON vs PO)
- Pluralization rules
- Format string substitution
- Fallback locale chains

**Recommendation:**
- **Phase 1:** Support `*_key` and literal fields
- **Phase 2:** Add simple catalog with dict/TOML backend
- **Phase 3:** Consider advanced features if needed

---

### Q4: Registry Pattern - Elaboration

**Reviewer Question (Comment #26):**
> "Can you elaborate on the registry concern?"

**Context & Concern:**

The registry maps type names (strings from descriptors) to control definition classes:

```python
descriptor = {
    "type": "interval",  # ← String type name
    "minimum": 0.0,
    "maximum": 1.0
}

# Registry resolves "interval" → IntervalDefinition class
definition = create_definition_from_descriptor(descriptor)
```

**The Question:** Where should this registry live?

#### Option A: Global Registry (Simplest)

**Implementation:**
```python
# vibecontrols/registry.py

_TYPE_REGISTRY: dict[str, type[ControlDefinition]] = {}

def register_type(name: str, definition_class: type[ControlDefinition]):
    """Register a control type globally."""
    _TYPE_REGISTRY[name] = definition_class

def get_type(name: str) -> type[ControlDefinition]:
    """Get control definition class by name."""
    if name not in _TYPE_REGISTRY:
        raise ConfigurationError(f"Unknown control type: {name}")
    return _TYPE_REGISTRY[name]

# Register built-in types at module import
register_type("boolean", BooleanDefinition)
register_type("text", TextDefinition)
register_type("interval", IntervalDefinition)
register_type("options", OptionsDefinition)
register_type("array", ArrayDefinition)
```

**Usage:**
```python
# Anywhere in the application
from vibecontrols.registry import get_type

def create_from_descriptor(descriptor: dict) -> ControlDefinition:
    """Create definition from descriptor."""
    type_class = get_type(descriptor["type"])
    return type_class(**descriptor)
```

**Pros:**
- Simple
- No need to pass registry around
- Works like Python's built-in type system

**Cons:**
- Global state (testing concerns)
- One namespace for all type names
- Can't have different type sets per application

---

#### Option B: Contextual Registry (More Flexible)

**Implementation:**
```python
class ControlRegistry:
    """Context-specific control type registry."""

    def __init__(self, parent: 'ControlRegistry | None' = None):
        """Create registry with optional parent for inheritance."""
        self._types: dict[str, type[ControlDefinition]] = {}
        self._parent = parent

    def register(self, name: str, definition_class: type[ControlDefinition]):
        """Register a type in this context."""
        self._types[name] = definition_class

    def get(self, name: str) -> type[ControlDefinition]:
        """Get type, checking parent if not found."""
        if name in self._types:
            return self._types[name]
        if self._parent:
            return self._parent.get(name)
        raise ConfigurationError(f"Unknown control type: {name}")

    def clone(self) -> 'ControlRegistry':
        """Create a child registry inheriting from this one."""
        return ControlRegistry(parent=self)


# Create default registry
DEFAULT_REGISTRY = ControlRegistry()
DEFAULT_REGISTRY.register("boolean", BooleanDefinition)
DEFAULT_REGISTRY.register("text", TextDefinition)
# ... etc
```

**Usage:**
```python
# Use default registry
descriptor_to_definition(descriptor)  # Uses DEFAULT_REGISTRY

# Or create custom registry for special application
custom_registry = DEFAULT_REGISTRY.clone()
custom_registry.register("email", EmailTextDefinition)
custom_registry.register("color", ColorDefinition)

# Use custom registry explicitly
definition = descriptor_to_definition(descriptor, registry=custom_registry)
```

**Pros:**
- Multiple type namespaces
- Easy testing (create isolated registry)
- Can extend without affecting global state
- Supports hierarchical type inheritance

**Cons:**
- More complex API
- Need to pass registry around or use context managers
- Overhead for simple cases

---

#### Option C: Explicit (No Registry)

**Implementation:**
```python
# No registry - caller provides type mapping
def descriptor_to_definition(
    descriptor: dict,
    type_map: dict[str, type[ControlDefinition]]
) -> ControlDefinition:
    """Create definition from descriptor with explicit type map."""
    type_name = descriptor["type"]
    if type_name not in type_map:
        raise ConfigurationError(f"Unknown type: {type_name}")

    type_class = type_map[type_name]
    return type_class(**descriptor)

# Caller maintains their own mapping
STANDARD_TYPES = {
    "boolean": BooleanDefinition,
    "text": TextDefinition,
    "interval": IntervalDefinition,
    "options": OptionsDefinition,
    "array": ArrayDefinition,
}

definition = descriptor_to_definition(my_descriptor, STANDARD_TYPES)
```

**Pros:**
- No hidden state
- Explicit and clear
- Maximum flexibility

**Cons:**
- Verbose
- Caller must manage type mappings
- Harder to have convenient defaults

---

#### Recommendation

**For This Project: Option A (Global Registry) with Option B features**

Hybrid approach:
- Global default registry for convenience
- Support custom registries when needed
- Best of both worlds

```python
# vibecontrols/registry.py

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
- Framework matches Python conventions (like `warnings.filterwarnings`)

---

## Additional Notes from Review

### Container/Array UI Hints (Comment #28)

Confirmed that containers need:
- `orientation` hint (horizontal, vertical, grid)
- `collapsible` hint (true/false)

Already addressed in architecture-review-response.md with `ContainerHints` dataclass.

---

### Related to Param Library (Comment #9, #27)

Reviewer familiar with `param` library. Constraints and cascades might reuse its machinery, but deferred for now.

**Note:** Consider `param` patterns when implementing Phase 3+ features.

---

## Summary of Updated Design Decisions

| Question | Answer | Phase |
|----------|--------|-------|
| LLM Integration | Separate layer nativizes controls | N/A (external) |
| Template Expansion | Not in this library | N/A (external) |
| Error Handling | Exceptions | Phase 1 |
| Value History | Defer, may add later | Phase 2+ |
| Scale | Handful of controls, correctness first | Phase 1 |
| Access Control | Future enhancement | Phase 3+ |
| Computed Controls | Future, with constraints/cascades | Phase 3+ |
| Framework Agnostic | Yes, per-framework hints later | Phase 1 / Phase 2+ |
| TOML Format Version | Outside tables | Phase 2 |
| Imports | Use `__.typx.Any` pattern | Phase 1 |
| Code Standards | Exceptions, immutability via project | Phase 1 |
| Pluggable Validators | Composable validator pattern | Phase 1 |
| Runtime Evolution | Defer or simple reload | Phase 2+ |
| i18n | Message keys + optional catalog | Phase 2 |
| Registry | Global default + custom option | Phase 1 |

---

## Next Steps

1. Get feedback on elaborations (validator, i18n, registry, evolution)
2. Begin Phase 1 implementation with clarified design
3. Create ADR (Architecture Decision Record) for key choices
4. Prototype Boolean type as proof-of-concept

---

## Questions Still Open

None - all questions have been answered or elaborated upon.
