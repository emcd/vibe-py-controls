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


''' Interval control type implementation. '''


from . import __


# Floating-point comparison tolerance for step alignment validation
_FLOAT_EPSILON = 1e-10


class IntervalHints( __.immut.DataclassObject ):
    ''' UI hints for interval controls. '''

    widget_preference: __.typx.Annotated[
        __.typx.Literal[ "slider", "spinbox" ] | None,  # noqa: F821
        __.ddoc.Doc(
            "Preferred widget type (slider for visual selection, spinbox "
            "for numeric entry)."
        )
    ] = None
    orientation: __.typx.Annotated[
        __.typx.Literal[ "horizontal", "vertical" ] | None,  # noqa: F821
        __.ddoc.Doc( "Orientation for slider widgets." )
    ] = None
    show_ticks: __.typx.Annotated[
        bool, __.ddoc.Doc( "Whether to display tick marks on sliders." )
    ] = False
    show_value: __.typx.Annotated[
        bool, __.ddoc.Doc( "Whether to display the current value." )
    ] = True
    label: __.typx.Annotated[
        __.typx.Optional[ str ],
        __.ddoc.Doc( "Display label for the control." )
    ] = None
    help_text: __.typx.Annotated[
        __.typx.Optional[ str ], __.ddoc.Doc( "Help or tooltip text." )
    ] = None


class IntervalDefinition( __.ControlDefinition ):
    ''' Interval control definition.

        Defines a control that accepts numeric values within a specified range
        with optional step granularity.
    '''

    minimum: __.typx.Annotated[
        float, __.ddoc.Doc( "Minimum allowed value (inclusive)." )
    ]
    maximum: __.typx.Annotated[
        float, __.ddoc.Doc( "Maximum allowed value (inclusive)." )
    ]
    default: __.typx.Annotated[
        float, __.ddoc.Doc( "Default numeric value." )
    ]
    grade: __.typx.Annotated[
        __.typx.Optional[ float ],
        __.ddoc.Doc(
            "Grade increment for discrete intervals. None means continuous."
        )
    ] = None
    validation_message: __.typx.Annotated[
        str,
        __.ddoc.Doc( "Custom error message for validation failures." )
    ] = "Value must be numeric"
    hints: __.typx.Annotated[
        IntervalHints, __.ddoc.Doc( "UI hints for rendering." )
    ] = __.dcls.field( default_factory = IntervalHints )

    def __post_init__( self ) -> None:
        ''' Validates definition parameters. '''
        if not isinstance( self.minimum, ( int, float ) ):
            raise __.DefinitionInvalidity(
                parameter = "minimum", issue = "must be numeric"
            )
        if not isinstance( self.maximum, ( int, float ) ):
            raise __.DefinitionInvalidity(
                parameter = "maximum", issue = "must be numeric"
            )
        if self.minimum > self.maximum:
            raise __.DefinitionInvalidity(
                parameter = "minimum", issue = "cannot exceed maximum"
            )
        if not isinstance( self.default, ( int, float ) ):
            raise __.DefinitionInvalidity(
                parameter = "default", issue = "must be numeric"
            )
        if not self.minimum <= self.default <= self.maximum:
            raise __.DefinitionInvalidity(
                parameter = "default",
                issue = "must be within bounds",
                detail = "minimum and maximum"
            )
        if self.grade is not None:
            if not isinstance( self.grade, ( int, float ) ):
                raise __.DefinitionInvalidity(
                    parameter = "grade", issue = "must be numeric"
                )
            if self.grade <= 0:
                raise __.DefinitionInvalidity(
                    parameter = "grade", issue = "must be positive"
                )

    def validate_value(
        self,
        value: __.typx.Annotated[
            __.typx.Any, __.ddoc.Doc( "Value to validate." )
        ]
    ) -> __.typx.Annotated[
        float,
        __.ddoc.Doc( "Value if it is valid numeric within range." ),
        __.ddoc.Raises(
            __.ControlInvalidity,
            "If value is not numeric."
        ),
        __.ddoc.Raises(
            __.BoundsConstraintViolation,
            "If value is out of range."
        ),
        __.ddoc.Raises(
            __.StepConstraintViolation,
            "If value violates step constraint."
        )
    ]:
        ''' Validates numeric value with range and step checking. '''
        if not isinstance( value, ( int, float ) ):
            raise __.ControlInvalidity( self.validation_message )
        if not self.minimum <= value <= self.maximum:
            raise __.BoundsConstraintViolation(
                minimum = self.minimum,
                maximum = self.maximum,
                actual = float( value )
            )
        if self.grade is not None:
            steps_from_minimum = ( value - self.minimum ) / self.grade
            deviation = abs( steps_from_minimum - round( steps_from_minimum ) )
            if not deviation < _FLOAT_EPSILON:
                raise __.StepConstraintViolation(
                    step = self.grade, minimum = self.minimum
                )
        return float( value )

    def produce_control(
        self,
        initial: __.typx.Annotated[
            __.typx.Any,
            __.ddoc.Doc(
                "Initial value for the control. If absent, uses default."
            )
        ] = __.absent
    ) -> __.typx.Annotated[
        'Interval',
        __.ddoc.Doc( "New Interval control." ),
        __.ddoc.Raises(
            __.ControlInvalidity, "If the initial value is invalid."
        )
    ]:
        ''' Produces interval control. '''
        if __.is_absent( initial ):
            validated = self.default
        else:
            validated = self.validate_value( initial )
        return Interval( definition = self, current = validated )

    def serialize_value(
        self,
        value: __.typx.Annotated[
            float, __.ddoc.Doc( "Numeric value to serialize." )
        ]
    ) -> __.typx.Annotated[ float, __.ddoc.Doc( "Value unchanged." ) ]:
        ''' Serializes numeric value.

            Numeric values serialize as-is since they are JSON-compatible.
        '''
        return value

    def produce_default(
        self
    ) -> __.typx.Annotated[ float, __.ddoc.Doc( "Default numeric value." ) ]:
        ''' Produces the default value for this control. '''
        return self.default


