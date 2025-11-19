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
and value management **without serialization or deserialization**. The plan
covers the core abstractions (protocols, validators, exceptions) and concrete
implementations (Boolean control type).

**Scope:** In-memory control operations only. Serialization/deserialization
testing is deferred to a separate test plan.

Coverage Analysis Summary
===============================================================================

Current Coverage State (as of 2025-11-19)
-------------------------------------------------------------------------------

Based on the coverage report provided in the planning prompt::

    Name                                  Stmts   Miss Branch BrPart  Cover   Missing
    ---------------------------------------------------------------------------------
    sources/vibecontrols/__/__init__.py       2      0      0      0   100%
    sources/vibecontrols/__/imports.py        8      4      0      0    50%   28, 33-38
    sources/vibecontrols/__/nomina.py         5      0      0      0   100%
    sources/vibecontrols/__init__.py          3      0      0      0   100%
    sources/vibecontrols/exceptions.py        7      4      0      0    43%   35-55
    ---------------------------------------------------------------------------------
    TOTAL                                    25      8      0      0    68%

**Critical Gap:** The following modules have **zero test coverage** as they
are not yet included in the coverage report:

- ``sources/vibecontrols/interfaces.py`` (139 lines) - Core protocols
- ``sources/vibecontrols/validation.py`` (298 lines) - Validation framework
- ``sources/vibecontrols/controls/boolean.py`` (166 lines) - Boolean control type
- ``sources/vibecontrols/controls/__init__.py`` (25 lines) - Controls exports

**Total Untested Lines:** Approximately 628 lines across 4 modules.

Specific Coverage Gaps by Module
-------------------------------------------------------------------------------

**sources/vibecontrols/exceptions.py** (lines 35-55)
  Uncovered exception class definitions:

  - Line 35-36: ``ControlError`` class definition
  - Lines 39-44: ``ControlInvalidity`` class definition
  - Lines 47-52: ``ConstraintViolation`` class definition
  - Lines 55-60: ``DefinitionInvalidity`` class definition

  **Note:** These are exception classes. Testing requires instantiation and
  raising to achieve coverage.

**sources/vibecontrols/__/imports.py** (lines 28, 33-38)
  Uncovered import statements (likely untouched imports):

  - Line 28: ``import collections.abc as cabc``
  - Lines 33-38: Conditional imports or unused imports

  **Note:** Import testing is typically handled by ``test_010_base.py`` but
  may need expansion.

**sources/vibecontrols/interfaces.py** (entire module - 0% coverage)
  Protocol definitions requiring testing:

  - Lines 28-97: ``ControlDefinition`` protocol with 4 abstract methods
  - Lines 99-139: ``Control`` protocol with 2 abstract methods

  **Challenge:** Protocols with ``@abstractmethod`` cannot be instantiated
  directly. Testing requires concrete implementations.

**sources/vibecontrols/validation.py** (entire module - 0% coverage)
  Five validator classes requiring comprehensive testing:

  - Lines 28-51: ``Validator`` protocol (abstract)
  - Lines 53-84: ``CompositeValidator`` - chains validators
  - Lines 87-133: ``ClassValidator`` - type validation
  - Lines 135-178: ``IntervalValidator`` - numeric range validation
  - Lines 181-241: ``SizeValidator`` - length validation
  - Lines 244-297: ``SelectionValidator`` - choice validation

  **Coverage Target:** Each validator needs tests for:

  - Valid inputs (happy path)
  - Invalid inputs (error paths)
  - Edge cases (boundary conditions)
  - Custom message handling
  - ``__post_init__`` message generation

**sources/vibecontrols/controls/boolean.py** (entire module - 0% coverage)
  Complete Boolean control implementation:

  - Lines 27-42: ``BooleanHints`` dataclass
  - Lines 44-115: ``BooleanDefinition`` class with 4 methods
  - Lines 117-166: ``Boolean`` control class with 3 methods

  **Coverage Target:** Tests must verify:

  - Definition creation with various parameters
  - Validation (valid/invalid values)
  - Control production (with/without initial values)
  - Immutable updates via ``copy()``
  - Boolean-specific ``toggle()`` method
  - Serialization (in separate test plan)

