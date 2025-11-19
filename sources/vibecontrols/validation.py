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
        __.ddoc.Doc( "Validated (and possibly transformed) value." ),
        __.ddoc.Raises( ControlInvalidity, "If validation fails." )
    ]:
        ''' Validates value, returning validated/transformed value. '''
        ...


class CompositeValidator( Validator ):
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
        __.ddoc.Doc( "Validated value after all validators." ),
        __.ddoc.Raises( ControlInvalidity, "If any validator fails." )
    ]:
        ''' Applies validators in sequence. '''
        result = value
        for validator in self.validators:
            result = validator( result )
        return result


class ClassValidator( Validator ):
    ''' Validates value type.

        Example:
            >>> validator = ClassValidator( bool )
            >>> validator( True )  # valid
            True
            >>> validator( "text" )  # raises ControlInvalidity
    '''

    expected_type: __.typx.Annotated[
        type | tuple[ type, ... ],
        __.ddoc.Doc( "Expected type or tuple of types." )
    ]
    message: __.typx.Annotated[
        str | None,
        __.ddoc.Doc( "Custom error message. If None, generates default." )
    ] = None

    def __post_init__( self ) -> None:
        ''' Computes default message if not provided. '''
        if self.message is None:
            if isinstance( self.expected_type, tuple ):
                type_names = ', '.join(
                    t.__name__ for t in self.expected_type
                )
                computed_message = f"Value must be one of: { type_names }"
            else:
                type_name = self.expected_type.__name__
                computed_message = f"Value must be { type_name }"
            object.__setattr__( self, 'message', computed_message )

    def __call__(
        self,
        value: __.typx.Annotated[
            __.typx.Any, __.ddoc.Doc( "Value to validate." )
        ]
    ) -> __.typx.Annotated[
        __.typx.Any,
        __.ddoc.Doc( "Value if type is correct." ),
        __.ddoc.Raises( ControlInvalidity, "If value is wrong type." )
    ]:
        ''' Validates value type. '''
        if not isinstance( value, self.expected_type ):
            raise ControlInvalidity( self.message )
        return value


class IntervalValidator( Validator ):
    ''' Validates numeric range.

        Example:
            >>> validator = IntervalValidator( 0.0, 1.0 )
            >>> validator( 0.5 )  # valid
            0.5
            >>> validator( 2.0 )  # raises ConstraintViolation
    '''

    minimum: __.typx.Annotated[
        float, __.ddoc.Doc( "Minimum allowed value (inclusive)." )
    ]
    maximum: __.typx.Annotated[
        float, __.ddoc.Doc( "Maximum allowed value (inclusive)." )
    ]
    message: __.typx.Annotated[
        str | None,
        __.ddoc.Doc( "Custom error message. If None, generates default." )
    ] = None

    def __post_init__( self ) -> None:
        ''' Computes default message if not provided. '''
        if self.message is None:
            computed_message = (
                f"Value must be between { self.minimum } and { self.maximum } "
                f"(inclusive)"
            )
            object.__setattr__( self, 'message', computed_message )

    def __call__(
        self,
        value: __.typx.Annotated[
            __.typx.Any, __.ddoc.Doc( "Value to validate." )
        ]
    ) -> __.typx.Annotated[
        __.typx.Any,
        __.ddoc.Doc( "Value if in range." ),
        __.ddoc.Raises( ConstraintViolation, "If value is out of range." )
    ]:
        ''' Validates value is in range. '''
        if not self.minimum <= value <= self.maximum:
            raise ConstraintViolation( self.message )
        return value


class SizeValidator( Validator ):
    ''' Validates sequence or collection length.

        Example:
            >>> validator = SizeValidator( min_length=1, max_length=10 )
            >>> validator( [ 1, 2, 3 ] )  # valid
            [1, 2, 3]
            >>> validator( [ ] )  # raises ConstraintViolation (too short)
    '''

    min_length: __.typx.Annotated[
        int | None,
        __.ddoc.Doc( "Minimum allowed length (inclusive). None = no minimum." )
    ] = None
    max_length: __.typx.Annotated[
        int | None,
        __.ddoc.Doc( "Maximum allowed length (inclusive). None = no maximum." )
    ] = None
    message: __.typx.Annotated[
        str | None,
        __.ddoc.Doc( "Custom error message. If None, generates default." )
    ] = None

    def __post_init__( self ) -> None:
        ''' Computes default message if not provided. '''
        if self.message is None:
            if self.min_length is not None and self.max_length is not None:
                computed_message = (
                    f"Length must be between { self.min_length } "
                    f"and { self.max_length }"
                )
            elif self.min_length is not None:
                computed_message = (
                    f"Length must be at least { self.min_length }"
                )
            elif self.max_length is not None:
                computed_message = (
                    f"Length must be at most { self.max_length }"
                )
            else:
                computed_message = "Invalid length"
            object.__setattr__( self, 'message', computed_message )

    def __call__(
        self,
        value: __.typx.Annotated[
            __.typx.Any,
            __.ddoc.Doc( "Value to validate (must support len())." )
        ]
    ) -> __.typx.Annotated[
        __.typx.Any,
        __.ddoc.Doc( "Value if length is valid." ),
        __.ddoc.Raises( ConstraintViolation, "If length is invalid." )
    ]:
        ''' Validates value length. '''
        length = len( value )
        if self.min_length is not None and length < self.min_length:
            raise ConstraintViolation( self.message )
        if self.max_length is not None and length > self.max_length:
            raise ConstraintViolation( self.message )
        return value


class SelectionValidator( Validator ):
    ''' Validates value is one of allowed choices.

        Example:
            >>> validator = SelectionValidator( [ "red", "green", "blue" ] )
            >>> validator( "red" )  # valid
            'red'
            >>> validator( "yellow" )  # raises ConstraintViolation
    '''

    # Maximum number of choices to display in error message
    _MAX_CHOICES_IN_MESSAGE = 5

    choices: __.typx.Annotated[
        frozenset[ __.typx.Any ],
        __.ddoc.Doc( "Allowed values." )
    ]
    message: __.typx.Annotated[
        str | None,
        __.ddoc.Doc( "Custom error message. If None, generates default." )
    ] = None

    def __post_init__( self ) -> None:
        ''' Normalizes choices and computes default message. '''
        # Normalize choices to frozenset
        if not isinstance( self.choices, frozenset ):
            object.__setattr__( self, 'choices', frozenset( self.choices ) )
        # Compute default message if not provided
        if self.message is None:
            # Limit displayed choices to avoid huge error messages
            if len( self.choices ) <= self._MAX_CHOICES_IN_MESSAGE:
                choices_str = ', '.join( repr( c ) for c in self.choices )
                computed_message = f"Value must be one of: { choices_str }"
            else:
                computed_message = (
                    f"Value must be one of { len( self.choices ) } "
                    f"allowed choices"
                )
            object.__setattr__( self, 'message', computed_message )

    def __call__(
        self,
        value: __.typx.Annotated[
            __.typx.Any, __.ddoc.Doc( "Value to validate." )
        ]
    ) -> __.typx.Annotated[
        __.typx.Any,
        __.ddoc.Doc( "Value if it's an allowed choice." ),
        __.ddoc.Raises( ConstraintViolation, "If value is not in choices." )
    ]:
        ''' Validates value is in allowed choices. '''
        if value not in self.choices:
            raise ConstraintViolation( self.message )
        return value
