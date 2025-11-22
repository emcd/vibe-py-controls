.. vim: set fileencoding=utf-8:
.. -*- coding: utf-8 -*-
.. +--------------------------------------------------------------------------+
   |                                                                          |
   | Licensed under the Apache License, Version 2.0 (the "License");          |
   | you may not use this file except in compliance with the License.         |
   | You may obtain a copy of the License at                                  |
   |                                                                          |
   |     http://www.apache.org/licenses/LICENSE-2.0                           |
   |                                                                          |
   | Unless required by applicable law or agreed to in writing, software      |
   | distributed under the License is distributed on an "AS IS" BASIS,        |
   | WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. |
   | See the License for the specific language governing permissions and      |
   | limitations under the License.                                           |
   |                                                                          |
   +--------------------------------------------------------------------------+


*******************************************************************************
Test Plan: Control Definitions and In-Memory Control Production
*******************************************************************************

Overview
===============================================================================

This test plan addresses systematic testing of control definitions and their
production of controls in memory, focusing on validation, control creation,
and value management **without serialization or deserialization**.

**Scope:** In-memory control operations for **all control types**:

- Boolean, Text, Interval, Options, Array
- Validation framework
- Exception hierarchy
- Protocol definitions

**Out of Scope:** Serialization/deserialization testing (covered in separate
test plan)

Coverage Summary
===============================================================================

Current Coverage State
-------------------------------------------------------------------------------

As of implementation::

    Name                                  Stmts   Miss Branch BrPart  Cover
    -----------------------------------------------------------------------
    sources/vibecontrols/exceptions.py      83     42     24      0    44%
    sources/vibecontrols/interfaces.py      25      6      0      0    76%
    sources/vibecontrols/validation.py      77      0     32      0   100%
    sources/vibecontrols/controls/
        boolean.py                          32      0      4      0   100%
        text.py                             48     24     14      0    39%
        interval.py                         70     42     30      0    28%
        options.py                          68     45     26      0    24%
        array.py                            95     65     32      0    24%

**Complete:** validation.py, controls/boolean.py
**In Progress:** text.py, interval.py, options.py, array.py
**Acceptable Gaps:** interfaces.py (abstract method bodies)

Target Coverage Goals
-------------------------------------------------------------------------------

**Line Coverage:** 100% for all control type modules

**Branch Coverage:** 100% for validation and error handling paths

**Exclusions:** Abstract method bodies in protocols (``...``) may be marked
with ``# pragma: no cover`` if needed

Test Strategy
===============================================================================

Testing Approach
-------------------------------------------------------------------------------

**Dependency Injection Pattern:**
  All testing uses dependency injection rather than monkey-patching. Immutable
  objects prevent monkey-patching by design.

**Layered Testing:**

  1. **Foundations (100-300 range):** Exceptions, protocols, validators
  2. **Control Types (400+ range):** Individual control implementations
  3. **Integration:** Cross-control interactions and protocol compliance

**No External Dependencies:**
  Tests use only standard library and project dependencies. No network calls,
  no real external services.

Test Module Organization
-------------------------------------------------------------------------------

**Foundation Test Modules:**

- ``test_000_package.py`` - Package sanity checks
- ``test_010_base.py`` - Common imports verification
- ``test_100_exceptions.py`` - Exception hierarchy
- ``test_200_interfaces.py`` - Protocol definitions
- ``test_300_validation.py`` - Validator framework

**Control Type Test Modules:**

- ``test_400_controls_boolean.py`` - Boolean control
- ``test_410_controls_text.py`` - Text control
- ``test_420_controls_interval.py`` - Interval control
- ``test_430_controls_options.py`` - Options control
- ``test_440_controls_array.py`` - Array control

**Numbering Rationale:**

- **100-level:** Foundational exceptions (lowest dependency)
- **200-level:** Core abstractions (protocols depend on exceptions)
- **300-level:** Validation framework (depends on exceptions and protocols)
- **400-level:** Concrete control types (depends on all above)

General Test Pattern for Control Types
===============================================================================

Standard Test Structure
-------------------------------------------------------------------------------

Each control type test module must follow this standardized structure to
ensure comprehensive coverage and consistency across all control types:

**Test Function Number Ranges:**

- **000-099:** Hints dataclass

  - Default creation
  - Individual field setting
  - All fields together
  - Immutability verification

- **100-199:** Definition creation and configuration

  - Default creation (all defaults)
  - Custom individual parameters
  - All parameters together
  - Immutability verification
  - ``__post_init__`` validation (parameter constraints)

- **200-299:** Definition.validate_value()

  - Valid inputs (type-specific values)
  - Invalid types (wrong types)
  - Invalid values (constraint violations)
  - Custom validation messages
  - Exception types verification
  - Edge cases and boundaries

- **300-399:** Definition.produce_control()

  - Without initial value (uses default)
  - With valid initial values
  - With invalid initial values (raises exception)
  - Explicit absent handling
  - Returns correct control type
  - Definition immutability after production

- **400-499:** Definition.serialize_value()

  - Type-specific serialization format
  - Note: Full serialization/deserialization in separate plan

- **500-599:** Definition.produce_default()

  - Default value production
  - Custom default values

- **600-699:** Control creation and attributes

  - Direct creation with definition and current
  - Definition attribute access
  - Current attribute access
  - Immutability verification

- **700-799:** Control.copy()

  - Copy with new valid values
  - Returns new instance (not same object)
  - Preserves definition reference
  - Invalid values raise exceptions
  - Original unchanged (immutability)

- **800-899:** Control type-specific methods

  - Boolean: ``toggle()``
  - Text: ``clear()``
  - Interval: ``increment()``, ``decrement()``
  - Options: (none currently)
  - Array: ``append()``, ``remove_at()``, ``insert_at()``, ``reorder()``

- **900-999:** Control.serialize()

  - Serializes current value
  - Delegates to definition.serialize_value()