Target Coverage Goals
-------------------------------------------------------------------------------

**Line Coverage:** 100% for all modules in scope

**Branch Coverage:** 100% where applicable (especially validators and error
handling paths)

**Specific Targets:**

- All exception classes: instantiated and raised in tests
- All validators: tested with valid, invalid, and edge case inputs
- All protocol methods: exercised through concrete implementations
- Boolean control: complete lifecycle testing (create → validate → update →
  toggle)

Test Strategy
===============================================================================

Testing Approach
-------------------------------------------------------------------------------

**Dependency Injection Pattern:**
  All testing uses dependency injection rather than monkey-patching. Immutable
  objects prevent monkey-patching by design.

**Layered Testing:**

  1. **Unit Tests (test modules 100-499):** Test individual components in
     isolation
  2. **Integration Tests (test modules 500+):** Test component interactions
  3. **Protocol Compliance:** Verify concrete implementations satisfy protocols

**No External Dependencies:**
  Tests use only standard library and project dependencies. No network calls,
  no real external services.

Test Module Organization
-------------------------------------------------------------------------------

The project uses a numbered test module scheme where lower numbers indicate
lower-level functionality. Proposed numbering for new test modules:

**Existing Test Modules:**

- ``test_000_package.py`` - Package sanity checks (already exists)
- ``test_010_base.py`` - Common imports verification (already exists)

**Planned Test Modules:**

- ``test_100_exceptions.py`` - Exception hierarchy testing
- ``test_200_interfaces.py`` - Protocol definitions and compliance
- ``test_300_validation.py`` - Validator framework
- ``test_400_controls_boolean.py`` - Boolean control type

**Rationale:**

- **100-level:** Foundational exceptions (lowest dependency)
- **200-level:** Core abstractions (protocols depend on exceptions)
- **300-level:** Validation framework (depends on exceptions and protocols)
- **400-level:** Concrete control types (depends on all above)

Basic Functionality Tests (000-099)
-------------------------------------------------------------------------------

The existing ``test_000_package.py`` and ``test_010_base.py`` provide basic
sanity checks. No additional tests needed in the 000-099 range for this plan.

Component-Specific Tests (100+)
===============================================================================

Exception Hierarchy Testing (test_100_exceptions.py)
-------------------------------------------------------------------------------

**Module:** ``sources/vibecontrols/exceptions.py``

**Test Function Numbering:**

- **000-099:** Basic exception functionality

  - ``test_000_exception_hierarchy`` - Verify inheritance chain
  - ``test_010_exception_instantiation`` - Create all exception types

- **100-199:** Omniexception base class

  - ``test_100_omniexception_creation`` - Instantiate with message
  - ``test_110_omniexception_inheritance`` - Verify base class relationship

- **200-299:** Omnierror class

  - ``test_200_omnierror_creation`` - Instantiate with message
  - ``test_210_omnierror_inheritance`` - Verify inheritance from Omniexception
    and Exception

- **300-399:** ControlError class

  - ``test_300_control_error_creation`` - Instantiate with message
  - ``test_310_control_error_catch`` - Verify catchable as ControlError
  - ``test_320_control_error_inheritance`` - Verify inheritance chain

- **400-499:** ControlInvalidity class

  - ``test_400_control_invalidity_creation`` - Instantiate with message
  - ``test_410_control_invalidity_value_error`` - Verify ValueError subclass
  - ``test_420_control_invalidity_catch`` - Catch as ControlInvalidity
  - ``test_430_control_invalidity_context`` - Verify exception chaining

- **500-599:** ConstraintViolation class

  - ``test_500_constraint_violation_creation`` - Instantiate with message
  - ``test_510_constraint_violation_inheritance`` - Verify ControlInvalidity
    subclass
  - ``test_520_constraint_violation_specificity`` - Distinguish from parent
    ControlInvalidity

- **600-699:** DefinitionInvalidity class

  - ``test_600_definition_invalidity_creation`` - Instantiate with message
  - ``test_610_definition_invalidity_value_error`` - Verify ValueError subclass
  - ``test_620_definition_invalidity_catch`` - Catch as DefinitionInvalidity

