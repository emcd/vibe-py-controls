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


''' Options control type implementation. '''


from . import __


class OptionsHints( __.immut.DataclassObject ):
    ''' UI hints for options controls. '''

    widget_preference: __.typx.Annotated[
        __.typx.Literal[ "select", "radio", "dropdown" ] | None,  # noqa: F821
        __.ddoc.Doc(
            "Preferred widget type (select for dropdown, radio for "
            "radio buttons)."
        )
    ] = None
    label: __.typx.Annotated[
        __.typx.Optional[ str ],
        __.ddoc.Doc( "Display label for the control." )
    ] = None
    help_text: __.typx.Annotated[
        __.typx.Optional[ str ], __.ddoc.Doc( "Help or tooltip text." )
    ] = None


class OptionsDefinition( __.immut.DataclassObject ):
    ''' Options control definition.

        Defines a control that accepts values from a predefined set of
        choices. Supports both single and multiple selection.
    '''

    choices: __.typx.Annotated[
        __.cabc.Sequence[ __.typx.Any ],
        __.ddoc.Doc( "Available choices for selection." )
    ]
    default: __.typx.Annotated[
        __.typx.Any | __.cabc.Sequence[ __.typx.Any ],
        __.ddoc.Doc(
            "Default value (single choice for single-select, sequence "
            "for multi-select)."
        )
    ]
    allow_multiple: __.typx.Annotated[
        bool,
        __.ddoc.Doc( "Whether multiple values can be selected." )
    ] = False
    validation_message: __.typx.Annotated[
        str,
        __.ddoc.Doc( "Custom error message for validation failures." )
    ] = "Value must be from available choices"
    hints: __.typx.Annotated[
        OptionsHints, __.ddoc.Doc( "UI hints for rendering." )
    ] = __.dcls.field( default_factory = OptionsHints )

    def __post_init__( self ) -> None:
        ''' Validates definition parameters and normalizes choices. '''
        if not self.choices:
            raise __.DefinitionInvalidity(
                parameter = "choices", issue = "cannot be empty"
            )
        # Normalize choices to tuple
        object.__setattr__( self, 'choices', tuple( self.choices ) )
        # Validate uniqueness of choices
        if len( self.choices ) != len( set( self.choices ) ):
            raise __.DefinitionInvalidity(
                parameter = "choices", issue = "must be unique"
            )
        # Validate default value
        try:
            self.validate_value( self.default )
        except __.ControlInvalidity as exception:
            raise __.DefinitionInvalidity(
                parameter = "default",
                issue = "is invalid",
                detail = str( exception )
            ) from exception

    def validate_value(
        self,
        value: __.typx.Annotated[
            __.typx.Any, __.ddoc.Doc( "Value to validate." )
        ]
    ) -> __.typx.Annotated[
        __.typx.Any | tuple[ __.typx.Any, ... ],
        __.ddoc.Doc(
            "Value if valid (single choice or tuple of choices)."
        ),
        __.ddoc.Raises(
            __.ControlInvalidity,
            "If value is not from available choices."
        ),
        __.ddoc.Raises(
            __.ConstraintViolation,
            "If value violates selection constraints."
        )
    ]:
        ''' Validates value is from available choices. '''
        if self.allow_multiple:
            if not isinstance( value, __.cabc.Sequence ):
                raise __.TypeInvalidity( expected = "a sequence" )
            # Type narrowing: after isinstance check, treat as Sequence[Any]
            sequence_value = __.typx.cast(
                __.cabc.Sequence[ __.typx.Any ], value
            )
            if not sequence_value:
                raise __.SizeConstraintViolation(
                    minimum = 1, maximum = __.absent, actual = 0,
                    label = "Selection count"
                )
            for item in sequence_value:
                if item not in self.choices:
                    raise __.SelectionConstraintViolation( value = item )
            # Check for duplicates
            if len( sequence_value ) != len( set( sequence_value ) ):
                raise __.UniquenessConstraintViolation( )
            return tuple( sequence_value )
        if value not in self.choices:
            raise __.ControlInvalidity( self.validation_message )
        return value

    def produce_control(
        self,
        initial: __.typx.Annotated[
            __.typx.Any,
            __.ddoc.Doc(
                "Initial value for the control. If absent, uses default."
            )
        ] = __.absent
    ) -> __.typx.Annotated[
        'Options',
        __.ddoc.Doc( "New Options control." ),
        __.ddoc.Raises(
            __.ControlInvalidity, "If the initial value is invalid."
        )
    ]:
        ''' Produces options control. '''
        if __.is_absent( initial ):
            validated = self.validate_value( self.default )
        else:
            validated = self.validate_value( initial )
        return Options( definition = self, current = validated )

    def serialize_value(
        self,
        value: __.typx.Annotated[
            __.typx.Any | tuple[ __.typx.Any, ... ],
            __.ddoc.Doc( "Value to serialize." )
        ]
    ) -> __.typx.Annotated[
        __.typx.Any | list[ __.typx.Any ],
        __.ddoc.Doc(
            "Value serialized (single value or list for multi-select)."
        )
    ]:
        ''' Serializes value.

            Single selections serialize as-is. Multiple selections serialize
            as lists for JSON compatibility.
        '''
        if self.allow_multiple:
            return list( value )
        return value

    def produce_default(
        self
    ) -> __.typx.Annotated[
        __.typx.Any | tuple[ __.typx.Any, ... ],
        __.ddoc.Doc( "Default value." )
    ]:
        ''' Produces the default value for this control. '''
        return self.validate_value( self.default )


