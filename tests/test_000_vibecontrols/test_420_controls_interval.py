# vim: set filetype=python fileencoding=utf-8:
# -*- coding: utf-8 -*-

#============================================================================#
#                                                                            #
#  Licensed under the Apache License, Version 2.0 (the "License");           #
#  you may not use this file except in compliance with the License.          #
#  You may obtain a copy of the License at                                   #
#                                                                            #
#      http://www.apache.org/licenses/LICENSE-2.0                            #
#                                                                            #
#  Unless required by applicable law or agreed to in writing, software       #
#  distributed under the License is distributed on an "AS IS" BASIS,         #
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  #
#  See the License for the specific language governing permissions and       #
#  limitations under the License.                                            #
#                                                                            #
#============================================================================#


''' Test suite for Interval control. '''


import pytest
from absence import absent

from frigid import exceptions as frigid_exceptions

from vibecontrols import exceptions
from vibecontrols.controls import interval


# 000-099: IntervalHints dataclass

def test_000_interval_hints_default_creation( ):
    ''' IntervalHints is created with defaults. '''
    hints = interval.IntervalHints( )
    assert hints.widget_preference is None
    assert hints.orientation is None
    assert hints.show_ticks is False
    assert hints.show_value is True
    assert hints.label is None
    assert hints.help_text is None


def test_010_interval_hints_with_slider( ):
    ''' IntervalHints is created with widget_preference (slider). '''
    hints = interval.IntervalHints( widget_preference = 'slider' )
    assert hints.widget_preference == 'slider'


def test_015_interval_hints_with_spinbox( ):
    ''' IntervalHints is created with widget_preference (spinbox). '''
    hints = interval.IntervalHints( widget_preference = 'spinbox' )
    assert hints.widget_preference == 'spinbox'


def test_020_interval_hints_with_horizontal( ):
    ''' IntervalHints is created with orientation (horizontal). '''
    hints = interval.IntervalHints( orientation = 'horizontal' )
    assert hints.orientation == 'horizontal'


def test_025_interval_hints_with_vertical( ):
    ''' IntervalHints is created with orientation (vertical). '''
    hints = interval.IntervalHints( orientation = 'vertical' )
    assert hints.orientation == 'vertical'


def test_030_interval_hints_with_ticks( ):
    ''' IntervalHints is created with show_ticks flag. '''
    hints = interval.IntervalHints( show_ticks = True )
    assert hints.show_ticks is True


def test_040_interval_hints_with_value( ):
    ''' IntervalHints is created with show_value flag. '''
    hints = interval.IntervalHints( show_value = False )
    assert hints.show_value is False


def test_050_interval_hints_with_label( ):
    ''' IntervalHints is created with label. '''
    hints = interval.IntervalHints( label = 'Volume' )
    assert hints.label == 'Volume'


def test_060_interval_hints_with_help( ):
    ''' IntervalHints is created with help_text. '''
    hints = interval.IntervalHints( help_text = 'Adjust volume level' )
    assert hints.help_text == 'Adjust volume level'


def test_070_interval_hints_all_fields( ):
    ''' IntervalHints is created with all fields together. '''
    hints = interval.IntervalHints(
        widget_preference = 'slider',
        orientation = 'horizontal',
        show_ticks = True,
        show_value = True,
        label = 'Temperature',
        help_text = 'Set temperature' )
    assert hints.widget_preference == 'slider'
    assert hints.orientation == 'horizontal'
    assert hints.show_ticks is True
    assert hints.show_value is True
    assert hints.label == 'Temperature'
    assert hints.help_text == 'Set temperature'


def test_080_interval_hints_immutability( ):
    ''' IntervalHints cannot be modified after creation. '''
    hints = interval.IntervalHints( label = 'Original' )
    with pytest.raises( frigid_exceptions.AttributeImmutability ):
        hints.label = 'Modified'


# 100-199: IntervalDefinition creation and configuration

def test_100_interval_definition_default_creation( ):
    ''' IntervalDefinition is created with required parameters. '''
    definition = interval.IntervalDefinition(
        minimum = 0.0, maximum = 100.0, default = 50.0 )
    assert definition.minimum == 0.0
    assert definition.maximum == 100.0
    assert definition.default == 50.0
    assert definition.grade is None
    assert definition.validation_message == 'Value must be numeric'
    assert isinstance( definition.hints, interval.IntervalHints )