**Test Data:**
  - Various error messages to verify message propagation
  - Exception chaining to verify ``from`` clause support

**Special Considerations:**

  - Test that all exceptions can be caught generically as ``Omniexception``
  - Verify proper exception chaining with ``from`` clause
  - Confirm ValueError inheritance for validation exceptions

Protocol Testing (test_200_interfaces.py)
-------------------------------------------------------------------------------

**Module:** ``sources/vibecontrols/interfaces.py``

**Challenge:** Protocols with ``@abstractmethod`` cannot be instantiated
directly. Testing requires concrete implementations (Boolean control type).

**Test Function Numbering:**

- **000-099:** Basic protocol characteristics

  - ``test_000_protocol_imports`` - Protocols are importable
  - ``test_010_protocol_abstractmethods`` - Verify abstractmethod decorators

- **100-199:** ControlDefinition protocol

  - ``test_100_control_definition_protocol_structure`` - Verify required
    methods exist
  - ``test_110_control_definition_not_instantiable`` - Cannot instantiate
    protocol directly
  - ``test_120_control_definition_implementation_compliance`` - Boolean
    definition satisfies protocol
  - ``test_130_control_definition_validate_value_signature`` - Signature matches
  - ``test_140_control_definition_produce_control_signature`` - Signature
    matches
  - ``test_150_control_definition_serialize_value_signature`` - Signature
    matches
  - ``test_160_control_definition_produce_default_signature`` - Signature
    matches

- **200-299:** Control protocol

  - ``test_200_control_protocol_structure`` - Verify required attributes and
    methods
  - ``test_210_control_not_instantiable`` - Cannot instantiate protocol directly
  - ``test_220_control_implementation_compliance`` - Boolean control satisfies
    protocol
  - ``test_230_control_definition_attribute`` - Has definition attribute
  - ``test_240_control_current_attribute`` - Has current attribute
  - ``test_250_control_copy_signature`` - Signature matches
  - ``test_260_control_serialize_signature`` - Signature matches

- **300-399:** Protocol typing and inheritance

  - ``test_300_protocol_isinstance_check`` - Concrete types pass isinstance
  - ``test_310_protocol_structural_typing`` - Duck typing compatibility
  - ``test_320_protocol_nominal_typing`` - ABC registration compatibility

**Testing Approach:**

  - Use Boolean control as the concrete implementation
  - Verify protocol compliance through ``isinstance()`` checks
  - Inspect method signatures to confirm protocol conformance
  - Test that protocols cannot be instantiated directly

**Dependencies:**

  - Requires Boolean control implementation (test_400_controls_boolean.py)
  - Tests may use Boolean as fixture but focus on protocol compliance

Validation Framework Testing (test_300_validation.py)
-------------------------------------------------------------------------------

**Module:** ``sources/vibecontrols/validation.py``

**Test Function Numbering:**

- **000-099:** Validator protocol basics

  - ``test_000_validator_protocol_importable`` - Protocol exists
  - ``test_010_validator_callable`` - Validators are callable

- **100-199:** CompositeValidator

  - ``test_100_composite_validator_creation`` - Create with multiple validators
  - ``test_110_composite_validator_empty`` - Create with no validators
  - ``test_120_composite_validator_single`` - Create with single validator
  - ``test_130_composite_validator_chaining`` - Validators execute in sequence
  - ``test_140_composite_validator_short_circuit`` - Stops on first failure
  - ``test_150_composite_validator_value_transformation`` - Each validator can
    transform value
  - ``test_160_composite_validator_exception_propagation`` - Exception from any
    validator propagates

- **200-299:** ClassValidator

  - ``test_200_class_validator_creation`` - Create with type
  - ``test_210_class_validator_valid_type`` - Accepts correct type
  - ``test_220_class_validator_invalid_type`` - Rejects wrong type
  - ``test_230_class_validator_multiple_types`` - Tuple of types support
  - ``test_240_class_validator_default_message`` - Auto-generated message for
    single type
  - ``test_250_class_validator_default_message_multiple`` - Auto-generated
    message for multiple types
  - ``test_260_class_validator_custom_message`` - Custom message used
  - ``test_270_class_validator_subclass`` - Subclass passes isinstance
  - ``test_280_class_validator_exact_type_bool`` - Strict bool (not int)