class Options( __.immut.DataclassObject ):
    ''' Options control.

        Represents the current state of an options control. Immutable - all
        operations return new instances.
    '''

    definition: __.typx.Annotated[
        OptionsDefinition, __.ddoc.Doc( "Options definition." )
    ]
    current: __.typx.Annotated[
        __.typx.Any | tuple[ __.typx.Any, ... ],
        __.ddoc.Doc(
            "Current selected value (single choice or tuple of choices)."
        )
    ]

    def copy(
        self,
        new_value: __.typx.Annotated[
            __.typx.Any,
            __.ddoc.Doc( "New value (single choice or sequence of choices)." )
        ]
    ) -> __.typx.Annotated[
        __.typx.Self,
        __.ddoc.Doc( "New Options control with the updated value." ),
        __.ddoc.Raises(
            __.ControlInvalidity, "If the new value is invalid."
        )
    ]:
        ''' Produces copy with a new value (immutable operation). '''
        validated = self.definition.validate_value( new_value )
        return Options(  # type: ignore[return-value]
            definition = self.definition, current = validated
        )

    def cycle_next(
        self
    ) -> __.typx.Annotated[
        __.typx.Self,
        __.ddoc.Doc( "New Options control with next choice selected." ),
        __.ddoc.Raises(
            __.CycleOperationFailure,
            "If control allows multiple selections."
        )
    ]:
        ''' Produces copy with next choice selected (wraps to first). '''
        if self.definition.allow_multiple:
            raise __.CycleOperationFailure( )
        current_index = self.definition.choices.index( self.current )
        next_index = ( current_index + 1 ) % len( self.definition.choices )
        return self.copy( self.definition.choices[ next_index ] )

    def cycle_previous(
        self
    ) -> __.typx.Annotated[
        __.typx.Self,
        __.ddoc.Doc( "New Options control with previous choice selected." ),
        __.ddoc.Raises(
            __.CycleOperationFailure,
            "If control allows multiple selections."
        )
    ]:
        ''' Produces copy with previous choice selected (wraps to last). '''
        if self.definition.allow_multiple:
            raise __.CycleOperationFailure( )
        current_index = self.definition.choices.index( self.current )
        previous_index = (
            ( current_index - 1 ) % len( self.definition.choices )
        )
        return self.copy( self.definition.choices[ previous_index ] )

    def serialize(
        self
    ) -> __.typx.Annotated[
        __.typx.Any | list[ __.typx.Any ],
        __.ddoc.Doc( "JSON-compatible representation of the current value." )
    ]:
        ''' Serializes current value. '''
        return self.definition.serialize_value( self.current )
