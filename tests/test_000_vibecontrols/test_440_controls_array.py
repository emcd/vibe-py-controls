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


''' Test suite for Array control. '''


import pytest
from absence import absent

from frigid import exceptions as frigid_exceptions

from vibecontrols import exceptions
from vibecontrols.controls import array, boolean


# 000-099: ArrayHints dataclass

def test_000_array_hints_default_creation( ):
    ''' ArrayHints is created with defaults. '''
    hints = array.ArrayHints( )
    assert hints.orientation == 'vertical'
    assert hints.collapsible is False
    assert hints.initially_collapsed is False
    assert hints.border is False
    assert hints.title is None
    assert hints.label is None
    assert hints.help_text is None


def test_010_array_hints_with_vertical( ):
    ''' ArrayHints is created with orientation (vertical). '''
    hints = array.ArrayHints( orientation = 'vertical' )
    assert hints.orientation == 'vertical'


def test_015_array_hints_with_horizontal( ):
    ''' ArrayHints is created with orientation (horizontal). '''
    hints = array.ArrayHints( orientation = 'horizontal' )
    assert hints.orientation == 'horizontal'


def test_020_array_hints_with_grid( ):
    ''' ArrayHints is created with orientation (grid). '''
    hints = array.ArrayHints( orientation = 'grid' )
    assert hints.orientation == 'grid'


def test_030_array_hints_with_collapsible( ):
    ''' ArrayHints is created with collapsible flag. '''
    hints = array.ArrayHints( collapsible = True )
    assert hints.collapsible is True


def test_040_array_hints_with_initially_collapsed( ):
    ''' ArrayHints is created with initially_collapsed flag. '''
    hints = array.ArrayHints( initially_collapsed = True )
    assert hints.initially_collapsed is True


def test_050_array_hints_with_border( ):
    ''' ArrayHints is created with border flag. '''
    hints = array.ArrayHints( border = True )
    assert hints.border is True


def test_060_array_hints_with_title( ):
    ''' ArrayHints is created with title. '''
    hints = array.ArrayHints( title = 'Items' )
    assert hints.title == 'Items'


def test_070_array_hints_with_label( ):
    ''' ArrayHints is created with label. '''
    hints = array.ArrayHints( label = 'Elements' )
    assert hints.label == 'Elements'


def test_080_array_hints_with_help( ):
    ''' ArrayHints is created with help_text. '''
    hints = array.ArrayHints( help_text = 'Manage items' )
    assert hints.help_text == 'Manage items'


def test_090_array_hints_all_fields( ):
    ''' ArrayHints is created with all fields together. '''
    hints = array.ArrayHints(
        orientation = 'grid',
        collapsible = True,
        initially_collapsed = True,
        border = True,
        title = 'My Items',
        label = 'Items',
        help_text = 'Add or remove items' )
    assert hints.orientation == 'grid'
    assert hints.collapsible is True
    assert hints.initially_collapsed is True
    assert hints.border is True
    assert hints.title == 'My Items'
    assert hints.label == 'Items'
    assert hints.help_text == 'Add or remove items'


def test_095_array_hints_immutability( ):
    ''' ArrayHints cannot be modified after creation. '''
    hints = array.ArrayHints( title = 'Original' )
    with pytest.raises( frigid_exceptions.AttributeImmutability ):
        hints.title = 'Modified'


# 100-199: ArrayDefinition creation and configuration

def test_100_array_definition_simple_elements( ):
    ''' ArrayDefinition is created with simple element type (Boolean). '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition( element_definition = element_def )
    assert definition.element_definition is element_def
    assert definition.size_min == 0
    assert definition.size_max is None
    assert definition.default_elements == ( )
    assert definition.allow_duplicates is True


def test_110_array_definition_with_size_min( ):
    ''' ArrayDefinition is created with size_min constraint. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition(
        element_definition = element_def,
        size_min = 2,
        default_elements = [ True, False ] )
    assert definition.size_min == 2