- **300-399:** IntervalValidator

  - ``test_300_interval_validator_creation`` - Create with min/max
  - ``test_310_interval_validator_in_range`` - Value within range passes
  - ``test_320_interval_validator_below_minimum`` - Value too low fails
  - ``test_330_interval_validator_above_maximum`` - Value too high fails
  - ``test_340_interval_validator_at_minimum`` - Boundary: minimum value passes
  - ``test_350_interval_validator_at_maximum`` - Boundary: maximum value passes
  - ``test_360_interval_validator_default_message`` - Auto-generated message
  - ``test_370_interval_validator_custom_message`` - Custom message used
  - ``test_380_interval_validator_float_precision`` - Handles floating point
    correctly

- **400-499:** SizeValidator

  - ``test_400_size_validator_creation`` - Create with min/max length
  - ``test_410_size_validator_min_only`` - Only minimum constraint
  - ``test_420_size_validator_max_only`` - Only maximum constraint
  - ``test_430_size_validator_both_constraints`` - Both min and max
  - ``test_440_size_validator_no_constraints`` - Neither (always passes?)
  - ``test_450_size_validator_valid_length`` - Length in range passes
  - ``test_460_size_validator_too_short`` - Below minimum fails
  - ``test_470_size_validator_too_long`` - Above maximum fails
  - ``test_480_size_validator_at_minimum`` - Boundary: minimum length passes
  - ``test_490_size_validator_at_maximum`` - Boundary: maximum length passes
  - ``test_495_size_validator_default_messages`` - Auto-generated messages for
    all cases
  - ``test_496_size_validator_custom_message`` - Custom message used
  - ``test_497_size_validator_various_types`` - Works with list, tuple, str,
    dict, etc.

- **500-599:** SelectionValidator

  - ``test_500_selection_validator_creation`` - Create with choices
  - ``test_510_selection_validator_valid_choice`` - Choice in set passes
  - ``test_520_selection_validator_invalid_choice`` - Choice not in set fails
  - ``test_530_selection_validator_frozenset_normalization`` - Choices converted
    to frozenset
  - ``test_540_selection_validator_few_choices_message`` - Shows all choices (≤5)
  - ``test_550_selection_validator_many_choices_message`` - Shows count only (>5)
  - ``test_560_selection_validator_custom_message`` - Custom message used
  - ``test_570_selection_validator_empty_choices`` - Edge: empty choice set
  - ``test_580_selection_validator_single_choice`` - Edge: single valid choice
  - ``test_590_selection_validator_hashable_choices`` - Choices must be hashable

**Test Data Strategies:**

  - **ClassValidator:** Test with bool, int, float, str, list, dict, custom
    classes
  - **IntervalValidator:** Test with integers, floats, edge boundaries (0.0,
    1.0, etc.)
  - **SizeValidator:** Test with various container types (list, tuple, str,
    dict)
  - **SelectionValidator:** Test with strings, numbers, and other hashable types
  - **CompositeValidator:** Chain different validator types to verify composition

**Special Considerations:**

  - Validators should be immutable (frozen dataclasses)
  - ``__post_init__`` message generation must be tested
  - Exception types must be correct (ControlInvalidity, ConstraintViolation)
  - Validators are reusable - same instance can validate multiple values

Boolean Control Testing (test_400_controls_boolean.py)
-------------------------------------------------------------------------------

**Module:** ``sources/vibecontrols/controls/boolean.py``

**Test Function Numbering:**

- **000-099:** BooleanHints dataclass

  - ``test_000_boolean_hints_default_creation`` - Create with defaults
  - ``test_010_boolean_hints_with_widget`` - Set widget_preference
  - ``test_020_boolean_hints_with_label`` - Set label
  - ``test_030_boolean_hints_with_help`` - Set help_text
  - ``test_040_boolean_hints_all_fields`` - Set all fields
  - ``test_050_boolean_hints_immutability`` - Cannot modify after creation

