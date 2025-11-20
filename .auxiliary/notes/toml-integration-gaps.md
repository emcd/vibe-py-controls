# TOML Integration Gaps and Design Decisions

**Date:** 2025-11-19
**Status:** Analysis complete, decisions recorded
**Context:** Comparison with ai-experiments reference implementation

## Executive Summary

Analyzed gaps between current implementation and requirements for TOML-based control loading (prompt templates and model specifications). This document records decisions on how to address each gap.

---

## Gap Analysis

### 1. Array/Sequence Terminology ✅ RESOLVED

**Status:** Clarified by user

**User Clarification:**
> "It was my intent to rename `FlexArray` to `Sequence`. The original `FlexArray` could handle nesting of arbitrary controls, including other `FlexArray` controls."

**What This Means:**
- There is only ONE array-like control type
- Original name: `FlexArray` (in ai-experiments)
- Intended name: `Sequence` (for this project)
- Our implementation: `Array`
- Capability: Can nest arbitrary controls, including other arrays
- UI hints needed: orientation, collapsible

**Verification:**
✅ Our `ArrayHints` already has:
```python
orientation: Literal["horizontal", "vertical", "grid"] = "vertical"
collapsible: bool = False
initially_collapsed: bool = False
```

**Decision:** ✅ **No gap - we have this**
- Our `Array` implementation matches the intended `Sequence` functionality
- Has all needed UI hints (orientation, collapsible)
- Supports arbitrary nesting via `element_definition: ControlDefinition`

---

### 2. Factory/Descriptor Pattern

**Status:** Planned for Phase 2, already documented

**What's Needed:**
```python
BUILTIN_TYPES: dict[str, type[ControlDefinition]] = {
    "boolean": BooleanDefinition,
    "text": TextDefinition,
    "discrete-interval": IntervalDefinition,  # Note: dash in name
    "options": OptionsDefinition,
    "flex-array": ArrayDefinition,
    # "sequence": SequenceDefinition,  # If distinct from array
}

def descriptor_to_definition(descriptor: dict) -> ControlDefinition:
    """Create control definition from TOML descriptor."""
    species = descriptor.get("species")
    class_ = BUILTIN_TYPES[species]
    # ... instantiation logic
```

**Decision:** Already covered in architecture-initial.md lines 480-563. Defer to deserialization phase.

---

### 3. Deserialization from TOML

**Status:** Planned for Phase 2

**Decision:** Already documented in architecture roadmap. Current focus is on proving Definition → Control pattern works with in-memory objects.

---

### 4. Nested Definition Handling

**Status:** Structurally supported, needs factory integration

**Current Implementation:**
```python
class ArrayDefinition:
    element_definition: __.ControlDefinition  # Accepts definition object
```

**TOML Format:**
```toml
[[variables]]
species = 'flex-array'
[variables.element]  # Nested descriptor, not object
species = 'text'
```

**What's Needed:**
When deserializing, recursively call `descriptor_to_definition()`:
```python
def instantiate_array_from_descriptor(descriptor: dict) -> ArrayDefinition:
    element_descriptor = descriptor.pop('element')
    element_def = descriptor_to_definition(element_descriptor)  # Recursive
    return ArrayDefinition(element_definition=element_def, **descriptor)
```

**Decision:** ✅ Our `Array` structure already supports this. Just needs factory pattern implementation in Phase 2.

---

### 5. Options Structure: Choice Labels

**Status:** Need design decision

**Original Format:**
```toml
[variables.options]
collaborator = { label = 'Collaborator' }
redditor = { label = 'Redditor / Stack Overflower' }
```

**Current Implementation:**
```python
class OptionsDefinition:
    choices: __.cabc.Sequence[__.typx.Any]  # Flat sequence, no labels
```

**Question:** Where should labels go?
- Overall control label: "Persona:" → Goes on `OptionsHints.label` ✅
- Per-choice labels: "Collaborator", "Redditor / Stack Overflower" → ???

**Options:**
A. Keep flat choices, labels are UI framework responsibility
B. Add optional choice labels: `choices: Sequence[Any | tuple[Any, str]]`
C. Create `Choice` dataclass: `@dataclass class Choice: value: Any; label: str | None`

**Analysis:**

**Option A: On OptionsDefinition**
```python
@dataclass(frozen=True)
class Choice:
    value: Any
    label: str | None = None

class OptionsDefinition:
    choices: Sequence[Choice]
```
*Pros:*
- Labels are semantic data about the choices themselves
- Same definition reusable with same labels
- Serialization includes labels (if needed for TOML roundtrip)
- Validation can reference labels in error messages
- In TOML, labels defined alongside choices (not separate UI section)

*Cons:*
- Couples data structure to presentation
- Definition becomes more complex
- Needs "display value" vs "internal value" distinction

**Option B: On OptionsHints**
```python
class OptionsHints:
    choice_labels: dict[Any, str] | None = None
```
*Pros:*
- Clean separation: Definition = logic, Hints = presentation
- Same definition can have different labels in different UIs
- Keeps Definition simple
- Consistent with other hint attributes

*Cons:*
- Must keep labels in sync with choices
- Can't serialize labels with values
- More work for UI adapters

**Recommendation:** Option A (on Definition)
- Labels are part of choice identity, not just presentation
- TOML structure shows labels alongside choices
- Enables TOML serialization roundtrips
- UI frameworks can still ignore labels if desired

**Decision:** 🔄 **Awaiting user preference**

---

### 6. Expression Evaluation

**Status:** Aspirational, not in MVP

**Original Syntax:**
```toml
maximum-from-expression = '{variable:tokens-limits.per-response}'
default-from-expression = '{attribute:maximum}'
```

