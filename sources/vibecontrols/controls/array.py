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


''' Array control type implementation. '''


from . import __


class ArrayHints( __.immut.DataclassObject ):
    ''' UI hints for array controls. '''

    orientation: __.typx.Annotated[
        __.typx.Literal[ "horizontal", "vertical", "grid" ],  # noqa: F821
        __.ddoc.Doc( "Layout orientation for array elements." )
    ] = "vertical"
    collapsible: __.typx.Annotated[
        bool, __.ddoc.Doc( "Whether the array can be collapsed." )
    ] = False
    initially_collapsed: __.typx.Annotated[
        bool,
        __.ddoc.Doc( "Whether the array starts collapsed." )
    ] = False
    border: __.typx.Annotated[
        bool, __.ddoc.Doc( "Whether to show a border around the array." )
    ] = False
    title: __.typx.Annotated[
        __.typx.Optional[ str ],
        __.ddoc.Doc( "Title for the array container." )
    ] = None
    label: __.typx.Annotated[
        __.typx.Optional[ str ],
        __.ddoc.Doc( "Display label for the control." )
    ] = None
    help_text: __.typx.Annotated[
        __.typx.Optional[ str ], __.ddoc.Doc( "Help or tooltip text." )
    ] = None


class ArrayDefinition( __.ControlDefinition ):
    ''' Array control definition.

        Defines a control that holds a dynamic sequence of elements, where
        each element conforms to a specified element definition. Supports
        size constraints, uniqueness requirements, and recursive nesting.
    '''

    element_definition: __.typx.Annotated[
        __.ControlDefinition,
        __.ddoc.Doc( "Definition for array elements." )
    ]
    size_min: __.typx.Annotated[
        int,
        __.ddoc.Doc(
            "Minimum number of elements (0 means no minimum)."
        )
    ] = 0
    size_max: __.typx.Annotated[
        __.typx.Optional[ int ],
        __.ddoc.Doc(
            "Maximum number of elements (None means no maximum)."
        )
    ] = None
    default_elements: __.typx.Annotated[
        __.cabc.Sequence[ __.typx.Any ],
        __.ddoc.Doc( "Default elements on creation." )
    ] = ( )
    allow_duplicates: __.typx.Annotated[
        bool,
        __.ddoc.Doc( "Whether duplicate values are allowed." )
    ] = True
    hints: __.typx.Annotated[
        ArrayHints, __.ddoc.Doc( "UI hints for rendering." )
    ] = __.dcls.field( default_factory = ArrayHints )

    def __post_init__( self ) -> None:
        ''' Validates definition parameters. '''
        if self.size_min < 0:
            raise __.DefinitionInvalidity(
                parameter = "size_min", issue = "cannot be negative"
            )
        if self.size_max is not None:
            if self.size_max < 0:
                raise __.DefinitionInvalidity(
                    parameter = "size_max", issue = "cannot be negative"
                )
            if self.size_min > self.size_max:
                raise __.DefinitionInvalidity(
                    parameter = "size_min",
                    issue = "cannot exceed",
                    detail = "maximum size"
                )
        # Normalize default_elements to tuple
        object.__setattr__(
            self, 'default_elements', tuple( self.default_elements )
        )
        # Validate default elements
        try:
            self.validate_value( self.default_elements )
        except __.ControlInvalidity as exception:
            raise __.DefinitionInvalidity(
                parameter = "default_elements",
                issue = "is invalid",
                detail = str( exception )
            ) from exception

    def validate_value(
        self,
        value: __.typx.Annotated[
            __.typx.Any, __.ddoc.Doc( "Value to validate." )
        ]
    ) -> __.typx.Annotated[
        tuple[ __.typx.Any, ... ],
        __.ddoc.Doc( "Validated tuple of elements." ),
        __.ddoc.Raises(
            __.TypeInvalidity,
            "If value is not a sequence."
        ),
        __.ddoc.Raises(
            __.ElementInvalidity,
            "If element is invalid."
        ),
        __.ddoc.Raises(
            __.SizeConstraintViolation,
            "If value violates size constraints."
        ),
        __.ddoc.Raises(
            __.UniquenessConstraintViolation,
            "If value violates uniqueness constraint."
        )
    ]:
        ''' Validates array value. '''
        if not isinstance( value, __.cabc.Sequence ):
            raise __.TypeInvalidity( expected = "a sequence" )
        sequence_value = __.typx.cast(
            __.cabc.Sequence[ __.typx.Any ], value )
        size = len( sequence_value )
        if size < self.size_min:
            raise __.SizeConstraintViolation(
                minimum = self.size_min,
                maximum = (
                    __.absent if self.size_max is None else self.size_max
                ),
                actual = size,
                label = "Array size" )
        if self.size_max is not None and size > self.size_max:
            raise __.SizeConstraintViolation(
                minimum = self.size_min,
                maximum = self.size_max,
                actual = size,
                label = "Array size" )
        validated_elements: list[ __.typx.Any ] = [ ]
        for index, element in enumerate( sequence_value ):
            # Try-except in loop is intentional: provides precise error
            # messages showing which specific element failed validation
            try:
                validated = self.element_definition.validate_value( element )
                validated_elements.append( validated )
            except __.ControlInvalidity as exception:  # noqa: PERF203
                raise __.ElementInvalidity(
                    index = index, cause = exception ) from exception
        if not self.allow_duplicates:
            unique_elements: set[ __.typx.Any ] = set( )
            for index, element in enumerate( validated_elements ):
                # Try-except in loop is intentional: elements may not be
                # hashable, need to provide clear error message
                try:
                    if element in unique_elements:
                        raise __.UniquenessConstraintViolation( index = index )
                    unique_elements.add( element )
                except TypeError as exception:  # noqa: PERF203
                    raise __.UniquenessConstraintViolation(  # pragma: no cover
                        index = index, hashable = False ) from exception
        return tuple( validated_elements )

    def produce_control(
        self,
        initial: __.typx.Annotated[
            __.typx.Any,
            __.ddoc.Doc(
                "Initial value for the control. If absent, uses default." )
        ] = __.absent
    ) -> __.typx.Annotated[
        'Array',
        __.ddoc.Doc( "New Array control." ),
        __.ddoc.Raises(
            __.ControlInvalidity, "If the initial value is invalid." )
    ]:
        ''' Produces array control. '''
        if __.is_absent( initial ):
            validated = self.validate_value( self.default_elements )
        else:
            validated = self.validate_value( initial )
        return Array( definition = self, current = validated )

    def serialize_value(
        self,
        value: __.typx.Annotated[
            tuple[ __.typx.Any, ... ],
            __.ddoc.Doc( "Array value to serialize." )
        ]
    ) -> __.typx.Annotated[
        list[ __.typx.Any ],
        __.ddoc.Doc( "List of serialized elements." )
    ]:
        ''' Serializes array value.

            Serializes each element using the element definition's
            serialization method.
        '''
        return [
            self.element_definition.serialize_value( element )
            for element in value ]

    def produce_default(
        self
    ) -> __.typx.Annotated[
        tuple[ __.typx.Any, ... ],
        __.ddoc.Doc( "Default array value." )
    ]:
        ''' Produces the default value for this control. '''
        return self.validate_value( self.default_elements )


