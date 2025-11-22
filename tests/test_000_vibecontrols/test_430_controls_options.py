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


''' Test suite for Options control. '''


import pytest
from absence import absent

from frigid import exceptions as frigid_exceptions

from vibecontrols import exceptions
from vibecontrols.controls import options


# 000-099: OptionsHints dataclass

def test_000_options_hints_default_creation( ):
    ''' OptionsHints is created with defaults. '''
    hints = options.OptionsHints( )
    assert hints.widget_preference is None
    assert hints.label is None
    assert hints.help_text is None


def test_010_options_hints_with_select( ):
    ''' OptionsHints is created with widget_preference (select). '''
    hints = options.OptionsHints( widget_preference = 'select' )
    assert hints.widget_preference == 'select'


def test_015_options_hints_with_radio( ):
    ''' OptionsHints is created with widget_preference (radio). '''
    hints = options.OptionsHints( widget_preference = 'radio' )
    assert hints.widget_preference == 'radio'


def test_020_options_hints_with_dropdown( ):
    ''' OptionsHints is created with widget_preference (dropdown). '''
    hints = options.OptionsHints( widget_preference = 'dropdown' )
    assert hints.widget_preference == 'dropdown'


def test_030_options_hints_with_label( ):
    ''' OptionsHints is created with label. '''
    hints = options.OptionsHints( label = 'Color' )
    assert hints.label == 'Color'


def test_040_options_hints_with_help( ):
    ''' OptionsHints is created with help_text. '''
    hints = options.OptionsHints( help_text = 'Select your color' )
    assert hints.help_text == 'Select your color'


def test_050_options_hints_all_fields( ):
    ''' OptionsHints is created with all fields together. '''
    hints = options.OptionsHints(
        widget_preference = 'radio',
        label = 'Size',
        help_text = 'Choose a size' )
    assert hints.widget_preference == 'radio'
    assert hints.label == 'Size'
    assert hints.help_text == 'Choose a size'


def test_060_options_hints_immutability( ):
    ''' OptionsHints cannot be modified after creation. '''
    hints = options.OptionsHints( label = 'Original' )
    with pytest.raises( frigid_exceptions.AttributeImmutability ):
        hints.label = 'Modified'


# 100-199: OptionsDefinition creation and configuration

def test_100_options_definition_single_select( ):
    ''' OptionsDefinition is created for single-select. '''
    definition = options.OptionsDefinition(
        choices = [ 'red', 'green', 'blue' ],
        default = 'red',
        allow_multiple = False )
    assert definition.choices == ( 'red', 'green', 'blue' )
    assert definition.default == 'red'
    assert definition.allow_multiple is False


def test_110_options_definition_multi_select( ):
    ''' OptionsDefinition is created for multi-select. '''
    definition = options.OptionsDefinition(
        choices = [ 'a', 'b', 'c' ],
        default = [ 'a', 'b' ],
        allow_multiple = True )
    assert definition.allow_multiple is True


def test_120_options_definition_string_choices( ):
    ''' OptionsDefinition is created with string choices. '''
    definition = options.OptionsDefinition(
        choices = [ 'apple', 'banana', 'cherry' ],
        default = 'apple' )
    assert definition.choices == ( 'apple', 'banana', 'cherry' )


def test_130_options_definition_integer_choices( ):
    ''' OptionsDefinition is created with integer choices. '''
    definition = options.OptionsDefinition(
        choices = [ 1, 2, 3, 4, 5 ],
        default = 3 )
    assert definition.choices == ( 1, 2, 3, 4, 5 )


def test_140_options_definition_mixed_type_choices( ):
    ''' OptionsDefinition is created with mixed type choices. '''
    definition = options.OptionsDefinition(
        choices = [ 'text', 42, 3.14, True ],
        default = 'text' )
    assert 'text' in definition.choices
    assert 42 in definition.choices
    assert 3.14 in definition.choices


