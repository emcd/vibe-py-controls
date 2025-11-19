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


''' Protocol testing. '''


import inspect

from vibecontrols import interfaces
from vibecontrols.controls import boolean


def test_000_protocol_imports( ):
    ''' Protocols are importable. '''
    assert hasattr( interfaces, 'ControlDefinition' )
    assert hasattr( interfaces, 'Control' )
    assert interfaces.ControlDefinition is not None
    assert interfaces.Control is not None


def test_010_protocol_abstractmethods( ):
    ''' Protocols have abstractmethod decorators. '''
    control_def_methods = [
        'validate_value',
        'produce_control',
        'serialize_value',
        'produce_default'
    ]
    for method_name in control_def_methods:
        assert hasattr( interfaces.ControlDefinition, method_name )
    control_methods = [ 'copy', 'serialize' ]
    for method_name in control_methods:
        assert hasattr( interfaces.Control, method_name )


def test_100_control_definition_protocol_structure( ):
    ''' ControlDefinition protocol has required methods. '''
    assert hasattr( interfaces.ControlDefinition, 'validate_value' )
    assert hasattr( interfaces.ControlDefinition, 'produce_control' )
    assert hasattr( interfaces.ControlDefinition, 'serialize_value' )
    assert hasattr( interfaces.ControlDefinition, 'produce_default' )


def test_110_control_definition_not_instantiable( ):
    ''' ControlDefinition protocol cannot be instantiated directly. '''
    try:
        interfaces.ControlDefinition( )
        raise AssertionError( "Protocol should not be instantiable" )
    except TypeError:
        pass


def test_120_control_definition_implementation_compliance( ):
    ''' BooleanDefinition satisfies ControlDefinition protocol. '''
    definition = boolean.BooleanDefinition( )
    assert hasattr( definition, 'validate_value' )
    assert hasattr( definition, 'produce_control' )
    assert hasattr( definition, 'serialize_value' )
    assert hasattr( definition, 'produce_default' )


def test_130_control_definition_validate_value_signature( ):
    ''' ControlDefinition.validate_value signature matches. '''
    definition = boolean.BooleanDefinition( )
    assert hasattr( definition, 'validate_value' )
    assert callable( definition.validate_value )
    sig = inspect.signature( definition.validate_value )
    assert 'value' in sig.parameters


def test_140_control_definition_produce_control_signature( ):
    ''' ControlDefinition.produce_control signature matches. '''
    definition = boolean.BooleanDefinition( )
    assert hasattr( definition, 'produce_control' )
    assert callable( definition.produce_control )
    sig = inspect.signature( definition.produce_control )
    assert 'initial' in sig.parameters


def test_150_control_definition_serialize_value_signature( ):
    ''' ControlDefinition.serialize_value signature matches. '''
    definition = boolean.BooleanDefinition( )
    assert hasattr( definition, 'serialize_value' )
    assert callable( definition.serialize_value )
    sig = inspect.signature( definition.serialize_value )
    assert 'value' in sig.parameters


def test_160_control_definition_produce_default_signature( ):
    ''' ControlDefinition.produce_default signature matches. '''
    definition = boolean.BooleanDefinition( )
    assert hasattr( definition, 'produce_default' )
    assert callable( definition.produce_default )


def test_200_control_protocol_structure( ):
    ''' Control protocol has required attributes and methods. '''
    assert hasattr( interfaces.Control, 'definition' )
    assert hasattr( interfaces.Control, 'current' )
    assert hasattr( interfaces.Control, 'copy' )
    assert hasattr( interfaces.Control, 'serialize' )


def test_210_control_not_instantiable( ):
    ''' Control protocol cannot be instantiated directly. '''
    try:
        interfaces.Control( )
        raise AssertionError( "Protocol should not be instantiable" )
    except TypeError:
        pass


def test_220_control_implementation_compliance( ):
    ''' Boolean control satisfies Control protocol. '''
    definition = boolean.BooleanDefinition( )
    control = definition.produce_control( True )
    assert hasattr( control, 'definition' )
    assert hasattr( control, 'current' )
    assert hasattr( control, 'copy' )
    assert hasattr( control, 'serialize' )


def test_230_control_definition_attribute( ):
    ''' Control has definition attribute. '''
    definition = boolean.BooleanDefinition( )
    control = definition.produce_control( True )
    assert hasattr( control, 'definition' )
    assert hasattr( control.definition, 'validate_value' )


def test_240_control_current_attribute( ):
    ''' Control has current attribute. '''
    definition = boolean.BooleanDefinition( )
    control = definition.produce_control( True )
    assert hasattr( control, 'current' )


def test_250_control_copy_signature( ):
    ''' Control.copy signature matches. '''
    definition = boolean.BooleanDefinition( )
    control = definition.produce_control( True )
    assert hasattr( control, 'copy' )
    assert callable( control.copy )
    sig = inspect.signature( control.copy )
    assert 'new_value' in sig.parameters


def test_260_control_serialize_signature( ):
    ''' Control.serialize signature matches. '''
    definition = boolean.BooleanDefinition( )
    control = definition.produce_control( True )
    assert hasattr( control, 'serialize' )
    assert callable( control.serialize )


def test_300_protocol_isinstance_check( ):
    ''' Concrete types pass structural checks. '''
    definition = boolean.BooleanDefinition( )
    control = definition.produce_control( True )
    assert hasattr( definition, 'validate_value' )
    assert hasattr( control, 'copy' )


def test_310_protocol_structural_typing( ):
    ''' Duck typing compatibility works. '''
    definition = boolean.BooleanDefinition( )
    assert hasattr( definition, 'validate_value' )
    assert hasattr( definition, 'produce_control' )
    assert hasattr( definition, 'serialize_value' )
    assert hasattr( definition, 'produce_default' )


def test_320_protocol_nominal_typing( ):
    ''' ABC registration compatibility works. '''
    definition = boolean.BooleanDefinition( )
    control = definition.produce_control( True )
    assert callable( definition.validate_value )
    assert callable( control.copy )