def test_110_interval_definition_with_grade( ):
    ''' IntervalDefinition is created with grade for discrete interval. '''
    definition = interval.IntervalDefinition(
        minimum = 0.0, maximum = 100.0, default = 50.0, grade = 5.0 )
    assert definition.grade == 5.0


def test_120_interval_definition_without_grade( ):
    ''' IntervalDefinition is created with grade=None for continuous. '''
    definition = interval.IntervalDefinition(
        minimum = 0.0, maximum = 100.0, default = 50.0, grade = None )
    assert definition.grade is None


def test_130_interval_definition_custom_message( ):
    ''' IntervalDefinition is created with custom validation_message. '''
    definition = interval.IntervalDefinition(
        minimum = 0.0, maximum = 10.0, default = 5.0,
        validation_message = 'Must be a number' )
    assert definition.validation_message == 'Must be a number'


def test_140_interval_definition_custom_hints( ):
    ''' IntervalDefinition is created with custom hints. '''
    hints = interval.IntervalHints( widget_preference = 'slider' )
    definition = interval.IntervalDefinition(
        minimum = 0.0, maximum = 100.0, default = 50.0, hints = hints )
    assert definition.hints is hints


def test_150_interval_definition_all_parameters( ):
    ''' IntervalDefinition is created with all parameters. '''
    hints = interval.IntervalHints( orientation = 'horizontal' )
    definition = interval.IntervalDefinition(
        minimum = 0.0,
        maximum = 100.0,
        default = 25.0,
        grade = 5.0,
        validation_message = 'Invalid number',
        hints = hints )
    assert definition.minimum == 0.0
    assert definition.maximum == 100.0
    assert definition.default == 25.0
    assert definition.grade == 5.0
    assert definition.validation_message == 'Invalid number'
    assert definition.hints is hints


def test_160_interval_definition_immutability( ):
    ''' IntervalDefinition cannot be modified after creation. '''
    definition = interval.IntervalDefinition(
        minimum = 0.0, maximum = 10.0, default = 5.0 )
    with pytest.raises( frigid_exceptions.AttributeImmutability ):
        definition.default = 7.0


def test_170_interval_definition_invalid_non_numeric_minimum( ):
    ''' Non-numeric minimum raises DefinitionInvalidity. '''
    with pytest.raises(
        exceptions.DefinitionInvalidity,
        match = 'minimum' ):
        interval.IntervalDefinition(
            minimum = 'zero', maximum = 10.0, default = 5.0 )


def test_171_interval_definition_invalid_non_numeric_maximum( ):
    ''' Non-numeric maximum raises DefinitionInvalidity. '''
    with pytest.raises(
        exceptions.DefinitionInvalidity,
        match = 'maximum' ):
        interval.IntervalDefinition(
            minimum = 0.0, maximum = 'ten', default = 5.0 )


def test_172_interval_definition_invalid_non_numeric_default( ):
    ''' Non-numeric default raises DefinitionInvalidity. '''
    with pytest.raises(
        exceptions.DefinitionInvalidity,
        match = 'default' ):
        interval.IntervalDefinition(
            minimum = 0.0, maximum = 10.0, default = 'five' )


def test_173_interval_definition_invalid_minimum_exceeds_maximum( ):
    ''' minimum > maximum raises DefinitionInvalidity. '''
    with pytest.raises(
        exceptions.DefinitionInvalidity,
        match = 'minimum' ):
        interval.IntervalDefinition(
            minimum = 100.0, maximum = 10.0, default = 50.0 )


def test_174_interval_definition_invalid_default_below_minimum( ):
    ''' default < minimum raises DefinitionInvalidity. '''
    with pytest.raises(
        exceptions.DefinitionInvalidity,
        match = 'default' ):
        interval.IntervalDefinition(
            minimum = 10.0, maximum = 100.0, default = 5.0 )


def test_175_interval_definition_invalid_default_above_maximum( ):
    ''' default > maximum raises DefinitionInvalidity. '''
    with pytest.raises(
        exceptions.DefinitionInvalidity,
        match = 'default' ):
        interval.IntervalDefinition(
            minimum = 10.0, maximum = 100.0, default = 105.0 )


