.. vim: set fileencoding=utf-8:
.. -*- coding: utf-8 -*-
.. +--------------------------------------------------------------------------+
   |                                                                          |
   | Licensed under the Apache License, Version 2.0 (the "License");          |
   | you may not use this file except in compliance with the License.         |
   | You may obtain a copy of the License at                                  |
   |                                                                          |
   |     http://www.apache.org/licenses/LICENSE-2.0                           |
   |                                                                          |
   | Unless required by applicable law or agreed to in writing, software      |
   | distributed under the License is distributed on an "AS IS" BASIS,        |
   | WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. |
   | See the License for the specific language governing permissions and      |
   | limitations under the License.                                           |
   |                                                                          |
   +--------------------------------------------------------------------------+

*******************************************************************************
                                 vibe-controls                                 
*******************************************************************************

.. image:: https://github.com/emcd/vibe-py-controls/actions/workflows/tester.yaml/badge.svg?branch=master&event=push
   :alt: Tests Status
   :target: https://github.com/emcd/vibe-py-controls/actions/workflows/tester.yaml

.. image:: https://emcd.github.io/vibe-py-controls/coverage.svg
   :alt: Code Coverage Percentage
   :target: https://github.com/emcd/vibe-py-controls/actions/workflows/tester.yaml

.. image:: https://img.shields.io/github/license/emcd/vibe-py-controls
   :alt: Project License
   :target: https://github.com/emcd/vibe-py-controls/blob/master/LICENSE.txt


🔧 **vibe-controls** is an abstract controls layer that provides UI framework-agnostic control definitions for building data-driven interfaces. It offers immutable, strongly-typed controls with composable validation that can bridge multiple UI frameworks (Panel, Streamlit, web forms, etc.) to backend systems like LLM APIs and prompt templates.

**Key Features** ⭐

- **Framework Agnostic**: Core abstractions work with any UI framework - map controls to widgets in Panel, Streamlit, Qt, or custom frameworks
- **Immutable by Design**: All controls are immutable using ``frigid`` - updates return new instances, preventing accidental state mutations
- **Composable Validation**: Lightweight, reusable validators that chain together without external dependencies (no Pydantic or attrs)
- **Type-Safe**: Leverages Protocol and DataclassProtocol for both structural and nominal typing with full static analysis support
- **JSON Serialization**: Built-in serialization to/from JSON for state persistence and transmission
- **Rich UI Hints**: Control-specific hint classes provide rendering guidance without coupling to specific frameworks

**Core Control Types** 📦

Currently implements:

- **Boolean**: True/false controls with strict type checking and toggle operations
- *(Future)*: Text, Interval (numeric ranges), Options (enumerations), Array (recursive containers)

**Examples** 💡

Create a boolean control with UI hints:

.. code-block:: python

    from vibecontrols.controls import BooleanDefinition, BooleanHints

    # Define a control specification
    definition = BooleanDefinition(
        default=False,
        hints=BooleanHints(
            label="Enable Dark Mode",
            help_text="Toggle dark theme for the interface"
        )
    )

    # Create an instance with initial value
    control = definition.produce_control(initial=True)
    print(control.current)  # True

    # Immutable updates
    toggled = control.toggle()
    print(toggled.current)  # False

Map controls to your UI framework of choice - the abstract layer handles validation and state while your adapter handles rendering.


Installation 📦
===============================================================================

Method: Install Python Package
-------------------------------------------------------------------------------

Install via `uv <https://github.com/astral-sh/uv/blob/main/README.md>`_ ``pip``
command:

::

    uv pip install vibe-controls

Or, install via ``pip``:

::

    pip install vibe-controls


**Use Cases** 🎯

- **LLM Interface Configuration**: Define controls for temperature, top_p, model selection, and other LLM parameters that map to different provider APIs
- **Prompt Template Parameters**: Create reusable control definitions that integrate with Jinja2 or other template systems
- **Multi-Framework UIs**: Define controls once, render in Panel for prototyping, Streamlit for dashboards, and web forms for production
- **Configuration Management**: Serialize control states to JSON for persistence, versioning, and transmission

**Architecture** 🏗️

The project follows a clean Definition/Control split pattern:

- **Definitions**: Immutable specifications that know how to validate, create controls, and serialize
- **Controls**: Pair a definition with current state - immutable instances that return new copies on updates
- **Validators**: Composable validation logic that can be reused across control types
- **UI Hints**: Optional rendering guidance that adapters can use to map controls to framework-specific widgets

For detailed architecture documentation, see the `architecture directory <architecture/>`_.


