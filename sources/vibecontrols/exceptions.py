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


''' Family of exceptions for package API. '''


from . import __


class Omniexception( __.immut.exceptions.Omniexception ):
    ''' Base for all exceptions raised by package API. '''


class Omnierror( Omniexception, Exception ):
    ''' Base for error exceptions raised by package API. '''


class ControlError( Omnierror ):
    ''' Base exception for control-related errors. '''


class ControlInvalidity( ControlError, ValueError ):
    ''' Control value invalidity.

        Raised when a value does not meet the requirements defined by a control
        definition (e.g., wrong type, out of range, invalid format).
    '''


class TypeInvalidity( ControlInvalidity ):
    ''' Type invalidity.

        Raised when a value is of the wrong type for a control.
    '''

    def __init__(
        self,
        *,
        expected: str,
        actual: __.Absential[ str ] = __.absent
    ):
        if not __.is_absent( actual ):
            message = f"Value must be { expected } (got { actual })."
        else:
            message = f"Value must be { expected }."
        super( ).__init__( message )


class ConstraintViolation( ControlInvalidity ):
    ''' Constraint violation.

        Raised when a value violates a specific constraint (e.g.,
        minimum/maximum bounds, size limits, uniqueness requirements).
    '''


class DefinitionInvalidity( ControlError, ValueError ):
    ''' Control definition invalidity.

        Raised when a control definition is improperly configured (e.g.,
        invalid parameters, inconsistent settings, missing required fields).
    '''

    def __init__(
        self,
        *,
        parameter: __.Absential[ str ] = __.absent,
        issue: __.Absential[ str ] = __.absent,
        detail: __.Absential[ str ] = __.absent
    ):
        parts: list[ str ] = [ ]
        if not __.is_absent( parameter ):
            parts.append( f"Parameter '{parameter}'" )
        else:
            parts.append( "Control definition" )
        if not __.is_absent( issue ):
            parts.append( issue )
        else:
            parts.append( "is invalid" )
        if not __.is_absent( detail ):
            message = f"{' '.join(parts)}: {detail}."
        else:
            message = f"{' '.join(parts)}."
        super( ).__init__( message )


class SizeConstraintViolation( ConstraintViolation ):
    ''' Size constraint violation.

        Raised when a value violates size constraints (e.g., sequence length,
        array size, text length).
    '''

    def __init__(
        self,
        *,
        minimum: __.Absential[ int ] = __.absent,
        maximum: __.Absential[ int ] = __.absent,
        actual: int,
        label: str = "Length"
    ):
        has_min = not __.is_absent( minimum )
        has_max = not __.is_absent( maximum )
        if has_min and has_max:
            message = (
                f"{ label } must be between { minimum } and { maximum } "
                f"(got { actual })."
            )
        elif has_min:
            message = (
                f"{ label } must be at least { minimum } (got { actual })."
            )
        elif has_max:
            message = (
                f"{ label } must be at most { maximum } (got { actual })."
            )
        else:
            message = f"{ label } constraint violated (got { actual })."
        super( ).__init__( message )


class BoundsConstraintViolation( ConstraintViolation ):
    ''' Bounds constraint violation.

        Raised when a numeric value is outside allowed minimum/maximum bounds.
    '''

    def __init__(
        self, *, minimum: float, maximum: float, actual: float
    ):
        message = (
            f"Value must be between { minimum } and { maximum } "
            f"(got { actual })."
        )
        super( ).__init__( message )


class StepConstraintViolation( ConstraintViolation ):
    ''' Step constraint violation.

        Raised when a numeric value does not align with required step
        increments.
    '''

    def __init__(
        self, *, step: float, minimum: float
    ):
        message = (
            f"Value must be aligned to step { step } from minimum { minimum }."
        )
        super( ).__init__( message )


class UniquenessConstraintViolation( ConstraintViolation ):
    ''' Uniqueness constraint violation.

        Raised when duplicate values are present where uniqueness is required.
    '''

    def __init__(
        self,
        *,
        index: __.Absential[ int ] = __.absent,
        hashable: bool = True
    ):
        if not hashable:
            message = (
                f"Element at index { index } is not hashable and cannot be "
                f"checked for uniqueness."
            )
        elif not __.is_absent( index ):
            message = f"Duplicate element at index { index }."
        else:
            message = "Duplicate values are not allowed."
        super( ).__init__( message )


class SelectionConstraintViolation( ConstraintViolation ):
    ''' Selection constraint violation.

        Raised when a value is not from the allowed set of choices.
    '''

    def __init__( self, *, value: __.Absential[ __.typx.Any ] = __.absent ):
        if not __.is_absent( value ):
            message = f"Value {value!r} is not in available choices."
        else:
            message = "Value is not in available choices."
        super( ).__init__( message )


class CycleOperationFailure( ControlError ):
    ''' Cycle operation failure.

        Raised when a cycle operation (next/previous) cannot be performed.
    '''

    def __init__( self ):
        message = "Cannot cycle through multi-select options."
        super( ).__init__( message )


class IncrementOperationFailure( ControlError ):
    ''' Increment operation failure.

        Raised when an increment/decrement operation cannot be performed.
    '''

    def __init__( self, *, operation: str = "increment" ):
        message = f"Cannot { operation } interval without defined step."
        super( ).__init__( message )


class ElementInvalidity( ControlInvalidity ):
    ''' Array element invalidity.

        Raised when an element at a specific index is invalid.
    '''

    def __init__( self, *, index: int, cause: Exception ):
        message = f"Element at index { index } is invalid: { cause }"
        super( ).__init__( message )


class IndexOutOfRange( ConstraintViolation ):
    ''' Array index out of range.

        Raised when an array index is outside valid bounds.
    '''

    def __init__(
        self, *, index: int, length: int, operation: str = "access"
    ):
        if operation == "insertion":
            message = (
                f"Index { index } is out of range for insertion into array "
                f"of length { length }."
            )
        else:
            message = (
                f"Index { index } is out of range for array of length "
                f"{ length }."
            )
        super( ).__init__( message )


class InvalidPermutation( ConstraintViolation ):
    ''' Invalid array permutation.

        Raised when a reorder operation receives an invalid permutation.
    '''

    def __init__(
        self,
        *,
        expected_length: int,
        actual_length: __.Absential[ int ] = __.absent
    ):
        if not __.is_absent( actual_length ):
            message = (
                f"Reorder indices must have length { expected_length } "
                f"(got { actual_length })."
            )
        else:
            message = (
                f"Reorder indices must be a permutation of "
                f"0..{ expected_length - 1 }."
            )
        super( ).__init__( message )
