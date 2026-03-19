neural_lam.docstring_parser
===========================

.. py:module:: neural_lam.docstring_parser

.. autoapi-nested-parse::

   Napoleon docstring parser wrapper for NumPy and Google-style docstrings.

   This module provides a wrapper around Napoleon to parse NumPy and Google-style
   docstrings and extract structured metadata.





Module Contents
---------------

.. py:class:: NapoleonDocstringParser

   Parser for NumPy and Google-style docstrings.

   Initialize the parser.


   .. py:method:: parse(docstring: str, name: str = '', doc_type: str = 'function') -> neural_lam.docstring_extraction.DocstringMetadata

      Parse a docstring and extract metadata.

      :param docstring: The docstring to parse.
      :type docstring: str
      :param name: The name of the documented object.
      :type name: str, optional
      :param doc_type: The type of object: 'function', 'class', or 'module'.
      :type doc_type: str, optional

      :returns: Structured metadata extracted from the docstring.
      :rtype: DocstringMetadata



   .. py:attribute:: google_sections
      :value: ['Args', 'Returns', 'Raises', 'Examples', 'Note', 'See Also']



   .. py:attribute:: numpy_sections
      :value: ['Parameters', 'Returns', 'Raises', 'Examples', 'Notes', 'See Also']