def test_120_array_definition_with_size_max( ):
    ''' ArrayDefinition is created with size_max constraint. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition(
        element_definition = element_def, size_max = 10 )
    assert definition.size_max == 10


def test_130_array_definition_with_both_sizes( ):
    ''' ArrayDefinition is created with both size_min and size_max. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition(
        element_definition = element_def,
        size_min = 2,
        size_max = 10,
        default_elements = [ True, False ] )
    assert definition.size_min == 2
    assert definition.size_max == 10


def test_140_array_definition_fixed_size( ):
    ''' ArrayDefinition is created with fixed size (size_min == size_max). '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition(
        element_definition = element_def, size_min = 5, size_max = 5,
        default_elements = [ True, False, True, False, True ] )
    assert definition.size_min == 5
    assert definition.size_max == 5


def test_150_array_definition_with_default_elements( ):
    ''' ArrayDefinition is created with default_elements. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition(
        element_definition = element_def,
        default_elements = [ True, False, True ] )
    assert definition.default_elements == ( True, False, True )


def test_160_array_definition_allow_duplicates_false( ):
    ''' ArrayDefinition is created with allow_duplicates=False. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition(
        element_definition = element_def, allow_duplicates = False )
    assert definition.allow_duplicates is False


def test_170_array_definition_custom_hints( ):
    ''' ArrayDefinition is created with custom hints. '''
    element_def = boolean.BooleanDefinition( )
    hints = array.ArrayHints( orientation = 'horizontal' )
    definition = array.ArrayDefinition(
        element_definition = element_def, hints = hints )
    assert definition.hints is hints


def test_180_array_definition_all_parameters( ):
    ''' ArrayDefinition is created with all parameters. '''
    element_def = boolean.BooleanDefinition( )
    hints = array.ArrayHints( border = True )
    definition = array.ArrayDefinition(
        element_definition = element_def,
        size_min = 1,
        size_max = 5,
        default_elements = [ True ],
        allow_duplicates = False,
        hints = hints )
    assert definition.size_min == 1
    assert definition.size_max == 5
    assert definition.allow_duplicates is False
    assert definition.hints is hints


def test_190_array_definition_immutability( ):
    ''' ArrayDefinition cannot be modified after creation. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition( element_definition = element_def )
    with pytest.raises( frigid_exceptions.AttributeImmutability ):
        definition.size_min = 5


def test_191_array_definition_invalid_negative_size_min( ):
    ''' Negative size_min raises DefinitionInvalidity. '''
    element_def = boolean.BooleanDefinition( )
    with pytest.raises(
        exceptions.DefinitionInvalidity,
        match = 'size_min' ):
        array.ArrayDefinition(
            element_definition = element_def, size_min = -1 )


def test_192_array_definition_invalid_negative_size_max( ):
    ''' Negative size_max raises DefinitionInvalidity. '''
    element_def = boolean.BooleanDefinition( )
    with pytest.raises(
        exceptions.DefinitionInvalidity,
        match = 'size_max' ):
        array.ArrayDefinition(
            element_definition = element_def, size_max = -5 )


def test_193_array_definition_invalid_min_exceeds_max( ):
    ''' size_min > size_max raises DefinitionInvalidity. '''
    element_def = boolean.BooleanDefinition( )
    with pytest.raises(
        exceptions.DefinitionInvalidity,
        match = 'size_min' ):
        array.ArrayDefinition(
            element_definition = element_def, size_min = 10, size_max = 5 )


def test_194_array_definition_invalid_default_below_min( ):
    ''' len(default_elements) < size_min raises DefinitionInvalidity. '''
    element_def = boolean.BooleanDefinition( )
    with pytest.raises( exceptions.DefinitionInvalidity ):
        array.ArrayDefinition(
            element_definition = element_def,
            size_min = 3,
            default_elements = [ True ] )


def test_195_array_definition_invalid_default_above_max( ):
    ''' len(default_elements) > size_max raises DefinitionInvalidity. '''
    element_def = boolean.BooleanDefinition( )
    with pytest.raises( exceptions.DefinitionInvalidity ):
        array.ArrayDefinition(
            element_definition = element_def,
            size_max = 2,
            default_elements = [ True, False, True ] )