def test_176_interval_definition_invalid_non_numeric_grade( ):
    ''' Non-numeric grade raises DefinitionInvalidity. '''
    with pytest.raises(
        exceptions.DefinitionInvalidity,
        match = 'grade' ):
        interval.IntervalDefinition(
            minimum = 0.0, maximum = 10.0, default = 5.0, grade = 'one' )


def test_177_interval_definition_invalid_zero_grade( ):
    ''' grade=0 raises DefinitionInvalidity. '''
    with pytest.raises(
        exceptions.DefinitionInvalidity,
        match = 'grade' ):
        interval.IntervalDefinition(
            minimum = 0.0, maximum = 10.0, default = 5.0, grade = 0 )


def test_178_interval_definition_invalid_negative_grade( ):
    ''' grade<0 raises DefinitionInvalidity. '''
    with pytest.raises(
        exceptions.DefinitionInvalidity,
        match = 'grade' ):
        interval.IntervalDefinition(
            minimum = 0.0, maximum = 10.0, default = 5.0, grade = -1.0 )


# 200-299: IntervalDefinition.validate_value()

def test_200_validate_value_valid_integer( ):
    ''' Valid integer in range passes validation. '''
    definition = interval.IntervalDefinition(
        minimum = 0.0, maximum = 100.0, default = 50.0 )
    result = definition.validate_value( 42 )
    assert result == 42.0


def test_210_validate_value_valid_float( ):
    ''' Valid float in range passes validation. '''
    definition = interval.IntervalDefinition(
        minimum = 0.0, maximum = 100.0, default = 50.0 )
    result = definition.validate_value( 42.5 )
    assert result == 42.5


def test_220_validate_value_at_minimum( ):
    ''' Value exactly at minimum boundary passes validation. '''
    definition = interval.IntervalDefinition(
        minimum = 0.0, maximum = 100.0, default = 50.0 )
    result = definition.validate_value( 0.0 )
    assert result == 0.0


def test_230_validate_value_at_maximum( ):
    ''' Value exactly at maximum boundary passes validation. '''
    definition = interval.IntervalDefinition(
        minimum = 0.0, maximum = 100.0, default = 50.0 )
    result = definition.validate_value( 100.0 )
    assert result == 100.0


def test_240_validate_value_below_minimum( ):
    ''' Value below minimum raises BoundsConstraintViolation. '''
    definition = interval.IntervalDefinition(
        minimum = 10.0, maximum = 100.0, default = 50.0 )
    with pytest.raises( exceptions.BoundsConstraintViolation ):
        definition.validate_value( 5.0 )


def test_250_validate_value_above_maximum( ):
    ''' Value above maximum raises BoundsConstraintViolation. '''
    definition = interval.IntervalDefinition(
        minimum = 0.0, maximum = 100.0, default = 50.0 )
    with pytest.raises( exceptions.BoundsConstraintViolation ):
        definition.validate_value( 105.0 )


def test_260_validate_value_continuous_no_grade( ):
    ''' grade=None allows any value in range. '''
    definition = interval.IntervalDefinition(
        minimum = 0.0, maximum = 100.0, default = 50.0, grade = None )
    result = definition.validate_value( 42.7531 )
    assert result == 42.7531


def test_270_validate_value_discrete_aligned( ):
    ''' Value aligned with grade (valid). '''
    definition = interval.IntervalDefinition(
        minimum = 0.0, maximum = 100.0, default = 50.0, grade = 5.0 )
    result = definition.validate_value( 45.0 )
    assert result == 45.0


def test_280_validate_value_discrete_misaligned( ):
    ''' Value misaligned with grade raises StepConstraintViolation. '''
    definition = interval.IntervalDefinition(
        minimum = 0.0, maximum = 100.0, default = 50.0, grade = 5.0 )
    with pytest.raises( exceptions.StepConstraintViolation ):
        definition.validate_value( 42.3 )


