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


''' Text control type implementation. '''


from . import __


class TextHints( __.immut.DataclassObject ):
    ''' UI hints for text controls. '''

    widget_preference: __.typx.Annotated[
        __.typx.Literal[ "input", "textarea" ] | None,  # noqa: F821
        __.ddoc.Doc(
            "Preferred widget type (input for single-line, textarea for "
            "multi-line)."
        )
    ] = None
    multiline: __.typx.Annotated[
        bool,
        __.ddoc.Doc( "Whether text should support multiple lines." )
    ] = False
    placeholder: __.typx.Annotated[
        __.typx.Optional[ str ],
        __.ddoc.Doc( "Placeholder text shown when empty." )
    ] = None
    label: __.typx.Annotated[
        __.typx.Optional[ str ],
        __.ddoc.Doc( "Display label for the control." )
    ] = None
    help_text: __.typx.Annotated[
        __.typx.Optional[ str ], __.ddoc.Doc( "Help or tooltip text." )
    ] = None


class TextDefinition( __.immut.DataclassObject ):
    ''' Text control definition.

        Defines a control that accepts string values with optional length
        constraints and pattern validation.
    '''

    default: __.typx.Annotated[
        str, __.ddoc.Doc( "Default text value." )
    ] = ''
    count_min: __.typx.Annotated[
        __.typx.Optional[ int ],
        __.ddoc.Doc(
            "Minimum allowed character count (inclusive). "
            "None means no minimum."
        )
    ] = None
    count_max: __.typx.Annotated[
        __.typx.Optional[ int ],
        __.ddoc.Doc(
            "Maximum allowed character count (inclusive). "
            "None means no maximum."
        )
    ] = None
    validation_message: __.typx.Annotated[
        str,
        __.ddoc.Doc( "Custom error message for validation failures." )
    ] = "Value must be a string"
    hints: __.typx.Annotated[
        TextHints, __.ddoc.Doc( "UI hints for rendering." )
    ] = __.dcls.field( default_factory = TextHints )

    def __post_init__( self ) -> None:
        ''' Validates definition parameters. '''
        if self.count_min is not None and self.count_min < 0:
            raise __.DefinitionInvalidity(
                parameter = "count_min", issue = "cannot be negative"
            )
        if self.count_max is not None and self.count_max < 0:
            raise __.DefinitionInvalidity(
                parameter = "count_max", issue = "cannot be negative"
            )
        if (
            self.count_min is not None
            and self.count_max is not None
            and self.count_min > self.count_max
        ):
            raise __.DefinitionInvalidity(
                parameter = "count_min",
                issue = "cannot exceed",
                detail = "maximum count"
            )

    def validate_value(
        self,
        value: __.typx.Annotated[
            __.typx.Any, __.ddoc.Doc( "Value to validate." )
        ]
    ) -> __.typx.Annotated[
        str,
        __.ddoc.Doc( "Value if it is a valid string." ),
        __.ddoc.Raises( __.ControlInvalidity, "If value is not a string." ),
        __.ddoc.Raises(
            __.SizeConstraintViolation,
            "If value violates length constraints."
        )
    ]:
        ''' Validates text value with type and character count checking. '''
        if not isinstance( value, str ):
            raise __.ControlInvalidity( self.validation_message )
        count = len( value )
        if self.count_min is not None and count < self.count_min:
            raise __.SizeConstraintViolation(
                minimum = self.count_min,
                maximum = (
                    __.absent if self.count_max is None else self.count_max
                ),
                actual = count,
                label = "Text character count"
            )
        if self.count_max is not None and count > self.count_max:
            raise __.SizeConstraintViolation(
                minimum = (
                    __.absent if self.count_min is None else self.count_min
                ),
                maximum = self.count_max,
                actual = count,
                label = "Text character count"
            )
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
        'Text',
        __.ddoc.Doc( "New Text control." ),
        __.ddoc.Raises(
            __.ControlInvalidity, "If the initial value is invalid."
        )
    ]:
        ''' Produces text control. '''
        if __.is_absent( initial ):
            validated = self.default
        else:
            validated = self.validate_value( initial )
        return Text( definition = self, current = validated )

    def serialize_value(
        self,
        value: __.typx.Annotated[
            str, __.ddoc.Doc( "Text value to serialize." )
        ]
    ) -> __.typx.Annotated[ str, __.ddoc.Doc( "Value unchanged." ) ]:
        ''' Serializes text value.

            Text values serialize as-is since they are JSON-compatible.
        '''
        return value

    def produce_default(
        self
    ) -> __.typx.Annotated[ str, __.ddoc.Doc( "Default text value." ) ]:
        ''' Produces the default value for this control. '''
        return self.default


class Text( __.immut.DataclassObject ):
    ''' Text control.

        Represents the current state of a text control. Immutable - all
        operations return new instances.
    '''

    definition: __.typx.Annotated[
        TextDefinition, __.ddoc.Doc( "Text definition." )
    ]
    current: __.typx.Annotated[
        str, __.ddoc.Doc( "Current text value." )
    ]

    def copy(
        self,
        new_value: __.typx.Annotated[
            __.typx.Any, __.ddoc.Doc( "New text value." )
        ]
    ) -> __.typx.Annotated[
        __.typx.Self,
        __.ddoc.Doc( "New Text control with the updated value." ),
        __.ddoc.Raises(
            __.ControlInvalidity, "If the new value is invalid."
        )
    ]:
        ''' Produces copy with a new value (immutable operation). '''
        validated = self.definition.validate_value( new_value )
        return Text(  # type: ignore[return-value]
            definition = self.definition, current = validated
        )

    def clear( self ) -> __.typx.Annotated[
        __.typx.Self,
        __.ddoc.Doc( "New Text control with empty value." )
    ]:
        ''' Produces copy with empty text. '''
        return self.copy( '' )

    def serialize(
        self
    ) -> __.typx.Annotated[
        str,
        __.ddoc.Doc( "JSON-compatible representation of the current value." )
    ]:
        ''' Serializes current value. '''
        return self.definition.serialize_value( self.current )