def test_150_options_definition_custom_message( ):
    ''' OptionsDefinition is created with custom validation_message. '''
    definition = options.OptionsDefinition(
        choices = [ 'a', 'b' ],
        default = 'a',
        validation_message = 'Must choose from list' )
    assert definition.validation_message == 'Must choose from list'


def test_160_options_definition_custom_hints( ):
    ''' OptionsDefinition is created with custom hints. '''
    hints = options.OptionsHints( widget_preference = 'radio' )
    definition = options.OptionsDefinition(
        choices = [ 'x', 'y', 'z' ],
        default = 'x',
        hints = hints )
    assert definition.hints is hints


def test_170_options_definition_all_parameters( ):
    ''' OptionsDefinition is created with all parameters. '''
    hints = options.OptionsHints( label = 'Choose' )
    definition = options.OptionsDefinition(
        choices = [ 1, 2, 3 ],
        default = [ 1, 2 ],
        allow_multiple = True,
        validation_message = 'Invalid choice',
        hints = hints )
    assert definition.allow_multiple is True
    assert definition.validation_message == 'Invalid choice'
    assert definition.hints is hints


def test_180_options_definition_immutability( ):
    ''' OptionsDefinition cannot be modified after creation. '''
    definition = options.OptionsDefinition(
        choices = [ 'a', 'b' ], default = 'a' )
    with pytest.raises( frigid_exceptions.AttributeImmutability ):
        definition.default = 'b'


def test_190_options_definition_invalid_empty_choices( ):
    ''' Empty choices raises DefinitionInvalidity. '''
    with pytest.raises(
        exceptions.DefinitionInvalidity,
        match = 'choices' ):
        options.OptionsDefinition( choices = [ ], default = None )


def test_191_options_definition_invalid_default_not_in_choices_single( ):
    ''' Default not in choices (single-select) raises DefinitionInvalidity. '''
    with pytest.raises( exceptions.DefinitionInvalidity ):
        options.OptionsDefinition(
            choices = [ 'a', 'b', 'c' ], default = 'x' )


def test_192_options_definition_invalid_default_not_in_choices_multi( ):
    ''' Default not in choices (multi-select) raises DefinitionInvalidity. '''
    with pytest.raises( exceptions.DefinitionInvalidity ):
        options.OptionsDefinition(
            choices = [ 'a', 'b', 'c' ],
            default = [ 'a', 'x' ],
            allow_multiple = True )


def test_193_options_definition_duplicate_choices( ):
    ''' Duplicate choices raise DefinitionInvalidity. '''
    with pytest.raises(
        exceptions.DefinitionInvalidity,
        match = 'unique' ):
        options.OptionsDefinition(
            choices = [ 'a', 'b', 'a' ], default = 'a' )


# 200-299: OptionsDefinition.validate_value()

def test_200_validate_value_single_valid( ):
    ''' Valid choice for single-select passes validation. '''
    definition = options.OptionsDefinition(
        choices = [ 'red', 'green', 'blue' ], default = 'red' )
    result = definition.validate_value( 'green' )
    assert result == 'green'


def test_210_validate_value_single_invalid( ):
    ''' Invalid choice for single-select raises ControlInvalidity. '''
    definition = options.OptionsDefinition(
        choices = [ 'a', 'b', 'c' ], default = 'a' )
    with pytest.raises( exceptions.ControlInvalidity ):
        definition.validate_value( 'x' )


def test_220_validate_value_multi_valid( ):
    ''' Valid choices for multi-select pass validation. '''
    definition = options.OptionsDefinition(
        choices = [ 'a', 'b', 'c', 'd' ],
        default = [ 'a' ],
        allow_multiple = True )
    result = definition.validate_value( [ 'b', 'c' ] )
    assert result == ( 'b', 'c' )


def test_230_validate_value_multi_empty( ):
    ''' Empty sequence for multi-select raises SizeConstraintViolation. '''
    definition = options.OptionsDefinition(
        choices = [ 'a', 'b' ],
        default = [ 'a' ],
        allow_multiple = True )
    with pytest.raises( exceptions.SizeConstraintViolation ):
        definition.validate_value( [ ] )