def test_290_validate_value_floating_point_precision( ):
    ''' Floating-point boundary precision is handled correctly. '''
    definition = interval.IntervalDefinition(
        minimum = 0.0, maximum = 1.0, default = 0.5, grade = 0.1 )
    # 0.3 should align with grade (0.0 + 3 * 0.1)
    result = definition.validate_value( 0.3 )
    assert result == 0.3


def test_291_validate_value_negative_range( ):
    ''' Values in negative range are handled correctly. '''
    definition = interval.IntervalDefinition(
        minimum = -10.0, maximum = -1.0, default = -5.0 )
    result = definition.validate_value( -7.0 )
    assert result == -7.0


def test_292_validate_value_range_with_zero( ):
    ''' Values in range including zero are handled correctly. '''
    definition = interval.IntervalDefinition(
        minimum = -10.0, maximum = 10.0, default = 0.0 )
    result = definition.validate_value( 0.0 )
    assert result == 0.0


def test_293_validate_value_small_grade( ):
    ''' Very small grade (0.01) is handled correctly. '''
    definition = interval.IntervalDefinition(
        minimum = 0.0, maximum = 1.0, default = 0.5, grade = 0.01 )
    result = definition.validate_value( 0.42 )
    assert result == 0.42


def test_294_validate_value_invalid_string( ):
    ''' String raises ControlInvalidity. '''
    definition = interval.IntervalDefinition(
        minimum = 0.0, maximum = 10.0, default = 5.0 )
    with pytest.raises(
        exceptions.ControlInvalidity,
        match = 'numeric' ):
        definition.validate_value( 'five' )


def test_295_validate_value_invalid_none( ):
    ''' None raises ControlInvalidity. '''
    definition = interval.IntervalDefinition(
        minimum = 0.0, maximum = 10.0, default = 5.0 )
    with pytest.raises(
        exceptions.ControlInvalidity,
        match = 'numeric' ):
        definition.validate_value( None )


def test_296_validate_value_custom_message( ):
    ''' Custom validation message appears in exception. '''
    definition = interval.IntervalDefinition(
        minimum = 0.0, maximum = 10.0, default = 5.0,
        validation_message = 'Must be a number' )
    with pytest.raises(
        exceptions.ControlInvalidity,
        match = 'Must be a number' ):
        definition.validate_value( 'text' )


# 300-399: IntervalDefinition.produce_control()

def test_300_produce_control_no_initial( ):
    ''' Control is produced with default value when no initial provided. '''
    definition = interval.IntervalDefinition(
        minimum = 0.0, maximum = 100.0, default = 42.0 )
    control = definition.produce_control( )
    assert control.current == 42.0


def test_310_produce_control_initial_integer( ):
    ''' Control is produced with valid initial integer. '''
    definition = interval.IntervalDefinition(
        minimum = 0.0, maximum = 100.0, default = 50.0 )
    control = definition.produce_control( initial = 75 )
    assert control.current == 75.0


def test_320_produce_control_initial_float( ):
    ''' Control is produced with valid initial float. '''
    definition = interval.IntervalDefinition(
        minimum = 0.0, maximum = 100.0, default = 50.0 )
    control = definition.produce_control( initial = 67.5 )
    assert control.current == 67.5


def test_330_produce_control_invalid_initial( ):
    ''' Invalid initial value raises exception. '''
    definition = interval.IntervalDefinition(
        minimum = 0.0, maximum = 100.0, default = 50.0 )
    with pytest.raises( exceptions.ControlInvalidity ):
        definition.produce_control( initial = 'invalid' )


def test_340_produce_control_absent( ):
    ''' Explicit absent uses default value. '''
    definition = interval.IntervalDefinition(
        minimum = 0.0, maximum = 100.0, default = 30.0 )
    control = definition.produce_control( initial = absent )
    assert control.current == 30.0


def test_350_produce_control_returns_interval( ):
    ''' produce_control returns Interval control type. '''
    definition = interval.IntervalDefinition(
        minimum = 0.0, maximum = 100.0, default = 50.0 )
    control = definition.produce_control( )
    assert isinstance( control, interval.Interval )


def test_360_produce_control_immutability( ):
    ''' Definition is unchanged after control production. '''
    definition = interval.IntervalDefinition(
        minimum = 0.0, maximum = 100.0, default = 50.0 )
    control = definition.produce_control( )
    assert definition.default == 50.0
    assert control.current == 50.0


