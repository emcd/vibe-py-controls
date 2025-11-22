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


''' Test suite for Text control. '''


import pytest
from absence import absent

from frigid import exceptions as frigid_exceptions

from vibecontrols import exceptions
from vibecontrols.controls import text


# 000-099: TextHints dataclass

def test_000_text_hints_default_creation( ):
    ''' TextHints is created with defaults. '''
    hints = text.TextHints( )
    assert hints.widget_preference is None
    assert hints.multiline is False
    assert hints.placeholder is None
    assert hints.label is None
    assert hints.help_text is None


def test_010_text_hints_with_widget( ):
    ''' TextHints is created with widget_preference (input). '''
    hints = text.TextHints( widget_preference = 'input' )
    assert hints.widget_preference == 'input'


def test_015_text_hints_with_textarea( ):
    ''' TextHints is created with widget_preference (textarea). '''
    hints = text.TextHints( widget_preference = 'textarea' )
    assert hints.widget_preference == 'textarea'


def test_020_text_hints_with_multiline( ):
    ''' TextHints is created with multiline flag. '''
    hints = text.TextHints( multiline = True )
    assert hints.multiline is True


def test_030_text_hints_with_placeholder( ):
    ''' TextHints is created with placeholder text. '''
    hints = text.TextHints( placeholder = 'Enter text here' )
    assert hints.placeholder == 'Enter text here'


def test_040_text_hints_with_label( ):
    ''' TextHints is created with label. '''
    hints = text.TextHints( label = 'Username' )
    assert hints.label == 'Username'


def test_050_text_hints_with_help( ):
    ''' TextHints is created with help_text. '''
    hints = text.TextHints( help_text = 'Enter your username' )
    assert hints.help_text == 'Enter your username'


def test_060_text_hints_all_fields( ):
    ''' TextHints is created with all fields together. '''
    hints = text.TextHints(
        widget_preference = 'textarea',
        multiline = True,
        placeholder = 'Enter description',
        label = 'Description',
        help_text = 'Provide a detailed description' )
    assert hints.widget_preference == 'textarea'
    assert hints.multiline is True
    assert hints.placeholder == 'Enter description'
    assert hints.label == 'Description'
    assert hints.help_text == 'Provide a detailed description'


def test_070_text_hints_immutability( ):
    ''' TextHints cannot be modified after creation. '''
    hints = text.TextHints( label = 'Original' )
    with pytest.raises( frigid_exceptions.AttributeImmutability ):
        hints.label = 'Modified'


# 100-199: TextDefinition creation and configuration

def test_100_text_definition_default_creation( ):
    ''' TextDefinition is created with all defaults. '''
    definition = text.TextDefinition( )
    assert definition.default == ''
    assert definition.count_min is None
    assert definition.count_max is None
    assert definition.validation_message == 'Value must be a string'
    assert isinstance( definition.hints, text.TextHints )


def test_110_text_definition_custom_default( ):
    ''' TextDefinition is created with custom default string. '''
    definition = text.TextDefinition( default = 'hello' )
    assert definition.default == 'hello'


def test_120_text_definition_count_min( ):
    ''' TextDefinition is created with count_min only. '''
    definition = text.TextDefinition( count_min = 5 )
    assert definition.count_min == 5
    assert definition.count_max is None


def test_130_text_definition_count_max( ):
    ''' TextDefinition is created with count_max only. '''
    definition = text.TextDefinition( count_max = 100 )
    assert definition.count_min is None
    assert definition.count_max == 100


def test_140_text_definition_both_counts( ):
    ''' TextDefinition is created with both count_min and count_max. '''
    definition = text.TextDefinition( count_min = 5, count_max = 100 )
    assert definition.count_min == 5
    assert definition.count_max == 100


def test_150_text_definition_custom_message( ):
    ''' TextDefinition is created with custom validation_message. '''
    definition = text.TextDefinition( validation_message = 'Must be text' )
    assert definition.validation_message == 'Must be text'


def test_160_text_definition_custom_hints( ):
    ''' TextDefinition is created with custom hints. '''
    hints = text.TextHints( multiline = True, label = 'Description' )
    definition = text.TextDefinition( hints = hints )
    assert definition.hints is hints


def test_170_text_definition_all_parameters( ):
    ''' TextDefinition is created with all parameters. '''
    hints = text.TextHints( multiline = True )
    definition = text.TextDefinition(
        default = 'default text',
        count_min = 10,
        count_max = 200,
        validation_message = 'Invalid text',
        hints = hints )
    assert definition.default == 'default text'
    assert definition.count_min == 10
    assert definition.count_max == 200
    assert definition.validation_message == 'Invalid text'
    assert definition.hints is hints


