# Architecture Review Response

**Date:** 2025-11-16
**Status:** Addressing PR #1 review feedback

## Review Feedback Summary

This document addresses the review feedback from @emcd on the initial architecture proposal.

---

## 1. Terminology: "Instance" → Better Alternative

### Problem
The term "Instance" for state holders creates confusion with Python class instances.

### Proposed Alternatives

#### Option A: **Value** (Recommended)
```python
class BooleanDefinition(ControlDefinition):
    """Defines a boolean control."""

    def create_value(self, initial=None) -> BooleanValue:
        """Create a control value from this definition."""
        ...

class BooleanValue(ControlValue):
    """Holds the current state of a boolean control."""
    definition: BooleanDefinition
    current: bool
```

**Rationale:**
- Clear: A "value" is what the user manipulates
- Familiar: Common in UI frameworks (e.g., "value property")
- Accurate: It represents the current value of the control

#### Option B: **State**
```python
class BooleanState(ControlState):
    definition: BooleanDefinition
    current: bool
```

**Rationale:**
- Descriptive: Emphasizes it holds state
- Common: Used in React, Vue, and other frameworks
- Clear separation from definition

#### Option C: **Binding**
```python
class BooleanBinding(ControlBinding):
    definition: BooleanDefinition
    current: bool
```

**Rationale:**
- Reflects data binding concept
- Common in MVVM patterns
- Suggests connection between model and view

#### Option D: **Model**
```python
class BooleanModel(ControlModel):
    definition: BooleanDefinition
    current: bool
```

**Rationale:**
- MVC/MVVM terminology
- Familiar to UI developers
- Clearly distinct from definition (schema)

### Recommendation: **Value**

I recommend **Value** because:
1. It's intuitive - users think "I'm setting the value"
2. It matches existing conventions (e.g., `<input value="...">`)
3. It's concise and unambiguous
4. It pairs well with "Definition" (Definition defines, Value stores)

**Naming Convention:**
- Base classes: `ControlDefinition`, `ControlValue`
- Concrete types: `BooleanDefinition`, `BooleanValue`
- Or: `BooleanDef`, `BooleanVal` for brevity

---

## 2. Type System Architecture

### Base Protocol with DataclassProtocol

Following the review guidance, use `Protocol` + `__.immut.DataclassProtocol` with `abc.abstractmethod`:

```python
from abc import abstractmethod
from typing import Protocol, Any, Self
import frigid as immut

class ControlDefinition(Protocol):
    """Protocol for control definitions.

    Defines the contract that all control definitions must implement.
    Uses both structural (Protocol) and nominal (ABC) typing.
    """

    @abstractmethod
    def validate_value(self, value: Any) -> Any:
        """Validate and normalize a value for this control.

        Args:
            value: Raw value to validate

        Returns:
            Normalized/coerced value

        Raises:
            ValidationError: If value is invalid
        """
        ...

    @abstractmethod
    def create_value(self, initial: Any = None) -> 'ControlValue':
        """Create a value holder for this control.

        Args:
            initial: Initial value (None for default)

        Returns:
            Control value with validated initial state
        """
        ...

    @abstractmethod
    def serialize_value(self, value: Any) -> Any:
        """Serialize a value to JSON-compatible format.

        Args:
            value: Value to serialize

        Returns:
            JSON-serializable representation
        """
        ...

    @abstractmethod
    def get_default(self) -> Any:
        """Get the default value for this control.

        Returns:
            Default value (already validated)
        """
        ...


class ControlValue(Protocol):
    """Protocol for control values.

    Represents the current state of a control paired with its definition.
    """

    definition: ControlDefinition
    current: Any

    @abstractmethod
    def update(self, new_value: Any) -> Self:
        """Update to a new value (immutable operation).

        Args:
            new_value: New value to set

        Returns:
            New ControlValue with updated value

        Raises:
            ValidationError: If new_value is invalid
        """
        ...

    @abstractmethod
    def serialize(self) -> Any:
        """Serialize current value.

        Returns:
            JSON-serializable representation
        """
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

    def validate_value(self, value: Any) -> bool:
        """Validate boolean value with strict type checking."""
        if not isinstance(value, bool):
            raise ValidationError(self.validation_message)
        return value

    def create_value(self, initial: Any = None) -> 'BooleanValue':
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

    def update(self, new_value: Any) -> Self:
        """Create new value with updated state."""
        validated = self.definition.validate_value(new_value)
        return BooleanValue(definition=self.definition, current=validated)

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

## 3. Validation Strategy (No Pydantic/attrs)

### Custom Validation Framework

Since external validation libraries are rejected, implement a lightweight custom system:

```python
from typing import Callable, Any
from dataclasses import dataclass, field

