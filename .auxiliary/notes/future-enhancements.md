# Future Enhancements and Aspirational Features

**Date:** 2025-11-19
**Status:** Tracking for post-MVP phases

## Expression Evaluation System

**Priority:** Phase 3+
**Status:** Aspirational - was never implemented in ai-experiments

### Motivation

Allow dynamic control parameter values that reference other configuration:

```toml
[[converser.controls]]
name = 'max-tokens'
species = 'discrete-interval'
default-from-expression = '{attribute:maximum}'
maximum-from-expression = '{variable:tokens-limits.per-response}'
```

### Expression Syntax

From ai-experiments TOML:
- `{variable:path.to.value}` - Reference variable from config
- `{attribute:field}` - Reference attribute of same control/definition

### Design Considerations

**Evaluation Timing:**
- Static evaluation at load time vs deferred evaluation
- Need context object with available variables

**Complexity:**
- Requires variable resolution system
- Need to handle circular dependencies
- Error handling for missing variables

**Scope:**
- Simple path lookup
- Or full expression language (arithmetic, conditionals)?

### Decision

**NOT in MVP.** Record as future enhancement when use cases emerge.

Simpler alternative: Just use default Python expressions in code, reserve TOML for static configuration.

---

## Additional Control Types

### Planned for Phase 2+

**Integer Control:**
- Distinct from Interval (discrete vs continuous semantics)
- May just be Interval with grade=1

**Float Control:**
- Continuous numeric without interval constraints
- May be redundant with Interval

**Date/Time Controls:**
- DateControl, TimeControl, DateTimeControl
- Timezone handling complexity

**Color Control:**
- HEX, RGB, HSL formats
- Color picker widgets

**File/Path Control:**
- File browser integration
- Path validation
- Accept/reject patterns

### Deferred Indefinitely

**Composite/Struct Control:**
- Nested control groups with named fields
- May be redundant with Sequence if we implement that

**Union/Variant Control:**
- Discriminated union of control types
- High complexity, unclear use case

**Reference Control:**
- Reference to another control's value
- Dependency tracking complexity

---

## Advanced Validation Features

### Conditional Validation

**Use Case:** Validate one control based on another's value

```python
# If persona == 'formal', require proper capitalization
if persona.current == 'formal':
    text_control.definition.pattern = r'^[A-Z].*'
```

**Complexity:** Cross-control dependencies, evaluation order

**Status:** Deferred to Phase 3+

### Custom Validators via Plugin System

**Use Case:** User-defined validation logic

```python
def validate_email(value: str) -> str:
    if '@' not in value:
        raise ValidationError("Must be valid email")
    return value

# Register custom validator
CUSTOM_VALIDATORS['email'] = validate_email
```

**Status:** Can be added with simple registry pattern when needed

---

## UI Framework Enhancements

### Auto-Layout System

**Use Case:** Automatic responsive layouts based on hints

```python
hints = LayoutHints(
    breakpoints={'sm': 1, 'md': 2, 'lg': 3},  # columns at different sizes
    grouping='auto'
)
```

**Status:** UI framework responsibility, not core library

### Theming Support

**Use Case:** Consistent styling across controls

**Status:** Framework-specific, use `framework_hints` dict

---

## Performance Optimizations

**Deferred until proven bottleneck** (per architecture principles)

Potential areas if needed:
- Validation caching for expensive operations
- Lazy evaluation of defaults
- Immutable datastructure optimization (structural sharing)

---

## Developer Experience

### Better Error Messages

**Current:** Basic exception messages
**Future:** Rich context with suggestions

```python
raise ValidationError(
    "Invalid temperature value",
    control_name="temperature",
    expected_range=(0.0, 1.0),
    actual_value=1.5,
    suggestion="Temperature must be between 0.0 and 1.0"
)
```

### Type Stub Generation

Auto-generate .pyi files for better IDE support

### Documentation Generation

Auto-generate control documentation from definitions

---

## Changelog

- 2025-11-19: Initial future enhancements tracking
