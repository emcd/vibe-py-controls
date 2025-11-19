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


''' Validation framework testing. '''


import pytest

from vibecontrols import exceptions, validation


def test_000_validator_protocol_importable( ):
    ''' Validator protocol is importable. '''
    assert hasattr( validation, 'Validator' )
    assert validation.Validator is not None


def test_010_validator_callable( ):
    ''' Validators are callable. '''
    validator = validation.ClassValidator( expected_type = bool )
    assert callable( validator )
    result = validator( True )
    assert result is True


def test_100_composite_validator_creation( ):
    ''' CompositeValidator is created with multiple validators. '''
    validator1 = validation.ClassValidator( expected_type = int )
    validator2 = validation.IntervalValidator( minimum = 0.0, maximum = 10.0 )
    composite = validation.CompositeValidator(
        validators = ( validator1, validator2 )
    )
    assert len( composite.validators ) == 2


def test_110_composite_validator_empty( ):
    ''' CompositeValidator is created with no validators. '''
    composite = validation.CompositeValidator( validators = ( ) )
    assert len( composite.validators ) == 0
    result = composite( "anything" )
    assert result == "anything"


def test_120_composite_validator_single( ):
    ''' CompositeValidator is created with single validator. '''
    validator = validation.ClassValidator( expected_type = str )
    composite = validation.CompositeValidator( validators = ( validator, ) )
    assert len( composite.validators ) == 1
    result = composite( "test" )
    assert result == "test"


def test_130_composite_validator_chaining( ):
    ''' Validators execute in sequence. '''
    validator1 = validation.ClassValidator( expected_type = int )
    validator2 = validation.IntervalValidator( minimum = 0.0, maximum = 100.0 )
    composite = validation.CompositeValidator(
        validators = ( validator1, validator2 )
    )
    result = composite( 50 )
    assert result == 50


def test_140_composite_validator_short_circuit( ):
    ''' CompositeValidator stops on first failure. '''
    validator1 = validation.ClassValidator( expected_type = int )
    validator2 = validation.IntervalValidator( minimum = 0.0, maximum = 10.0 )
    composite = validation.CompositeValidator(
        validators = ( validator1, validator2 )
    )
    with pytest.raises( exceptions.ControlInvalidity, match = "must be int" ):
        composite( "not an int" )


def test_150_composite_validator_value_transformation( ):
    ''' Each validator can transform value. '''
    def uppercase_validator( value ):
        return value.upper( )
    validator1 = validation.ClassValidator( expected_type = str )
    composite = validation.CompositeValidator(
        validators = ( validator1, uppercase_validator )
    )
    result = composite( "test" )
    assert result == "TEST"


def test_160_composite_validator_exception_propagation( ):
    ''' Exception from any validator propagates. '''
    validator1 = validation.ClassValidator( expected_type = int )
    validator2 = validation.IntervalValidator( minimum = 0.0, maximum = 10.0 )
    composite = validation.CompositeValidator(
        validators = ( validator1, validator2 )
    )
    with pytest.raises( exceptions.ConstraintViolation ):
        composite( 20 )


def test_200_class_validator_creation( ):
    ''' ClassValidator is created with type. '''
    validator = validation.ClassValidator( expected_type = bool )
    assert validator.expected_type is bool


def test_210_class_validator_valid_type( ):
    ''' ClassValidator accepts correct type. '''
    validator = validation.ClassValidator( expected_type = bool )
    result = validator( True )
    assert result is True


def test_220_class_validator_invalid_type( ):
    ''' ClassValidator rejects wrong type. '''
    validator = validation.ClassValidator( expected_type = bool )
    with pytest.raises( exceptions.ControlInvalidity, match = "must be bool" ):
        validator( "not a bool" )


def test_230_class_validator_multiple_types( ):
    ''' ClassValidator supports tuple of types. '''
    validator = validation.ClassValidator( expected_type = ( int, float ) )
    assert validator( 42 ) == 42
    assert validator( 3.14 ) == 3.14
    with pytest.raises( exceptions.ControlInvalidity ):
        validator( "string" )


def test_240_class_validator_default_message( ):
    ''' ClassValidator auto-generates message for single type. '''
    validator = validation.ClassValidator( expected_type = str )
    assert "must be str" in validator.message


def test_250_class_validator_default_message_multiple( ):
    ''' ClassValidator auto-generates message for multiple types. '''
    validator = validation.ClassValidator( expected_type = ( int, float ) )
    assert "must be one of" in validator.message
    assert "int" in validator.message
    assert "float" in validator.message


def test_260_class_validator_custom_message( ):
    ''' ClassValidator uses custom message. '''
    validator = validation.ClassValidator(
        expected_type = bool, message = "Custom message"
    )
    assert validator.message == "Custom message"
    with pytest.raises(
        exceptions.ControlInvalidity, match = "Custom message"
    ):
        validator( 123 )


def test_270_class_validator_subclass( ):
    ''' ClassValidator accepts subclass via isinstance. '''
    class CustomBool:
        pass
    validator = validation.ClassValidator( expected_type = object )
    assert validator( CustomBool( ) )