def test_180_text_definition_immutability( ):
    ''' TextDefinition cannot be modified after creation. '''
    definition = text.TextDefinition( default = 'original' )
    with pytest.raises( frigid_exceptions.AttributeImmutability ):
        definition.default = 'modified'


def test_190_text_definition_invalid_negative_count_min( ):
    ''' Negative count_min raises DefinitionInvalidity. '''
    with pytest.raises(
        exceptions.DefinitionInvalidity,
        match = 'count_min' ):
        text.TextDefinition( count_min = -1 )


def test_191_text_definition_invalid_negative_count_max( ):
    ''' Negative count_max raises DefinitionInvalidity. '''
    with pytest.raises(
        exceptions.DefinitionInvalidity,
        match = 'count_max' ):
        text.TextDefinition( count_max = -5 )


def test_192_text_definition_invalid_min_exceeds_max( ):
    ''' count_min > count_max raises DefinitionInvalidity. '''
    with pytest.raises(
        exceptions.DefinitionInvalidity,
        match = 'count_min' ):
        text.TextDefinition( count_min = 100, count_max = 50 )


# 200-299: TextDefinition.validate_value()

def test_200_validate_value_valid_string( ):
    ''' Valid non-empty string passes validation. '''
    definition = text.TextDefinition( )
    result = definition.validate_value( 'hello world' )
    assert result == 'hello world'


def test_210_validate_value_empty_string( ):
    ''' Empty string is valid by default. '''
    definition = text.TextDefinition( )
    result = definition.validate_value( '' )
    assert result == ''


def test_220_validate_value_long_string( ):
    ''' Very long string passes validation without constraints. '''
    definition = text.TextDefinition( )
    long_text = 'a' * 10000
    result = definition.validate_value( long_text )
    assert result == long_text


def test_230_validate_value_unicode( ):
    ''' Unicode characters (emoji, etc.) pass validation. '''
    definition = text.TextDefinition( )
    unicode_text = 'Hello 🌍 世界'
    result = definition.validate_value( unicode_text )
    assert result == unicode_text


def test_240_validate_value_newlines( ):
    ''' Strings with newline characters pass validation. '''
    definition = text.TextDefinition( )
    text_with_newlines = 'Line 1\nLine 2\nLine 3'
    result = definition.validate_value( text_with_newlines )
    assert result == text_with_newlines


def test_250_validate_value_at_count_min( ):
    ''' String exactly at count_min boundary passes validation. '''
    definition = text.TextDefinition( count_min = 5 )
    result = definition.validate_value( 'hello' )
    assert result == 'hello'


def test_260_validate_value_at_count_max( ):
    ''' String exactly at count_max boundary passes validation. '''
    definition = text.TextDefinition( count_max = 5 )
    result = definition.validate_value( 'hello' )
    assert result == 'hello'


def test_270_validate_value_below_count_min( ):
    ''' String below count_min raises SizeConstraintViolation. '''
    definition = text.TextDefinition( count_min = 10 )
    with pytest.raises(
        exceptions.SizeConstraintViolation ):
        definition.validate_value( 'short' )


def test_280_validate_value_above_count_max( ):
    ''' String above count_max raises SizeConstraintViolation. '''
    definition = text.TextDefinition( count_max = 5 )
    with pytest.raises(
        exceptions.SizeConstraintViolation ):
        definition.validate_value( 'too long text' )


def test_290_validate_value_invalid_integer( ):
    ''' Integer raises ControlInvalidity. '''
    definition = text.TextDefinition( )
    with pytest.raises(
        exceptions.ControlInvalidity,
        match = 'string' ):
        definition.validate_value( 42 )


def test_291_validate_value_invalid_bool( ):
    ''' Boolean raises ControlInvalidity. '''
    definition = text.TextDefinition( )
    with pytest.raises(
        exceptions.ControlInvalidity,
        match = 'string' ):
        definition.validate_value( True )


def test_292_validate_value_invalid_none( ):
    ''' None raises ControlInvalidity. '''
    definition = text.TextDefinition( )
    with pytest.raises(
        exceptions.ControlInvalidity,
        match = 'string' ):
        definition.validate_value( None )


def test_293_validate_value_invalid_list( ):
    ''' List raises ControlInvalidity. '''
    definition = text.TextDefinition( )
    with pytest.raises(
        exceptions.ControlInvalidity,
        match = 'string' ):
        definition.validate_value( [ 'a', 'b' ] )