# 200-299: ArrayDefinition.validate_value()

def test_200_validate_value_valid_array( ):
    ''' Valid array of elements passes validation. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition( element_definition = element_def )
    result = definition.validate_value( [ True, False, True ] )
    assert result == ( True, False, True )


def test_210_validate_value_empty_array( ):
    ''' Empty array is valid when size_min=0. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition( element_definition = element_def )
    result = definition.validate_value( [ ] )
    assert result == ( )


def test_220_validate_value_single_element( ):
    ''' Single element array passes validation. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition( element_definition = element_def )
    result = definition.validate_value( [ True ] )
    assert result == ( True, )


def test_230_validate_value_at_size_min( ):
    ''' Array exactly at size_min boundary passes validation. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition(
        element_definition = element_def,
        size_min = 2,
        default_elements = [ True, False ] )
    result = definition.validate_value( [ True, False ] )
    assert result == ( True, False )


def test_240_validate_value_at_size_max( ):
    ''' Array exactly at size_max boundary passes validation. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition(
        element_definition = element_def, size_max = 3 )
    result = definition.validate_value( [ True, False, True ] )
    assert result == ( True, False, True )


def test_250_validate_value_below_size_min( ):
    ''' Array below size_min raises SizeConstraintViolation. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition(
        element_definition = element_def, size_min = 3,
        default_elements = [ True, False, True ] )
    with pytest.raises( exceptions.SizeConstraintViolation ):
        definition.validate_value( [ True ] )


def test_260_validate_value_above_size_max( ):
    ''' Array above size_max raises SizeConstraintViolation. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition(
        element_definition = element_def, size_max = 2 )
    with pytest.raises( exceptions.SizeConstraintViolation ):
        definition.validate_value( [ True, False, True ] )


def test_270_validate_value_invalid_element_type( ):
    ''' Wrong element type raises ElementInvalidity. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition( element_definition = element_def )
    with pytest.raises( exceptions.ElementInvalidity ):
        definition.validate_value( [ True, 'not a bool' ] )


def test_280_validate_value_element_constraint_violation( ):
    ''' Element constraint violation raises ElementInvalidity. '''
    from vibecontrols.controls import text
    element_def = text.TextDefinition( count_min = 5 )
    definition = array.ArrayDefinition( element_definition = element_def )
    with pytest.raises( exceptions.ElementInvalidity ):
        definition.validate_value( [ 'valid text', 'no' ] )


def test_290_validate_value_with_duplicates_allowed( ):
    ''' Duplicates are valid when allow_duplicates=True. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition(
        element_definition = element_def, allow_duplicates = True )
    result = definition.validate_value( [ True, True, False ] )
    assert result == ( True, True, False )


def test_291_validate_value_with_duplicates_disallowed( ):
    ''' Duplicates raise UniquenessConstraintViolation when disallowed. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition(
        element_definition = element_def, allow_duplicates = False )
    with pytest.raises( exceptions.UniquenessConstraintViolation ):
        definition.validate_value( [ True, False, True ] )


def test_292_validate_value_invalid_not_sequence( ):
    ''' Non-sequence raises TypeInvalidity. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition( element_definition = element_def )
    with pytest.raises( exceptions.TypeInvalidity ):
        definition.validate_value( 42 )


def test_293_validate_value_tuple_sequence( ):
    ''' Tuple input is valid and converted to tuple internally. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition( element_definition = element_def )
    result = definition.validate_value( ( True, False ) )
    assert result == ( True, False )


def test_294_validate_value_list_sequence( ):
    ''' List input is valid and converted to tuple. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition( element_definition = element_def )
    result = definition.validate_value( [ True, False ] )
    assert result == ( True, False )
    assert isinstance( result, tuple )


# 300-399: ArrayDefinition.produce_control()

def test_300_produce_control_no_initial( ):
    ''' Control is produced with default_elements when no initial provided. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition(
        element_definition = element_def,
        default_elements = [ True, False ] )
    control = definition.produce_control( )
    assert control.current == ( True, False )