def test_280_class_validator_exact_type_bool( ):
    ''' ClassValidator validates strict bool (not int). '''
    validator = validation.ClassValidator( expected_type = bool )
    assert validator( True ) is True
    assert validator( False ) is False
    with pytest.raises( exceptions.ControlInvalidity ):
        validator( 1 )
    with pytest.raises( exceptions.ControlInvalidity ):
        validator( 0 )


def test_300_interval_validator_creation( ):
    ''' IntervalValidator is created with min/max. '''
    validator = validation.IntervalValidator( minimum = 0.0, maximum = 10.0 )
    assert validator.minimum == 0.0
    assert validator.maximum == 10.0


def test_310_interval_validator_in_range( ):
    ''' Value within range passes. '''
    validator = validation.IntervalValidator( minimum = 0.0, maximum = 10.0 )
    assert validator( 5.0 ) == 5.0


def test_320_interval_validator_below_minimum( ):
    ''' Value too low fails. '''
    validator = validation.IntervalValidator( minimum = 0.0, maximum = 10.0 )
    with pytest.raises( exceptions.ConstraintViolation, match = "between" ):
        validator( -1.0 )


def test_330_interval_validator_above_maximum( ):
    ''' Value too high fails. '''
    validator = validation.IntervalValidator( minimum = 0.0, maximum = 10.0 )
    with pytest.raises( exceptions.ConstraintViolation, match = "between" ):
        validator( 11.0 )


def test_340_interval_validator_at_minimum( ):
    ''' Boundary: minimum value passes. '''
    validator = validation.IntervalValidator( minimum = 0.0, maximum = 10.0 )
    assert validator( 0.0 ) == 0.0


def test_350_interval_validator_at_maximum( ):
    ''' Boundary: maximum value passes. '''
    validator = validation.IntervalValidator( minimum = 0.0, maximum = 10.0 )
    assert validator( 10.0 ) == 10.0


def test_360_interval_validator_default_message( ):
    ''' IntervalValidator auto-generates message. '''
    validator = validation.IntervalValidator( minimum = 0.0, maximum = 100.0 )
    assert "between" in validator.message
    assert "0.0" in validator.message
    assert "100.0" in validator.message


def test_370_interval_validator_custom_message( ):
    ''' IntervalValidator uses custom message. '''
    validator = validation.IntervalValidator(
        minimum = 0.0, maximum = 1.0, message = "Custom range message"
    )
    assert validator.message == "Custom range message"
    with pytest.raises(
        exceptions.ConstraintViolation, match = "Custom range"
    ):
        validator( 2.0 )


def test_380_interval_validator_float_precision( ):
    ''' IntervalValidator handles floating point correctly. '''
    validator = validation.IntervalValidator( minimum = 0.0, maximum = 1.0 )
    assert validator( 0.5 ) == 0.5
    assert validator( 0.999999 ) == 0.999999


def test_400_size_validator_creation( ):
    ''' SizeValidator is created with min/max length. '''
    validator = validation.SizeValidator( min_length = 1, max_length = 10 )
    assert validator.min_length == 1
    assert validator.max_length == 10


def test_410_size_validator_min_only( ):
    ''' SizeValidator with only minimum constraint. '''
    validator = validation.SizeValidator( min_length = 2 )
    assert validator( [ 1, 2, 3 ] ) == [ 1, 2, 3 ]
    with pytest.raises( exceptions.ConstraintViolation ):
        validator( [ 1 ] )


def test_420_size_validator_max_only( ):
    ''' SizeValidator with only maximum constraint. '''
    validator = validation.SizeValidator( max_length = 3 )
    assert validator( [ 1, 2 ] ) == [ 1, 2 ]
    with pytest.raises( exceptions.ConstraintViolation ):
        validator( [ 1, 2, 3, 4 ] )


def test_430_size_validator_both_constraints( ):
    ''' SizeValidator with both min and max constraints. '''
    validator = validation.SizeValidator( min_length = 2, max_length = 4 )
    assert validator( [ 1, 2, 3 ] ) == [ 1, 2, 3 ]
    with pytest.raises( exceptions.ConstraintViolation ):
        validator( [ 1 ] )
    with pytest.raises( exceptions.ConstraintViolation ):
        validator( [ 1, 2, 3, 4, 5 ] )


def test_440_size_validator_no_constraints( ):
    ''' SizeValidator with neither constraint. '''
    validator = validation.SizeValidator( )
    assert validator( [ ] ) == [ ]
    assert validator( [ 1, 2, 3, 4, 5 ] ) == [ 1, 2, 3, 4, 5 ]


def test_450_size_validator_valid_length( ):
    ''' Length in range passes. '''
    validator = validation.SizeValidator( min_length = 1, max_length = 5 )
    assert validator( [ 1, 2, 3 ] ) == [ 1, 2, 3 ]


def test_460_size_validator_too_short( ):
    ''' Below minimum length fails. '''
    validator = validation.SizeValidator( min_length = 3 )
    with pytest.raises( exceptions.ConstraintViolation, match = "at least" ):
        validator( [ 1, 2 ] )