- **1000-1099:** Integration scenarios

  - Complete lifecycle (create → validate → update → serialize)
  - Multiple controls sharing same definition
  - Controls are independent (modifying one doesn't affect another)
  - Protocol compliance verification

Testing Patterns
-------------------------------------------------------------------------------

**Immutability Verification:**

  All tests that create or update objects must verify immutability:

  1. Create original object
  2. Perform operation (should return new instance)
  3. Assert original is unchanged
  4. Assert new instance has expected value
  5. Assert ``id(original) != id(new_instance)``

**Exception Testing:**

  Use ``pytest.raises`` with message inspection::

    with pytest.raises(ControlInvalidity, match="expected text") as exc_info:
        validator(invalid_value)

**Protocol Compliance Testing:**

  Use ``hasattr`` checks and signature inspection::

    assert hasattr(definition, 'validate_value')
    assert hasattr(definition, 'produce_control')
    assert callable(definition.validate_value)

**Fixture Usage:**

  Create reusable fixtures for common test objects in conftest.py or module
  scope.

Control Type: Text
===============================================================================

**Module:** ``sources/vibecontrols/controls/text.py``

**Test Module:** ``test_410_controls_text.py``

**Target Coverage:** 100%

Key Features
-------------------------------------------------------------------------------

- String validation (strict type checking)
- Length constraints (``count_min``, ``count_max``)
- Type-specific method: ``clear()`` returns control with empty string
- Multiline support (metadata only, no validation impact)

Required Test Coverage
-------------------------------------------------------------------------------

**000-099: TextHints dataclass**

- ``test_000_text_hints_default_creation`` - Create with all defaults
- ``test_010_text_hints_with_widget`` - Set widget_preference (input)
- ``test_015_text_hints_with_textarea`` - Set widget_preference (textarea)
- ``test_020_text_hints_with_multiline`` - Set multiline flag
- ``test_030_text_hints_with_placeholder`` - Set placeholder text
- ``test_040_text_hints_with_label`` - Set label
- ``test_050_text_hints_with_help`` - Set help_text
- ``test_060_text_hints_all_fields`` - Set all fields together
- ``test_070_text_hints_immutability`` - Cannot modify after creation

**100-199: TextDefinition creation and configuration**

- ``test_100_text_definition_default_creation`` - Create with all defaults
- ``test_110_text_definition_custom_default`` - Set custom default string
- ``test_120_text_definition_count_min`` - Set count_min only
- ``test_130_text_definition_count_max`` - Set count_max only
- ``test_140_text_definition_both_counts`` - Set both count_min and count_max
- ``test_150_text_definition_custom_message`` - Set validation_message
- ``test_160_text_definition_custom_hints`` - Set custom hints
- ``test_170_text_definition_all_parameters`` - Set all parameters
- ``test_180_text_definition_immutability`` - Cannot modify after creation
- ``test_190_text_definition_invalid_negative_count_min`` - Negative count_min raises DefinitionInvalidity
- ``test_191_text_definition_invalid_negative_count_max`` - Negative count_max raises DefinitionInvalidity
- ``test_192_text_definition_invalid_min_exceeds_max`` - count_min > count_max raises DefinitionInvalidity

**200-299: TextDefinition.validate_value()**

- ``test_200_validate_value_valid_string`` - Valid non-empty string
- ``test_210_validate_value_empty_string`` - Empty string (valid by default)
- ``test_220_validate_value_long_string`` - Very long string
- ``test_230_validate_value_unicode`` - Unicode characters (emoji, etc.)
- ``test_240_validate_value_newlines`` - Strings with newline characters
- ``test_250_validate_value_at_count_min`` - Exactly at count_min boundary
- ``test_260_validate_value_at_count_max`` - Exactly at count_max boundary
- ``test_270_validate_value_below_count_min`` - Below count_min raises SizeConstraintViolation
- ``test_280_validate_value_above_count_max`` - Above count_max raises SizeConstraintViolation
- ``test_290_validate_value_invalid_integer`` - Integer raises ControlInvalidity
- ``test_291_validate_value_invalid_bool`` - Boolean raises ControlInvalidity
- ``test_292_validate_value_invalid_none`` - None raises ControlInvalidity
- ``test_293_validate_value_invalid_list`` - List raises ControlInvalidity
- ``test_294_validate_value_custom_message`` - Custom message in exception

**300-399: TextDefinition.produce_control()**

- ``test_300_produce_control_no_initial`` - Use default value
- ``test_310_produce_control_initial_valid`` - Set valid initial string
- ``test_320_produce_control_initial_empty`` - Set empty initial string
- ``test_330_produce_control_invalid_initial`` - Invalid initial raises exception
- ``test_340_produce_control_absent`` - Explicit absent uses default
- ``test_350_produce_control_returns_text`` - Returns Text control type
- ``test_360_produce_control_immutability`` - Definition unchanged after production

**400-499: TextDefinition.serialize_value()**

- ``test_400_serialize_value_string`` - String serializes as-is
- ``test_410_serialize_value_empty`` - Empty string serializes as-is
- ``test_420_serialize_value_unicode`` - Unicode string serializes correctly

**500-599: TextDefinition.produce_default()**

- ``test_500_produce_default_empty`` - Default is empty string
- ``test_510_produce_default_custom`` - Custom default respected

**600-699: Text control creation and attributes**

- ``test_600_text_control_creation`` - Create with definition and current
- ``test_610_text_control_definition_attribute`` - Has definition attribute
- ``test_620_text_control_current_attribute`` - Has current attribute
- ``test_630_text_control_immutability`` - Cannot modify attributes

**700-799: Text.copy()**

- ``test_700_copy_to_new_string`` - Copy with new string value
- ``test_710_copy_to_empty`` - Copy with empty string
- ``test_720_copy_returns_new_instance`` - Returns different instance
- ``test_730_copy_preserves_definition`` - Definition unchanged
- ``test_740_copy_invalid_value`` - Invalid value raises ControlInvalidity
- ``test_750_copy_original_unchanged`` - Original control unchanged

**800-899: Text.clear()**

- ``test_800_clear_returns_empty`` - clear() returns control with empty string
- ``test_810_clear_returns_new_instance`` - Returns different instance
- ``test_820_clear_preserves_definition`` - Definition unchanged
- ``test_830_clear_original_unchanged`` - Original control unchanged
- ``test_840_clear_with_count_min`` - clear() with count_min constraint (may violate if count_min > 0)

**900-999: Text.serialize()**

- ``test_900_serialize_string`` - Serialize non-empty string
- ``test_910_serialize_empty`` - Serialize empty string
- ``test_920_serialize_delegates_to_definition`` - Uses definition.serialize_value()

**1000-1099: Integration scenarios**

- ``test_1000_complete_lifecycle`` - Create → validate → update → serialize
- ``test_1010_multiple_controls_same_definition`` - Share definition across controls
- ``test_1020_controls_independent`` - Modifying one doesn't affect another
- ``test_1030_protocol_compliance`` - Implements Control and ControlDefinition protocols

Control Type: Interval
===============================================================================

**Module:** ``sources/vibecontrols/controls/interval.py``

**Test Module:** ``test_420_controls_interval.py``

**Target Coverage:** 100%

Key Features
-------------------------------------------------------------------------------

- Numeric validation (int and float accepted)
- Range constraints (``minimum``, ``maximum``)
- Optional step validation (``grade`` for discrete intervals)
- Type-specific methods: ``increment()``, ``decrement()``
- Floating-point precision handling (``_FLOAT_EPSILON``)

Required Test Coverage
-------------------------------------------------------------------------------

**000-099: IntervalHints dataclass**

- ``test_000_interval_hints_default_creation`` - Create with all defaults
- ``test_010_interval_hints_with_slider`` - Set widget_preference (slider)
- ``test_015_interval_hints_with_spinbox`` - Set widget_preference (spinbox)
- ``test_020_interval_hints_with_horizontal`` - Set orientation (horizontal)
- ``test_025_interval_hints_with_vertical`` - Set orientation (vertical)
- ``test_030_interval_hints_with_ticks`` - Set show_ticks flag
- ``test_040_interval_hints_with_value`` - Set show_value flag
- ``test_050_interval_hints_with_label`` - Set label
- ``test_060_interval_hints_with_help`` - Set help_text
- ``test_070_interval_hints_all_fields`` - Set all fields together
- ``test_080_interval_hints_immutability`` - Cannot modify after creation

**100-199: IntervalDefinition creation and configuration**

- ``test_100_interval_definition_default_creation`` - Create with required parameters
- ``test_110_interval_definition_with_grade`` - Set grade for discrete interval
- ``test_120_interval_definition_without_grade`` - grade=None for continuous
- ``test_130_interval_definition_custom_message`` - Set validation_message
- ``test_140_interval_definition_custom_hints`` - Set custom hints
- ``test_150_interval_definition_all_parameters`` - Set all parameters
- ``test_160_interval_definition_immutability`` - Cannot modify after creation
- ``test_170_interval_definition_invalid_non_numeric_minimum`` - Non-numeric minimum raises DefinitionInvalidity
- ``test_171_interval_definition_invalid_non_numeric_maximum`` - Non-numeric maximum raises DefinitionInvalidity
- ``test_172_interval_definition_invalid_non_numeric_default`` - Non-numeric default raises DefinitionInvalidity
- ``test_173_interval_definition_invalid_minimum_exceeds_maximum`` - minimum > maximum raises DefinitionInvalidity
- ``test_174_interval_definition_invalid_default_below_minimum`` - default < minimum raises DefinitionInvalidity
- ``test_175_interval_definition_invalid_default_above_maximum`` - default > maximum raises DefinitionInvalidity
- ``test_176_interval_definition_invalid_non_numeric_grade`` - Non-numeric grade raises DefinitionInvalidity
- ``test_177_interval_definition_invalid_zero_grade`` - grade=0 raises DefinitionInvalidity
- ``test_178_interval_definition_invalid_negative_grade`` - grade<0 raises DefinitionInvalidity

**200-299: IntervalDefinition.validate_value()**

- ``test_200_validate_value_valid_integer`` - Valid integer in range
- ``test_210_validate_value_valid_float`` - Valid float in range
- ``test_220_validate_value_at_minimum`` - Exactly at minimum boundary
- ``test_230_validate_value_at_maximum`` - Exactly at maximum boundary
- ``test_240_validate_value_below_minimum`` - Below minimum raises BoundsConstraintViolation
- ``test_250_validate_value_above_maximum`` - Above maximum raises BoundsConstraintViolation
- ``test_260_validate_value_continuous_no_grade`` - grade=None allows any value in range
- ``test_270_validate_value_discrete_aligned`` - Value aligned with grade (valid)
- ``test_280_validate_value_discrete_misaligned`` - Value misaligned with grade raises StepConstraintViolation
- ``test_290_validate_value_floating_point_precision`` - Floating-point boundary precision
- ``test_291_validate_value_negative_range`` - Values in negative range (minimum=-10, maximum=-1)
- ``test_292_validate_value_range_with_zero`` - Values in range including zero
- ``test_293_validate_value_small_grade`` - Very small grade (e.g., 0.01)
- ``test_294_validate_value_invalid_string`` - String raises ControlInvalidity
- ``test_295_validate_value_invalid_bool`` - Boolean raises ControlInvalidity
- ``test_296_validate_value_invalid_none`` - None raises ControlInvalidity
- ``test_297_validate_value_custom_message`` - Custom message in exception

**300-399: IntervalDefinition.produce_control()**

- ``test_300_produce_control_no_initial`` - Use default value
- ``test_310_produce_control_initial_integer`` - Set valid initial integer
- ``test_320_produce_control_initial_float`` - Set valid initial float
- ``test_330_produce_control_invalid_initial`` - Invalid initial raises exception
- ``test_340_produce_control_absent`` - Explicit absent uses default
- ``test_350_produce_control_returns_interval`` - Returns Interval control type
- ``test_360_produce_control_immutability`` - Definition unchanged after production

**400-499: IntervalDefinition.serialize_value()**

- ``test_400_serialize_value_integer`` - Integer serializes as-is
- ``test_410_serialize_value_float`` - Float serializes as-is
- ``test_420_serialize_value_at_boundary`` - Boundary values serialize correctly

**500-599: IntervalDefinition.produce_default()**

- ``test_500_produce_default`` - Produces configured default value
- ``test_510_produce_default_custom`` - Custom default respected

**600-699: Interval control creation and attributes**

- ``test_600_interval_control_creation`` - Create with definition and current
- ``test_610_interval_control_definition_attribute`` - Has definition attribute
- ``test_620_interval_control_current_attribute`` - Has current attribute
- ``test_630_interval_control_immutability`` - Cannot modify attributes

**700-799: Interval.copy()**

- ``test_700_copy_to_new_value`` - Copy with new numeric value
- ``test_710_copy_to_minimum`` - Copy to minimum boundary
- ``test_720_copy_to_maximum`` - Copy to maximum boundary
- ``test_730_copy_returns_new_instance`` - Returns different instance
- ``test_740_copy_preserves_definition`` - Definition unchanged
- ``test_750_copy_invalid_value`` - Invalid value raises ControlInvalidity
- ``test_760_copy_original_unchanged`` - Original control unchanged

**800-899: Interval.increment() and Interval.decrement()**

- ``test_800_increment_with_grade`` - Successful increment when grade defined
- ``test_810_increment_at_maximum`` - Increment at maximum raises BoundsConstraintViolation
- ``test_820_increment_returns_new_instance`` - Returns different instance
- ``test_830_increment_preserves_definition`` - Definition unchanged
- ``test_840_increment_without_grade`` - Increment with grade=None raises IncrementOperationFailure
- ``test_850_decrement_with_grade`` - Successful decrement when grade defined
- ``test_860_decrement_at_minimum`` - Decrement at minimum raises BoundsConstraintViolation
- ``test_870_decrement_returns_new_instance`` - Returns different instance
- ``test_880_decrement_preserves_definition`` - Definition unchanged
- ``test_890_decrement_without_grade`` - Decrement with grade=None raises IncrementOperationFailure

**900-999: Interval.serialize()**

- ``test_900_serialize_integer`` - Serialize integer value
- ``test_910_serialize_float`` - Serialize float value
- ``test_920_serialize_delegates_to_definition`` - Uses definition.serialize_value()

**1000-1099: Integration scenarios**

- ``test_1000_complete_lifecycle`` - Create → validate → update → serialize
- ``test_1010_multiple_controls_same_definition`` - Share definition across controls
- ``test_1020_controls_independent`` - Modifying one doesn't affect another
- ``test_1030_protocol_compliance`` - Implements Control and ControlDefinition protocols
- ``test_1040_increment_decrement_chain`` - Chain multiple increment/decrement operations

Control Type: Options
===============================================================================

**Module:** ``sources/vibecontrols/controls/options.py``

**Test Module:** ``test_430_controls_options.py``

**Target Coverage:** 100%

Key Features
-------------------------------------------------------------------------------

- Selection from predefined choices
- Single-select and multi-select support (``allow_multiple``)
- Choice validation (value must be in choices)
- No type-specific control methods beyond base protocol

Required Test Coverage
-------------------------------------------------------------------------------

**000-099: OptionsHints dataclass**

- ``test_000_options_hints_default_creation`` - Create with all defaults
- ``test_010_options_hints_with_select`` - Set widget_preference (select)
- ``test_015_options_hints_with_radio`` - Set widget_preference (radio)
- ``test_020_options_hints_with_dropdown`` - Set widget_preference (dropdown)
- ``test_030_options_hints_with_label`` - Set label
- ``test_040_options_hints_with_help`` - Set help_text
- ``test_050_options_hints_all_fields`` - Set all fields together
- ``test_060_options_hints_immutability`` - Cannot modify after creation

**100-199: OptionsDefinition creation and configuration**

- ``test_100_options_definition_single_select`` - Create single-select (allow_multiple=False)
- ``test_110_options_definition_multi_select`` - Create multi-select (allow_multiple=True)
- ``test_120_options_definition_string_choices`` - Choices with strings
- ``test_130_options_definition_integer_choices`` - Choices with integers
- ``test_140_options_definition_mixed_type_choices`` - Choices with mixed types
- ``test_150_options_definition_custom_message`` - Set validation_message
- ``test_160_options_definition_custom_hints`` - Set custom hints
- ``test_170_options_definition_all_parameters`` - Set all parameters
- ``test_180_options_definition_immutability`` - Cannot modify after creation
- ``test_190_options_definition_invalid_empty_choices`` - Empty choices raises DefinitionInvalidity
- ``test_191_options_definition_invalid_default_not_in_choices_single`` - Default not in choices (single-select) raises DefinitionInvalidity
- ``test_192_options_definition_invalid_default_not_in_choices_multi`` - Default not in choices (multi-select) raises DefinitionInvalidity

**200-299: OptionsDefinition.validate_value()**

- ``test_200_validate_value_single_valid`` - Valid choice for single-select
- ``test_210_validate_value_single_invalid`` - Invalid choice for single-select raises ConstraintViolation
- ``test_220_validate_value_multi_valid`` - Valid choices for multi-select
- ``test_230_validate_value_multi_empty`` - Empty sequence for multi-select (valid if allowed)
- ``test_240_validate_value_multi_single_item`` - Single item for multi-select
- ``test_250_validate_value_multi_all_choices`` - All choices selected for multi-select
- ``test_260_validate_value_multi_invalid_one`` - One invalid choice in multi-select raises ConstraintViolation
- ``test_270_validate_value_multi_duplicates`` - Duplicate values in multi-select (behavior TBD)
- ``test_280_validate_value_single_when_multi_expected`` - Single value when multi-select raises
- ``test_290_validate_value_multi_when_single_expected`` - Multiple values when single-select raises
- ``test_291_validate_value_custom_message`` - Custom message in exception

**300-399: OptionsDefinition.produce_control()**

- ``test_300_produce_control_no_initial_single`` - Use default value (single-select)
- ``test_310_produce_control_no_initial_multi`` - Use default value (multi-select)
- ``test_320_produce_control_initial_valid_single`` - Set valid initial (single-select)
- ``test_330_produce_control_initial_valid_multi`` - Set valid initial (multi-select)
- ``test_340_produce_control_invalid_initial`` - Invalid initial raises exception
- ``test_350_produce_control_absent`` - Explicit absent uses default
- ``test_360_produce_control_returns_options`` - Returns Options control type
- ``test_370_produce_control_immutability`` - Definition unchanged after production

**400-499: OptionsDefinition.serialize_value()**

- ``test_400_serialize_value_single`` - Single choice serializes as value
- ``test_410_serialize_value_multi`` - Multiple choices serialize as list
- ``test_420_serialize_value_preserves_type`` - Original value type preserved

**500-599: OptionsDefinition.produce_default()**

- ``test_500_produce_default_single`` - Default single choice
- ``test_510_produce_default_multi`` - Default multiple choices
- ``test_520_produce_default_custom`` - Custom default respected

**600-699: Options control creation and attributes**

- ``test_600_options_control_creation`` - Create with definition and current
- ``test_610_options_control_definition_attribute`` - Has definition attribute
- ``test_620_options_control_current_attribute`` - Has current attribute
- ``test_630_options_control_immutability`` - Cannot modify attributes

**700-799: Options.copy()**

- ``test_700_copy_to_new_choice_single`` - Copy with new choice (single-select)
- ``test_710_copy_to_new_choices_multi`` - Copy with new choices (multi-select)
- ``test_720_copy_returns_new_instance`` - Returns different instance
- ``test_730_copy_preserves_definition`` - Definition unchanged
- ``test_740_copy_invalid_value`` - Invalid value raises ConstraintViolation
- ``test_750_copy_original_unchanged`` - Original control unchanged

**800-899: (Reserved for type-specific methods - none currently)**

**900-999: Options.serialize()**

- ``test_900_serialize_single`` - Serialize single selection
- ``test_910_serialize_multi`` - Serialize multiple selections
- ``test_920_serialize_delegates_to_definition`` - Uses definition.serialize_value()

**1000-1099: Integration scenarios**

- ``test_1000_complete_lifecycle`` - Create → validate → update → serialize
- ``test_1010_multiple_controls_same_definition`` - Share definition across controls
- ``test_1020_controls_independent`` - Modifying one doesn't affect another
- ``test_1030_protocol_compliance`` - Implements Control and ControlDefinition protocols
- ``test_1040_single_choice_edge_case`` - Single choice in choices (only one valid option)
- ``test_1050_many_choices`` - Many choices (>100) performance

Control Type: Array
===============================================================================

**Module:** ``sources/vibecontrols/controls/array.py``

**Test Module:** ``test_440_controls_array.py``

**Target Coverage:** 100%

**Complexity:** Highest - supports recursion and multiple operations

Key Features
-------------------------------------------------------------------------------

- Recursive element validation via ``element_definition``
- Size constraints (``size_min``, ``size_max``)
- Duplicate detection (``allow_duplicates``)
- Type-specific methods:

  - ``append(element)`` - add to end
  - ``remove_at(index)`` - remove by position
  - ``insert_at(index, element)`` - insert at position
  - ``reorder(new_order)`` - rearrange by index sequence

- Supports nesting (Array of Arrays, Array of any control type)

Required Test Coverage
-------------------------------------------------------------------------------

**000-099: ArrayHints dataclass**

- ``test_000_array_hints_default_creation`` - Create with all defaults
- ``test_010_array_hints_with_vertical`` - Set orientation (vertical)
- ``test_015_array_hints_with_horizontal`` - Set orientation (horizontal)
- ``test_020_array_hints_with_grid`` - Set orientation (grid)
- ``test_030_array_hints_with_collapsible`` - Set collapsible flag
- ``test_040_array_hints_with_initially_collapsed`` - Set initially_collapsed
- ``test_050_array_hints_with_border`` - Set border flag
- ``test_060_array_hints_with_title`` - Set title
- ``test_070_array_hints_with_label`` - Set label
- ``test_080_array_hints_with_help`` - Set help_text
- ``test_090_array_hints_all_fields`` - Set all fields together
- ``test_095_array_hints_immutability`` - Cannot modify after creation

**100-199: ArrayDefinition creation and configuration**

- ``test_100_array_definition_simple_elements`` - Create with simple element type (e.g., Boolean)
- ``test_110_array_definition_with_size_min`` - Set size_min constraint
- ``test_120_array_definition_with_size_max`` - Set size_max constraint
- ``test_130_array_definition_with_both_sizes`` - Set both size_min and size_max
- ``test_140_array_definition_fixed_size`` - size_min == size_max (fixed size)
- ``test_150_array_definition_with_default_elements`` - Set default_elements
- ``test_160_array_definition_allow_duplicates_false`` - Disallow duplicates
- ``test_170_array_definition_custom_hints`` - Set custom hints
- ``test_180_array_definition_all_parameters`` - Set all parameters
- ``test_190_array_definition_immutability`` - Cannot modify after creation
- ``test_191_array_definition_invalid_negative_size_min`` - Negative size_min raises DefinitionInvalidity
- ``test_192_array_definition_invalid_negative_size_max`` - Negative size_max raises DefinitionInvalidity
- ``test_193_array_definition_invalid_min_exceeds_max`` - size_min > size_max raises DefinitionInvalidity
- ``test_194_array_definition_invalid_default_below_min`` - len(default_elements) < size_min raises DefinitionInvalidity
- ``test_195_array_definition_invalid_default_above_max`` - len(default_elements) > size_max raises DefinitionInvalidity

**200-299: ArrayDefinition.validate_value()**

- ``test_200_validate_value_valid_array`` - Valid array of elements
- ``test_210_validate_value_empty_array`` - Empty array (valid if size_min=0)
- ``test_220_validate_value_single_element`` - Single element array
- ``test_230_validate_value_at_size_min`` - Exactly at size_min boundary
- ``test_240_validate_value_at_size_max`` - Exactly at size_max boundary
- ``test_250_validate_value_below_size_min`` - Below size_min raises SizeConstraintViolation
- ``test_260_validate_value_above_size_max`` - Above size_max raises SizeConstraintViolation
- ``test_270_validate_value_invalid_element_type`` - Wrong element type raises ControlInvalidity
- ``test_280_validate_value_element_constraint_violation`` - Element constraint violation raises
- ``test_290_validate_value_with_duplicates_allowed`` - Duplicates valid when allowed
- ``test_291_validate_value_with_duplicates_disallowed`` - Duplicates raise when disallowed
- ``test_292_validate_value_invalid_not_sequence`` - Non-sequence raises ControlInvalidity
- ``test_293_validate_value_tuple_sequence`` - Tuple input (valid, converted to tuple internally)
- ``test_294_validate_value_list_sequence`` - List input (valid, converted to tuple)

**300-399: ArrayDefinition.produce_control()**

- ``test_300_produce_control_no_initial`` - Use default_elements
- ``test_310_produce_control_initial_valid`` - Set valid initial array
- ``test_320_produce_control_initial_empty`` - Set empty initial array
- ``test_330_produce_control_invalid_initial`` - Invalid initial raises exception
- ``test_340_produce_control_absent`` - Explicit absent uses default
- ``test_350_produce_control_returns_array`` - Returns Array control type
- ``test_360_produce_control_immutability`` - Definition unchanged after production

**400-499: ArrayDefinition.serialize_value()**

- ``test_400_serialize_value_array`` - Array serializes as list
- ``test_410_serialize_value_empty`` - Empty array serializes as empty list
- ``test_420_serialize_value_nested`` - Nested array serializes recursively
- ``test_430_serialize_value_preserves_order`` - Order preserved in serialization

**500-599: ArrayDefinition.produce_default()**

- ``test_500_produce_default_empty`` - Default is empty tuple
- ``test_510_produce_default_with_elements`` - Default elements respected

**600-699: Array control creation and attributes**

- ``test_600_array_control_creation`` - Create with definition and current
- ``test_610_array_control_definition_attribute`` - Has definition attribute
- ``test_620_array_control_current_attribute`` - Has current attribute (tuple)
- ``test_630_array_control_immutability`` - Cannot modify attributes

**700-799: Array.copy()**

- ``test_700_copy_to_new_array`` - Copy with new array value
- ``test_710_copy_to_empty`` - Copy to empty array
- ``test_720_copy_returns_new_instance`` - Returns different instance
- ``test_730_copy_preserves_definition`` - Definition unchanged
- ``test_740_copy_invalid_value`` - Invalid value raises ControlInvalidity
- ``test_750_copy_original_unchanged`` - Original control unchanged

**800-899: Array.append()**

- ``test_800_append_valid_element`` - Successful append
- ``test_810_append_at_size_max`` - Append when at size_max raises SizeConstraintViolation
- ``test_820_append_invalid_element`` - Invalid element raises ControlInvalidity
- ``test_830_append_returns_new_instance`` - Returns different instance
- ``test_840_append_preserves_definition`` - Definition unchanged
- ``test_850_append_original_unchanged`` - Original array unchanged

**900-999: Array.remove_at()**

- ``test_900_remove_at_valid_index`` - Successful removal
- ``test_910_remove_at_first`` - Remove first element (index 0)
- ``test_920_remove_at_last`` - Remove last element
- ``test_930_remove_at_size_min`` - Remove when at size_min raises SizeConstraintViolation
- ``test_940_remove_at_invalid_negative_index`` - Negative index raises IndexError
- ``test_950_remove_at_invalid_beyond_length`` - Index >= length raises IndexError
- ``test_960_remove_at_returns_new_instance`` - Returns different instance
- ``test_970_remove_at_preserves_definition`` - Definition unchanged
- ``test_980_remove_at_original_unchanged`` - Original array unchanged

**1000-1099: Array.insert_at()**

- ``test_1000_insert_at_beginning`` - Insert at index 0
- ``test_1010_insert_at_middle`` - Insert at middle index
- ``test_1020_insert_at_end`` - Insert at end (equivalent to append)
- ``test_1030_insert_at_size_max`` - Insert when at size_max raises SizeConstraintViolation
- ``test_1040_insert_at_invalid_element`` - Invalid element raises ControlInvalidity
- ``test_1050_insert_at_invalid_index`` - Invalid index raises IndexError
- ``test_1060_insert_at_returns_new_instance`` - Returns different instance
- ``test_1070_insert_at_preserves_definition`` - Definition unchanged
- ``test_1080_insert_at_original_unchanged`` - Original array unchanged

**1100-1199: Array.reorder()**

- ``test_1100_reorder_valid_permutation`` - Valid reordering
- ``test_1110_reorder_reverse`` - Reverse order
- ``test_1120_reorder_partial_swap`` - Swap two elements
- ``test_1130_reorder_no_change`` - Same order (identity permutation)
- ``test_1140_reorder_invalid_wrong_count`` - Wrong number of indices raises
- ``test_1150_reorder_invalid_out_of_range`` - Index out of range raises
- ``test_1160_reorder_invalid_duplicates`` - Duplicate indices raises
- ``test_1170_reorder_returns_new_instance`` - Returns different instance
- ``test_1180_reorder_preserves_definition`` - Definition unchanged
- ``test_1190_reorder_original_unchanged`` - Original array unchanged

**1200-1299: Array.serialize()**

- ``test_1200_serialize_simple_elements`` - Serialize array of simple elements
- ``test_1210_serialize_nested_arrays`` - Serialize nested arrays
- ``test_1220_serialize_delegates_to_definition`` - Uses definition.serialize_value()

**1300-1399: Integration scenarios**

- ``test_1300_complete_lifecycle`` - Create → validate → update → serialize
- ``test_1310_multiple_controls_same_definition`` - Share definition across controls
- ``test_1320_controls_independent`` - Modifying one doesn't affect another
- ``test_1330_protocol_compliance`` - Implements Control and ControlDefinition protocols
- ``test_1340_nested_single_level`` - Array of Arrays (single nesting)
- ``test_1350_nested_multiple_levels`` - Array of Arrays of Arrays (deep nesting)
- ``test_1360_mixed_operations_chain`` - Chain append, remove, insert, reorder
- ``test_1370_size_constraint_interactions`` - Size constraints with all operations
- ``test_1380_duplicate_detection`` - Duplicate handling when allow_duplicates=False

Implementation Notes
===============================================================================

Testing Patterns Specific to Each Type
-------------------------------------------------------------------------------

**Text:**

- Focus on string validation and length constraints
- Empty string is valid edge case
- ``clear()`` method must be tested for immutability

**Interval:**

- Focus on numeric validation and range constraints
- Floating-point precision critical for grade alignment
- ``increment()``/``decrement()`` must check boundaries

**Options:**

- Focus on selection from finite set
- Choice dataclass adds complexity (value + label)
- Empty choices set is invalid definition

**Array:**

- Most complex - recursive structure
- Each operation must maintain immutability
- Size constraints interact with all operations
- Element validation must be tested thoroughly

Dependencies and Injection
-------------------------------------------------------------------------------

**No Monkey-Patching:**
  Immutable objects prevent monkey-patching. All testing uses real objects and
  dependency injection where needed.

**No External Services:**
  All tests run in-memory. No filesystem operations, no network calls.

**Test Isolation:**
  Each test is independent. No shared mutable state between tests.

Fixture Organization
-------------------------------------------------------------------------------

**Common Fixtures (in conftest.py or module scope):**

- Sample definitions for each control type
- Sample controls for each type
- Reusable validators
- Exception matchers

**Type-Specific Fixtures:**

- Text: various length constraint combinations
- Interval: continuous vs discrete definitions
- Options: few vs many choices, with/without labels
- Array: simple element types, nested arrays, various size constraints

Private Function Testing
-------------------------------------------------------------------------------

**No Private Functions in Scope:**
  All classes tested here have only public methods. Private functions should
  be tested through public API only.

**Constants:**
  Module-level constants like ``_FLOAT_EPSILON`` in interval.py are tested
  indirectly through grade validation tests.

Test Module Numbering Rationale
-------------------------------------------------------------------------------

**Chosen Numbering:**

- ``test_410_controls_text.py`` - Next after Boolean (400)
- ``test_420_controls_interval.py`` - After Text
- ``test_430_controls_options.py`` - After Interval
- ``test_440_controls_array.py`` - Last (most complex)

**Rationale:**

- Increments of 10 allow for insertion of related tests later
- Complexity increases: Text (simplest) → Array (most complex)
- Dependencies: Array may use other control types as elements

Linter Suppressions
-------------------------------------------------------------------------------

**Acceptable Suppressions:**

- ``# type: ignore[return-value]`` for Self return types (if needed)
- Test functions may use ``# noqa`` for long parameter lists if required

**Minimize Suppressions:**
  Tests should be fully typed without suppressions where possible.

Success Metrics
===============================================================================

Coverage Targets
-------------------------------------------------------------------------------

**Per Module:**

- ``text.py``: 100% line coverage (currently 39%)
- ``interval.py``: 100% line coverage (currently 28%)
- ``options.py``: 100% line coverage (currently 24%)
- ``array.py``: 100% line coverage (currently 24%)

**Branch Coverage:**

- All conditional paths in validators: 100%
- All error handling paths: 100%
- All ``__post_init__`` validations: 100%

Functional Completeness
-------------------------------------------------------------------------------

**All Tests Passing:**
  All planned tests must pass with no skips or xfails.

**Protocol Compliance Verified:**
  All control types must demonstrably satisfy Control and ControlDefinition
  protocols.

**Immutability Enforced:**
  All immutability tests must confirm objects cannot be mutated.

**Type-Specific Methods Verified:**
  All type-specific methods (toggle, clear, increment, decrement, array
  operations) must be fully tested.

Test Quality Standards
-------------------------------------------------------------------------------

**Descriptive Test Names:**
  Test function names must clearly indicate what is being tested.

**Single-Line Docstrings:**
  Every test function has a concise single-line docstring describing behavior.

**No Test Code Duplication:**
  Use fixtures and helper functions to avoid repeating test setup.

**Fast Execution:**
  All tests run in memory, target < 5 seconds for full control type test suite.

Implementation Priorities
-------------------------------------------------------------------------------

**Recommended Order:**

1. **Text** (~4 hours) - Simplest after Boolean, straightforward constraints
2. **Interval** (~4 hours) - Moderate complexity with grade validation
3. **Options** (~4 hours) - Moderate complexity with Choice dataclass
4. **Array** (~6 hours) - Most complex with recursion and multiple operations

**Total Estimated Effort:** 18 hours

**Rationale:**
  Build from simple to complex. Text and Interval are independent. Options
  is independent. Array is most complex and can leverage understanding from
  simpler types.

Potential Challenges and Mitigations
===============================================================================

Challenge 1: Floating-Point Precision (Interval)
-------------------------------------------------------------------------------

**Problem:**
  Grade alignment testing requires careful floating-point comparison.

**Mitigation:**
  - Use module constant ``_FLOAT_EPSILON = 1e-10``
  - Test values known to align exactly
  - Test values known to misalign
  - Document precision expectations in tests

Challenge 2: Choice Dataclass Complexity (Options)
-------------------------------------------------------------------------------

**Problem:**
  Choice has value + label, but validation uses value only.

**Mitigation:**
  - Test Choice creation separately from Options validation
  - Verify label is preserved but not used in validation
  - Test choice equality (should compare by value)
  - Document label as metadata

Challenge 3: Array Recursion (Array)
-------------------------------------------------------------------------------

**Problem:**
  Nested arrays can create complex test scenarios.

**Mitigation:**
  - Start with simple element types (Boolean)
  - Add single-level nesting tests
  - Add multi-level nesting tests progressively
  - Use fixtures for common nested structures
  - Test depth limits if any

Challenge 4: Size Constraints on Array Operations
-------------------------------------------------------------------------------

**Problem:**
  Every array operation must validate size constraints.

**Mitigation:**
  - Create fixtures with arrays at size boundaries
  - Test each operation at size_min and size_max
  - Test operations that would violate constraints
  - Verify exception types and messages

Challenge 5: Test Suite Performance
-------------------------------------------------------------------------------

**Problem:**
  Large test suites can slow down development feedback.

**Mitigation:**
  - Keep tests focused and fast (in-memory only)
  - Use pytest markers for subsets (e.g., ``@pytest.mark.text``)
  - Avoid redundant test setup
  - Use fixtures efficiently

Architectural Recommendations
===============================================================================

Testability Assessment
-------------------------------------------------------------------------------

**Current Architecture: Excellent Testability**

  - Clean separation of concerns (protocols, validators, controls)
  - Dependency injection friendly (validators are injectable)
  - Immutable by design (no hidden state mutations)
  - No external dependencies (all in-memory)
  - Protocol-based design enables testing through concrete types
  - Each control type is self-contained

**No Architectural Changes Needed:**
  The current design is highly testable. No refactoring required to achieve
  100% coverage for any control type.

Future Enhancements for Testing
-------------------------------------------------------------------------------

**Property-Based Testing (Optional):**
  Consider adding Hypothesis tests for validators:

  - Any string within length constraints should pass Text validation
  - Any number in range should pass Interval validation
  - Any value in choices should pass Options validation
  - Any array within size constraints should pass Array validation

  **Benefit:** Catches edge cases not covered by example-based tests.

**Performance Benchmarking (Optional):**
  While correctness is prioritized, simple benchmarks could be useful:

  - Control creation performance (target: < 1ms per creation)
  - Array operation performance (especially for large arrays)

  **Note:** Only add if performance issues arise in practice.

Areas Requiring ``# pragma: no cover``
-------------------------------------------------------------------------------

**None Expected:**
  All code in scope should be 100% coverable through tests. No defensive code,
  no platform-specific branches, no impossible-to-trigger paths identified.

**Abstract Methods in Protocols:**
  The ``...`` bodies of abstract methods in protocols (interfaces.py) are
  typically uncovered, but this is acceptable as they are not meant to be
  executed.

  **Current:** 76% coverage in interfaces.py is acceptable. The 6 missing
  statements are abstract method bodies.

Test Implementation Timeline
===============================================================================

Sequential Implementation Order
-------------------------------------------------------------------------------

**Session 1: Text Control**

  1. Implement test_410_controls_text.py (~4 hours)
  2. Verify 100% coverage for text.py
  3. Ensure all tests pass
  4. Commit

**Session 2: Interval Control**

  1. Implement test_420_controls_interval.py (~4 hours)
  2. Verify 100% coverage for interval.py
  3. Ensure all tests pass
  4. Commit

**Session 3: Options Control**

  1. Implement test_430_controls_options.py (~4 hours)
  2. Verify 100% coverage for options.py
  3. Ensure all tests pass
  4. Commit

**Session 4: Array Control**

  1. Implement test_440_controls_array.py (~6 hours)
  2. Verify 100% coverage for array.py
  3. Ensure all tests pass
  4. Commit

**Session 5: Final Review**

  1. Review coverage reports for all modules
  2. Fill any remaining gaps
  3. Update documentation
  4. Final commit

Final Validation
===============================================================================

Checklist Before Completion
-------------------------------------------------------------------------------

- [ ] test_410_controls_text.py created and passing
- [ ] test_420_controls_interval.py created and passing
- [ ] test_430_controls_options.py created and passing
- [ ] test_440_controls_array.py created and passing
- [ ] Coverage report shows 100% for all control type modules
- [ ] No ``# pragma: no cover`` used (except protocol abstract methods)
- [ ] All tests have single-line docstrings
- [ ] Test function numbering follows plan
- [ ] No monkey-patching used anywhere
- [ ] No external services or network calls
- [ ] All linters pass
- [ ] All tests complete in < 10 seconds total
- [ ] This test plan updated with any lessons learned

Post-Implementation Review
-------------------------------------------------------------------------------

**Coverage Verification:**

  Run coverage report and verify 100% line coverage for::

    sources/vibecontrols/controls/text.py
    sources/vibecontrols/controls/interval.py
    sources/vibecontrols/controls/options.py
    sources/vibecontrols/controls/array.py

**Manual Testing:**

  Import and exercise key paths manually in Python REPL for each type.

**Integration Verification:**

  Verify all control types work end-to-end without serialization:

  - Definition → Control → Updates → Values

Next Test Plans
===============================================================================

**Serialization and Deserialization:**
  Separate test plan for TOML/JSON serialization:

  - Descriptor parsing (TOML → Definition)
  - Control serialization (Control → JSON)
  - Roundtrip testing (TOML → Definition → Control → JSON → Control)
  - Type registry (BUILTIN_TYPES, descriptor_to_definition)
  - Nested structures (Array with nested definitions)

**Cross-Control Integration:**
  Once multiple control types exist and serialization works:

  - Control collections (managing multiple controls together)
  - Control dependencies (if implemented)
  - Control state synchronization (if implemented)

Conclusion
===============================================================================

This test plan provides a systematic approach to achieving 100% test coverage
for all control type definitions and in-memory control production. The plan
follows project testing principles:

- **Dependency injection over monkey-patching**
- **Systematic coverage of all code paths**
- **Clean test organization with numbered modules**
- **Immutability verification at every step**
- **Standardized test structure across all control types**

All control types must follow the same structural pattern with type-specific
variations for unique features, constraints, and operations.

**Ready for implementation.**