def test_240_validate_value_multi_single_item( ):
    ''' Single item for multi-select passes validation. '''
    definition = options.OptionsDefinition(
        choices = [ 'a', 'b', 'c' ],
        default = [ 'a' ],
        allow_multiple = True )
    result = definition.validate_value( [ 'b' ] )
    assert result == ( 'b', )


def test_250_validate_value_multi_all_choices( ):
    ''' All choices selected for multi-select passes validation. '''
    definition = options.OptionsDefinition(
        choices = [ 'a', 'b', 'c' ],
        default = [ 'a' ],
        allow_multiple = True )
    result = definition.validate_value( [ 'a', 'b', 'c' ] )
    assert result == ( 'a', 'b', 'c' )


def test_260_validate_value_multi_invalid_one( ):
    ''' Invalid choice in multi-select raises SelectionConstraintViolation. '''
    definition = options.OptionsDefinition(
        choices = [ 'a', 'b', 'c' ],
        default = [ 'a' ],
        allow_multiple = True )
    with pytest.raises( exceptions.SelectionConstraintViolation ):
        definition.validate_value( [ 'a', 'x' ] )


def test_270_validate_value_multi_duplicates( ):
    ''' Duplicates in multi-select raise UniquenessConstraintViolation. '''
    definition = options.OptionsDefinition(
        choices = [ 'a', 'b', 'c' ],
        default = [ 'a' ],
        allow_multiple = True )
    with pytest.raises( exceptions.UniquenessConstraintViolation ):
        definition.validate_value( [ 'a', 'b', 'a' ] )


def test_280_validate_value_multi_when_single_expected( ):
    ''' Multiple values when single-select raises ControlInvalidity. '''
    definition = options.OptionsDefinition(
        choices = [ 'a', 'b', 'c' ], default = 'a' )
    with pytest.raises( exceptions.ControlInvalidity ):
        definition.validate_value( [ 'a', 'b' ] )


def test_291_validate_value_custom_message( ):
    ''' Custom validation message appears in exception. '''
    definition = options.OptionsDefinition(
        choices = [ 'a', 'b' ],
        default = 'a',
        validation_message = 'Must choose from list' )
    with pytest.raises(
        exceptions.ControlInvalidity,
        match = 'Must choose from list' ):
        definition.validate_value( 'x' )


# 300-399: OptionsDefinition.produce_control()

def test_300_produce_control_no_initial_single( ):
    ''' Control is produced with default value (single-select). '''
    definition = options.OptionsDefinition(
        choices = [ 'a', 'b', 'c' ], default = 'b' )
    control = definition.produce_control( )
    assert control.current == 'b'


def test_310_produce_control_no_initial_multi( ):
    ''' Control is produced with default value (multi-select). '''
    definition = options.OptionsDefinition(
        choices = [ 'a', 'b', 'c' ],
        default = [ 'a', 'b' ],
        allow_multiple = True )
    control = definition.produce_control( )
    assert control.current == ( 'a', 'b' )


def test_320_produce_control_initial_valid_single( ):
    ''' Control is produced with valid initial (single-select). '''
    definition = options.OptionsDefinition(
        choices = [ 'a', 'b', 'c' ], default = 'a' )
    control = definition.produce_control( initial = 'c' )
    assert control.current == 'c'


def test_330_produce_control_initial_valid_multi( ):
    ''' Control is produced with valid initial (multi-select). '''
    definition = options.OptionsDefinition(
        choices = [ 'a', 'b', 'c' ],
        default = [ 'a' ],
        allow_multiple = True )
    control = definition.produce_control( initial = [ 'b', 'c' ] )
    assert control.current == ( 'b', 'c' )


