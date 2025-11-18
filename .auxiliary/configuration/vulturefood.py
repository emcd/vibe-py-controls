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

# --- Protocols (Base classes used for structural typing) ---
from vibecontrols.protocols import Control, ControlDefinition
_ = Control
_ = ControlDefinition

# --- Validation (Public API) ---
from vibecontrols.validation import (
    ChoiceValidator,
    CompositeValidator,
    LengthValidator,
    RangeValidator,
    TypeValidator,
)
_ = ChoiceValidator
_ = CompositeValidator
_ = LengthValidator
_ = RangeValidator
_ = TypeValidator

# --- Boolean Control (Public API and Protocol Implementations) ---
from vibecontrols.controls.boolean import (
    Boolean,
    BooleanDefinition,
    BooleanHints,
)

# Whitelist protocol method implementations
_ = BooleanDefinition.create_control
_ = BooleanDefinition.produce_default
_ = Boolean.toggle
_ = Boolean.serialize

# Whitelist dataclass attributes (used by external code)
_ = BooleanHints.widget_preference
_ = BooleanHints.label
_ = BooleanHints.help_text
_ = BooleanDefinition.hints
