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
    def __call__(
        self,
        value: __.typx.Annotated[
            __.typx.Any, __.ddoc.Doc( "Value to validate." )
        ]
    ) -> __.typx.Annotated[
        __.typx.Any,
        __.ddoc.Doc( "Validated (and possibly transformed) value." )
    ]:
        ''' Validates value, returning validated/transformed value.

        Raises:
            ControlInvalidity: If validation fails.
        '''
        ...


class CompositeValidator( __.immut.DataclassObject ):
    ''' Chains multiple validators together.

    Validators are applied in sequence. Each validator receives the output
    of the previous validator.

    Example:
        >>> validator = CompositeValidator(
        ...     ClassValidator( float ),
        ...     IntervalValidator( 0.0, 1.0 )
        ... )
        >>> validator( 0.5 )  # passes both validations
        0.5
    '''

    validators: tuple[ Validator, ... ]

    def __call__(
        self,
        value: __.typx.Annotated[
            __.typx.Any, __.ddoc.Doc( "Value to validate." )
        ]
    ) -> __.typx.Annotated[
        __.typx.Any,
        __.ddoc.Doc( "Validated value after all validators." )
    ]:
        ''' Applies validators in sequence.

        Raises:
            ControlInvalidity: If any validator fails.
        '''
        result = value
        for validator in self.validators:
            result = validator( result )
        return result


class ClassValidator( __.immut.DataclassObject ):
    ''' Validates value type.

    Example:
        >>> validator = ClassValidator( bool )
        >>> validator( True )  # valid
        True
        >>> validator( "text" )  # raises ControlInvalidity
    '''

    expected_type: type | tuple[ type, ... ]
    message: str

    def __new__(
        cls,
        expected_type: __.typx.Annotated[
            type | tuple[ type, ... ],
            __.ddoc.Doc( "Expected type or tuple of types." )
        ],
        message: __.typx.Annotated[
            str | None,
            __.ddoc.Doc(
                "Custom error message. If None, generates default."
            )
        ] = None
    ):
        ''' Creates type validator instance. '''
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

    def __call__(
        self,
        value: __.typx.Annotated[
            __.typx.Any, __.ddoc.Doc( "Value to validate." )
        ]
    ) -> __.typx.Annotated[
        __.typx.Any, __.ddoc.Doc( "Value if type is correct." )
    ]:
        ''' Validates value type.

        Raises:
            ControlInvalidity: If value is wrong type.
        '''
        if not isinstance( value, self.expected_type ):
            raise ControlInvalidity( self.message )
        return value


class IntervalValidator( __.immut.DataclassObject ):
    ''' Validates numeric range.

    Example:
        >>> validator = IntervalValidator( 0.0, 1.0 )
        >>> validator( 0.5 )  # valid
        0.5
        >>> validator( 2.0 )  # raises ConstraintViolation
    '''

    minimum: float
    maximum: float
    message: str

    def __new__(
        cls,
        minimum: __.typx.Annotated[
            float, __.ddoc.Doc( "Minimum allowed value (inclusive)." )
        ],
        maximum: __.typx.Annotated[
            float, __.ddoc.Doc( "Maximum allowed value (inclusive)." )
        ],
        message: __.typx.Annotated[
            str | None,
            __.ddoc.Doc(
                "Custom error message. If None, generates default."
            )
        ] = None
    ):
        ''' Creates range validator instance. '''
        if message is None:
            message = (
                f"Value must be between { minimum } and { maximum } "
                f"(inclusive)"
            )
        return super().__new__(
            cls, minimum = minimum, maximum = maximum, message = message
        )

    def __call__(
        self,
        value: __.typx.Annotated[
            __.typx.Any, __.ddoc.Doc( "Value to validate." )
        ]
    ) -> __.typx.Annotated[
        __.typx.Any, __.ddoc.Doc( "Value if in range." )
    ]:
        ''' Validates value is in range.

        Raises:
            ConstraintViolation: If value is out of range.
        '''
        if not self.minimum <= value <= self.maximum:
            raise ConstraintViolation( self.message )
        return value


class SizeValidator( __.immut.DataclassObject ):
    ''' Validates sequence or collection length.

    Example:
        >>> validator = SizeValidator( min_length=1, max_length=10 )
        >>> validator( [ 1, 2, 3 ] )  # valid
        [1, 2, 3]
        >>> validator( [ ] )  # raises ConstraintViolation (too short)
    '''

    min_length: int | None
    max_length: int | None
    message: str

    def __new__(
        cls,
        min_length: __.typx.Annotated[
            int | None,
            __.ddoc.Doc(
                "Minimum allowed length (inclusive). None = no minimum."
            )
        ] = None,
        max_length: __.typx.Annotated[
            int | None,
            __.ddoc.Doc(
                "Maximum allowed length (inclusive). None = no maximum."
            )
        ] = None,
        message: __.typx.Annotated[
            str | None,
            __.ddoc.Doc(
                "Custom error message. If None, generates default."
            )
        ] = None
    ):
        ''' Creates length validator instance. '''
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

    def __call__(
        self,
        value: __.typx.Annotated[
            __.typx.Any,
            __.ddoc.Doc( "Value to validate (must support len())." )
        ]
    ) -> __.typx.Annotated[
        __.typx.Any, __.ddoc.Doc( "Value if length is valid." )
    ]:
        ''' Validates value length.

        Raises:
            ConstraintViolation: If length is invalid.
        '''
        length = len( value )
        if self.min_length is not None and length < self.min_length:
            raise ConstraintViolation( self.message )
        if self.max_length is not None and length > self.max_length:
            raise ConstraintViolation( self.message )
        return value


class SelectionValidator( __.immut.DataclassObject ):
    ''' Validates value is one of allowed choices.

    Example:
        >>> validator = SelectionValidator( [ "red", "green", "blue" ] )
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
        choices: __.typx.Annotated[
            __.cabc.Collection[ __.typx.Any ],
            __.ddoc.Doc( "Collection of allowed values." )
        ],
        message: __.typx.Annotated[
            str | None,
            __.ddoc.Doc(
                "Custom error message. If None, generates default."
            )
        ] = None
    ):
        ''' Creates choice validator instance. '''
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

    def __call__(
        self,
        value: __.typx.Annotated[
            __.typx.Any, __.ddoc.Doc( "Value to validate." )
        ]
    ) -> __.typx.Annotated[
        __.typx.Any, __.ddoc.Doc( "Value if it's an allowed choice." )
    ]:
        ''' Validates value is in allowed choices.

        Raises:
            ConstraintViolation: If value is not in choices.
        '''
        if value not in self.choices:
            raise ConstraintViolation( self.message )
        return value
