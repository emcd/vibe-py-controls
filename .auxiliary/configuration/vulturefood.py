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


''' Whitelist for Vulture dead code detection.

Items listed here are part of the public API or protocol implementations
that Vulture cannot detect as being used.
'''


# --- Type Aliases (Public API) ---
from vibecontrols.__.nomina import (
    ComparisonResult,
    NominativeArguments,
    PositionalArguments,
    package_name,
)
_ = ComparisonResult
_ = NominativeArguments
_ = PositionalArguments
_ = package_name

# --- Exceptions (Public API) ---
from vibecontrols.exceptions import (
    ConstraintViolation,
    ControlInvalidity,
    DefinitionInvalidity,
)
_ = ConstraintViolation
_ = ControlInvalidity
_ = DefinitionInvalidity

# --- Interfaces (Base classes used for structural typing) ---
from vibecontrols.interfaces import Control, ControlDefinition
_ = Control
_ = ControlDefinition

# --- Validation (Public API) ---
from vibecontrols.validation import (
    ClassValidator,
    CompositeValidator,
    IntervalValidator,
    SelectionValidator,
    SizeValidator,
)
_ = ClassValidator
_ = CompositeValidator
_ = IntervalValidator
_ = SelectionValidator
_ = SizeValidator

# --- Boolean Control (Public API and Protocol Implementations) ---
from vibecontrols.controls.boolean import (
    Boolean,
    BooleanDefinition,
    BooleanHints,
)

# Whitelist protocol method implementations
_ = BooleanDefinition.produce_control
_ = BooleanDefinition.produce_default
_ = Boolean.toggle
_ = Boolean.serialize

# Whitelist dataclass attributes (used by external code)
_ = BooleanHints.widget_preference
_ = BooleanHints.label
_ = BooleanHints.help_text
_ = BooleanDefinition.hints

# --- Text Control (Public API and Protocol Implementations) ---
from vibecontrols.controls.text import (
    Text,
    TextDefinition,
    TextHints,
)

_ = TextDefinition.produce_control
_ = TextDefinition.produce_default
_ = Text.clear
_ = Text.serialize
_ = TextHints.widget_preference
_ = TextHints.multiline
_ = TextHints.placeholder
_ = TextHints.label
_ = TextHints.help_text
_ = TextDefinition.hints

# --- Interval Control (Public API and Protocol Implementations) ---
from vibecontrols.controls.interval import (
    Interval,
    IntervalDefinition,
    IntervalHints,
)

_ = IntervalDefinition.produce_control
_ = IntervalDefinition.produce_default
_ = Interval.increment
_ = Interval.decrement
_ = Interval.serialize
_ = IntervalHints.widget_preference
_ = IntervalHints.orientation
_ = IntervalHints.show_ticks
_ = IntervalHints.show_value
_ = IntervalHints.label
_ = IntervalHints.help_text
_ = IntervalDefinition.hints

# --- Options Control (Public API and Protocol Implementations) ---
from vibecontrols.controls.options import (
    Options,
    OptionsDefinition,
    OptionsHints,
)

_ = OptionsDefinition.produce_control
_ = OptionsDefinition.produce_default
_ = Options.cycle_next
_ = Options.cycle_previous
_ = Options.serialize
_ = OptionsHints.widget_preference
_ = OptionsHints.label
_ = OptionsHints.help_text
_ = OptionsDefinition.hints

# --- Array Control (Public API and Protocol Implementations) ---
from vibecontrols.controls.array import (
    Array,
    ArrayDefinition,
    ArrayHints,
)

_ = ArrayDefinition.produce_control
_ = ArrayDefinition.produce_default
_ = Array.remove_at
_ = Array.insert_at
_ = Array.reorder
_ = Array.serialize
_ = ArrayHints.orientation
_ = ArrayHints.collapsible
_ = ArrayHints.initially_collapsed
_ = ArrayHints.border
_ = ArrayHints.title
_ = ArrayHints.label
_ = ArrayHints.help_text
_ = ArrayDefinition.hints