def test_310_produce_control_initial_valid( ):
    ''' Control is produced with valid initial array. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition( element_definition = element_def )
    control = definition.produce_control( initial = [ True, True ] )
    assert control.current == ( True, True )


def test_320_produce_control_initial_empty( ):
    ''' Control is produced with empty initial array. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition( element_definition = element_def )
    control = definition.produce_control( initial = [ ] )
    assert control.current == ( )


def test_330_produce_control_invalid_initial( ):
    ''' Invalid initial value raises exception. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition(
        element_definition = element_def,
        size_min = 2,
        default_elements = [ True, False ] )
    with pytest.raises( exceptions.ControlInvalidity ):
        definition.produce_control( initial = [ True ] )


def test_340_produce_control_absent( ):
    ''' Explicit absent uses default_elements. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition(
        element_definition = element_def,
        default_elements = [ False ] )
    control = definition.produce_control( initial = absent )
    assert control.current == ( False, )


def test_350_produce_control_returns_array( ):
    ''' produce_control returns Array control type. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition( element_definition = element_def )
    control = definition.produce_control( )
    assert isinstance( control, array.Array )


def test_360_produce_control_immutability( ):
    ''' Definition is unchanged after control production. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition(
        element_definition = element_def,
        default_elements = [ True ] )
    control = definition.produce_control( )
    assert definition.default_elements == ( True, )
    assert control.current == ( True, )


# 400-499: ArrayDefinition.serialize_value()

def test_400_serialize_value_array( ):
    ''' Array serializes as list. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition( element_definition = element_def )
    result = definition.serialize_value( ( True, False, True ) )
    assert result == [ True, False, True ]


def test_410_serialize_value_empty( ):
    ''' Empty array serializes as empty list. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition( element_definition = element_def )
    result = definition.serialize_value( ( ) )
    assert result == [ ]


def test_420_serialize_value_nested( ):
    ''' Nested array serializes recursively. '''
    inner_def = boolean.BooleanDefinition( )
    outer_def = array.ArrayDefinition( element_definition = inner_def )
    nested_def = array.ArrayDefinition( element_definition = outer_def )
    result = nested_def.serialize_value( ( ( True, False ), ( True, ) ) )
    assert result == [ [ True, False ], [ True ] ]


def test_430_serialize_value_preserves_order( ):
    ''' Order is preserved in serialization. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition( element_definition = element_def )
    result = definition.serialize_value( ( False, True, False, True ) )
    assert result == [ False, True, False, True ]


# 500-599: ArrayDefinition.produce_default()

def test_500_produce_default_empty( ):
    ''' Default is empty tuple when not specified. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition( element_definition = element_def )
    result = definition.produce_default( )
    assert result == ( )


def test_510_produce_default_with_elements( ):
    ''' Default elements are respected. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition(
        element_definition = element_def,
        default_elements = [ True, False ] )
    result = definition.produce_default( )
    assert result == ( True, False )


# 600-699: Array control creation and attributes

def test_600_array_control_creation( ):
    ''' Array control is created with definition and current. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition( element_definition = element_def )
    control = array.Array(
        definition = definition, current = ( True, False ) )
    assert control.definition is definition
    assert control.current == ( True, False )


def test_610_array_control_definition_attribute( ):
    ''' Array control has definition attribute. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition( element_definition = element_def )
    control = array.Array( definition = definition, current = ( ) )
    assert hasattr( control, 'definition' )
    assert control.definition is definition


def test_620_array_control_current_attribute( ):
    ''' Array control has current attribute (tuple). '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition( element_definition = element_def )
    control = array.Array( definition = definition, current = ( True, ) )
    assert hasattr( control, 'current' )
    assert control.current == ( True, )
    assert isinstance( control.current, tuple )


def test_630_array_control_immutability( ):
    ''' Array control attributes cannot be modified. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition( element_definition = element_def )
    control = array.Array( definition = definition, current = ( True, ) )
    with pytest.raises( frigid_exceptions.AttributeImmutability ):
        control.current = ( False, )


# 700-799: Array.copy()

def test_700_copy_to_new_array( ):
    ''' Control is copied with new array value. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition( element_definition = element_def )
    original = array.Array( definition = definition, current = ( True, ) )
    copied = original.copy( [ False, True ] )
    assert copied.current == ( False, True )
    assert original.current == ( True, )


