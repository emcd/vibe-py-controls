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


''' Boolean control testing. '''


import pytest

from vibecontrols import exceptions
from vibecontrols.controls import boolean


def test_000_boolean_hints_default_creation( ):
    ''' BooleanHints is created with defaults. '''
    hints = boolean.BooleanHints( )
    assert hints.widget_preference is None
    assert hints.label is None
    assert hints.help_text is None


def test_010_boolean_hints_with_widget( ):
    ''' BooleanHints is created with widget_preference. '''
    hints = boolean.BooleanHints( widget_preference = 'checkbox' )
    assert hints.widget_preference == 'checkbox'


def test_020_boolean_hints_with_label( ):
    ''' BooleanHints is created with label. '''
    hints = boolean.BooleanHints( label = 'Enable feature' )
    assert hints.label == 'Enable feature'


def test_030_boolean_hints_with_help( ):
    ''' BooleanHints is created with help_text. '''
    hints = boolean.BooleanHints( help_text = 'Toggle to enable' )
    assert hints.help_text == 'Toggle to enable'


def test_040_boolean_hints_all_fields( ):
    ''' BooleanHints is created with all fields. '''
    hints = boolean.BooleanHints(
        widget_preference = 'toggle',
        label = 'Feature toggle',
        help_text = 'Enable or disable feature'
    )
    assert hints.widget_preference == 'toggle'
    assert hints.label == 'Feature toggle'
    assert hints.help_text == 'Enable or disable feature'


def test_050_boolean_hints_immutability( ):
    ''' BooleanHints cannot be modified after creation. '''
    hints = boolean.BooleanHints( label = 'Original' )
    with pytest.raises( Exception ):
        hints.label = 'Modified'


def test_100_boolean_definition_default_creation( ):
    ''' BooleanDefinition is created with all defaults. '''
    definition = boolean.BooleanDefinition( )
    assert definition.default is False
    assert 'boolean' in definition.validation_message
    assert isinstance( definition.hints, boolean.BooleanHints )


def test_110_boolean_definition_custom_default( ):
    ''' BooleanDefinition is created with default=True. '''
    definition = boolean.BooleanDefinition( default = True )
    assert definition.default is True


def test_120_boolean_definition_custom_message( ):
    ''' BooleanDefinition is created with validation_message. '''
    definition = boolean.BooleanDefinition(
        validation_message = 'Custom validation error'
    )
    assert definition.validation_message == 'Custom validation error'


def test_130_boolean_definition_custom_hints( ):
    ''' BooleanDefinition is created with custom hints. '''
    hints = boolean.BooleanHints( label = 'Test label' )
    definition = boolean.BooleanDefinition( hints = hints )
    assert definition.hints.label == 'Test label'


def test_140_boolean_definition_all_parameters( ):
    ''' BooleanDefinition is created with all parameters. '''
    hints = boolean.BooleanHints(
        widget_preference = 'toggle', label = 'Enable'
    )
    definition = boolean.BooleanDefinition(
        default = True,
        validation_message = 'Must be boolean',
        hints = hints
    )
    assert definition.default is True
    assert definition.validation_message == 'Must be boolean'
    assert definition.hints.widget_preference == 'toggle'


def test_150_boolean_definition_immutability( ):
    ''' BooleanDefinition cannot be modified after creation. '''
    definition = boolean.BooleanDefinition( default = False )
    with pytest.raises( Exception ):
        definition.default = True


def test_200_validate_value_true( ):
    ''' BooleanDefinition validates True. '''
    definition = boolean.BooleanDefinition( )
    result = definition.validate_value( True )
    assert result is True


def test_210_validate_value_false( ):
    ''' BooleanDefinition validates False. '''
    definition = boolean.BooleanDefinition( )
    result = definition.validate_value( False )
    assert result is False


def test_220_validate_value_invalid_integer( ):
    ''' BooleanDefinition rejects integer (even 0/1). '''
    definition = boolean.BooleanDefinition( )
    with pytest.raises( exceptions.ControlInvalidity, match = 'boolean' ):
        definition.validate_value( 1 )
    with pytest.raises( exceptions.ControlInvalidity, match = 'boolean' ):
        definition.validate_value( 0 )


def test_230_validate_value_invalid_string( ):
    ''' BooleanDefinition rejects string "true"/"false". '''
    definition = boolean.BooleanDefinition( )
    with pytest.raises( exceptions.ControlInvalidity, match = 'boolean' ):
        definition.validate_value( 'true' )
    with pytest.raises( exceptions.ControlInvalidity, match = 'boolean' ):
        definition.validate_value( 'false' )


def test_240_validate_value_invalid_none( ):
    ''' BooleanDefinition rejects None. '''
    definition = boolean.BooleanDefinition( )
    with pytest.raises( exceptions.ControlInvalidity, match = 'boolean' ):
        definition.validate_value( None )


