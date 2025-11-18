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


''' Base protocols for control definitions and controls. '''


from . import __


class ControlDefinition( __.immut.DataclassProtocol, __.typx.Protocol ):
    ''' Protocol for control definitions.

    A control definition is an immutable specification that describes:
    - How to validate values
    - How to create controls with initial values
    - How to serialize values
    - What the default value should be

    Uses both structural (Protocol) and nominal (ABC from DataclassProtocol)
    typing to enable flexible implementation while enforcing required methods.
    '''

    @__.abc.abstractmethod
    def validate_value( self, value: __.typx.Any ) -> __.typx.Any:
        ''' Validate and normalize a value for this control.

        Args:
            value: The value to validate

        Returns:
            The validated (and possibly normalized) value

        Raises:
            ValidationError: If the value is invalid
        '''
        ...

    @__.abc.abstractmethod
    def create_control( self, initial: __.typx.Any = __.absent ) -> 'Control':
        ''' Create a control from this definition.

        Args:
            initial: Initial value for the control. If absent, uses default.

        Returns:
            A new control with the initial value

        Raises:
            ValidationError: If the initial value is invalid
        '''
        ...

    @__.abc.abstractmethod
    def serialize_value( self, value: __.typx.Any ) -> __.typx.Any:
        ''' Serialize a value to JSON-compatible format.

        Args:
            value: The value to serialize

        Returns:
            JSON-compatible representation of the value
        '''
        ...

    @__.abc.abstractmethod
    def produce_default( self ) -> __.typx.Any:
        ''' Produce the default value for this control.

        Returns:
            The default value
        '''
        ...


class Control( __.immut.DataclassProtocol, __.typx.Protocol ):
    ''' Protocol for controls.

    A control represents the current state of a control, pairing a definition
    with a current value. Controls are immutable - all update operations
    return new control instances.

    Uses both structural (Protocol) and nominal (ABC from DataclassProtocol)
    typing to enable flexible implementation while enforcing required methods.
    '''

    definition: ControlDefinition
    current: __.typx.Any

    @__.abc.abstractmethod
    def update( self, new_value: __.typx.Any ) -> __.typx.Self:
        ''' Update to a new value (immutable operation).

        Args:
            new_value: The new value for the control

        Returns:
            A new control instance with the updated value

        Raises:
            ValidationError: If the new value is invalid
        '''
        ...

    @__.abc.abstractmethod
    def serialize( self ) -> __.typx.Any:
        ''' Serialize current value to JSON-compatible format.

        Returns:
            JSON-compatible representation of the current value
        '''
        ...