- **100-199:** BooleanDefinition creation and configuration

  - ``test_100_boolean_definition_default_creation`` - Create with all defaults
  - ``test_110_boolean_definition_custom_default`` - Set default=True
  - ``test_120_boolean_definition_custom_message`` - Set validation_message
  - ``test_130_boolean_definition_custom_hints`` - Set custom hints
  - ``test_140_boolean_definition_all_parameters`` - Set all parameters
  - ``test_150_boolean_definition_immutability`` - Cannot modify after creation

- **200-299:** BooleanDefinition.validate_value()

  - ``test_200_validate_value_true`` - Validate True
  - ``test_210_validate_value_false`` - Validate False
  - ``test_220_validate_value_invalid_integer`` - Reject integer (even 0/1)
  - ``test_230_validate_value_invalid_string`` - Reject string "true"/"false"
  - ``test_240_validate_value_invalid_none`` - Reject None
  - ``test_250_validate_value_custom_message`` - Custom message in exception
  - ``test_260_validate_value_exception_type`` - Raises ControlInvalidity

- **300-399:** BooleanDefinition.produce_control()

  - ``test_300_produce_control_no_initial`` - Use default value
  - ``test_310_produce_control_initial_true`` - Set initial to True
  - ``test_320_produce_control_initial_false`` - Set initial to False
  - ``test_330_produce_control_invalid_initial`` - Invalid value raises exception
  - ``test_340_produce_control_absent`` - Explicit absent uses default
  - ``test_350_produce_control_returns_boolean`` - Returns Boolean control type
  - ``test_360_produce_control_immutability`` - Definition unchanged after
    producing control

- **400-499:** BooleanDefinition.serialize_value()

  - ``test_400_serialize_value_true`` - True serializes as True
  - ``test_410_serialize_value_false`` - False serializes as False

- **500-599:** BooleanDefinition.produce_default()

  - ``test_500_produce_default_false`` - Default is False
  - ``test_510_produce_default_custom`` - Custom default respected

- **600-699:** Boolean control creation and attributes

  - ``test_600_boolean_control_creation`` - Create with definition and current
  - ``test_610_boolean_control_definition_attribute`` - Has definition attribute
  - ``test_620_boolean_control_current_attribute`` - Has current attribute
  - ``test_630_boolean_control_immutability`` - Cannot modify attributes

- **700-799:** Boolean.copy()

  - ``test_700_copy_to_true`` - Copy with new value True
  - ``test_710_copy_to_false`` - Copy with new value False
  - ``test_720_copy_returns_new_instance`` - Returns different instance
  - ``test_730_copy_preserves_definition`` - Definition unchanged
  - ``test_740_copy_invalid_value`` - Invalid value raises ControlInvalidity
  - ``test_750_copy_original_unchanged`` - Original control unchanged (immutability)

- **800-899:** Boolean.toggle()

  - ``test_800_toggle_true_to_false`` - True → False
  - ``test_810_toggle_false_to_true`` - False → True
  - ``test_820_toggle_returns_new_instance`` - Returns different instance
  - ``test_830_toggle_preserves_definition`` - Definition unchanged
  - ``test_840_toggle_original_unchanged`` - Original control unchanged
  - ``test_850_toggle_multiple_times`` - Chain multiple toggles

- **900-999:** Boolean.serialize()

  - ``test_900_serialize_true`` - Serialize True
  - ``test_910_serialize_false`` - Serialize False
  - ``test_920_serialize_delegates_to_definition`` - Uses
    definition.serialize_value()

- **1000-1099:** Integration scenarios

  - ``test_1000_complete_lifecycle`` - Create → validate → update → serialize
  - ``test_1010_multiple_controls_same_definition`` - Share definition across
    controls
  - ``test_1020_controls_independent`` - Modifying one doesn't affect another
  - ``test_1030_protocol_compliance`` - Implements Control and ControlDefinition
    protocols

**Test Data:**

  - Valid boolean values: True, False
  - Invalid values: 0, 1, "true", "false", None, [], {}, etc.
  - Various custom messages and hints

**Special Considerations:**

  - Test strict boolean type checking (not truthy/falsy)
  - Verify immutability at every operation
  - Test protocol compliance (isinstance checks)
  - Ensure definition can be shared across multiple controls safely