@dataclass
class ValidationRule:
    """Single validation rule."""

    predicate: Callable[[Any], bool]
    """Function that returns True if value is valid."""

    message: str
    """Error message if validation fails."""

    transform: Callable[[Any], Any] | None = None
    """Optional transformation to apply before validation."""

    def __call__(self, value: Any) -> Any:
        """Apply this rule.

        Args:
            value: Value to validate

        Returns:
            Transformed value if transformation exists, else original

        Raises:
            ValidationError: If validation fails
        """
        check_value = value if self.transform is None else self.transform(value)
        if not self.predicate(check_value):
            raise ValidationError(self.message)
        return check_value


class Validator:
    """Composable validator with multiple rules."""

    def __init__(self, *rules: ValidationRule):
        self.rules = rules

    def validate(self, value: Any) -> Any:
        """Run all validation rules.

        Args:
            value: Value to validate

        Returns:
            Final validated/transformed value

        Raises:
            ValidationError: If any rule fails
        """
        result = value
        for rule in self.rules:
            result = rule(result)
        return result

    def __call__(self, value: Any) -> Any:
        """Shortcut for validate()."""
        return self.validate(value)


# Predefined validators
class Validators:
    """Library of common validators."""

    @staticmethod
    def is_type(expected_type: type, message: str | None = None) -> ValidationRule:
        """Validate value is of expected type."""
        msg = message or f"Value must be of type {expected_type.__name__}"
        return ValidationRule(
            predicate=lambda v: isinstance(v, expected_type),
            message=msg
        )

    @staticmethod
    def in_range(minimum: float, maximum: float,
                 message: str | None = None) -> ValidationRule:
        """Validate numeric value is in range."""
        msg = message or f"Value must be between {minimum} and {maximum}"
        return ValidationRule(
            predicate=lambda v: minimum <= v <= maximum,
            message=msg
        )

    @staticmethod
    def one_of(choices: set, message: str | None = None) -> ValidationRule:
        """Validate value is one of allowed choices."""
        msg = message or f"Value must be one of: {choices}"
        return ValidationRule(
            predicate=lambda v: v in choices,
            message=msg
        )

    @staticmethod
    def matches_pattern(pattern: str, message: str | None = None) -> ValidationRule:
        """Validate string matches regex pattern."""
        import re
        regex = re.compile(pattern)
        msg = message or f"Value must match pattern: {pattern}"
        return ValidationRule(
            predicate=lambda v: bool(regex.match(str(v))),
            message=msg
        )
```

### Usage Example

```python
class IntervalDefinition(DataclassProtocol):
    """Numeric interval control."""

    minimum: float
    maximum: float
    step: float = 1.0
    default: float | None = None

    def __post_init__(self):
        """Build validator on initialization."""
        self._validator = Validator(
            Validators.is_type((int, float), "Value must be numeric"),
            Validators.in_range(
                self.minimum, self.maximum,
                f"Value must be between {self.minimum} and {self.maximum}"
            )
        )

    def validate_value(self, value: Any) -> float:
        """Validate interval value."""
        return self._validator(value)

    def get_default(self) -> float:
        """Return default or minimum."""
        return self.default if self.default is not None else self.minimum