def test_470_size_validator_too_long( ):
    ''' Above maximum length fails. '''
    validator = validation.SizeValidator( max_length = 3 )
    with pytest.raises( exceptions.ConstraintViolation, match = "at most" ):
        validator( [ 1, 2, 3, 4 ] )


def test_480_size_validator_at_minimum( ):
    ''' Boundary: minimum length passes. '''
    validator = validation.SizeValidator( min_length = 2 )
    assert validator( [ 1, 2 ] ) == [ 1, 2 ]


def test_490_size_validator_at_maximum( ):
    ''' Boundary: maximum length passes. '''
    validator = validation.SizeValidator( max_length = 3 )
    assert validator( [ 1, 2, 3 ] ) == [ 1, 2, 3 ]


def test_495_size_validator_default_messages( ):
    ''' SizeValidator auto-generates messages for all cases. '''
    validator_both = validation.SizeValidator( min_length = 2, max_length = 5 )
    assert "between" in validator_both.message
    validator_min = validation.SizeValidator( min_length = 3 )
    assert "at least" in validator_min.message
    validator_max = validation.SizeValidator( max_length = 10 )
    assert "at most" in validator_max.message


def test_496_size_validator_custom_message( ):
    ''' SizeValidator uses custom message. '''
    validator = validation.SizeValidator(
        min_length = 1, message = "Custom size message"
    )
    assert validator.message == "Custom size message"
    with pytest.raises(
        exceptions.ConstraintViolation, match = "Custom size"
    ):
        validator( [ ] )


def test_497_size_validator_various_types( ):
    ''' SizeValidator works with list, tuple, str, dict. '''
    validator = validation.SizeValidator( min_length = 2, max_length = 4 )
    assert validator( [ 1, 2, 3 ] ) == [ 1, 2, 3 ]
    assert validator( ( 1, 2 ) ) == ( 1, 2 )
    assert validator( "abc" ) == "abc"
    assert validator( { 'a': 1, 'b': 2 } ) == { 'a': 1, 'b': 2 }


def test_500_selection_validator_creation( ):
    ''' SelectionValidator is created with choices. '''
    validator = validation.SelectionValidator( choices = [ 'a', 'b', 'c' ] )
    assert 'a' in validator.choices
    assert 'b' in validator.choices
    assert 'c' in validator.choices


def test_510_selection_validator_valid_choice( ):
    ''' Choice in set passes. '''
    validator = validation.SelectionValidator(
        choices = [ 'red', 'green', 'blue' ]
    )
    assert validator( 'red' ) == 'red'


def test_520_selection_validator_invalid_choice( ):
    ''' Choice not in set fails. '''
    validator = validation.SelectionValidator(
        choices = [ 'red', 'green', 'blue' ]
    )
    with pytest.raises(
        exceptions.ConstraintViolation, match = "must be one"
    ):
        validator( 'yellow' )


def test_530_selection_validator_frozenset_normalization( ):
    ''' Choices are converted to frozenset. '''
    validator = validation.SelectionValidator( choices = [ 'a', 'b', 'c' ] )
    assert isinstance( validator.choices, frozenset )
    validator2 = validation.SelectionValidator(
        choices = frozenset( [ 'x', 'y' ] )
    )
    assert isinstance( validator2.choices, frozenset )


def test_540_selection_validator_few_choices_message( ):
    ''' SelectionValidator shows all choices (≤5). '''
    validator = validation.SelectionValidator( choices = [ 'a', 'b', 'c' ] )
    assert "'a'" in validator.message or '"a"' in validator.message
    assert "'b'" in validator.message or '"b"' in validator.message
    assert "'c'" in validator.message or '"c"' in validator.message


def test_550_selection_validator_many_choices_message( ):
    ''' SelectionValidator shows count only (>5). '''
    choices = [ f"choice{i}" for i in range( 10 ) ]
    validator = validation.SelectionValidator( choices = choices )
    assert "10" in validator.message
    assert "allowed choices" in validator.message


def test_560_selection_validator_custom_message( ):
    ''' SelectionValidator uses custom message. '''
    validator = validation.SelectionValidator(
        choices = [ 'x', 'y' ], message = "Custom choice message"
    )
    assert validator.message == "Custom choice message"
    with pytest.raises(
        exceptions.ConstraintViolation, match = "Custom choice"
    ):
        validator( 'z' )


def test_570_selection_validator_empty_choices( ):
    ''' Edge: empty choice set. '''
    validator = validation.SelectionValidator( choices = [ ] )
    with pytest.raises( exceptions.ConstraintViolation ):
        validator( 'anything' )


def test_580_selection_validator_single_choice( ):
    ''' Edge: single valid choice. '''
    validator = validation.SelectionValidator( choices = [ 'only' ] )
    assert validator( 'only' ) == 'only'
    with pytest.raises( exceptions.ConstraintViolation ):
        validator( 'other' )


def test_590_selection_validator_hashable_choices( ):
    ''' Choices must be hashable. '''
    validator = validation.SelectionValidator( choices = [ 1, 2, 3 ] )
    assert validator( 2 ) == 2
    validator_str = validation.SelectionValidator( choices = [ 'a', 'b' ] )
    assert validator_str( 'a' ) == 'a'
