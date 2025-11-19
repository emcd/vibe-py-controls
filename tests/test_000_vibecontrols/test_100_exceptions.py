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


''' Exception hierarchy testing. '''


import pytest

from vibecontrols import exceptions


def test_000_exception_hierarchy( ):
    ''' Exception hierarchy is correctly structured. '''
    assert issubclass( exceptions.Omnierror, exceptions.Omniexception )
    assert issubclass( exceptions.ControlError, exceptions.Omnierror )
    assert issubclass( exceptions.ControlInvalidity, exceptions.ControlError )
    assert issubclass(
        exceptions.ConstraintViolation, exceptions.ControlInvalidity
    )
    assert issubclass(
        exceptions.DefinitionInvalidity, exceptions.ControlError
    )


def test_010_exception_instantiation( ):
    ''' All exception types can be instantiated. '''
    exc1 = exceptions.Omniexception( "test message" )
    assert str( exc1 ) == "test message"
    exc2 = exceptions.Omnierror( "test message" )
    assert str( exc2 ) == "test message"
    exc3 = exceptions.ControlError( "test message" )
    assert str( exc3 ) == "test message"
    exc4 = exceptions.ControlInvalidity( "test message" )
    assert str( exc4 ) == "test message"
    exc5 = exceptions.ConstraintViolation( "test message" )
    assert str( exc5 ) == "test message"
    exc6 = exceptions.DefinitionInvalidity( "test message" )
    assert str( exc6 ) == "test message"


def test_100_omniexception_creation( ):
    ''' Omniexception is created with message. '''
    exc = exceptions.Omniexception( "base exception message" )
    assert str( exc ) == "base exception message"


def test_110_omniexception_inheritance( ):
    ''' Omniexception has correct base class relationship. '''
    exc = exceptions.Omniexception( "test" )
    assert isinstance( exc, exceptions.Omniexception )


def test_200_omnierror_creation( ):
    ''' Omnierror is created with message. '''
    exc = exceptions.Omnierror( "error message" )
    assert str( exc ) == "error message"


def test_210_omnierror_inheritance( ):
    ''' Omnierror inherits from both Omniexception and Exception. '''
    exc = exceptions.Omnierror( "test" )
    assert isinstance( exc, exceptions.Omniexception )
    assert isinstance( exc, Exception )


def test_300_control_error_creation( ):
    ''' ControlError is created with message. '''
    exc = exceptions.ControlError( "control error message" )
    assert str( exc ) == "control error message"


def test_310_control_error_catch( ):
    ''' ControlError is catchable as ControlError. '''
    with pytest.raises( exceptions.ControlError ):
        raise exceptions.ControlError( "test error" )


def test_320_control_error_inheritance( ):
    ''' ControlError inherits from Omnierror. '''
    exc = exceptions.ControlError( "test" )
    assert isinstance( exc, exceptions.Omnierror )
    assert isinstance( exc, exceptions.Omniexception )


def test_400_control_invalidity_creation( ):
    ''' ControlInvalidity is created with message. '''
    exc = exceptions.ControlInvalidity( "value is invalid" )
    assert str( exc ) == "value is invalid"


def test_410_control_invalidity_value_error( ):
    ''' ControlInvalidity is a ValueError subclass. '''
    exc = exceptions.ControlInvalidity( "test" )
    assert isinstance( exc, ValueError )


def test_420_control_invalidity_catch( ):
    ''' ControlInvalidity is catchable as ControlInvalidity. '''
    with pytest.raises( exceptions.ControlInvalidity ):
        raise exceptions.ControlInvalidity( "invalid value" )


def test_430_control_invalidity_context( ):
    ''' ControlInvalidity supports exception chaining. '''
    original_error = ValueError( "original error" )
    try:
        raise exceptions.ControlInvalidity(
            "wrapped error"
        ) from original_error
    except exceptions.ControlInvalidity as exc:
        assert exc.__cause__ is original_error
        assert str( exc ) == "wrapped error"


def test_500_constraint_violation_creation( ):
    ''' ConstraintViolation is created with message. '''
    exc = exceptions.ConstraintViolation( "constraint violated" )
    assert str( exc ) == "constraint violated"


def test_510_constraint_violation_inheritance( ):
    ''' ConstraintViolation is a ControlInvalidity subclass. '''
    exc = exceptions.ConstraintViolation( "test" )
    assert isinstance( exc, exceptions.ControlInvalidity )
    assert isinstance( exc, exceptions.ControlError )


def test_520_constraint_violation_specificity( ):
    ''' ConstraintViolation is distinguishable from ControlInvalidity. '''
    with pytest.raises( exceptions.ConstraintViolation ):
        raise exceptions.ConstraintViolation( "test" )
    try:
        raise exceptions.ConstraintViolation( "test" )
    except exceptions.ControlInvalidity:
        pass  # Should also be catchable as parent


def test_600_definition_invalidity_creation( ):
    ''' DefinitionInvalidity is created with message. '''
    exc = exceptions.DefinitionInvalidity( "definition invalid" )
    assert str( exc ) == "definition invalid"


def test_610_definition_invalidity_value_error( ):
    ''' DefinitionInvalidity is a ValueError subclass. '''
    exc = exceptions.DefinitionInvalidity( "test" )
    assert isinstance( exc, ValueError )


def test_620_definition_invalidity_catch( ):
    ''' DefinitionInvalidity is catchable as DefinitionInvalidity. '''
    with pytest.raises( exceptions.DefinitionInvalidity ):
        raise exceptions.DefinitionInvalidity( "invalid definition" )