def test_710_copy_to_empty( ):
    ''' Control is copied to empty array. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition( element_definition = element_def )
    control = array.Array(
        definition = definition, current = ( True, False ) )
    copied = control.copy( [ ] )
    assert copied.current == ( )


def test_720_copy_returns_new_instance( ):
    ''' copy() returns a different instance. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition( element_definition = element_def )
    original = array.Array( definition = definition, current = ( ) )
    copied = original.copy( [ True ] )
    assert id( original ) != id( copied )


def test_730_copy_preserves_definition( ):
    ''' copy() preserves definition reference. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition( element_definition = element_def )
    original = array.Array( definition = definition, current = ( ) )
    copied = original.copy( [ True ] )
    assert copied.definition is definition


def test_740_copy_invalid_value( ):
    ''' Copying with invalid value raises ControlInvalidity. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition(
        element_definition = element_def,
        size_min = 2,
        default_elements = [ True, False ] )
    control = array.Array(
        definition = definition, current = ( True, False ) )
    with pytest.raises( exceptions.ControlInvalidity ):
        control.copy( [ True ] )


def test_750_copy_original_unchanged( ):
    ''' Original control is unchanged after copy. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition( element_definition = element_def )
    original = array.Array( definition = definition, current = ( True, ) )
    original.copy( [ False ] )
    assert original.current == ( True, )


# 800-899: Array.append()

def test_800_append_valid_element( ):
    ''' Element is successfully appended. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition( element_definition = element_def )
    control = array.Array( definition = definition, current = ( True, ) )
    appended = control.append( False )
    assert appended.current == ( True, False )


def test_810_append_at_size_max( ):
    ''' Append at size_max raises SizeConstraintViolation. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition(
        element_definition = element_def, size_max = 2 )
    control = array.Array(
        definition = definition, current = ( True, False ) )
    with pytest.raises( exceptions.SizeConstraintViolation ):
        control.append( True )


def test_820_append_invalid_element( ):
    ''' Invalid element raises ControlInvalidity. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition( element_definition = element_def )
    control = array.Array( definition = definition, current = ( ) )
    with pytest.raises( exceptions.ControlInvalidity ):
        control.append( 'not a bool' )


def test_830_append_returns_new_instance( ):
    ''' append() returns a different instance. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition( element_definition = element_def )
    original = array.Array( definition = definition, current = ( ) )
    appended = original.append( True )
    assert id( original ) != id( appended )


def test_840_append_preserves_definition( ):
    ''' append() preserves definition reference. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition( element_definition = element_def )
    control = array.Array( definition = definition, current = ( ) )
    appended = control.append( True )
    assert appended.definition is definition


def test_850_append_original_unchanged( ):
    ''' Original array is unchanged after append. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition( element_definition = element_def )
    original = array.Array( definition = definition, current = ( True, ) )
    original.append( False )
    assert original.current == ( True, )


# 900-999: Array.remove_at()

def test_900_remove_at_valid_index( ):
    ''' Element is successfully removed. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition( element_definition = element_def )
    control = array.Array(
        definition = definition, current = ( True, False, True ) )
    removed = control.remove_at( 1 )
    assert removed.current == ( True, True )


def test_910_remove_at_first( ):
    ''' First element (index 0) is removed. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition( element_definition = element_def )
    control = array.Array(
        definition = definition, current = ( True, False ) )
    removed = control.remove_at( 0 )
    assert removed.current == ( False, )


def test_920_remove_at_last( ):
    ''' Last element is removed. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition( element_definition = element_def )
    control = array.Array(
        definition = definition, current = ( True, False, True ) )
    removed = control.remove_at( 2 )
    assert removed.current == ( True, False )