def test_340_produce_control_invalid_initial( ):
    ''' Invalid initial value raises exception. '''
    definition = options.OptionsDefinition(
        choices = [ 'a', 'b' ], default = 'a' )
    with pytest.raises( exceptions.ControlInvalidity ):
        definition.produce_control( initial = 'x' )


def test_350_produce_control_absent( ):
    ''' Explicit absent uses default value. '''
    definition = options.OptionsDefinition(
        choices = [ 'a', 'b' ], default = 'a' )
    control = definition.produce_control( initial = absent )
    assert control.current == 'a'


def test_360_produce_control_returns_options( ):
    ''' produce_control returns Options control type. '''
    definition = options.OptionsDefinition(
        choices = [ 'a', 'b' ], default = 'a' )
    control = definition.produce_control( )
    assert isinstance( control, options.Options )


def test_370_produce_control_immutability( ):
    ''' Definition is unchanged after control production. '''
    definition = options.OptionsDefinition(
        choices = [ 'a', 'b' ], default = 'a' )
    control = definition.produce_control( )
    assert definition.default == 'a'
    assert control.current == 'a'


# 400-499: OptionsDefinition.serialize_value()

def test_400_serialize_value_single( ):
    ''' Single choice serializes as value. '''
    definition = options.OptionsDefinition(
        choices = [ 'a', 'b', 'c' ], default = 'a' )
    result = definition.serialize_value( 'b' )
    assert result == 'b'


def test_410_serialize_value_multi( ):
    ''' Multiple choices serialize as list. '''
    definition = options.OptionsDefinition(
        choices = [ 'a', 'b', 'c' ],
        default = [ 'a' ],
        allow_multiple = True )
    result = definition.serialize_value( ( 'a', 'b' ) )
    assert result == [ 'a', 'b' ]


def test_420_serialize_value_preserves_type( ):
    ''' Original value type is preserved in serialization. '''
    definition = options.OptionsDefinition(
        choices = [ 1, 2, 3 ], default = 1 )
    result = definition.serialize_value( 2 )
    assert result == 2
    assert isinstance( result, int )


# 500-599: OptionsDefinition.produce_default()

def test_500_produce_default_single( ):
    ''' Default single choice is produced. '''
    definition = options.OptionsDefinition(
        choices = [ 'a', 'b', 'c' ], default = 'b' )
    result = definition.produce_default( )
    assert result == 'b'


def test_510_produce_default_multi( ):
    ''' Default multiple choices are produced. '''
    definition = options.OptionsDefinition(
        choices = [ 'a', 'b', 'c' ],
        default = [ 'a', 'c' ],
        allow_multiple = True )
    result = definition.produce_default( )
    assert result == ( 'a', 'c' )


def test_520_produce_default_custom( ):
    ''' Custom default is respected. '''
    definition = options.OptionsDefinition(
        choices = [ 1, 2, 3, 4, 5 ], default = 4 )
    result = definition.produce_default( )
    assert result == 4


# 600-699: Options control creation and attributes

def test_600_options_control_creation( ):
    ''' Options control is created with definition and current. '''
    definition = options.OptionsDefinition(
        choices = [ 'a', 'b' ], default = 'a' )
    control = options.Options( definition = definition, current = 'b' )
    assert control.definition is definition
    assert control.current == 'b'


def test_610_options_control_definition_attribute( ):
    ''' Options control has definition attribute. '''
    definition = options.OptionsDefinition(
        choices = [ 'a', 'b' ], default = 'a' )
    control = options.Options( definition = definition, current = 'a' )
    assert hasattr( control, 'definition' )
    assert control.definition is definition


def test_620_options_control_current_attribute( ):
    ''' Options control has current attribute. '''
    definition = options.OptionsDefinition(
        choices = [ 'a', 'b' ], default = 'a' )
    control = options.Options( definition = definition, current = 'a' )
    assert hasattr( control, 'current' )
    assert control.current == 'a'


