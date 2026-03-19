neural_lam.search_integration
=============================

.. py:module:: neural_lam.search_integration

.. autoapi-nested-parse::

   Search index integration for API documentation.

   This module provides functionality to integrate API reference content
   into the documentation search index.





Module Contents
---------------

.. py:class:: SearchIndexIntegration

   Integration system for API content in search index.

   Initialize the search index integration.


   .. py:method:: add_class_to_index(class_name: str, module_name: str, class_docstring: str, page: str) -> SearchableContent

      Add a class to the search index.

      :param class_name: Name of the class.
      :type class_name: str
      :param module_name: Name of the module containing the class.
      :type module_name: str
      :param class_docstring: Class docstring.
      :type class_docstring: str
      :param page: Path to the class page.
      :type page: str

      :returns: * *SearchableContent* -- The added searchable content.
                * **Validates** (*Requirement 3.4*)



   .. py:method:: add_function_to_index(function_name: str, module_name: str, function_docstring: str, page: str) -> SearchableContent

      Add a function to the search index.

      :param function_name: Name of the function.
      :type function_name: str
      :param module_name: Name of the module containing the function.
      :type module_name: str
      :param function_docstring: Function docstring.
      :type function_docstring: str
      :param page: Path to the function page.
      :type page: str

      :returns: * *SearchableContent* -- The added searchable content.
                * **Validates** (*Requirement 3.4*)



   .. py:method:: add_module_to_index(module_name: str, module_docstring: str, page: str) -> SearchableContent

      Add a module to the search index.

      :param module_name: Name of the module.
      :type module_name: str
      :param module_docstring: Module docstring.
      :type module_docstring: str
      :param page: Path to the module page.
      :type page: str

      :returns: * *SearchableContent* -- The added searchable content.
                * **Validates** (*Requirement 3.4*)



   .. py:method:: export_to_json() -> List[Dict[str, Any]]

      Export the search index to JSON format.

      :returns: Search index as a list of dictionaries.
      :rtype: List[Dict[str, Any]]



   .. py:method:: get_all_by_type(content_type: str) -> List[SearchableContent]

      Get all searchable content of a specific type.

      :param content_type: Type to filter by: 'module', 'class', 'function'.
      :type content_type: str

      :returns: All searchable content items of the specified type.
      :rtype: List[SearchableContent]



   .. py:method:: get_index_size() -> int

      Get the number of items in the search index.

      :returns: Number of searchable items.
      :rtype: int



   .. py:method:: search(query: str) -> List[SearchableContent]

      Search the index for content matching the query.

      :param query: Search query.
      :type query: str

      :returns: * *List[SearchableContent]* -- Matching searchable content items.
                * **Validates** (*Requirement 3.6*)



   .. py:method:: search_by_type(query: str, content_type: str) -> List[SearchableContent]

      Search the index for content of a specific type.

      :param query: Search query.
      :type query: str
      :param content_type: Type to filter by: 'module', 'class', 'function'.
      :type content_type: str

      :returns: Matching searchable content items of the specified type.
      :rtype: List[SearchableContent]



   .. py:attribute:: searchable_items
      :type:  List[SearchableContent]
      :value: []



.. py:class:: SearchableContent

   Represents searchable content from API documentation.


   .. py:attribute:: anchor
      :type:  Optional[str]
      :value: None


      Optional anchor within the page.


   .. py:attribute:: content
      :type:  str

      Main content text.


   .. py:attribute:: keywords
      :type:  List[str]

      Search keywords.


   .. py:attribute:: page
      :type:  str

      Page path.


   .. py:attribute:: title
      :type:  str

      Title of the content.


   .. py:attribute:: type
      :type:  str

      'module', 'class', 'function'.

      :type: Type


