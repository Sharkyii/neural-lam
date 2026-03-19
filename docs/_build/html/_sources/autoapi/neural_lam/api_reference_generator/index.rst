neural_lam.api_reference_generator
==================================

.. py:module:: neural_lam.api_reference_generator

.. autoapi-nested-parse::

   API reference page generation module.

   This module provides functionality to generate reStructuredText API reference
   pages for modules, classes, and functions.







Module Contents
---------------

.. py:class:: ClassInfo

   Information about a class for page generation.


   .. py:attribute:: attributes
      :type:  List[dict]

      Attributes in the class.


   .. py:attribute:: bases
      :type:  List[str]

      Base classes.


   .. py:attribute:: docstring
      :type:  str

      Class docstring.


   .. py:attribute:: methods
      :type:  List[neural_lam.docstring_extraction.DocstringMetadata]

      Methods in the class.


   .. py:attribute:: mro
      :type:  List[str]

      Method resolution order.


   .. py:attribute:: name
      :type:  str

      Class name.


.. py:class:: FunctionInfo

   Information about a function for page generation.


   .. py:attribute:: docstring
      :type:  str

      Function docstring.


   .. py:attribute:: name
      :type:  str

      Function name.


   .. py:attribute:: parameters
      :type:  List[neural_lam.docstring_extraction.Parameter]

      Function parameters.


   .. py:attribute:: raises
      :type:  List[neural_lam.docstring_extraction.Exception]

      Documented exceptions.


   .. py:attribute:: returns
      :type:  Optional[neural_lam.docstring_extraction.Return]

      Return value documentation.


   .. py:attribute:: signature
      :type:  str

      Function signature.


.. py:function:: generate_class_page(class_name: str, module_name: str, class_docstring: str, methods: List[neural_lam.docstring_extraction.DocstringMetadata], attributes: List[dict], bases: List[str], mro: List[str]) -> str

   Generate a reStructuredText class reference page.

   :param class_name: Name of the class.
   :type class_name: str
   :param module_name: Name of the module containing the class.
   :type module_name: str
   :param class_docstring: Class docstring.
   :type class_docstring: str
   :param methods: Methods in the class.
   :type methods: List[DocstringMetadata]
   :param attributes: Attributes in the class.
   :type attributes: List[dict]
   :param bases: Base classes.
   :type bases: List[str]
   :param mro: Method resolution order.
   :type mro: List[str]

   :returns: * *str* -- Generated reStructuredText content for the class page.
             * **Validates** (*Requirements 2.3, 7.5*)


.. py:function:: generate_function_page(function_name: str, module_name: str, signature: str, docstring: str, parameters: List[neural_lam.docstring_extraction.Parameter], returns: Optional[neural_lam.docstring_extraction.Return], raises: List[neural_lam.docstring_extraction.Exception]) -> str

   Generate a reStructuredText function reference page.

   :param function_name: Name of the function.
   :type function_name: str
   :param module_name: Name of the module containing the function.
   :type module_name: str
   :param signature: Function signature.
   :type signature: str
   :param docstring: Function docstring.
   :type docstring: str
   :param parameters: Function parameters.
   :type parameters: List[Parameter]
   :param returns: Return value documentation.
   :type returns: Optional[Return]
   :param raises: Documented exceptions.
   :type raises: List[DocException]

   :returns: * *str* -- Generated reStructuredText content for the function page.
             * **Validates** (*Requirements 2.4*)


.. py:function:: generate_module_page(module_name: str, module_docstring: str, classes: List[neural_lam.docstring_extraction.DocstringMetadata], functions: List[neural_lam.docstring_extraction.DocstringMetadata]) -> str

   Generate a reStructuredText module reference page.

   :param module_name: Name of the module.
   :type module_name: str
   :param module_docstring: Module docstring.
   :type module_docstring: str
   :param classes: Classes in the module.
   :type classes: List[DocstringMetadata]
   :param functions: Functions in the module.
   :type functions: List[DocstringMetadata]

   :returns: * *str* -- Generated reStructuredText content for the module page.
             * **Validates** (*Requirements 2.1, 2.2*)