def test_294_validate_value_custom_message( ):
    ''' Custom validation message appears in exception. '''
    definition = text.TextDefinition( validation_message = 'Must be text' )
    with pytest.raises(
        exceptions.ControlInvalidity,
        match = 'Must be text' ):
        definition.validate_value( 123 )


# 300-399: TextDefinition.produce_control()

def test_300_produce_control_no_initial( ):
    ''' Control is produced with default value when no initial provided. '''
    definition = text.TextDefinition( default = 'default text' )
    control = definition.produce_control( )
    assert control.current == 'default text'


def test_310_produce_control_initial_valid( ):
    ''' Control is produced with valid initial string. '''
    definition = text.TextDefinition( )
    control = definition.produce_control( initial = 'custom value' )
    assert control.current == 'custom value'


def test_320_produce_control_initial_empty( ):
    ''' Control is produced with empty initial string. '''
    definition = text.TextDefinition( )
    control = definition.produce_control( initial = '' )
    assert control.current == ''


def test_330_produce_control_invalid_initial( ):
    ''' Invalid initial value raises exception. '''
    definition = text.TextDefinition( )
    with pytest.raises( exceptions.ControlInvalidity ):
        definition.produce_control( initial = 42 )


def test_340_produce_control_absent( ):
    ''' Explicit absent uses default value. '''
    definition = text.TextDefinition( default = 'default' )
    control = definition.produce_control( initial = absent )
    assert control.current == 'default'


def test_350_produce_control_returns_text( ):
    ''' produce_control returns Text control type. '''
    definition = text.TextDefinition( )
    control = definition.produce_control( )
    assert isinstance( control, text.Text )


def test_360_produce_control_immutability( ):
    ''' Definition is unchanged after control production. '''
    definition = text.TextDefinition( default = 'original' )
    control = definition.produce_control( )
    assert definition.default == 'original'
    assert control.current == 'original'


# 400-499: TextDefinition.serialize_value()

def test_400_serialize_value_string( ):
    ''' String serializes as-is. '''
    definition = text.TextDefinition( )
    result = definition.serialize_value( 'hello' )
    assert result == 'hello'


def test_410_serialize_value_empty( ):
    ''' Empty string serializes as-is. '''
    definition = text.TextDefinition( )
    result = definition.serialize_value( '' )
    assert result == ''


def test_420_serialize_value_unicode( ):
    ''' Unicode string serializes correctly. '''
    definition = text.TextDefinition( )
    unicode_text = 'Hello 🌍 世界'
    result = definition.serialize_value( unicode_text )
    assert result == unicode_text


# 500-599: TextDefinition.produce_default()

def test_500_produce_default_empty( ):
    ''' Default is empty string when not specified. '''
    definition = text.TextDefinition( )
    result = definition.produce_default( )
    assert result == ''


def test_510_produce_default_custom( ):
    ''' Custom default is respected. '''
    definition = text.TextDefinition( default = 'custom default' )
    result = definition.produce_default( )
    assert result == 'custom default'


# 600-699: Text control creation and attributes

def test_600_text_control_creation( ):
    ''' Text control is created with definition and current. '''
    definition = text.TextDefinition( )
    control = text.Text( definition = definition, current = 'value' )
    assert control.definition is definition
    assert control.current == 'value'


def test_610_text_control_definition_attribute( ):
    ''' Text control has definition attribute. '''
    definition = text.TextDefinition( )
    control = text.Text( definition = definition, current = 'test' )
    assert hasattr( control, 'definition' )
    assert control.definition is definition


def test_620_text_control_current_attribute( ):
    ''' Text control has current attribute. '''
    definition = text.TextDefinition( )
    control = text.Text( definition = definition, current = 'test' )
    assert hasattr( control, 'current' )
    assert control.current == 'test'


def test_630_text_control_immutability( ):
    ''' Text control attributes cannot be modified. '''
    definition = text.TextDefinition( )
    control = text.Text( definition = definition, current = 'original' )
    with pytest.raises( frigid_exceptions.AttributeImmutability ):
        control.current = 'modified'


# 700-799: Text.copy()

def test_700_copy_to_new_string( ):
    ''' Control is copied with new string value. '''
    definition = text.TextDefinition( )
    original = text.Text( definition = definition, current = 'original' )
    copied = original.copy( 'new value' )
    assert copied.current == 'new value'
    assert original.current == 'original'


def test_710_copy_to_empty( ):
    ''' Control is copied with empty string. '''
    definition = text.TextDefinition( )
    original = text.Text( definition = definition, current = 'text' )
    copied = original.copy( '' )
    assert copied.current == ''