```

### Advantages

1. **Lightweight**: No external dependencies
2. **Composable**: Chain multiple validators
3. **Reusable**: Library of common validators
4. **Extensible**: Easy to add custom rules
5. **Type-safe**: Works with type checkers

---

## 4. Array Type: Inheritance Pattern

Per review feedback, use inheritance for ABC abstract method enforcement:

```python
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Sequence
from frigid import DataclassProtocol

T = TypeVar('T')

class ArrayDefinition(DataclassProtocol, ABC, Generic[T]):
    """Array container control definition.

    Attributes:
        element_definition: Definition for array elements
        min_size: Minimum number of elements (0 = no minimum)
        max_size: Maximum number of elements (None = no maximum)
        default_elements: Default elements on creation
        allow_duplicates: Whether duplicate values are allowed
    """

    element_definition: ControlDefinition
    min_size: int = 0
    max_size: int | None = None
    default_elements: Sequence[Any] = ()
    allow_duplicates: bool = True

    def validate_value(self, value: Sequence[Any]) -> tuple:
        """Validate array value.

        Checks:
        - Is a sequence
        - Size constraints
        - Each element valid per element_definition
        - No duplicates (if configured)

        Args:
            value: Sequence to validate

        Returns:
            Validated tuple of elements

        Raises:
            ValidationError: If validation fails
        """
        if not isinstance(value, Sequence):
            raise ValidationError("Array value must be a sequence")

        # Check size constraints
        size = len(value)
        if size < self.min_size:
            raise ValidationError(
                f"Array must have at least {self.min_size} elements"
            )
        if self.max_size is not None and size > self.max_size:
            raise ValidationError(
                f"Array must have at most {self.max_size} elements"
            )

        # Validate each element
        validated = tuple(
            self.element_definition.validate_value(elem)
            for elem in value
        )

        # Check uniqueness if required
        if not self.allow_duplicates and len(validated) != len(set(validated)):
            raise ValidationError("Array elements must be unique")

        return validated

    def create_value(self, initial: Sequence[Any] | None = None) -> 'ArrayValue':
        """Create array value."""
        elements = initial if initial is not None else self.default_elements
        validated = self.validate_value(elements)
        return ArrayValue(definition=self, current=validated)

    def serialize_value(self, value: Sequence[Any]) -> list:
        """Serialize array to list."""
        return [
            self.element_definition.serialize_value(elem)
            for elem in value
        ]

    def get_default(self) -> tuple:
        """Return default elements."""
        return tuple(self.default_elements)


class ArrayValue(DataclassProtocol, Generic[T]):
    """Array control value holder.

    Provides operations for manipulating array elements.
    All operations return new ArrayValue (immutable).

    Attributes:
        definition: Array definition
        current: Current array elements (tuple)
    """

    definition: ArrayDefinition[T]
    current: tuple[T, ...]

    def update(self, new_value: Sequence[Any]) -> Self:
        """Replace entire array."""
        validated = self.definition.validate_value(new_value)
        return ArrayValue(definition=self.definition, current=validated)

    def append(self, element: Any) -> Self:
        """Append element to array.

        Args:
            element: Element to append

        Returns:
            New ArrayValue with element appended

        Raises:
            ValidationError: If constraints violated
        """
        new_elements = (*self.current, element)
        return self.update(new_elements)

    def remove_at(self, index: int) -> Self:
        """Remove element at index.

        Args:
            index: Index to remove

        Returns:
            New ArrayValue with element removed

        Raises:
            IndexError: If index out of range
            ValidationError: If constraints violated
        """
        if not 0 <= index < len(self.current):
            raise IndexError(f"Index {index} out of range")
        new_elements = (*self.current[:index], *self.current[index+1:])
        return self.update(new_elements)

    def insert_at(self, index: int, element: Any) -> Self:
        """Insert element at index."""
        new_elements = (*self.current[:index], element, *self.current[index:])
        return self.update(new_elements)

    def reorder(self, new_order: Sequence[int]) -> Self:
        """Reorder elements by indices."""
        new_elements = tuple(self.current[i] for i in new_order)
        return self.update(new_elements)

    def serialize(self) -> list:
        """Serialize current array."""
        return self.definition.serialize_value(self.current)
