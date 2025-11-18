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
from .exceptions import ControlInvalidity


class ControlDefinition( __.immut.DataclassProtocol, __.typx.Protocol ):
    ''' Protocol for control definitions.

        A control definition is an immutable specification that describes:
        - How to validate values
        - How to create controls with initial values
        - How to serialize values
        - What the default value should be

        Uses both structural (Protocol) and nominal (ABC from
        DataclassProtocol) typing to enable flexible implementation while
        enforcing required methods.
    '''

    @__.abc.abstractmethod
    def validate_value(
        self,
        value: __.typx.Annotated[
            __.typx.Any, __.ddoc.Doc( "Value to validate." )
        ]
    ) -> __.typx.Annotated[
        __.typx.Any,
        __.ddoc.Doc( "Validated (and possibly normalized) value." ),
        __.ddoc.Raises( ControlInvalidity, "If the value is invalid." )
    ]:
        ''' Validates and normalizes a value for this control. '''
        ...

    @__.abc.abstractmethod
    def produce_control(
        self,
        initial: __.typx.Annotated[
            __.typx.Any,
            __.ddoc.Doc(
                "Initial value for the control. "
                "If absent, uses default."
            )
        ] = __.absent
    ) -> __.typx.Annotated[
        'Control',
        __.ddoc.Doc( "New control with the initial value." ),
        __.ddoc.Raises(
            ControlInvalidity, "If the initial value is invalid."
        )
    ]:
        ''' Produces a control from this definition. '''
        ...

    @__.abc.abstractmethod
    def serialize_value(
        self,
        value: __.typx.Annotated[
            __.typx.Any, __.ddoc.Doc( "Value to serialize." )
        ]
    ) -> __.typx.Annotated[
        __.typx.Any,
        __.ddoc.Doc( "JSON-compatible representation of the value." )
    ]:
        ''' Serializes a value to JSON-compatible format. '''
        ...

    @__.abc.abstractmethod
    def produce_default(
        self
    ) -> __.typx.Annotated[ __.typx.Any, __.ddoc.Doc( "Default value." ) ]:
        ''' Produces the default value for this control. '''
        ...


class Control( __.immut.DataclassProtocol, __.typx.Protocol ):
    ''' Protocol for controls.

        A control represents the current state of a control, pairing a
        definition with a current value. Controls are immutable - all
        update operations return new control instances.

        Uses both structural (Protocol) and nominal (ABC from
        DataclassProtocol) typing to enable flexible implementation while
        enforcing required methods.
    '''

    definition: ControlDefinition
    current: __.typx.Any

    @__.abc.abstractmethod
    def copy(
        self,
        new_value: __.typx.Annotated[
            __.typx.Any, __.ddoc.Doc( "New value for the control." )
        ]
    ) -> __.typx.Annotated[
        __.typx.Self,
        __.ddoc.Doc( "New control instance with the updated value." ),
        __.ddoc.Raises( ControlInvalidity, "If the new value is invalid." )
    ]:
        ''' Produces copy with a new value (immutable operation). '''
        ...

    @__.abc.abstractmethod
    def serialize(
        self
    ) -> __.typx.Annotated[
        __.typx.Any,
        __.ddoc.Doc( "JSON-compatible representation of the current value." )
    ]:
        ''' Serializes current value to JSON-compatible format. '''
        ...