def test_720_copy_returns_new_instance( ):
    ''' copy() returns a different instance. '''
    definition = text.TextDefinition( )
    original = text.Text( definition = definition, current = 'test' )
    copied = original.copy( 'new' )
    assert id( original ) != id( copied )


def test_730_copy_preserves_definition( ):
    ''' copy() preserves definition reference. '''
    definition = text.TextDefinition( )
    original = text.Text( definition = definition, current = 'test' )
    copied = original.copy( 'new' )
    assert copied.definition is definition


def test_740_copy_invalid_value( ):
    ''' Copying with invalid value raises ControlInvalidity. '''
    definition = text.TextDefinition( )
    control = text.Text( definition = definition, current = 'test' )
    with pytest.raises( exceptions.ControlInvalidity ):
        control.copy( 123 )


def test_750_copy_original_unchanged( ):
    ''' Original control is unchanged after copy. '''
    definition = text.TextDefinition( )
    original = text.Text( definition = definition, current = 'original' )
    original.copy( 'new' )
    assert original.current == 'original'


# 800-899: Text.clear()

def test_800_clear_returns_empty( ):
    ''' clear() returns control with empty string. '''
    definition = text.TextDefinition( )
    control = text.Text( definition = definition, current = 'text' )
    cleared = control.clear( )
    assert cleared.current == ''


def test_810_clear_returns_new_instance( ):
    ''' clear() returns a different instance. '''
    definition = text.TextDefinition( )
    control = text.Text( definition = definition, current = 'text' )
    cleared = control.clear( )
    assert id( control ) != id( cleared )


def test_820_clear_preserves_definition( ):
    ''' clear() preserves definition reference. '''
    definition = text.TextDefinition( )
    control = text.Text( definition = definition, current = 'text' )
    cleared = control.clear( )
    assert cleared.definition is definition


def test_830_clear_original_unchanged( ):
    ''' Original control is unchanged after clear(). '''
    definition = text.TextDefinition( )
    original = text.Text( definition = definition, current = 'original' )
    original.clear( )
    assert original.current == 'original'


def test_840_clear_with_count_min( ):
    ''' clear() with count_min constraint raises SizeConstraintViolation. '''
    definition = text.TextDefinition( count_min = 5 )
    control = definition.produce_control( initial = 'valid text' )
    with pytest.raises(
        exceptions.SizeConstraintViolation ):
        control.clear( )


# 900-999: Text.serialize()

def test_900_serialize_string( ):
    ''' Non-empty string serializes correctly. '''
    definition = text.TextDefinition( )
    control = text.Text( definition = definition, current = 'hello' )
    result = control.serialize( )
    assert result == 'hello'


def test_910_serialize_empty( ):
    ''' Empty string serializes correctly. '''
    definition = text.TextDefinition( )
    control = text.Text( definition = definition, current = '' )
    result = control.serialize( )
    assert result == ''


def test_920_serialize_delegates_to_definition( ):
    ''' serialize() delegates to definition.serialize_value(). '''
    definition = text.TextDefinition( )
    control = text.Text( definition = definition, current = 'test' )
    expected = definition.serialize_value( 'test' )
    result = control.serialize( )
    assert result == expected


# 1000-1099: Integration scenarios

def test_1000_complete_lifecycle( ):
    ''' Complete lifecycle: Create → validate → update → serialize. '''
    definition = text.TextDefinition( count_min = 3, count_max = 20 )
    validated = definition.validate_value( 'hello' )
    control = definition.produce_control( initial = validated )
    updated = control.copy( 'world' )
    serialized = updated.serialize( )
    assert serialized == 'world'


def test_1010_multiple_controls_same_definition( ):
    ''' Multiple controls share same definition. '''
    definition = text.TextDefinition( default = 'default' )
    control1 = definition.produce_control( )
    control2 = definition.produce_control( initial = 'custom' )
    assert control1.definition is control2.definition
    assert control1.definition is definition


def test_1020_controls_independent( ):
    ''' Modifying one control does not affect another. '''
    definition = text.TextDefinition( )
    control1 = definition.produce_control( initial = 'first' )
    control2 = definition.produce_control( initial = 'second' )
    modified = control1.copy( 'modified' )
    assert control1.current == 'first'
    assert control2.current == 'second'
    assert modified.current == 'modified'


def test_1030_protocol_compliance( ):
    ''' Text control implements required protocols. '''
    definition = text.TextDefinition( )
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