Implementation Notes
===============================================================================

Testing Patterns
-------------------------------------------------------------------------------

**Immutability Verification:**

  All tests that create or update objects must verify immutability by:

  1. Creating original object
  2. Performing operation (should return new instance)
  3. Asserting original is unchanged
  4. Asserting new instance has expected value

**Exception Testing:**

  Use ``pytest.raises`` with message inspection::

    with pytest.raises( ControlInvalidity ) as exc_info:
        validator( invalid_value )
    assert "expected message" in str( exc_info.value )

**Protocol Compliance Testing:**

  Use ``isinstance`` checks and signature inspection::

    from vibecontrols.interfaces import ControlDefinition
    from vibecontrols.controls import BooleanDefinition

    def test_protocol_compliance():
        definition = BooleanDefinition( )
        assert isinstance( definition, ControlDefinition )

**Fixture Usage:**

  Create reusable fixtures for common test objects::

    @pytest.fixture
    def boolean_definition():
        ''' Standard boolean definition for testing. '''
        return BooleanDefinition( )

    @pytest.fixture
    def boolean_control( boolean_definition ):
        ''' Standard boolean control for testing. '''
        return boolean_definition.produce_control( True )

Dependencies and Injection
-------------------------------------------------------------------------------

**No Monkey-Patching:**
  Immutable objects prevent monkey-patching. All testing uses real objects and
  dependency injection where needed.

**No External Services:**
  All tests run in-memory. No filesystem operations, no network calls.

**Test Isolation:**
  Each test is independent. No shared mutable state between tests.

Test Data Organization
-------------------------------------------------------------------------------

**No External Test Data:**
  All test data is inline in test functions or simple fixtures. No external
  files needed for this test plan (in-memory focus).

**Future Consideration:**
  When serialization testing is added, may need test data files under
  ``tests/data/`` for TOML descriptors and JSON fixtures.

Private Function Testing
-------------------------------------------------------------------------------

**No Private Functions in Scope:**
  All classes tested here have only public methods. Private functions should
  be tested through public API only.

**Protocol Methods:**
  Abstract methods in protocols are tested through concrete implementations
  (Boolean control type).

Test Module Numbering Rationale
-------------------------------------------------------------------------------

**Proposed Numbering:**

- ``test_100_exceptions.py`` - Lowest level, no dependencies
- ``test_200_interfaces.py`` - Depends on exceptions, tested via Boolean
- ``test_300_validation.py`` - Depends on exceptions
- ``test_400_controls_boolean.py`` - Depends on all above

**Alternatives Considered:**

- Using ``test_1X0_`` for subpackage modules (e.g., ``test_410_controls_boolean.py``)

  **Decision:** Keep simple numbering for now. Use ``4X0`` range if more
  control types added (e.g., ``test_410_controls_boolean.py``,
  ``test_420_controls_text.py``, etc.).

Linter Suppressions
-------------------------------------------------------------------------------

**Acceptable Suppressions:**

- ``# type: ignore[return-value]`` in ``boolean.py:145`` - Already present in
  source, acceptable for Self return type
- Test functions may use ``# noqa: PLR0913`` if many parameters needed

**No ``type: ignore`` in Tests:**
  Tests should be fully typed without suppressions where possible.

Success Metrics
===============================================================================

Coverage Targets
-------------------------------------------------------------------------------

**Line Coverage:**
  - ``exceptions.py``: 100% (currently 43%)
  - ``interfaces.py``: 100% (currently 0%)
  - ``validation.py``: 100% (currently 0%)
  - ``controls/boolean.py``: 100% (currently 0%)

**Branch Coverage:**
  - All conditional paths in validators: 100%
  - All error handling paths: 100%

Functional Completeness
-------------------------------------------------------------------------------

**All Tests Passing:**
  All planned tests must pass with no skips or xfails.

**Protocol Compliance Verified:**
  Boolean control type must demonstrably satisfy both Control and
  ControlDefinition protocols.

**Immutability Enforced:**
  All immutability tests must confirm objects cannot be mutated.

**Exception Hierarchy Validated:**
  All exceptions must be catchable at appropriate levels of the hierarchy.