def test_930_remove_at_size_min( ):
    ''' Remove at size_min raises SizeConstraintViolation. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition(
        element_definition = element_def,
        size_min = 2,
        default_elements = [ True, False ] )
    control = array.Array(
        definition = definition, current = ( True, False ) )
    with pytest.raises( exceptions.SizeConstraintViolation ):
        control.remove_at( 0 )


def test_940_remove_at_invalid_negative_index( ):
    ''' Negative index raises IndexOutOfRange. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition( element_definition = element_def )
    control = array.Array( definition = definition, current = ( True, ) )
    with pytest.raises( exceptions.IndexOutOfRange ):
        control.remove_at( -1 )


def test_950_remove_at_invalid_beyond_length( ):
    ''' Index >= length raises IndexOutOfRange. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition( element_definition = element_def )
    control = array.Array(
        definition = definition, current = ( True, False ) )
    with pytest.raises( exceptions.IndexOutOfRange ):
        control.remove_at( 2 )


def test_960_remove_at_returns_new_instance( ):
    ''' remove_at() returns a different instance. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition( element_definition = element_def )
    original = array.Array(
        definition = definition, current = ( True, False ) )
    removed = original.remove_at( 0 )
    assert id( original ) != id( removed )


def test_970_remove_at_preserves_definition( ):
    ''' remove_at() preserves definition reference. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition( element_definition = element_def )
    control = array.Array(
        definition = definition, current = ( True, False ) )
    removed = control.remove_at( 0 )
    assert removed.definition is definition


def test_980_remove_at_original_unchanged( ):
    ''' Original array is unchanged after remove_at. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition( element_definition = element_def )
    original = array.Array(
        definition = definition, current = ( True, False ) )
    original.remove_at( 0 )
    assert original.current == ( True, False )


# 1000-1099: Array.insert_at()

def test_1000_insert_at_beginning( ):
    ''' Element is inserted at index 0. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition( element_definition = element_def )
    control = array.Array(
        definition = definition, current = ( False, True ) )
    inserted = control.insert_at( 0, True )
    assert inserted.current == ( True, False, True )


def test_1010_insert_at_middle( ):
    ''' Element is inserted at middle index. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition( element_definition = element_def )
    control = array.Array(
        definition = definition, current = ( True, True ) )
    inserted = control.insert_at( 1, False )
    assert inserted.current == ( True, False, True )


def test_1020_insert_at_end( ):
    ''' Element is inserted at end (equivalent to append). '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition( element_definition = element_def )
    control = array.Array( definition = definition, current = ( True, ) )
    inserted = control.insert_at( 1, False )
    assert inserted.current == ( True, False )


def test_1030_insert_at_size_max( ):
    ''' Insert at size_max raises SizeConstraintViolation. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition(
        element_definition = element_def, size_max = 2 )
    control = array.Array(
        definition = definition, current = ( True, False ) )
    with pytest.raises( exceptions.SizeConstraintViolation ):
        control.insert_at( 0, True )


def test_1040_insert_at_invalid_element( ):
    ''' Invalid element raises ControlInvalidity. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition( element_definition = element_def )
    control = array.Array( definition = definition, current = ( ) )
    with pytest.raises( exceptions.ControlInvalidity ):
        control.insert_at( 0, 'invalid' )


def test_1050_insert_at_invalid_index( ):
    ''' Invalid index raises IndexOutOfRange. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition( element_definition = element_def )
    control = array.Array( definition = definition, current = ( True, ) )
    with pytest.raises( exceptions.IndexOutOfRange ):
        control.insert_at( 3, False )


def test_1060_insert_at_returns_new_instance( ):
    ''' insert_at() returns a different instance. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition( element_definition = element_def )
    original = array.Array( definition = definition, current = ( ) )
    inserted = original.insert_at( 0, True )
    assert id( original ) != id( inserted )


def test_1070_insert_at_preserves_definition( ):
    ''' insert_at() preserves definition reference. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition( element_definition = element_def )
    control = array.Array( definition = definition, current = ( ) )
    inserted = control.insert_at( 0, True )
    assert inserted.definition is definition


