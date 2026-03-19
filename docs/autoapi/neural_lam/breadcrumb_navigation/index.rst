neural_lam.breadcrumb_navigation
================================

.. py:module:: neural_lam.breadcrumb_navigation

.. autoapi-nested-parse::

   Breadcrumb navigation generator for API documentation.

   This module provides functionality to generate breadcrumb navigation
   for module hierarchies in the API reference.





Module Contents
---------------

.. py:class:: BreadcrumbItem

   Represents a single breadcrumb item.


   .. py:attribute:: is_current
      :type:  bool
      :value: False


      Whether this is the current page.


   .. py:attribute:: name
      :type:  str

      Display name.


   .. py:attribute:: path
      :type:  str

      Path to the page.


.. py:class:: BreadcrumbNavigationGenerator(base_path: str = 'autoapi')

   Generator for breadcrumb navigation.

   Initialize the breadcrumb generator.

   :param base_path: Base path for API reference pages (default: "autoapi").
   :type base_path: str, optional


   .. py:method:: generate_breadcrumbs(module_path: str) -> List[BreadcrumbItem]

      Generate breadcrumb items for a module path.

      :param module_path: Full module path (e.g., "neural_lam.data.datastore").
      :type module_path: str

      :returns: * *List[BreadcrumbItem]* -- List of breadcrumb items from root to current module.
                * **Validates** (*Requirement 3.5*)



   .. py:method:: generate_breadcrumbs_for_class(module_path: str, class_name: str) -> List[BreadcrumbItem]

      Generate breadcrumb items for a class.

      :param module_path: Full module path.
      :type module_path: str
      :param class_name: Name of the class.
      :type class_name: str

      :returns: * *List[BreadcrumbItem]* -- List of breadcrumb items from root to current class.
                * **Validates** (*Requirement 3.5*)



   .. py:method:: generate_breadcrumbs_for_function(module_path: str, function_name: str) -> List[BreadcrumbItem]

      Generate breadcrumb items for a function.

      :param module_path: Full module path.
      :type module_path: str
      :param function_name: Name of the function.
      :type function_name: str

      :returns: * *List[BreadcrumbItem]* -- List of breadcrumb items from root to current function.
                * **Validates** (*Requirement 3.5*)



   .. py:method:: generate_html(breadcrumbs: List[BreadcrumbItem]) -> str

      Generate HTML for breadcrumb navigation.

      :param breadcrumbs: List of breadcrumb items.
      :type breadcrumbs: List[BreadcrumbItem]

      :returns: * *str* -- HTML for the breadcrumb navigation.
                * **Validates** (*Requirement 3.5*)



   .. py:method:: generate_markdown(breadcrumbs: List[BreadcrumbItem]) -> str

      Generate Markdown for breadcrumb navigation.

      :param breadcrumbs: List of breadcrumb items.
      :type breadcrumbs: List[BreadcrumbItem]

      :returns: * *str* -- Markdown for the breadcrumb navigation.
                * **Validates** (*Requirement 3.5*)



   .. py:method:: generate_rst(breadcrumbs: List[BreadcrumbItem]) -> str

      Generate reStructuredText for breadcrumb navigation.

      :param breadcrumbs: List of breadcrumb items.
      :type breadcrumbs: List[BreadcrumbItem]

      :returns: * *str* -- reStructuredText for the breadcrumb navigation.
                * **Validates** (*Requirement 3.5*)



   .. py:method:: validate_breadcrumbs(breadcrumbs: List[BreadcrumbItem]) -> Tuple[bool, List[str]]

      Validate breadcrumb structure.

      :param breadcrumbs: List of breadcrumb items to validate.
      :type breadcrumbs: List[BreadcrumbItem]

      :returns: * *Tuple[bool, List[str]]* -- Tuple of (is_valid, error_messages).
                * **Validates** (*Requirement 3.5*)



   .. py:attribute:: base_path
      :value: 'autoapi'



