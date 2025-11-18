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


from dataclasses import field

from . import __


class BooleanHints( __.immut.DataclassObject ):
    ''' UI hints for boolean controls.

    Attributes:
        widget_preference: Preferred widget type (checkbox, toggle, radio)
        label: Display label for the control
        help_text: Help or tooltip text
    '''

    widget_preference: (
        __.typx.Literal[ "checkbox", "toggle", "radio" ] | None  # noqa: F821
    ) = None
    label: str | None = None
    help_text: str | None = None


class BooleanDefinition( __.immut.DataclassObject ):
    ''' Boolean control definition.

    Defines a control that accepts true/false values with strict type checking.

    Attributes:
        default: Default boolean value
        validation_message: Custom error message for validation failures
        hints: UI hints for rendering
    '''

    default: bool = False
    validation_message: str = "Value must be a boolean"
    hints: BooleanHints = field( default_factory = BooleanHints )

    def validate_value(
        self,
        value: __.typx.Annotated[
            __.typx.Any, __.ddoc.Doc( "Value to validate." )
        ]
    ) -> __.typx.Annotated[ bool, __.ddoc.Doc( "Value if it is a boolean." ) ]:
        ''' Validates boolean value with strict type checking.

        Raises:
            ControlInvalidity: If value is not a boolean.
        '''
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
        'Boolean', __.ddoc.Doc( "New Boolean control." )
    ]:
        ''' Produces boolean control.

        Raises:
            ControlInvalidity: If the initial value is invalid.
        '''
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


class Boolean( __.immut.DataclassObject ):
    ''' Boolean control.

    Represents the current state of a boolean control. Immutable - all
    operations return new instances.

    Attributes:
        definition: The boolean definition
        current: Current boolean value
    '''

    definition: BooleanDefinition
    current: bool

    def copy(
        self,
        new_value: __.typx.Annotated[
            __.typx.Any, __.ddoc.Doc( "New boolean value." )
        ]
    ) -> __.typx.Annotated[
        __.typx.Self,
        __.ddoc.Doc( "New Boolean control with the updated value." )
    ]:
        ''' Produces copy with a new value (immutable operation).

        Raises:
            ControlInvalidity: If the new value is invalid.
        '''
        validated = self.definition.validate_value( new_value )
        return Boolean(  # type: ignore[return-value]
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