def test_1080_insert_at_original_unchanged( ):
    ''' Original array is unchanged after insert_at. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition( element_definition = element_def )
    original = array.Array( definition = definition, current = ( True, ) )
    original.insert_at( 0, False )
    assert original.current == ( True, )


# 1100-1199: Array.reorder()

def test_1100_reorder_valid_permutation( ):
    ''' Elements are reordered with valid permutation. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition( element_definition = element_def )
    control = array.Array(
        definition = definition, current = ( True, False, True ) )
    reordered = control.reorder( [ 2, 0, 1 ] )
    assert reordered.current == ( True, True, False )


def test_1110_reorder_reverse( ):
    ''' Elements are reversed. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition( element_definition = element_def )
    control = array.Array(
        definition = definition, current = ( True, False, True ) )
    reordered = control.reorder( [ 2, 1, 0 ] )
    assert reordered.current == ( True, False, True )


def test_1120_reorder_partial_swap( ):
    ''' Two elements are swapped. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition( element_definition = element_def )
    control = array.Array(
        definition = definition, current = ( True, False, True ) )
    reordered = control.reorder( [ 1, 0, 2 ] )
    assert reordered.current == ( False, True, True )


def test_1130_reorder_no_change( ):
    ''' Same order (identity permutation). '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition( element_definition = element_def )
    control = array.Array(
        definition = definition, current = ( True, False ) )
    reordered = control.reorder( [ 0, 1 ] )
    assert reordered.current == ( True, False )


def test_1140_reorder_invalid_wrong_count( ):
    ''' Wrong number of indices raises InvalidPermutation. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition( element_definition = element_def )
    control = array.Array(
        definition = definition, current = ( True, False ) )
    with pytest.raises( exceptions.InvalidPermutation ):
        control.reorder( [ 0 ] )


def test_1150_reorder_invalid_out_of_range( ):
    ''' Index out of range raises InvalidPermutation. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition( element_definition = element_def )
    control = array.Array(
        definition = definition, current = ( True, False ) )
    with pytest.raises( exceptions.InvalidPermutation ):
        control.reorder( [ 0, 5 ] )


def test_1160_reorder_invalid_duplicates( ):
    ''' Duplicate indices raise InvalidPermutation. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition( element_definition = element_def )
    control = array.Array(
        definition = definition, current = ( True, False, True ) )
    with pytest.raises( exceptions.InvalidPermutation ):
        control.reorder( [ 0, 0, 1 ] )


def test_1170_reorder_returns_new_instance( ):
    ''' reorder() returns a different instance. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition( element_definition = element_def )
    original = array.Array(
        definition = definition, current = ( True, False ) )
    reordered = original.reorder( [ 1, 0 ] )
    assert id( original ) != id( reordered )


def test_1180_reorder_preserves_definition( ):
    ''' reorder() preserves definition reference. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition( element_definition = element_def )
    control = array.Array(
        definition = definition, current = ( True, False ) )
    reordered = control.reorder( [ 1, 0 ] )
    assert reordered.definition is definition


def test_1190_reorder_original_unchanged( ):
    ''' Original array is unchanged after reorder. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition( element_definition = element_def )
    original = array.Array(
        definition = definition, current = ( True, False ) )
    original.reorder( [ 1, 0 ] )
    assert original.current == ( True, False )


# 1200-1299: Array.serialize()

def test_1200_serialize_simple_elements( ):
    ''' Array of simple elements serializes correctly. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition( element_definition = element_def )
    control = array.Array(
        definition = definition, current = ( True, False, True ) )
    result = control.serialize( )
    assert result == [ True, False, True ]


def test_1210_serialize_nested_arrays( ):
    ''' Nested arrays serialize correctly. '''
    inner_def = boolean.BooleanDefinition( )
    outer_def = array.ArrayDefinition( element_definition = inner_def )
    nested_def = array.ArrayDefinition( element_definition = outer_def )
    control = array.Array(
        definition = nested_def, current = ( ( True, False ), ( True, ) ) )
    result = control.serialize( )
    assert result == [ [ True, False ], [ True ] ]