def test_630_options_control_immutability( ):
    ''' Options control attributes cannot be modified. '''
    definition = options.OptionsDefinition(
        choices = [ 'a', 'b' ], default = 'a' )
    control = options.Options( definition = definition, current = 'a' )
    with pytest.raises( frigid_exceptions.AttributeImmutability ):
        control.current = 'b'


# 700-799: Options.copy()

def test_700_copy_to_new_choice_single( ):
    ''' Control is copied with new choice (single-select). '''
    definition = options.OptionsDefinition(
        choices = [ 'a', 'b', 'c' ], default = 'a' )
    original = options.Options( definition = definition, current = 'a' )
    copied = original.copy( 'b' )
    assert copied.current == 'b'
    assert original.current == 'a'


def test_710_copy_to_new_choices_multi( ):
    ''' Control is copied with new choices (multi-select). '''
    definition = options.OptionsDefinition(
        choices = [ 'a', 'b', 'c' ],
        default = [ 'a' ],
        allow_multiple = True )
    original = options.Options( definition = definition, current = ( 'a', ) )
    copied = original.copy( [ 'b', 'c' ] )
    assert copied.current == ( 'b', 'c' )


def test_720_copy_returns_new_instance( ):
    ''' copy() returns a different instance. '''
    definition = options.OptionsDefinition(
        choices = [ 'a', 'b' ], default = 'a' )
    original = options.Options( definition = definition, current = 'a' )
    copied = original.copy( 'b' )
    assert id( original ) != id( copied )


def test_730_copy_preserves_definition( ):
    ''' copy() preserves definition reference. '''
    definition = options.OptionsDefinition(
        choices = [ 'a', 'b' ], default = 'a' )
    original = options.Options( definition = definition, current = 'a' )
    copied = original.copy( 'b' )
    assert copied.definition is definition


def test_740_copy_invalid_value( ):
    ''' Copying with invalid value raises ControlInvalidity. '''
    definition = options.OptionsDefinition(
        choices = [ 'a', 'b' ], default = 'a' )
    control = options.Options( definition = definition, current = 'a' )
    with pytest.raises( exceptions.ControlInvalidity ):
        control.copy( 'x' )


def test_750_copy_original_unchanged( ):
    ''' Original control is unchanged after copy. '''
    definition = options.OptionsDefinition(
        choices = [ 'a', 'b' ], default = 'a' )
    original = options.Options( definition = definition, current = 'a' )
    original.copy( 'b' )
    assert original.current == 'a'


# 800-899: Options.cycle_next() and Options.cycle_previous()

def test_800_cycle_next_valid( ):
    ''' cycle_next() selects next choice. '''
    definition = options.OptionsDefinition(
        choices = [ 'a', 'b', 'c' ], default = 'a' )
    control = options.Options( definition = definition, current = 'a' )
    cycled = control.cycle_next( )
    assert cycled.current == 'b'


def test_810_cycle_next_wraps( ):
    ''' cycle_next() wraps to first choice from last. '''
    definition = options.OptionsDefinition(
        choices = [ 'a', 'b', 'c' ], default = 'a' )
    control = options.Options( definition = definition, current = 'c' )
    cycled = control.cycle_next( )
    assert cycled.current == 'a'


def test_820_cycle_next_with_multi_select( ):
    ''' cycle_next() with multi-select raises CycleOperationFailure. '''
    definition = options.OptionsDefinition(
        choices = [ 'a', 'b', 'c' ],
        default = [ 'a' ],
        allow_multiple = True )
    control = options.Options( definition = definition, current = ( 'a', ) )
    with pytest.raises( exceptions.CycleOperationFailure ):
        control.cycle_next( )


def test_830_cycle_previous_valid( ):
    ''' cycle_previous() selects previous choice. '''
    definition = options.OptionsDefinition(
        choices = [ 'a', 'b', 'c' ], default = 'b' )
    control = options.Options( definition = definition, current = 'b' )
    cycled = control.cycle_previous( )
    assert cycled.current == 'a'