# 400-499: IntervalDefinition.serialize_value()

def test_400_serialize_value_integer( ):
    ''' Integer serializes as-is (as float). '''
    definition = interval.IntervalDefinition(
        minimum = 0.0, maximum = 100.0, default = 50.0 )
    result = definition.serialize_value( 42.0 )
    assert result == 42.0


def test_410_serialize_value_float( ):
    ''' Float serializes as-is. '''
    definition = interval.IntervalDefinition(
        minimum = 0.0, maximum = 100.0, default = 50.0 )
    result = definition.serialize_value( 42.5 )
    assert result == 42.5


def test_420_serialize_value_at_boundary( ):
    ''' Boundary values serialize correctly. '''
    definition = interval.IntervalDefinition(
        minimum = 0.0, maximum = 100.0, default = 50.0 )
    assert definition.serialize_value( 0.0 ) == 0.0
    assert definition.serialize_value( 100.0 ) == 100.0


# 500-599: IntervalDefinition.produce_default()

def test_500_produce_default( ):
    ''' Configured default value is produced. '''
    definition = interval.IntervalDefinition(
        minimum = 0.0, maximum = 100.0, default = 75.0 )
    result = definition.produce_default( )
    assert result == 75.0


def test_510_produce_default_custom( ):
    ''' Custom default is respected. '''
    definition = interval.IntervalDefinition(
        minimum = -10.0, maximum = 10.0, default = -3.5 )
    result = definition.produce_default( )
    assert result == -3.5


# 600-699: Interval control creation and attributes

def test_600_interval_control_creation( ):
    ''' Interval control is created with definition and current. '''
    definition = interval.IntervalDefinition(
        minimum = 0.0, maximum = 100.0, default = 50.0 )
    control = interval.Interval( definition = definition, current = 42.0 )
    assert control.definition is definition
    assert control.current == 42.0


def test_610_interval_control_definition_attribute( ):
    ''' Interval control has definition attribute. '''
    definition = interval.IntervalDefinition(
        minimum = 0.0, maximum = 100.0, default = 50.0 )
    control = interval.Interval( definition = definition, current = 50.0 )
    assert hasattr( control, 'definition' )
    assert control.definition is definition


def test_620_interval_control_current_attribute( ):
    ''' Interval control has current attribute. '''
    definition = interval.IntervalDefinition(
        minimum = 0.0, maximum = 100.0, default = 50.0 )
    control = interval.Interval( definition = definition, current = 50.0 )
    assert hasattr( control, 'current' )
    assert control.current == 50.0


def test_630_interval_control_immutability( ):
    ''' Interval control attributes cannot be modified. '''
    definition = interval.IntervalDefinition(
        minimum = 0.0, maximum = 100.0, default = 50.0 )
    control = interval.Interval( definition = definition, current = 50.0 )
    with pytest.raises( frigid_exceptions.AttributeImmutability ):
        control.current = 75.0


# 700-799: Interval.copy()

def test_700_copy_to_new_value( ):
    ''' Control is copied with new numeric value. '''
    definition = interval.IntervalDefinition(
        minimum = 0.0, maximum = 100.0, default = 50.0 )
    original = interval.Interval( definition = definition, current = 50.0 )
    copied = original.copy( 75.0 )
    assert copied.current == 75.0
    assert original.current == 50.0


def test_710_copy_to_minimum( ):
    ''' Control is copied to minimum boundary. '''
    definition = interval.IntervalDefinition(
        minimum = 0.0, maximum = 100.0, default = 50.0 )
    control = interval.Interval( definition = definition, current = 50.0 )
    copied = control.copy( 0.0 )
    assert copied.current == 0.0


def test_720_copy_to_maximum( ):
    ''' Control is copied to maximum boundary. '''
    definition = interval.IntervalDefinition(
        minimum = 0.0, maximum = 100.0, default = 50.0 )
    control = interval.Interval( definition = definition, current = 50.0 )
    copied = control.copy( 100.0 )
    assert copied.current == 100.0