def test_250_validate_value_custom_message( ):
    ''' BooleanDefinition uses custom message in exception. '''
    definition = boolean.BooleanDefinition(
        validation_message = 'Custom error message'
    )
    with pytest.raises( exceptions.ControlInvalidity, match = 'Custom error' ):
        definition.validate_value( 'invalid' )


def test_260_validate_value_exception_type( ):
    ''' BooleanDefinition raises ControlInvalidity. '''
    definition = boolean.BooleanDefinition( )
    with pytest.raises( exceptions.ControlInvalidity ):
        definition.validate_value( [ ] )


def test_300_produce_control_no_initial( ):
    ''' BooleanDefinition uses default value when no initial provided. '''
    definition = boolean.BooleanDefinition( default = False )
    control = definition.produce_control( )
    assert control.current is False


def test_310_produce_control_initial_true( ):
    ''' BooleanDefinition sets initial to True. '''
    definition = boolean.BooleanDefinition( )
    control = definition.produce_control( initial = True )
    assert control.current is True


def test_320_produce_control_initial_false( ):
    ''' BooleanDefinition sets initial to False. '''
    definition = boolean.BooleanDefinition( default = True )
    control = definition.produce_control( initial = False )
    assert control.current is False


def test_330_produce_control_invalid_initial( ):
    ''' BooleanDefinition raises exception for invalid initial value. '''
    definition = boolean.BooleanDefinition( )
    with pytest.raises( exceptions.ControlInvalidity ):
        definition.produce_control( initial = 'not a bool' )


def test_340_produce_control_absent( ):
    ''' BooleanDefinition handles explicit absent by using default. '''
    from vibecontrols.controls import __
    definition = boolean.BooleanDefinition( default = True )
    control = definition.produce_control( initial = __.absent )
    assert control.current is True


def test_350_produce_control_returns_boolean( ):
    ''' BooleanDefinition returns Boolean control type. '''
    definition = boolean.BooleanDefinition( )
    control = definition.produce_control( True )
    assert isinstance( control, boolean.Boolean )


def test_360_produce_control_immutability( ):
    ''' BooleanDefinition is unchanged after producing control. '''
    definition = boolean.BooleanDefinition( default = False )
    original_default = definition.default
    _ = definition.produce_control( True )
    assert definition.default == original_default


def test_400_serialize_value_true( ):
    ''' BooleanDefinition serializes True as True. '''
    definition = boolean.BooleanDefinition( )
    result = definition.serialize_value( True )
    assert result is True


def test_410_serialize_value_false( ):
    ''' BooleanDefinition serializes False as False. '''
    definition = boolean.BooleanDefinition( )
    result = definition.serialize_value( False )
    assert result is False


def test_500_produce_default_false( ):
    ''' BooleanDefinition default is False. '''
    definition = boolean.BooleanDefinition( )
    default = definition.produce_default( )
    assert default is False


def test_510_produce_default_custom( ):
    ''' BooleanDefinition respects custom default. '''
    definition = boolean.BooleanDefinition( default = True )
    default = definition.produce_default( )
    assert default is True


def test_600_boolean_control_creation( ):
    ''' Boolean control is created with definition and current. '''
    definition = boolean.BooleanDefinition( )
    control = boolean.Boolean( definition = definition, current = True )
    assert control.definition is definition
    assert control.current is True


def test_610_boolean_control_definition_attribute( ):
    ''' Boolean control has definition attribute. '''
    definition = boolean.BooleanDefinition( )
    control = boolean.Boolean( definition = definition, current = False )
    assert hasattr( control, 'definition' )
    assert isinstance( control.definition, boolean.BooleanDefinition )


def test_620_boolean_control_current_attribute( ):
    ''' Boolean control has current attribute. '''
    definition = boolean.BooleanDefinition( )
    control = boolean.Boolean( definition = definition, current = True )
    assert hasattr( control, 'current' )
    assert control.current is True


def test_630_boolean_control_immutability( ):
    ''' Boolean control cannot modify attributes. '''
    definition = boolean.BooleanDefinition( )
    control = boolean.Boolean( definition = definition, current = True )
    with pytest.raises( Exception ):
        control.current = False


def test_700_copy_to_true( ):
    ''' Boolean.copy creates copy with new value True. '''
    definition = boolean.BooleanDefinition( )
    control = boolean.Boolean( definition = definition, current = False )
    new_control = control.copy( True )
    assert new_control.current is True


def test_710_copy_to_false( ):
    ''' Boolean.copy creates copy with new value False. '''
    definition = boolean.BooleanDefinition( )
    control = boolean.Boolean( definition = definition, current = True )
    new_control = control.copy( False )
    assert new_control.current is False


def test_720_copy_returns_new_instance( ):
    ''' Boolean.copy returns different instance. '''
    definition = boolean.BooleanDefinition( )
    control = boolean.Boolean( definition = definition, current = True )
    new_control = control.copy( False )
    assert new_control is not control
    assert id( new_control ) != id( control )


