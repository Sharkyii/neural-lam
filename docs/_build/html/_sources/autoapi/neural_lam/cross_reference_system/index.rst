neural_lam.cross_reference_system
=================================

.. py:module:: neural_lam.cross_reference_system

.. autoapi-nested-parse::

   Cross-reference system for linking documentation pages.

   This module provides functionality to create and manage cross-references
   between tutorials, guides, and API reference documentation.





Module Contents
---------------

.. py:class:: CrossReference

   Represents a cross-reference between documentation pages.


   .. py:attribute:: anchor
      :type:  Optional[str]
      :value: None


      Optional anchor within the target page.


   .. py:attribute:: link_text
      :type:  str

      Text to display for the link.


   .. py:attribute:: source_page
      :type:  str

      Source documentation page.


   .. py:attribute:: target_name
      :type:  str

      Name of the target (function, class, module).


   .. py:attribute:: target_page
      :type:  str

      Target documentation page.


.. py:class:: CrossReferenceSystem

   System for managing cross-references between documentation pages.

   Initialize the cross-reference system.


   .. py:method:: create_reference(source_page: str, target_name: str, link_text: Optional[str] = None) -> Optional[CrossReference]

      Create a cross-reference from source to target API element.

      :param source_page: Source documentation page.
      :type source_page: str
      :param target_name: Name of the target API element.
      :type target_name: str
      :param link_text: Text to display for the link (default: target_name).
      :type link_text: str, optional

      :returns: * *Optional[CrossReference]* -- Created cross-reference if target exists, None otherwise.
                * **Validates** (*Requirement 3.3*)



   .. py:method:: find_api_references_in_text(text: str) -> List[str]

      Find potential API element references in text.

      :param text: Text to search for API references.
      :type text: str

      :returns: List of API element names found in the text.
      :rtype: List[str]



   .. py:method:: generate_markdown_reference(ref: CrossReference) -> str

      Generate Markdown for a cross-reference.

      :param ref: The cross-reference to generate.
      :type ref: CrossReference

      :returns: Markdown link.
      :rtype: str



   .. py:method:: generate_rst_reference(ref: CrossReference) -> str

      Generate reStructuredText for a cross-reference.

      :param ref: The cross-reference to generate.
      :type ref: CrossReference

      :returns: reStructuredText link.
      :rtype: str



   .. py:method:: get_broken_references() -> List[CrossReference]

      Get all broken cross-references.

      :returns: List of broken cross-references.
      :rtype: List[CrossReference]



   .. py:method:: get_references_for_page(page: str) -> List[CrossReference]

      Get all cross-references from a specific page.

      :param page: The source page.
      :type page: str

      :returns: List of cross-references from the page.
      :rtype: List[CrossReference]



   .. py:method:: get_references_to_page(page: str) -> List[CrossReference]

      Get all cross-references to a specific page.

      :param page: The target page.
      :type page: str

      :returns: List of cross-references to the page.
      :rtype: List[CrossReference]



   .. py:method:: register_api_element(name: str, page: str) -> None

      Register an API element (function, class, module).

      :param name: Name of the API element.
      :type name: str
      :param page: Path to the API reference page.
      :type page: str
      :param Validates:
      :type Validates: Requirement 3.3



   .. py:method:: validate_references() -> Tuple[List[CrossReference], List[CrossReference]]

      Validate all cross-references.

      :returns: * *Tuple[List[CrossReference], List[CrossReference]]* -- Tuple of (valid_references, broken_references).
                * **Validates** (*Requirement 3.3*)



   .. py:attribute:: api_elements
      :type:  Dict[str, str]


   .. py:attribute:: references
      :type:  List[CrossReference]
      :value: []