Test Quality Standards
-------------------------------------------------------------------------------

**Descriptive Test Names:**
  Test function names must clearly indicate what is being tested.

**Single-Line Docstrings:**
  Every test function has a concise single-line docstring describing behavior.

**No Test Code Duplication:**
  Use fixtures and helper functions to avoid repeating test setup.

**Fast Execution:**
  All tests run in memory, target < 2 seconds for full test suite.

Implementation Priorities
-------------------------------------------------------------------------------

**Phase 1 (Immediate):**

  1. ``test_100_exceptions.py`` - Foundation for error handling
  2. ``test_300_validation.py`` - Needed by Boolean control

**Phase 2 (Next):**

  3. ``test_400_controls_boolean.py`` - Complete Boolean implementation coverage
  4. ``test_200_interfaces.py`` - Protocol compliance verification

**Rationale:**
  Exceptions and validators are needed first. Boolean control can be tested
  before protocol compliance tests since the latter uses Boolean as an example.

Potential Challenges and Mitigations
===============================================================================

Challenge 1: Testing Abstract Protocols
-------------------------------------------------------------------------------

**Problem:**
  Protocols with ``@abstractmethod`` cannot be instantiated directly for testing.

**Mitigation:**
  - Test protocol structure through inspection (``hasattr``, ``getattr``)
  - Test protocol compliance through concrete implementation (Boolean)
  - Verify ``isinstance`` checks work correctly
  - Document that protocols are tested via Boolean in test docstrings

Challenge 2: Immutability Verification
-------------------------------------------------------------------------------

**Problem:**
  Verifying immutability requires careful test design to detect mutations.

**Mitigation:**
  - Store original values before operations
  - Assert original unchanged after operations
  - Use ``id()`` to verify new instances created
  - Test that direct attribute assignment raises AttributeError (if applicable)

Challenge 3: Strict Boolean Type Checking
-------------------------------------------------------------------------------

**Problem:**
  Python's bool is a subclass of int, making type checking tricky.

**Mitigation:**
  - Test that integers (0, 1) are rejected
  - Test that only ``True`` and ``False`` pass
  - Use ``type(value) is bool`` rather than ``isinstance`` in implementation
  - Document this strictness in tests

Challenge 4: Validator Message Generation
-------------------------------------------------------------------------------

**Problem:**
  Validators auto-generate messages in ``__post_init__``. Testing requires
  verifying both auto-generated and custom messages.

**Mitigation:**
  - Test default message generation separately from custom messages
  - Inspect ``message`` attribute after creation
  - Verify messages appear in raised exceptions
  - Test edge cases (single type vs multiple types, few vs many choices)

Challenge 5: Coverage of ``__post_init__``
-------------------------------------------------------------------------------

**Problem:**
  DataclassObject ``__post_init__`` methods may not show in coverage without
  explicit testing.

**Mitigation:**
  - Create instances with various parameter combinations
  - Verify computed attributes (messages) are correct
  - Test both default and custom message paths

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

**No Architectural Changes Needed:**
  The current design is already highly testable. No refactoring required to
  achieve 100% coverage.

Future Enhancements for Testing
-------------------------------------------------------------------------------

**Test README Documentation:**
  Create ``tests/README.md`` documenting:

  - Test module numbering scheme (100=exceptions, 200=protocols, etc.)
  - Testing patterns specific to this project
  - Fixture usage conventions
  - No rationale for ``patch`` needed (none used)

**Hypothesis Property-Based Testing:**
  Consider adding property-based tests for validators:

  - ``ClassValidator``: any value of correct type should pass
  - ``IntervalValidator``: any value in range should pass
  - ``SelectionValidator``: any choice in set should pass

  **Benefit:** Catches edge cases not covered by example-based tests.

**Performance Benchmarking:**
  While correctness is prioritized, consider simple benchmarks:

  - Validator performance (target: < 1ms per validation)
  - Control creation performance (target: < 1ms per creation)

  **Note:** Only add if performance issues arise in practice.

Areas Requiring ``# pragma: no cover``
-------------------------------------------------------------------------------

**None Expected:**
  All code in scope should be 100% coverable through tests. No defensive code,
  no platform-specific branches, no impossible-to-trigger paths identified.