```

### Container UI Hints

For collapsible sections and layout control:

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


class ArrayDefinition(DataclassProtocol, ABC, Generic[T]):
    """Array with UI hints."""

    element_definition: ControlDefinition
    min_size: int = 0
    max_size: int | None = None
    default_elements: Sequence[Any] = ()
    allow_duplicates: bool = True

    # UI customization
    container_hints: ContainerHints = field(default_factory=ContainerHints)
```

---

## 5. Deferred Features

Per review feedback, defer these to future phases:

### Additional Control Types (Phase 2+)
- Integer (distinct from Interval)
- Float (continuous numeric)
- Date/Time
- Color
- File/Path
- Composite/Struct
- Union/Variant
- Reference

### Advanced Features (Phase 3+)
- Computed/derived controls
- Undo/redo support
- Access control (read-only, disabled, hidden)
- Schema evolution/versioning
- Reactive programming (observables)

### Focus for Phase 1

**Core types only:**
1. Boolean
2. Text
3. Interval (numeric range)
4. Options (enumeration)
5. Array (container)

**Essential features:**
- Definition/Value split
- Validation framework
- Serialization (JSON)
- TOML descriptor parsing
- Basic UI hints

---

## 6. Revised Implementation Phases

### Phase 1: Foundation (MVP)
**Goal:** Core functionality with 5 basic types

1. Base abstractions (ControlDefinition, ControlValue protocols)
2. Custom validation framework
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

### Phase 4: Advanced Types (If Needed)
**Goal:** Extended type system

1. Additional types based on real use cases
2. Composite types
3. Cross-control dependencies
4. Computed controls

### Phase 5: Production Readiness
**Goal:** Robustness and performance

1. Performance optimization
2. Comprehensive documentation
3. Migration guides
4. Production examples
5. Benchmarks

---

## 7. Open Questions from Initial Review

### Q1: Should controls integrate directly with LLM APIs?
**Clarification Needed:**
- Should `IntervalDefinition("temperature")` serialize directly to `{"temperature": 0.7}` for API calls?
- Or should there be a separate layer that maps controls to API parameters?

### Q2: Prompt template integration?
**Clarification Needed:**
- Does this library handle template expansion (Jinja2, etc.)?
- Or does it just provide values to external template engines?

### Q3: Multiple value support?
**Use Case:** Some controls may need to track history or multiple states
- Current value
- Previous value (for change detection)
- Default value (for reset)

Should ControlValue support this natively or leave it to application layer?

### Q4: Validation error handling strategy?
**Options:**
1. Exceptions (current approach)
2. Result types (Ok/Err pattern)
3. Error accumulation (collect all errors before raising)

Which is preferred?

### Q5: Registry pattern scope?
**Options:**
1. Global type registry
2. Contextual (per-application)
3. Explicit (pass registry around)

Which approach fits the project philosophy?

---

## 8. Summary of Changes from Initial Proposal

| Aspect | Initial Proposal | Revised Approach |
|--------|-----------------|------------------|
| **Terminology** | Instance | Value |
| **Base Classes** | ABC or Protocol | Protocol + DataclassProtocol + abstractmethod |
| **Validation** | Pydantic | Custom lightweight framework |
| **Array Design** | Composition question | Inheritance (ABC enforcement) |
| **Additional Types** | Phase 1 | Deferred to Phase 2+ |
| **Dependencies** | Pydantic, attrs considered | None (use frigid, absence) |
| **Container Features** | Not specified | UI hints (collapsible, orientation) |

---

## 9. Next Steps

