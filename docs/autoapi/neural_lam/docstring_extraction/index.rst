neural_lam.docstring_extraction
===============================

.. py:module:: neural_lam.docstring_extraction

.. autoapi-nested-parse::

   Docstring extraction and metadata parsing module.

   This module provides functionality to extract and parse docstrings from Python
   modules, classes, and functions, converting them into structured metadata.







Module Contents
---------------

.. py:class:: DocstringMetadata

   Structured representation of parsed docstring.


   .. py:attribute:: deprecated
      :type:  bool
      :value: False


      Whether deprecated.


   .. py:attribute:: description
      :type:  str

      Main docstring text.


   .. py:attribute:: examples
      :type:  List[str]
      :value: []


      Code examples.


   .. py:attribute:: name
      :type:  str

      Function/class name.


   .. py:attribute:: notes
      :type:  Optional[str]
      :value: None


      Additional notes.


   .. py:attribute:: parameters
      :type:  List[Parameter]
      :value: []


      Function parameters.


   .. py:attribute:: raises
      :type:  List[Exception]
      :value: []


      Documented exceptions.


   .. py:attribute:: returns
      :type:  Optional[Return]
      :value: None


      Return value documentation.


   .. py:attribute:: see_also
      :type:  List[str]
      :value: []


      Related items.


   .. py:attribute:: type
      :type:  str

      'function', 'class', or 'module'.

      :type: Type


.. py:class:: Exception

   Exception documentation.


   .. py:attribute:: description
      :type:  str

      When raised.


   .. py:attribute:: name
      :type:  str

      Exception type.


.. py:class:: Parameter

   Function parameter documentation.


   .. py:attribute:: default
      :type:  Optional[str]
      :value: None


      Default value.


   .. py:attribute:: description
      :type:  str

      Parameter description.


   .. py:attribute:: name
      :type:  str

      Parameter name.


   .. py:attribute:: type
      :type:  str

      Parameter type.


.. py:class:: Return

   Return value documentation.


   .. py:attribute:: description
      :type:  str

      Return description.


   .. py:attribute:: type
      :type:  str

      Return type.


.. py:function:: extract_class_docstring(cls) -> Optional[DocstringMetadata]

   Extract docstring metadata from a class.

   :param cls: The class to extract docstring from.
   :type cls: type

   :returns: Metadata for the class docstring, or None if no docstring exists.
   :rtype: Optional[DocstringMetadata]


.. py:function:: extract_class_members(cls) -> dict

   Extract all public members from a class.

   :param cls: The class to extract members from.
   :type cls: type

   :returns: Dictionary with keys 'methods' and 'attributes' containing extracted metadata.
   :rtype: dict


.. py:function:: extract_function_docstring(func) -> Optional[DocstringMetadata]

   Extract docstring metadata from a function or method.

   :param func: The function or method to extract docstring from.
   :type func: callable

   :returns: Metadata for the function docstring, or None if no docstring exists.
   :rtype: Optional[DocstringMetadata]


.. py:function:: extract_module_docstring(module) -> Optional[DocstringMetadata]

   Extract docstring metadata from a module.

   :param module: The module to extract docstring from.
   :type module: module

   :returns: Metadata for the module docstring, or None if no docstring exists.
   :rtype: Optional[DocstringMetadata]


.. py:function:: extract_module_members(module) -> dict

   Extract all public members from a module.

   :param module: The module to extract members from.
   :type module: module

   :returns: Dictionary with keys 'classes' and 'functions' containing extracted metadata.
   :rtype: dict