**Abstract Methods in Protocols:**
  The ``...`` bodies of abstract methods in protocols are typically uncovered,
  but this is acceptable as they are not meant to be executed. Coverage tools
  may or may not flag these.

  **If flagged:** May use ``# pragma: no cover`` on ``...`` in protocols only.

Test Implementation Timeline
===============================================================================

Estimated Effort
-------------------------------------------------------------------------------

**Per Module:**

  - ``test_100_exceptions.py``: ~2 hours (simple, ~25 tests)
  - ``test_300_validation.py``: ~6 hours (complex, ~60 tests)
  - ``test_400_controls_boolean.py``: ~4 hours (comprehensive, ~40 tests)
  - ``test_200_interfaces.py``: ~2 hours (depends on Boolean, ~20 tests)

**Total:** Approximately 14 hours for complete implementation

**Assumptions:**

  - Experienced with pytest and project testing patterns
  - No unexpected issues with frigid DataclassObject behavior
  - Existing source code is correct and doesn't require fixes

Sequential Implementation Order
-------------------------------------------------------------------------------

**Session 1:**

  1. ``test_100_exceptions.py`` - Quick foundation
  2. Start ``test_300_validation.py`` - CompositeValidator and ClassValidator

**Session 2:**

  3. Complete ``test_300_validation.py`` - Remaining validators
  4. Start ``test_400_controls_boolean.py`` - BooleanHints, BooleanDefinition

**Session 3:**

  5. Complete ``test_400_controls_boolean.py`` - Boolean control and integration
  6. ``test_200_interfaces.py`` - Protocol compliance using Boolean

**Session 4:**

  7. Review coverage reports
  8. Fill any gaps
  9. Update ``tests/README.md`` (create if needed)

Final Validation
===============================================================================

Checklist Before Completion
-------------------------------------------------------------------------------

- [ ] All planned test modules created and passing
- [ ] ``hatch --env develop run coverage report`` shows 100% for target modules
- [ ] No ``# pragma: no cover`` used (except possibly protocol ``...`` bodies)
- [ ] All tests have single-line docstrings
- [ ] Test function numbering follows plan
- [ ] No monkey-patching used anywhere
- [ ] No external services or network calls
- [ ] ``hatch --env develop run linters`` passes
- [ ] ``hatch --env develop run testers`` completes under 2 seconds
- [ ] ``tests/README.md`` updated with new test module numbering

Post-Implementation Review
-------------------------------------------------------------------------------

**Coverage Verification:**

  Run coverage report and verify 100% line coverage for::

    sources/vibecontrols/exceptions.py
    sources/vibecontrols/interfaces.py
    sources/vibecontrols/validation.py
    sources/vibecontrols/controls/boolean.py

**Manual Testing:**

  Import and exercise key paths manually in Python REPL:

  - Create Boolean definition
  - Produce control
  - Update control
  - Toggle control
  - Test validation failures

**Integration Verification:**

  Verify Boolean control works end-to-end without serialization:

  - Definition → Control → Updates → Values

Next Test Plans
===============================================================================

**Serialization and Deserialization:**
  Separate test plan for JSON/TOML serialization:

  - ``test_500_serialization_json.py``
  - ``test_600_serialization_toml.py`` (descriptor parsing)

**Additional Control Types:**
  As more control types are implemented:

  - ``test_410_controls_text.py``
  - ``test_420_controls_interval.py``
  - ``test_430_controls_options.py``
  - ``test_440_controls_array.py``

**Cross-Control Integration:**
  Once multiple control types exist:

  - ``test_700_control_collections.py`` (managing multiple controls)
  - ``test_800_control_registry.py`` (type registry and descriptor_to_definition)

Conclusion
===============================================================================

This test plan provides a systematic approach to achieving 100% test coverage
for control definitions and in-memory control production. The plan follows
project testing principles:

- **Dependency injection over monkey-patching**
- **Systematic coverage of all code paths**
- **Clean test organization with numbered modules**
- **Immutability verification at every step**

The current architecture is highly testable with no changes needed. All code
can be fully tested through the public API using real objects and dependency
injection.

**Ready for implementation.**
