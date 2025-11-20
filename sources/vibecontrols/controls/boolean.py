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


''' Boolean control type implementation. '''


from . import __


class BooleanHints( __.immut.DataclassObject ):
    ''' UI hints for boolean controls. '''

    widget_preference: __.typx.Annotated[
        __.typx.Literal[ "checkbox", "toggle", "radio" ] | None,  # noqa: F821
        __.ddoc.Doc(
            "Preferred widget type (checkbox, toggle, radio)."
        )
    ] = None
    label: __.typx.Annotated[
        __.typx.Optional[ str ],
        __.ddoc.Doc( "Display label for the control." )
    ] = None
    help_text: __.typx.Annotated[
        __.typx.Optional[ str ], __.ddoc.Doc( "Help or tooltip text." )
    ] = None


class BooleanDefinition( __.ControlDefinition ):
    ''' Boolean control definition.

        Defines a control that accepts true/false values with strict type
        checking.
    '''

    default: __.typx.Annotated[
        bool, __.ddoc.Doc( "Default boolean value." )
    ] = False
    validation_message: __.typx.Annotated[
        str, __.ddoc.Doc( "Custom error message for validation failures." )
    ] = "Value must be a boolean"
    hints: __.typx.Annotated[
        BooleanHints, __.ddoc.Doc( "UI hints for rendering." )
    ] = __.dcls.field( default_factory = BooleanHints )

    def validate_value(
        self,
        value: __.typx.Annotated[
            __.typx.Any, __.ddoc.Doc( "Value to validate." )
        ]
    ) -> __.typx.Annotated[
        bool,
        __.ddoc.Doc( "Value if it is a boolean." ),
        __.ddoc.Raises( __.ControlInvalidity, "If value is not a boolean." )
    ]:
        ''' Validates boolean value with strict type checking. '''
        if not isinstance( value, bool ):
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
        'Boolean',
        __.ddoc.Doc( "New Boolean control." ),
        __.ddoc.Raises(
            __.ControlInvalidity, "If the initial value is invalid."
        )
    ]:
        ''' Produces boolean control. '''
        if __.is_absent( initial ):
            validated = self.default
        else:
            validated = self.validate_value( initial )
        return Boolean( definition = self, current = validated )

    def serialize_value(
        self,
        value: __.typx.Annotated[
            bool, __.ddoc.Doc( "Boolean value to serialize." )
        ]
    ) -> __.typx.Annotated[ bool, __.ddoc.Doc( "Value unchanged." ) ]:
        ''' Serializes boolean value.

        Boolean values serialize as-is since they are JSON-compatible.
        '''
        return value

    def produce_default(
        self
    ) -> __.typx.Annotated[ bool, __.ddoc.Doc( "Default boolean value." ) ]:
        ''' Produces the default value for this control. '''
        return self.default


class Boolean( __.Control ):
    ''' Boolean control.

        Represents the current state of a boolean control. Immutable - all
        operations return new instances.
    '''

    definition: __.typx.Annotated[
        BooleanDefinition, __.ddoc.Doc( "Boolean definition." )
    ]
    current: __.typx.Annotated[
        bool, __.ddoc.Doc( "Current boolean value." )
    ]

    def copy(
        self,
        value: __.typx.Annotated[
            __.typx.Any, __.ddoc.Doc( "New boolean value." )
        ]
    ) -> __.typx.Annotated[
        __.typx.Self,
        __.ddoc.Doc( "New Boolean control with the updated value." ),
        __.ddoc.Raises(
            __.ControlInvalidity, "If the new value is invalid."
        )
    ]:
        ''' Produces copy with a new value (immutable operation). '''
        validated = self.definition.validate_value( value )
        return type( self )(
            definition = self.definition, current = validated
        )

    def toggle(
        self
    ) -> __.typx.Annotated[
        __.typx.Self,
        __.ddoc.Doc( "New Boolean control with the toggled value." )
    ]:
        ''' Toggles the boolean value. '''
        return self.copy( not self.current )

    def serialize(
        self
    ) -> __.typx.Annotated[
        bool,
        __.ddoc.Doc( "JSON-compatible representation of the current value." )
    ]:
        ''' Serializes current value. '''
        return self.definition.serialize_value( self.current )