1. **Get feedback** on terminology choice (Value vs State vs Binding vs Model)
2. **Clarify** open questions (Q1-Q5 above)
3. **Prototype** core abstractions with frigid.DataclassProtocol
4. **Implement** one complete type (Boolean) as proof-of-concept
5. **Test** the pattern with actual usage scenarios
6. **Iterate** based on findings

---

## 10. Example: Complete Boolean Type

Here's what a complete Boolean implementation would look like with the revised architecture:

```python
# vibecontrols/types/boolean.py

from abc import abstractmethod
from typing import Any, Self
from frigid import DataclassProtocol

from vibecontrols.exceptions import ValidationError
from vibecontrols.protocols import ControlDefinition, ControlValue


class BooleanDefinition(DataclassProtocol):
    """Boolean control definition.

    Validates strict boolean values (no truthy/falsy conversion).

    Attributes:
        default: Default boolean value
        validation_message: Custom error message for invalid values

    Example:
        >>> defn = BooleanDefinition(default=False)
        >>> value = defn.create_value()
        >>> value.current
        False
        >>> updated = value.update(True)
        >>> updated.current
        True
    """

    default: bool = False
    validation_message: str = "Value must be a boolean (True or False)"

    def validate_value(self, value: Any) -> bool:
        """Validate boolean with strict type checking.

        Args:
            value: Value to validate

        Returns:
            Validated boolean value

        Raises:
            ValidationError: If value is not exactly True or False
        """
        # Strict check: reject truthy/falsy non-booleans
        if not isinstance(value, bool):
            raise ValidationError(self.validation_message)
        return value

    def create_value(self, initial: Any = None) -> 'BooleanValue':
        """Create boolean value holder.

        Args:
            initial: Initial value (None uses default)

        Returns:
            New BooleanValue with validated initial state
        """
        initial_val = initial if initial is not None else self.default
        validated = self.validate_value(initial_val)
        return BooleanValue(definition=self, current=validated)

    def serialize_value(self, value: bool) -> bool:
        """Serialize boolean value.

        Booleans serialize as-is (JSON compatible).

        Args:
            value: Boolean to serialize

        Returns:
            The boolean value
        """
        return value

    def get_default(self) -> bool:
        """Get default value.

        Returns:
            Default boolean value
        """
        return self.default


class BooleanValue(DataclassProtocol):
    """Boolean control value holder.

    Immutable pairing of a boolean definition with current state.

    Attributes:
        definition: The boolean definition
        current: Current boolean value

    Example:
        >>> defn = BooleanDefinition(default=False)
        >>> value = BooleanValue(definition=defn, current=True)
        >>> value.current
        True
        >>> toggled = value.toggle()
        >>> toggled.current
        False
    """

    definition: BooleanDefinition
    current: bool

    def update(self, new_value: Any) -> Self:
        """Update to new boolean value.

        Args:
            new_value: New boolean value

        Returns:
            New BooleanValue with updated state

        Raises:
            ValidationError: If new_value is not a boolean
        """
        validated = self.definition.validate_value(new_value)
        return BooleanValue(definition=self.definition, current=validated)

    def toggle(self) -> Self:
        """Toggle the boolean value.

        Returns:
            New BooleanValue with inverted state
        """
        return self.update(not self.current)

    def serialize(self) -> bool:
        """Serialize current value.

        Returns:
            Current boolean value
        """
        return self.definition.serialize_value(self.current)
```

This shows:
- Clean Protocol implementation
- frigid.DataclassProtocol for immutability
- Custom validation
- Type-specific operations (toggle)
- Comprehensive docstrings
- Immutable update pattern

---

## Conclusion

The revised architecture addresses all review feedback:

✅ Better terminology (Value instead of Instance)
✅ Protocol + DataclassProtocol pattern with abstractmethod
✅ Custom validation framework (no Pydantic/attrs)
✅ Inheritance pattern for Arrays
✅ Deferred advanced types to future phases
✅ Container UI hints for collapsible sections

Ready to proceed with implementation once terminology and open questions are confirmed!