class Interval( __.Control ):
    ''' Interval control.

        Represents the current state of an interval control. Immutable - all
        operations return new instances.
    '''

    definition: __.typx.Annotated[
        IntervalDefinition, __.ddoc.Doc( "Interval definition." )
    ]
    current: __.typx.Annotated[
        float, __.ddoc.Doc( "Current numeric value." )
    ]

    def copy(
        self,
        value: __.typx.Annotated[
            __.typx.Any, __.ddoc.Doc( "New numeric value." )
        ]
    ) -> __.typx.Annotated[
        __.typx.Self,
        __.ddoc.Doc( "New Interval control with the updated value." ),
        __.ddoc.Raises(
            __.ControlInvalidity, "If the new value is invalid."
        )
    ]:
        ''' Produces copy with a new value (immutable operation). '''
        validated = self.definition.validate_value( value )
        return type( self )(
            definition = self.definition, current = validated
        )

    def increment(
        self
    ) -> __.typx.Annotated[
        __.typx.Self,
        __.ddoc.Doc( "New Interval control with incremented value." ),
        __.ddoc.Raises(
            __.IncrementOperationFailure,
            "If grade is not defined."
        ),
        __.ddoc.Raises(
            __.BoundsConstraintViolation,
            "If increment would exceed maximum."
        )
    ]:
        ''' Produces copy with value incremented by grade. '''
        if self.definition.grade is None:
            raise __.IncrementOperationFailure( operation = "increment" )
        new_value = self.current + self.definition.grade
        return self.copy( new_value )

    def decrement(
        self
    ) -> __.typx.Annotated[
        __.typx.Self,
        __.ddoc.Doc( "New Interval control with decremented value." ),
        __.ddoc.Raises(
            __.IncrementOperationFailure,
            "If grade is not defined."
        ),
        __.ddoc.Raises(
            __.BoundsConstraintViolation,
            "If decrement would fall below minimum."
        )
    ]:
        ''' Produces copy with value decremented by grade. '''
        if self.definition.grade is None:
            raise __.IncrementOperationFailure( operation = "decrement" )
        new_value = self.current - self.definition.grade
        return self.copy( new_value )

    def serialize(
        self
    ) -> __.typx.Annotated[
        float,
        __.ddoc.Doc( "JSON-compatible representation of the current value." )
    ]:
        ''' Serializes current value. '''
        return self.definition.serialize_value( self.current )
