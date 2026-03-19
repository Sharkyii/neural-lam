neural_lam.metadata_serialization
=================================

.. py:module:: neural_lam.metadata_serialization

.. autoapi-nested-parse::

   Metadata serialization and deserialization module.

   This module provides functionality to serialize and deserialize docstring metadata
   to/from JSON and YAML formats, with support for round-trip conversion.







Module Contents
---------------

.. py:function:: deserialize_from_json(json_str: str) -> neural_lam.docstring_extraction.DocstringMetadata

   Deserialize metadata from JSON format.

   :param json_str: JSON string representation of metadata.
   :type json_str: str

   :returns: Deserialized metadata object.
   :rtype: DocstringMetadata


.. py:function:: deserialize_from_yaml(yaml_str: str) -> neural_lam.docstring_extraction.DocstringMetadata

   Deserialize metadata from YAML format.

   :param yaml_str: YAML string representation of metadata.
   :type yaml_str: str

   :returns: Deserialized metadata object.
   :rtype: DocstringMetadata

   :raises ImportError: If PyYAML is not installed.


.. py:function:: pretty_print(metadata: neural_lam.docstring_extraction.DocstringMetadata) -> str

   Format metadata in a human-readable way for debugging and inspection.

   :param metadata: The metadata to format.
   :type metadata: DocstringMetadata

   :returns: Human-readable string representation of the metadata.
   :rtype: str


.. py:function:: serialize_to_json(metadata: neural_lam.docstring_extraction.DocstringMetadata, indent: int = 2) -> str

   Serialize metadata to JSON format.

   :param metadata: The metadata to serialize.
   :type metadata: DocstringMetadata
   :param indent: Number of spaces for indentation (default: 2).
   :type indent: int, optional

   :returns: JSON string representation of the metadata.
   :rtype: str


.. py:function:: serialize_to_yaml(metadata: neural_lam.docstring_extraction.DocstringMetadata) -> str

   Serialize metadata to YAML format.

   :param metadata: The metadata to serialize.
   :type metadata: DocstringMetadata

   :returns: YAML string representation of the metadata.
   :rtype: str

   :raises ImportError: If PyYAML is not installed.


.. py:data:: HAS_YAML
   :value: True


