neural_lam.toc_integration
==========================

.. py:module:: neural_lam.toc_integration

.. autoapi-nested-parse::

   Table of Contents (TOC) integration module.

   This module provides functionality to integrate API reference documentation
   into the main documentation table of contents.





Module Contents
---------------

.. py:function:: add_api_reference_to_toc(toc_data: Dict[str, Any], api_ref_file: str = 'autoapi/index', position: str = 'after_tutorials') -> Dict[str, Any]

   Add API reference section to the table of contents.

   :param toc_data: Current TOC structure.
   :type toc_data: Dict[str, Any]
   :param api_ref_file: Path to the API reference index file (default: "autoapi/index").
   :type api_ref_file: str, optional
   :param position: Where to place the API reference:
                    - "after_tutorials": After tutorials section
                    - "at_end": At the end of parts
                    - "before_advanced": Before advanced guides
   :type position: str, optional

   :returns: * *Dict[str, Any]* -- Updated TOC structure with API reference section.
             * **Validates** (*Requirements 3.1, 3.2*)


.. py:function:: get_api_reference_section(toc_data: Dict[str, Any]) -> Optional[Dict[str, Any]]

   Get the API reference section from the TOC.

   :param toc_data: TOC structure.
   :type toc_data: Dict[str, Any]

   :returns: The API reference section if it exists, None otherwise.
   :rtype: Optional[Dict[str, Any]]


.. py:function:: load_toc(toc_path: str) -> Dict[str, Any]

   Load the Jupyter Book table of contents.

   :param toc_path: Path to the _toc.yml file.
   :type toc_path: str

   :returns: Parsed TOC structure.
   :rtype: Dict[str, Any]


.. py:function:: remove_api_reference_from_toc(toc_data: Dict[str, Any]) -> Dict[str, Any]

   Remove the API reference section from the TOC.

   :param toc_data: TOC structure.
   :type toc_data: Dict[str, Any]

   :returns: Updated TOC structure without API reference section.
   :rtype: Dict[str, Any]


.. py:function:: save_toc(toc_path: str, toc_data: Dict[str, Any]) -> None

   Save the Jupyter Book table of contents.

   :param toc_path: Path to the _toc.yml file.
   :type toc_path: str
   :param toc_data: TOC structure to save.
   :type toc_data: Dict[str, Any]