class Array( __.Control ):
    ''' Array control.

        Represents the current state of an array control. Immutable - all
        operations return new instances.
    '''

    definition: __.typx.Annotated[
        ArrayDefinition, __.ddoc.Doc( "Array definition." )
    ]
    current: __.typx.Annotated[
        tuple[ __.typx.Any, ... ],
        __.ddoc.Doc( "Current array elements." )
    ]

    def copy(
        self,
        value: __.typx.Annotated[
            __.cabc.Sequence[ __.typx.Any ],
            __.ddoc.Doc( "New array elements." )
        ]
    ) -> __.typx.Annotated[
        __.typx.Self,
        __.ddoc.Doc( "New Array control with the updated value." ),
        __.ddoc.Raises(
            __.ControlInvalidity, "If the new value is invalid."
        )
    ]:
        ''' Produces copy with new elements (immutable operation). '''
        validated = self.definition.validate_value( value )
        return type( self )(
            definition = self.definition, current = validated
        )

    def append(
        self,
        element: __.typx.Annotated[
            __.typx.Any, __.ddoc.Doc( "Element to append." )
        ]
    ) -> __.typx.Annotated[
        __.typx.Self,
        __.ddoc.Doc( "New Array control with element appended." ),
        __.ddoc.Raises(
            __.ControlInvalidity, "If the element is invalid."
        ),
        __.ddoc.Raises(
            __.ConstraintViolation,
            "If appending would violate size or uniqueness constraints."
        )
    ]:
        ''' Produces copy with element appended. '''
        new_elements = ( *self.current, element )
        return self.copy( new_elements )

    def remove_at(
        self,
        index: __.typx.Annotated[
            int, __.ddoc.Doc( "Index of element to remove." )
        ],
    ) -> __.typx.Annotated[
        __.typx.Self,
        __.ddoc.Doc( "New Array control with element removed." ),
        __.ddoc.Raises(
            __.IndexOutOfRange,
            "If index is invalid."
        ),
        __.ddoc.Raises(
            __.SizeConstraintViolation,
            "If removal would violate size constraint." )
    ]:
        ''' Produces copy with element at index removed. '''
        if not 0 <= index < len( self.current ):
            raise __.IndexOutOfRange(
                index = index, length = len( self.current )
            )
        new_elements = self.current[ :index ] + self.current[ index + 1: ]
        return self.copy( new_elements )

    def insert_at(
        self,
        index: __.typx.Annotated[
            int, __.ddoc.Doc( "Index at which to insert element." )
        ],
        element: __.typx.Annotated[
            __.typx.Any, __.ddoc.Doc( "Element to insert." )
        ]
    ) -> __.typx.Annotated[
        __.typx.Self,
        __.ddoc.Doc( "New Array control with element inserted." ),
        __.ddoc.Raises(
            __.ControlInvalidity, "If the element is invalid."
        ),
        __.ddoc.Raises(
            __.IndexOutOfRange,
            "If index is invalid."
        ),
        __.ddoc.Raises(
            __.SizeConstraintViolation,
            "If insertion would violate size constraint."
        ),
        __.ddoc.Raises(
            __.UniquenessConstraintViolation,
            "If insertion would violate uniqueness constraint."
        )
    ]:
        ''' Produces copy with element inserted at index. '''
        if not 0 <= index <= len( self.current ):
            raise __.IndexOutOfRange(
                index = index,
                length = len( self.current ),
                operation = "insertion"
            )
        new_elements = (
            *self.current[ :index ], element, *self.current[ index: ]
        )
        return self.copy( new_elements )

    def reorder(
        self,
        new_order: __.typx.Annotated[
            __.cabc.Sequence[ int ],
            __.ddoc.Doc(
                "New order as sequence of indices (must be permutation)."
            )
        ]
    ) -> __.typx.Annotated[
        __.typx.Self,
        __.ddoc.Doc( "New Array control with reordered elements." ),
        __.ddoc.Raises(
            __.InvalidPermutation,
            "If new_order is not a valid permutation."
        )
    ]:
        ''' Produces copy with elements reordered. '''
        if len( new_order ) != len( self.current ):
            raise __.InvalidPermutation(
                expected_length = len( self.current ),
                actual_length = len( new_order )
            )
        if set( new_order ) != set( range( len( self.current ) ) ):
            raise __.InvalidPermutation(
                expected_length = len( self.current )
            )
        try:
            new_elements = tuple( self.current[ i ] for i in new_order )
        except IndexError as exception:  # pragma: no cover
            raise __.InvalidPermutation(  # pragma: no cover
                expected_length = len( self.current )
            ) from exception
        return self.copy( new_elements )

    def serialize(
        self
    ) -> __.typx.Annotated[
        list[ __.typx.Any ],
        __.ddoc.Doc( "JSON-compatible representation of the current value." )
    ]:
        ''' Serializes current value. '''
        return self.definition.serialize_value( self.current )
