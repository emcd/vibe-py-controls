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


from dataclasses import dataclass, field

from . import __


@dataclass( frozen = True )
class BooleanHints:
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

    def validate_value( self, value: __.typx.Any ) -> bool:
        ''' Validate boolean value with strict type checking.

        Args:
            value: The value to validate

        Returns:
            The value if it is a boolean

        Raises:
            ControlInvalidity: If value is not a boolean
        '''
        if not isinstance( value, bool ):
            raise __.ControlInvalidity( self.validation_message )
        return value

    def create_control(
        self,
        initial: __.typx.Any = __.absent
    ) -> 'Boolean':
        ''' Create boolean control.

        Args:
            initial: Initial value for the control. If absent, uses default.

        Returns:
            A new Boolean control

        Raises:
            ControlInvalidity: If the initial value is invalid
        '''
        if __.is_absent( initial ):
            validated = self.default
        else:
            validated = self.validate_value( initial )
        return Boolean( definition = self, current = validated )

    def serialize_value( self, value: bool ) -> bool:
        ''' Serialize boolean value.

        Boolean values serialize as-is since they are JSON-compatible.

        Args:
            value: The boolean value to serialize

        Returns:
            The value unchanged
        '''
        return value

    def produce_default( self ) -> bool:
        ''' Produce the default value for this control.

        Returns:
            The default boolean value
        '''
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

    def update( self, new_value: __.typx.Any ) -> __.typx.Self:
        ''' Update to a new value (immutable operation).

        Args:
            new_value: The new boolean value

        Returns:
            A new Boolean control with the updated value

        Raises:
            ControlInvalidity: If the new value is invalid
        '''
        validated = self.definition.validate_value( new_value )
        return Boolean(  # type: ignore[return-value]
            definition = self.definition, current = validated
        )

    def toggle( self ) -> __.typx.Self:
        ''' Toggle the boolean value.

        Returns:
            A new Boolean control with the toggled value
        '''
        return self.update( not self.current )

    def serialize( self ) -> bool:
        ''' Serialize current value.

        Returns:
            JSON-compatible representation of the current value
        '''
        return self.definition.serialize_value( self.current )
