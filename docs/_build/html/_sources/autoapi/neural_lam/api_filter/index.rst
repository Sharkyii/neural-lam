neural_lam.api_filter
=====================

.. py:module:: neural_lam.api_filter

.. autoapi-nested-parse::

   API filtering and customization module.

   This module provides functionality to filter and customize which API elements
   are included in the generated documentation.







Module Contents
---------------

.. py:class:: FilterConfig

   Configuration for API filtering.


   .. py:attribute:: exclude_modules
      :type:  List[str]
      :value: []


      Modules to explicitly exclude.


   .. py:attribute:: include_dunder
      :type:  bool
      :value: False


      Whether to include dunder (__name__) members.


   .. py:attribute:: include_modules
      :type:  List[str]
      :value: []


      Modules to explicitly include (empty = include all).


   .. py:attribute:: include_private
      :type:  bool
      :value: False


      Whether to include private (underscore-prefixed) members.


.. py:function:: filter_module_members(members: List[Any], config: Optional[FilterConfig] = None) -> List[Any]

   Filter module members based on configuration.

   :param members: List of (name, object) tuples to filter.
   :type members: List[Any]
   :param config: Filter configuration.
   :type config: FilterConfig, optional

   :returns: * *List[Any]* -- Filtered list of members.
             * **Validates** (*Requirements 1.5, 7.1, 7.3*)


.. py:function:: get_deprecation_message(obj: Any) -> Optional[str]

   Extract the deprecation message from an object's docstring.

   :param obj: The object to check.
   :type obj: Any

   :returns: * *Optional[str]* -- The deprecation message, or None if not deprecated.
             * **Validates** (*Requirement 7.2*)


.. py:function:: has_skip_directive(obj: Any) -> bool

   Check if an API element has an autodoc skip directive.

   :param obj: The object to check.
   :type obj: Any

   :returns: * *bool* -- True if the element should be skipped.
             * **Validates** (*Requirement 7.3*)


.. py:function:: is_deprecated(obj: Any) -> bool

   Check if an API element is marked as deprecated.

   :param obj: The object to check.
   :type obj: Any

   :returns: * *bool* -- True if the element is deprecated.
             * **Validates** (*Requirement 7.2*)


.. py:function:: is_dunder(name: str) -> bool

   Check if a name is a dunder method (__name__).

   :param name: The name to check.
   :type name: str

   :returns: True if the name is a dunder.
   :rtype: bool


.. py:function:: is_module_included(module_name: str, config: FilterConfig) -> bool

   Check if a module should be included based on configuration.

   :param module_name: The module name to check.
   :type module_name: str
   :param config: Filter configuration.
   :type config: FilterConfig

   :returns: * *bool* -- True if the module should be included.
             * **Validates** (*Requirement 7.4*)


.. py:function:: is_private(name: str) -> bool

   Check if a name is private (underscore-prefixed).

   :param name: The name to check.
   :type name: str

   :returns: * *bool* -- True if the name is private.
             * **Validates** (*Requirements 1.5, 7.1*)


.. py:function:: should_include(name: str, config: Optional[FilterConfig] = None) -> bool

   Determine if an API element should be included in documentation.

   :param name: The element name.
   :type name: str
   :param config: Filter configuration. Uses defaults if not provided.
   :type config: FilterConfig, optional

   :returns: * *bool* -- True if the element should be included.
             * **Validates** (*Requirements 1.5, 7.1*)