**Decision:** ✓ Record as future enhancement
- Never implemented in ai-experiments either
- Deferred to Phase 3+ ("Advanced Features")
- Document in architecture-initial.md advanced features section

**Location:** Document in `.auxiliary/notes/future-enhancements.md`

---

### 7. Optional Controls

**Status:** Need to add

**Original Usage:**
```toml
[[converser.controls.elements]]
name = 'top-k'
optional = true  # User can toggle whether to include this control
species = 'discrete-interval'
```

**What's Needed:**
Add metadata flag to all Definition classes:
```python
class BooleanDefinition(DataclassObject):
    optional: bool = False  # Metadata, not validated
    # ... existing fields
```

**Decision:** ✅ **Implement in next iteration**
- Simple boolean flag on Definition
- UI frameworks can hide/show optional controls
- Doesn't affect validation logic

**Priority:** Medium - needed for model specifications TOML

---

### 8. Attribute Handling: Per-Framework Hints

**Status:** Design approved

**Current Implementation:**
```python
@dataclass
class BooleanHints:
    widget_preference: Literal["checkbox", "toggle", "radio"] | None = None
    label: str | None = None
    help_text: str | None = None
```

**Enhancement Needed:**
```python
from dataclasses import field

@dataclass
class BooleanHints:
    widget_preference: Literal["checkbox", "toggle", "radio"] | None = None
    label: str | None = None
    help_text: str | None = None

    # Escape hatch for framework-specific customization
    framework_hints: dict[str, dict[str, __.typx.Any]] = field(default_factory=dict)
    # Example:
    # {
    #     "panel": {"sizing_mode": "stretch_width", "css_classes": ["custom"]},
    #     "streamlit": {"help": "extended help text"},
    #     "rich": {"border_style": "blue"}
    # }
```

**Decision:** ✅ **Add to all Hints classes**
- Keeps strongly-typed common hints
- Provides escape hatch for framework-specific needs
- Doesn't pollute main hint attributes

**Priority:** Low - can be added anytime without breaking changes

---

### 9. Naming Conventions: Latin Etymology and Quantifier Placement

**Status:** Requires refactoring

**Current Issues:**

**A. Mixed Etymology:**
- `max_length` (Latin maximum + Germanic)
- `min_size` (Latin minimum + Germanic)
- `step` (Germanic) vs `grade` (Latin gradus)

**B. Quantifier Placement:**
Project standard: Quantifiers as **suffixes**
- ❌ `max_size`, `min_size`, `max_length`, `min_length`
- ✅ `size_maximum`, `size_minimum`, `length_maximum`, `length_minimum`

**C. Exception Names:**
- `TypeInvalidity` - OK (both Latin-derived)
- `SizeConstraintViolation` - OK
- But need to audit all exception names for consistency

**Required Changes:**

**Parameter Names (Array):**
```python
# Current
class ArrayDefinition:
    min_size: int = 0
    max_size: int | None = None

# Should be:
class ArrayDefinition:
    size_min: int = 0
    size_max: int | None = None
```

**Parameter Names (Text):**
```python
# Current
class TextDefinition:
    min_length: int | None = None
    max_length: int | None = None

# Should be (prefer "count" over "length"):
class TextDefinition:
    count_min: int | None = None
    count_max: int | None = None
```

**Note on Etymology:**
- "size" is actually Latin-derived (via Old French "sise" from Latin "sessus")
- "min/max" abbreviations are acceptable (common usage)
- Prefer "count" or "quantity" over "length" where possible

**Parameter Names (Interval):**
```python
# Current
class IntervalDefinition:
    minimum: float
    maximum: float
    step: float | None = None  # Germanic

# Should be:
class IntervalDefinition:
    minimum: float  # Already correct (no quantifier)
    maximum: float  # Already correct
    grade: float | None = None  # Latin gradus - matches ai-experiments
```

**Decision:** ✅ **Refactor after conversation compaction**
1. Audit all parameter names across all files
2. Apply naming conventions:
   - Quantifiers as suffixes: `size_min`, `size_max`
   - Use "min/max" abbreviations (acceptable)
   - Prefer "count" over "length" where possible
   - Use Latin-derived terms consistently
3. Update tests to match
4. Update documentation

**Breaking Change:** Yes, but pre-release so acceptable

**Priority:** HIGH - do before adding more control types

**User Note:** Wait for conversation compaction before starting

---

## Implementation Priorities

### Must Have (Before Phase 2)
1. ✅ Core control types (Boolean, Text, Interval, Options, Array) - **DONE**
2. 🔄 Naming convention refactor - **NEXT SESSION**
3. 🔄 Add `optional` flag to Definitions - **NEXT SESSION**
4. 🔄 Clarify Sequence vs Array distinction - **NEEDS USER INPUT**

### Should Have (Phase 2: Deserialization)
5. Factory pattern implementation
6. Nested descriptor handling
7. Options choice labels (depending on decision)

### Nice to Have (Phase 2+)
8. Per-framework hints dictionary
9. Expression evaluation (Phase 3+)

---

## References

- ai-experiments controls: https://github.com/emcd/ai-experiments/blob/master/sources/aiwb/controls/core.py
- Prompt template TOML: https://github.com/emcd/ai-experiments/blob/master/data/prompts/descriptors/pair-programmer.toml
- Model attributes TOML: https://github.com/emcd/ai-experiments/blob/master/data/providers/anthropic/attributes.toml
- Architecture doc: `.auxiliary/notes/architecture-initial.md`

---

## Changelog

- 2025-11-19: Initial analysis and decision recording
