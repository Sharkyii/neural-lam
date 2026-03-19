neural_lam.search_index_integration
===================================

.. py:module:: neural_lam.search_index_integration

.. autoapi-nested-parse::

   Search index integration for API documentation.

   This module provides functionality to integrate API reference content
   into the documentation search index.





Module Contents
---------------

.. py:class:: SearchIndexEntry

   Represents an entry in the search index.


   .. py:attribute:: api_path
      :type:  str

      Full API path (e.g., 'neural_lam.module.ClassName').


   .. py:attribute:: content
      :type:  str

      Content to be indexed.


   .. py:attribute:: entry_type
      :type:  str

      'module', 'class', 'function', 'method'.

      :type: Type of entry


   .. py:attribute:: keywords
      :type:  List[str]
      :value: []


      Keywords for searching.


   .. py:attribute:: module
      :type:  str

      Module containing the item.


   .. py:attribute:: title
      :type:  str

      Title of the indexed item.


   .. py:attribute:: url
      :type:  str

      URL to the documentation page.


.. py:class:: SearchIndexIntegrator(search_index_path: Optional[pathlib.Path] = None)

   Integrates API documentation into the search index.

   Initialize the search index integrator.

   :param search_index_path: Path to the search index file (JSON).
   :type search_index_path: Optional[Path]


   .. py:method:: add_class_entry(class_name: str, module_name: str, class_docstring: str, url: str, bases: Optional[List[str]] = None) -> None

      Add a class entry to the search index.

      :param class_name: Name of the class.
      :type class_name: str
      :param module_name: Name of the module containing the class.
      :type module_name: str
      :param class_docstring: Class docstring.
      :type class_docstring: str
      :param url: URL to the class documentation page.
      :type url: str
      :param bases: Base classes.
      :type bases: Optional[List[str]]
      :param Validates:
      :type Validates: Requirements 3.4



   .. py:method:: add_entry(entry: SearchIndexEntry) -> None

      Add an entry to the search index.

      :param entry: Entry to add to the index.
      :type entry: SearchIndexEntry



   .. py:method:: add_function_entry(function_name: str, module_name: str, function_docstring: str, url: str, signature: Optional[str] = None) -> None

      Add a function entry to the search index.

      :param function_name: Name of the function.
      :type function_name: str
      :param module_name: Name of the module containing the function.
      :type module_name: str
      :param function_docstring: Function docstring.
      :type function_docstring: str
      :param url: URL to the function documentation page.
      :type url: str
      :param signature: Function signature.
      :type signature: Optional[str]
      :param Validates:
      :type Validates: Requirements 3.4



   .. py:method:: add_method_entry(method_name: str, class_name: str, module_name: str, method_docstring: str, url: str) -> None

      Add a method entry to the search index.

      :param method_name: Name of the method.
      :type method_name: str
      :param class_name: Name of the class containing the method.
      :type class_name: str
      :param module_name: Name of the module containing the class.
      :type module_name: str
      :param method_docstring: Method docstring.
      :type method_docstring: str
      :param url: URL to the method documentation page.
      :type url: str
      :param Validates:
      :type Validates: Requirements 3.4



   .. py:method:: add_module_entry(module_name: str, module_docstring: str, url: str) -> None

      Add a module entry to the search index.

      :param module_name: Name of the module.
      :type module_name: str
      :param module_docstring: Module docstring.
      :type module_docstring: str
      :param url: URL to the module documentation page.
      :type url: str



   .. py:method:: get_entries_by_module(module_name: str) -> List[SearchIndexEntry]

      Get all entries for a specific module.

      :param module_name: Name of the module.
      :type module_name: str

      :returns: List of entries for the module.
      :rtype: List[SearchIndexEntry]



   .. py:method:: get_entries_by_type(entry_type: str) -> List[SearchIndexEntry]

      Get all entries of a specific type.

      :param entry_type: Type of entries to retrieve ('module', 'class', 'function', 'method').
      :type entry_type: str

      :returns: List of entries of the specified type.
      :rtype: List[SearchIndexEntry]



   .. py:method:: get_statistics() -> Dict[str, int]

      Get statistics about the search index.

      :returns: Dictionary with statistics.
      :rtype: Dict[str, int]



   .. py:method:: load_from_json(input_path: pathlib.Path) -> None

      Load the search index from a JSON file.

      :param input_path: Path to load the JSON file from.
      :type input_path: Path



   .. py:method:: save_to_json(output_path: pathlib.Path) -> None

      Save the search index to a JSON file.

      :param output_path: Path to save the JSON file.
      :type output_path: Path



   .. py:method:: search(query: str) -> List[SearchIndexEntry]

      Search the index for entries matching the query.

      :param query: Search query.
      :type query: str

      :returns: List of matching entries.
      :rtype: List[SearchIndexEntry]



   .. py:attribute:: entries
      :type:  Dict[str, SearchIndexEntry]


   .. py:attribute:: modules
      :type:  Set[str]


   .. py:attribute:: search_index_path
      :value: None