def test_1220_serialize_delegates_to_definition( ):
    ''' serialize() delegates to definition.serialize_value(). '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition( element_definition = element_def )
    control = array.Array(
        definition = definition, current = ( True, False ) )
    expected = definition.serialize_value( ( True, False ) )
    result = control.serialize( )
    assert result == expected


# 1300-1399: Integration scenarios

def test_1300_complete_lifecycle( ):
    ''' Complete lifecycle: Create → validate → update → serialize. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition(
        element_definition = element_def,
        size_min = 1,
        size_max = 5,
        default_elements = [ True ] )
    validated = definition.validate_value( [ True, False ] )
    control = definition.produce_control( initial = validated )
    updated = control.append( True )
    serialized = updated.serialize( )
    assert serialized == [ True, False, True ]


def test_1310_multiple_controls_same_definition( ):
    ''' Multiple controls share same definition. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition( element_definition = element_def )
    control1 = definition.produce_control( )
    control2 = definition.produce_control( initial = [ True ] )
    assert control1.definition is control2.definition
    assert control1.definition is definition


def test_1320_controls_independent( ):
    ''' Modifying one control does not affect another. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition( element_definition = element_def )
    control1 = definition.produce_control( initial = [ True ] )
    control2 = definition.produce_control( initial = [ False ] )
    modified = control1.append( False )
    assert control1.current == ( True, )
    assert control2.current == ( False, )
    assert modified.current == ( True, False )


def test_1330_protocol_compliance( ):
    ''' Array control implements required protocols. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition( element_definition = element_def )
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


def test_1340_nested_single_level( ):
    ''' Array of Arrays (single nesting). '''
    inner_def = boolean.BooleanDefinition( )
    inner_array_def = array.ArrayDefinition( element_definition = inner_def )
    outer_def = array.ArrayDefinition( element_definition = inner_array_def )
    control = outer_def.produce_control(
        initial = [ [ True, False ], [ True ] ] )
    assert control.current == ( ( True, False ), ( True, ) )


def test_1350_nested_multiple_levels( ):
    ''' Array of Arrays of Arrays (deep nesting). '''
    bool_def = boolean.BooleanDefinition( )
    level1_def = array.ArrayDefinition( element_definition = bool_def )
    level2_def = array.ArrayDefinition( element_definition = level1_def )
    level3_def = array.ArrayDefinition( element_definition = level2_def )
    control = level3_def.produce_control(
        initial = [ [ [ True ], [ False ] ], [ [ True, False ] ] ] )
    assert control.current == (
        ( ( True, ), ( False, ) ), ( ( True, False ), ) )


def test_1360_mixed_operations_chain( ):
    ''' Chain append, remove, insert, reorder operations. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition( element_definition = element_def )
    control = definition.produce_control( initial = [ True ] )
    result = (
        control.append( False )
        .append( True )
        .remove_at( 0 )
        .insert_at( 0, True )
        .reorder( [ 1, 0, 2 ] ) )
    assert result.current == ( False, True, True )


def test_1370_size_constraint_interactions( ):
    ''' Size constraints with all operations. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition(
        element_definition = element_def,
        size_min = 1,
        size_max = 3,
        default_elements = [ True ] )
    control = definition.produce_control( initial = [ True, False ] )
    # Can append up to max
    appended = control.append( True )
    assert len( appended.current ) == 3
    # Cannot append beyond max
    with pytest.raises( exceptions.SizeConstraintViolation ):
        appended.append( False )
    # Can remove down to min
    removed = appended.remove_at( 0 ).remove_at( 0 )
    assert len( removed.current ) == 1
    # Cannot remove below min
    with pytest.raises( exceptions.SizeConstraintViolation ):
        removed.remove_at( 0 )


def test_1380_duplicate_detection( ):
    ''' Duplicate handling when allow_duplicates=False. '''
    element_def = boolean.BooleanDefinition( )
    definition = array.ArrayDefinition(
        element_definition = element_def, allow_duplicates = False )
    control = definition.produce_control( initial = [ True, False ] )
    # Cannot add duplicate
    with pytest.raises( exceptions.UniquenessConstraintViolation ):
        control.append( True )