Contribution 🤝
===============================================================================

Contribution to this project is welcome! However, it must follow the `code of
conduct
<https://emcd.github.io/python-project-common/stable/sphinx-html/common/conduct.html>`_
for the project.

Please file bug reports and feature requests in the `issue tracker
<https://github.com/emcd/vibe-py-controls/issues>`_ or submit `pull
requests <https://github.com/emcd/vibe-py-controls/pulls>`_ to
improve the source code or documentation.

For development guidance and standards, please see the `development guide
<https://emcd.github.io/vibe-py-controls/stable/sphinx-html/contribution.html#development>`_.


Additional Indicia
===============================================================================

.. image:: https://img.shields.io/github/last-commit/emcd/vibe-py-controls
   :alt: GitHub last commit
   :target: https://github.com/emcd/vibe-py-controls

.. image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-grayscale-inverted-border-orange.json
   :alt: Copier
   :target: https://github.com/copier-org/copier

.. image:: https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg
   :alt: Hatch
   :target: https://github.com/pypa/hatch

.. image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit
   :alt: pre-commit
   :target: https://github.com/pre-commit/pre-commit

.. image:: https://microsoft.github.io/pyright/img/pyright_badge.svg
   :alt: Pyright
   :target: https://microsoft.github.io/pyright

.. image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json
   :alt: Ruff
   :target: https://github.com/astral-sh/ruff


Other Projects by This Author 🌟
===============================================================================


* `python-absence <https://github.com/emcd/python-absence>`_ (`absence <https://pypi.org/project/absence/>`_ on PyPI) 

  🕳️ A Python library package which provides a **sentinel for absent values** - a falsey, immutable singleton that represents the absence of a value in contexts where ``None`` or ``False`` may be valid values.
* `python-accretive <https://github.com/emcd/python-accretive>`_ (`accretive <https://pypi.org/project/accretive/>`_ on PyPI) 

  🌌 A Python library package which provides **accretive data structures** - collections which can grow but never shrink.
* `python-classcore <https://github.com/emcd/python-classcore>`_ (`classcore <https://pypi.org/project/classcore/>`_ on PyPI) 

  🏭 A Python library package which provides **foundational class factories and decorators** for providing classes with attributes immutability and concealment and other custom behaviors.
* `python-detextive <https://github.com/emcd/python-detextive>`_ (`detextive <https://pypi.org/project/detextive/>`_ on PyPI) 

  🕵️ A Python library which provides consolidated text detection capabilities for reliable content analysis. Offers MIME type detection, character set detection, and line separator processing.
* `python-dynadoc <https://github.com/emcd/python-dynadoc>`_ (`dynadoc <https://pypi.org/project/dynadoc/>`_ on PyPI) 

  📝 A Python library package which bridges the gap between **rich annotations** and **automatic documentation generation** with configurable renderers and support for reusable fragments.
* `python-falsifier <https://github.com/emcd/python-falsifier>`_ (`falsifier <https://pypi.org/project/falsifier/>`_ on PyPI) 

  🎭 A very simple Python library package which provides a **base class for falsey objects** - objects that evaluate to ``False`` in boolean contexts.
* `python-frigid <https://github.com/emcd/python-frigid>`_ (`frigid <https://pypi.org/project/frigid/>`_ on PyPI) 

  🔒 A Python library package which provides **immutable data structures** - collections which cannot be modified after creation.
* `python-icecream-truck <https://github.com/emcd/python-icecream-truck>`_ (`icecream-truck <https://pypi.org/project/icecream-truck/>`_ on PyPI) 

  🍦 **Flavorful Debugging** - A Python library which enhances the powerful and well-known ``icecream`` package with flavored traces, configuration hierarchies, customized outputs, ready-made recipes, and more.
* `python-librovore <https://github.com/emcd/python-librovore>`_ (`librovore <https://pypi.org/project/librovore/>`_ on PyPI) 

  🐲 **Documentation Search Engine** - An intelligent documentation search and extraction tool that provides both a command-line interface for humans and an MCP (Model Context Protocol) server for AI agents. Search across Sphinx and MkDocs sites with fuzzy matching, extract clean markdown content, and integrate seamlessly with AI development workflows.
* `python-mimeogram <https://github.com/emcd/python-mimeogram>`_ (`mimeogram <https://pypi.org/project/mimeogram/>`_ on PyPI) 

  📨 A command-line tool for **exchanging collections of files with Large Language Models** - bundle multiple files into a single clipboard-ready document while preserving directory structure and metadata... good for code reviews, project sharing, and LLM interactions.
