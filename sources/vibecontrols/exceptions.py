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


''' Family of exceptions for package API. '''


from . import __


class Omniexception( __.immut.exceptions.Omniexception ):
    ''' Base for all exceptions raised by package API. '''


class Omnierror( Omniexception, Exception ):
    ''' Base for error exceptions raised by package API. '''


class ControlError( Omnierror ):
    ''' Base exception for control-related errors. '''


class ControlInvalidity( ControlError, ValueError ):
    ''' Control value invalidity.

    Raised when a value does not meet the requirements defined by a control
    definition (e.g., wrong type, out of range, invalid format).
    '''


class ConstraintViolation( ControlInvalidity ):
    ''' Constraint violation.

    Raised when a value violates a specific constraint (e.g., minimum/maximum
    bounds, size limits, uniqueness requirements).
    '''


class DefinitionInvalidity( ControlError, ValueError ):
    ''' Control definition invalidity.

    Raised when a control definition is improperly configured (e.g., invalid
    parameters, inconsistent settings, missing required fields).
    '''