def test_730_copy_returns_new_instance( ):
    ''' copy() returns a different instance. '''
    definition = interval.IntervalDefinition(
        minimum = 0.0, maximum = 100.0, default = 50.0 )
    original = interval.Interval( definition = definition, current = 50.0 )
    copied = original.copy( 75.0 )
    assert id( original ) != id( copied )


def test_740_copy_preserves_definition( ):
    ''' copy() preserves definition reference. '''
    definition = interval.IntervalDefinition(
        minimum = 0.0, maximum = 100.0, default = 50.0 )
    original = interval.Interval( definition = definition, current = 50.0 )
    copied = original.copy( 75.0 )
    assert copied.definition is definition


def test_750_copy_invalid_value( ):
    ''' Copying with invalid value raises ControlInvalidity. '''
    definition = interval.IntervalDefinition(
        minimum = 0.0, maximum = 100.0, default = 50.0 )
    control = interval.Interval( definition = definition, current = 50.0 )
    with pytest.raises( exceptions.ControlInvalidity ):
        control.copy( 'invalid' )


def test_760_copy_original_unchanged( ):
    ''' Original control is unchanged after copy. '''
    definition = interval.IntervalDefinition(
        minimum = 0.0, maximum = 100.0, default = 50.0 )
    original = interval.Interval( definition = definition, current = 50.0 )
    original.copy( 25.0 )
    assert original.current == 50.0


# 800-899: Interval.increment() and Interval.decrement()

def test_800_increment_with_grade( ):
    ''' Successful increment when grade defined. '''
    definition = interval.IntervalDefinition(
        minimum = 0.0, maximum = 100.0, default = 50.0, grade = 5.0 )
    control = interval.Interval( definition = definition, current = 50.0 )
    incremented = control.increment( )
    assert incremented.current == 55.0


def test_810_increment_at_maximum( ):
    ''' Increment at maximum raises BoundsConstraintViolation. '''
    definition = interval.IntervalDefinition(
        minimum = 0.0, maximum = 100.0, default = 50.0, grade = 5.0 )
    control = interval.Interval( definition = definition, current = 100.0 )
    with pytest.raises( exceptions.BoundsConstraintViolation ):
        control.increment( )


def test_820_increment_returns_new_instance( ):
    ''' increment() returns a different instance. '''
    definition = interval.IntervalDefinition(
        minimum = 0.0, maximum = 100.0, default = 50.0, grade = 5.0 )
    original = interval.Interval( definition = definition, current = 50.0 )
    incremented = original.increment( )
    assert id( original ) != id( incremented )


def test_830_increment_preserves_definition( ):
    ''' increment() preserves definition reference. '''
    definition = interval.IntervalDefinition(
        minimum = 0.0, maximum = 100.0, default = 50.0, grade = 5.0 )
    control = interval.Interval( definition = definition, current = 50.0 )
    incremented = control.increment( )
    assert incremented.definition is definition


def test_840_increment_without_grade( ):
    ''' Increment with grade=None raises IncrementOperationFailure. '''
    definition = interval.IntervalDefinition(
        minimum = 0.0, maximum = 100.0, default = 50.0, grade = None )
    control = interval.Interval( definition = definition, current = 50.0 )
    with pytest.raises( exceptions.IncrementOperationFailure ):
        control.increment( )


def test_850_decrement_with_grade( ):
    ''' Successful decrement when grade defined. '''
    definition = interval.IntervalDefinition(
        minimum = 0.0, maximum = 100.0, default = 50.0, grade = 5.0 )
    control = interval.Interval( definition = definition, current = 50.0 )
    decremented = control.decrement( )
    assert decremented.current == 45.0


def test_860_decrement_at_minimum( ):
    ''' Decrement at minimum raises BoundsConstraintViolation. '''
    definition = interval.IntervalDefinition(
        minimum = 0.0, maximum = 100.0, default = 50.0, grade = 5.0 )
    control = interval.Interval( definition = definition, current = 0.0 )
    with pytest.raises( exceptions.BoundsConstraintViolation ):
        control.decrement( )


def test_870_decrement_returns_new_instance( ):
    ''' decrement() returns a different instance. '''
    definition = interval.IntervalDefinition(
        minimum = 0.0, maximum = 100.0, default = 50.0, grade = 5.0 )
    original = interval.Interval( definition = definition, current = 50.0 )
    decremented = original.decrement( )
    assert id( original ) != id( decremented )