def test_840_cycle_previous_wraps( ):
    ''' cycle_previous() wraps to last choice from first. '''
    definition = options.OptionsDefinition(
        choices = [ 'a', 'b', 'c' ], default = 'a' )
    control = options.Options( definition = definition, current = 'a' )
    cycled = control.cycle_previous( )
    assert cycled.current == 'c'


def test_850_cycle_previous_with_multi_select( ):
    ''' cycle_previous() with multi-select raises CycleOperationFailure. '''
    definition = options.OptionsDefinition(
        choices = [ 'a', 'b' ],
        default = [ 'a' ],
        allow_multiple = True )
    control = options.Options( definition = definition, current = ( 'a', ) )
    with pytest.raises( exceptions.CycleOperationFailure ):
        control.cycle_previous( )


# 900-999: Options.serialize()

def test_900_serialize_single( ):
    ''' Single selection serializes correctly. '''
    definition = options.OptionsDefinition(
        choices = [ 'a', 'b', 'c' ], default = 'a' )
    control = options.Options( definition = definition, current = 'b' )
    result = control.serialize( )
    assert result == 'b'


def test_910_serialize_multi( ):
    ''' Multiple selections serialize correctly. '''
    definition = options.OptionsDefinition(
        choices = [ 'a', 'b', 'c' ],
        default = [ 'a' ],
        allow_multiple = True )
    control = options.Options(
        definition = definition, current = ( 'a', 'c' ) )
    result = control.serialize( )
    assert result == [ 'a', 'c' ]


def test_920_serialize_delegates_to_definition( ):
    ''' serialize() delegates to definition.serialize_value(). '''
    definition = options.OptionsDefinition(
        choices = [ 1, 2, 3 ], default = 1 )
    control = options.Options( definition = definition, current = 2 )
    expected = definition.serialize_value( 2 )
    result = control.serialize( )
    assert result == expected


# 1000-1099: Integration scenarios

def test_1000_complete_lifecycle( ):
    ''' Complete lifecycle: Create → validate → update → serialize. '''
    definition = options.OptionsDefinition(
        choices = [ 'small', 'medium', 'large' ], default = 'medium' )
    validated = definition.validate_value( 'small' )
    control = definition.produce_control( initial = validated )
    updated = control.copy( 'large' )
    serialized = updated.serialize( )
    assert serialized == 'large'


def test_1010_multiple_controls_same_definition( ):
    ''' Multiple controls share same definition. '''
    definition = options.OptionsDefinition(
        choices = [ 'a', 'b', 'c' ], default = 'a' )
    control1 = definition.produce_control( )
    control2 = definition.produce_control( initial = 'b' )
    assert control1.definition is control2.definition
    assert control1.definition is definition


def test_1020_controls_independent( ):
    ''' Modifying one control does not affect another. '''
    definition = options.OptionsDefinition(
        choices = [ 'a', 'b', 'c' ], default = 'a' )
    control1 = definition.produce_control( initial = 'a' )
    control2 = definition.produce_control( initial = 'b' )
    modified = control1.copy( 'c' )
    assert control1.current == 'a'
    assert control2.current == 'b'
    assert modified.current == 'c'


def test_1030_protocol_compliance( ):
    ''' Options control implements required protocols. '''
    definition = options.OptionsDefinition(
        choices = [ 'a', 'b' ], default = 'a' )
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


def test_1040_single_choice_edge_case( ):
    ''' Single choice in choices (only one valid option). '''
    definition = options.OptionsDefinition(
        choices = [ 'only' ], default = 'only' )
    control = definition.produce_control( )
    assert control.current == 'only'
    cycled = control.cycle_next( )
    assert cycled.current == 'only'


def test_1050_many_choices( ):
    ''' Many choices (>100) are handled correctly. '''
    choices = list( range( 200 ) )
    definition = options.OptionsDefinition(
        choices = choices, default = 0 )
    control = definition.produce_control( initial = 150 )
    assert control.current == 150
