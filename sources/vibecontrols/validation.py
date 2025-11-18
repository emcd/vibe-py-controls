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


''' Validation framework for control values. '''


from . import __
from .exceptions import ConstraintViolation, ControlInvalidity


class Validator( __.immut.DataclassProtocol, __.typx.Protocol ):
    ''' Protocol for value validators.

    Validators are callables that take a value, validate it, and return
    the validated (and possibly transformed) value. They raise
    ControlInvalidity or its subclasses if validation fails.

    Can be implemented as classes with __call__ or as plain functions.
    '''

    @__.abc.abstractmethod
    def __call__( self, value: __.typx.Any ) -> __.typx.Any:
        ''' Validate value, returning validated/transformed value.

        Args:
            value: The value to validate

        Returns:
            The validated (and possibly transformed) value

        Raises:
            ControlInvalidity: If validation fails
        '''
        ...


class CompositeValidator( __.immut.DataclassObject ):
    ''' Chains multiple validators together.

    Validators are applied in sequence. Each validator receives the output
    of the previous validator.

    Example:
        >>> validator = CompositeValidator(
        ...     TypeValidator( float ),
        ...     RangeValidator( 0.0, 1.0 )
        ... )
        >>> validator( 0.5 )  # passes both validations
        0.5
    '''

    validators: tuple[ Validator, ... ]

    def __call__( self, value: __.typx.Any ) -> __.typx.Any:
        ''' Apply validators in sequence.

        Args:
            value: The value to validate

        Returns:
            The validated value after all validators

        Raises:
            ControlInvalidity: If any validator fails
        '''
        result = value
        for validator in self.validators:
            result = validator( result )
        return result


class TypeValidator( __.immut.DataclassObject ):
    ''' Validates value type.

    Example:
        >>> validator = TypeValidator( bool )
        >>> validator( True )  # valid
        True
        >>> validator( "text" )  # raises ControlInvalidity
    '''

    expected_type: type | tuple[ type, ... ]
    message: str

    def __new__(
        cls,
        expected_type: type | tuple[ type, ... ],
        message: str | None = None
    ):
        ''' Create type validator instance.

        Args:
            expected_type: Expected type or tuple of types
            message: Custom error message. If None, generates default.
        '''
        if message is None:
            if isinstance( expected_type, tuple ):
                type_names = ', '.join( t.__name__ for t in expected_type )
                message = f"Value must be one of: { type_names }"
            else:
                message = f"Value must be { expected_type.__name__ }"
        # Use super().__new__ which handles DataclassObject initialization
        return super().__new__(
            cls, expected_type = expected_type, message = message
        )

    def __call__( self, value: __.typx.Any ) -> __.typx.Any:
        ''' Validate value type.

        Args:
            value: The value to validate

        Returns:
            The value if type is correct

        Raises:
            ControlInvalidity: If value is wrong type
        '''
        if not isinstance( value, self.expected_type ):
            raise ControlInvalidity( self.message )
        return value


class RangeValidator( __.immut.DataclassObject ):
    ''' Validates numeric range.

    Example:
        >>> validator = RangeValidator( 0.0, 1.0 )
        >>> validator( 0.5 )  # valid
        0.5
        >>> validator( 2.0 )  # raises ConstraintViolation
    '''

    minimum: float
    maximum: float
    message: str

    def __new__(
        cls,
        minimum: float,
        maximum: float,
        message: str | None = None
    ):
        ''' Create range validator instance.

        Args:
            minimum: Minimum allowed value (inclusive)
            maximum: Maximum allowed value (inclusive)
            message: Custom error message. If None, generates default.
        '''
        if message is None:
            message = (
                f"Value must be between { minimum } and { maximum } "
                f"(inclusive)"
            )
        return super().__new__(
            cls, minimum = minimum, maximum = maximum, message = message
        )

    def __call__( self, value: __.typx.Any ) -> __.typx.Any:
        ''' Validate value is in range.

        Args:
            value: The value to validate

        Returns:
            The value if in range

        Raises:
            ConstraintViolation: If value is out of range
        '''
        if not self.minimum <= value <= self.maximum:
            raise ConstraintViolation( self.message )
        return value


class LengthValidator( __.immut.DataclassObject ):
    ''' Validates sequence or collection length.

    Example:
        >>> validator = LengthValidator( min_length=1, max_length=10 )
        >>> validator( [ 1, 2, 3 ] )  # valid
        [1, 2, 3]
        >>> validator( [ ] )  # raises ConstraintViolation (too short)
    '''

    min_length: int | None
    max_length: int | None
    message: str

    def __new__(
        cls,
        min_length: int | None = None,
        max_length: int | None = None,
        message: str | None = None
    ):
        ''' Create length validator instance.

        Args:
            min_length: Minimum allowed length (inclusive). None = no minimum.
            max_length: Maximum allowed length (inclusive). None = no maximum.
            message: Custom error message. If None, generates default.
        '''
        if message is None:
            if min_length is not None and max_length is not None:
                message = (
                    f"Length must be between { min_length } and { max_length }"
                )
            elif min_length is not None:
                message = f"Length must be at least { min_length }"
            elif max_length is not None:
                message = f"Length must be at most { max_length }"
            else:
                message = "Invalid length"
        return super().__new__(
            cls,
            min_length = min_length,
            max_length = max_length,
            message = message
        )

    def __call__( self, value: __.typx.Any ) -> __.typx.Any:
        ''' Validate value length.

        Args:
            value: The value to validate (must support len())

        Returns:
            The value if length is valid

        Raises:
            ConstraintViolation: If length is invalid
        '''
        length = len( value )
        if self.min_length is not None and length < self.min_length:
            raise ConstraintViolation( self.message )
        if self.max_length is not None and length > self.max_length:
            raise ConstraintViolation( self.message )
        return value


class ChoiceValidator( __.immut.DataclassObject ):
    ''' Validates value is one of allowed choices.

    Example:
        >>> validator = ChoiceValidator( [ "red", "green", "blue" ] )
        >>> validator( "red" )  # valid
        'red'
        >>> validator( "yellow" )  # raises ConstraintViolation
    '''

    # Maximum number of choices to display in error message
    _MAX_CHOICES_IN_MESSAGE = 5

    choices: frozenset[ __.typx.Any ]
    message: str

    def __new__(
        cls,
        choices: __.cabc.Collection[ __.typx.Any ],
        message: str | None = None
    ):
        ''' Create choice validator instance.

        Args:
            choices: Collection of allowed values
            message: Custom error message. If None, generates default.
        '''
        choices_frozen = frozenset( choices ) if not isinstance(
            choices, frozenset
        ) else choices
        if message is None:
            # Limit displayed choices to avoid huge error messages
            if len( choices_frozen ) <= cls._MAX_CHOICES_IN_MESSAGE:
                choices_str = ', '.join( repr( c ) for c in choices_frozen )
                message = f"Value must be one of: { choices_str }"
            else:
                message = (
                    f"Value must be one of { len( choices_frozen ) } "
                    f"allowed choices"
                )
        return super().__new__(
            cls, choices = choices_frozen, message = message
        )

    def __call__( self, value: __.typx.Any ) -> __.typx.Any:
        ''' Validate value is in allowed choices.

        Args:
            value: The value to validate

        Returns:
            The value if it's an allowed choice

        Raises:
            ConstraintViolation: If value is not in choices
        '''
        if value not in self.choices:
            raise ConstraintViolation( self.message )
        return value