def test_880_decrement_preserves_definition( ):
    ''' decrement() preserves definition reference. '''
    definition = interval.IntervalDefinition(
        minimum = 0.0, maximum = 100.0, default = 50.0, grade = 5.0 )
    control = interval.Interval( definition = definition, current = 50.0 )
    decremented = control.decrement( )
    assert decremented.definition is definition


def test_890_decrement_without_grade( ):
    ''' Decrement with grade=None raises IncrementOperationFailure. '''
    definition = interval.IntervalDefinition(
        minimum = 0.0, maximum = 100.0, default = 50.0, grade = None )
    control = interval.Interval( definition = definition, current = 50.0 )
    with pytest.raises( exceptions.IncrementOperationFailure ):
        control.decrement( )


# 900-999: Interval.serialize()

def test_900_serialize_integer( ):
    ''' Integer value serializes correctly. '''
    definition = interval.IntervalDefinition(
        minimum = 0.0, maximum = 100.0, default = 50.0 )
    control = interval.Interval( definition = definition, current = 42.0 )
    result = control.serialize( )
    assert result == 42.0


def test_910_serialize_float( ):
    ''' Float value serializes correctly. '''
    definition = interval.IntervalDefinition(
        minimum = 0.0, maximum = 100.0, default = 50.0 )
    control = interval.Interval( definition = definition, current = 42.5 )
    result = control.serialize( )
    assert result == 42.5


def test_920_serialize_delegates_to_definition( ):
    ''' serialize() delegates to definition.serialize_value(). '''
    definition = interval.IntervalDefinition(
        minimum = 0.0, maximum = 100.0, default = 50.0 )
    control = interval.Interval( definition = definition, current = 75.0 )
    expected = definition.serialize_value( 75.0 )
    result = control.serialize( )
    assert result == expected


# 1000-1099: Integration scenarios

def test_1000_complete_lifecycle( ):
    ''' Complete lifecycle: Create → validate → update → serialize. '''
    definition = interval.IntervalDefinition(
        minimum = 0.0, maximum = 100.0, default = 50.0, grade = 5.0 )
    validated = definition.validate_value( 60.0 )
    control = definition.produce_control( initial = validated )
    updated = control.copy( 70.0 )
    serialized = updated.serialize( )
    assert serialized == 70.0


def test_1010_multiple_controls_same_definition( ):
    ''' Multiple controls share same definition. '''
    definition = interval.IntervalDefinition(
        minimum = 0.0, maximum = 100.0, default = 50.0 )
    control1 = definition.produce_control( )
    control2 = definition.produce_control( initial = 75.0 )
    assert control1.definition is control2.definition
    assert control1.definition is definition


def test_1020_controls_independent( ):
    ''' Modifying one control does not affect another. '''
    definition = interval.IntervalDefinition(
        minimum = 0.0, maximum = 100.0, default = 50.0 )
    control1 = definition.produce_control( initial = 25.0 )
    control2 = definition.produce_control( initial = 75.0 )
    modified = control1.copy( 30.0 )
    assert control1.current == 25.0
    assert control2.current == 75.0
    assert modified.current == 30.0


def test_1030_protocol_compliance( ):
    ''' Interval control implements required protocols. '''
    definition = interval.IntervalDefinition(
        minimum = 0.0, maximum = 100.0, default = 50.0 )
    control = definition.produce_control( )
    assert hasattr( definition, 'validate_value' )
    assert hasattr( definition, 'produce_control' )
    assert hasattr( definition, 'serialize_value' )
    assert hasattr( definition, 'produce_default' )
    assert hasattr( control, 'copy' )
    assert hasattr( control, 'serialize' )
    assert callable( definition.validate_value )
    assert callable( definition.produce_control )
    assert callable( control.copy )
    assert callable( control.serialize )


def test_1040_increment_decrement_chain( ):
    ''' Multiple increment/decrement operations can be chained. '''
    definition = interval.IntervalDefinition(
        minimum = 0.0, maximum = 100.0, default = 50.0, grade = 10.0 )
    control = definition.produce_control( )
    result = control.increment( ).increment( ).decrement( )
    assert result.current == 60.0