def test_730_copy_preserves_definition( ):
    ''' Boolean.copy preserves definition. '''
    definition = boolean.BooleanDefinition( )
    control = boolean.Boolean( definition = definition, current = True )
    new_control = control.copy( False )
    assert new_control.definition is control.definition


def test_740_copy_invalid_value( ):
    ''' Boolean.copy raises ControlInvalidity for invalid value. '''
    definition = boolean.BooleanDefinition( )
    control = boolean.Boolean( definition = definition, current = True )
    with pytest.raises( exceptions.ControlInvalidity ):
        control.copy( 'not a bool' )


def test_750_copy_original_unchanged( ):
    ''' Boolean.copy leaves original control unchanged (immutability). '''
    definition = boolean.BooleanDefinition( )
    control = boolean.Boolean( definition = definition, current = True )
    original_value = control.current
    _ = control.copy( False )
    assert control.current == original_value


def test_800_toggle_true_to_false( ):
    ''' Boolean.toggle changes True → False. '''
    definition = boolean.BooleanDefinition( )
    control = boolean.Boolean( definition = definition, current = True )
    toggled = control.toggle( )
    assert toggled.current is False


def test_810_toggle_false_to_true( ):
    ''' Boolean.toggle changes False → True. '''
    definition = boolean.BooleanDefinition( )
    control = boolean.Boolean( definition = definition, current = False )
    toggled = control.toggle( )
    assert toggled.current is True


def test_820_toggle_returns_new_instance( ):
    ''' Boolean.toggle returns different instance. '''
    definition = boolean.BooleanDefinition( )
    control = boolean.Boolean( definition = definition, current = True )
    toggled = control.toggle( )
    assert toggled is not control
    assert id( toggled ) != id( control )


def test_830_toggle_preserves_definition( ):
    ''' Boolean.toggle preserves definition. '''
    definition = boolean.BooleanDefinition( )
    control = boolean.Boolean( definition = definition, current = True )
    toggled = control.toggle( )
    assert toggled.definition is control.definition


def test_840_toggle_original_unchanged( ):
    ''' Boolean.toggle leaves original control unchanged. '''
    definition = boolean.BooleanDefinition( )
    control = boolean.Boolean( definition = definition, current = True )
    original_value = control.current
    _ = control.toggle( )
    assert control.current == original_value


def test_850_toggle_multiple_times( ):
    ''' Boolean.toggle can be chained multiple times. '''
    definition = boolean.BooleanDefinition( )
    control = boolean.Boolean( definition = definition, current = False )
    toggled_once = control.toggle( )
    assert toggled_once.current is True
    toggled_twice = toggled_once.toggle( )
    assert toggled_twice.current is False
    toggled_thrice = toggled_twice.toggle( )
    assert toggled_thrice.current is True


def test_900_serialize_true( ):
    ''' Boolean.serialize serializes True. '''
    definition = boolean.BooleanDefinition( )
    control = boolean.Boolean( definition = definition, current = True )
    serialized = control.serialize( )
    assert serialized is True


def test_910_serialize_false( ):
    ''' Boolean.serialize serializes False. '''
    definition = boolean.BooleanDefinition( )
    control = boolean.Boolean( definition = definition, current = False )
    serialized = control.serialize( )
    assert serialized is False


def test_920_serialize_delegates_to_definition( ):
    ''' Boolean.serialize uses definition.serialize_value(). '''
    definition = boolean.BooleanDefinition( )
    control = boolean.Boolean( definition = definition, current = True )
    result = control.serialize( )
    expected = definition.serialize_value( control.current )
    assert result == expected


def test_1000_complete_lifecycle( ):
    ''' Complete lifecycle: Create → validate → update → serialize. '''
    definition = boolean.BooleanDefinition( default = False )
    control = definition.produce_control( )
    assert control.current is False
    updated = control.copy( True )
    assert updated.current is True
    serialized = updated.serialize( )
    assert serialized is True


def test_1010_multiple_controls_same_definition( ):
    ''' Same definition can be shared across controls. '''
    definition = boolean.BooleanDefinition( )
    control1 = definition.produce_control( True )
    control2 = definition.produce_control( False )
    assert control1.definition is control2.definition
    assert control1.current is True
    assert control2.current is False


def test_1020_controls_independent( ):
    ''' Modifying one control does not affect another. '''
    definition = boolean.BooleanDefinition( )
    control1 = definition.produce_control( True )
    control2 = definition.produce_control( False )
    modified = control1.copy( False )
    assert control1.current is True
    assert control2.current is False
    assert modified.current is False


def test_1030_protocol_compliance( ):
    ''' Boolean implements Control and ControlDefinition protocols. '''
    definition = boolean.BooleanDefinition( )
    control = definition.produce_control( True )
    assert hasattr( definition, 'validate_value' )
    assert hasattr( definition, 'produce_control' )
    assert hasattr( control, 'definition' )
    assert hasattr( control, 'current' )
    assert hasattr( control, 'copy' )
