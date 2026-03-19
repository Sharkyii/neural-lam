neural_lam.doc_sync
===================

.. py:module:: neural_lam.doc_sync

.. autoapi-nested-parse::

   Documentation synchronization module.

   This module provides functionality to detect source code changes and keep
   API documentation synchronized with the codebase.





Module Contents
---------------

.. py:class:: ChangeRecord

   Represents a detected change in source code.


   .. py:attribute:: change_type
      :type:  str

      'added', 'removed', 'modified', 'signature_changed'.

      :type: Type


   .. py:attribute:: details
      :type:  str
      :value: ''


      Additional details about the change.


   .. py:attribute:: element_name
      :type:  str

      Name of the changed element.


   .. py:attribute:: is_breaking
      :type:  bool
      :value: False


      Whether the change is a breaking change.


   .. py:attribute:: module
      :type:  str

      Module where the change occurred.


.. py:class:: ConsistencyChecker

   Verifies that documented APIs still exist in source code.

   Validates: Requirement 4.5


   .. py:method:: check_consistency(documented_elements: Set[str], existing_elements: Set[str], module_name: str = '') -> List[ChangeRecord]

      Check for orphaned documentation (documented but no longer exists).

      :param documented_elements: Set of element names in the documentation.
      :type documented_elements: Set[str]
      :param existing_elements: Set of element names currently in the source code.
      :type existing_elements: Set[str]
      :param module_name: Name of the module being checked.
      :type module_name: str, optional

      :returns: * *List[ChangeRecord]* -- List of orphaned documentation records.
                * **Validates** (*Requirement 4.5*)



.. py:class:: DocumentationRegenerator

   Regenerates documentation pages when source changes.

   Validates: Requirements 4.2, 4.3, 4.4

   Initialize the regenerator.


   .. py:method:: clear_pending() -> None

      Clear the pending regeneration list.



   .. py:method:: get_pending() -> List[str]

      Get list of modules pending regeneration.

      :returns: List of module names pending regeneration.
      :rtype: List[str]



   .. py:method:: process_changes(changes: List[ChangeRecord]) -> List[str]

      Process a list of changes and schedule regenerations.

      :param changes: List of detected changes.
      :type changes: List[ChangeRecord]

      :returns: * *List[str]* -- List of modules scheduled for regeneration.
                * **Validates** (*Requirements 4.2, 4.3, 4.4*)



   .. py:method:: schedule_regeneration(module_name: str) -> None

      Schedule a module for documentation regeneration.

      :param module_name: Name of the module to regenerate.
      :type module_name: str
      :param Validates:
      :type Validates: Requirement 4.2



   .. py:attribute:: pending_regenerations
      :type:  List[str]
      :value: []



.. py:class:: SignatureChangeDetector

   Detects breaking changes in function signatures.

   Validates: Requirement 4.6


   .. py:method:: detect_signature_change(old_source: str, new_source: str, func_name: str) -> Optional[ChangeRecord]

      Detect breaking changes in a function signature.

      :param old_source: Old source code of the function.
      :type old_source: str
      :param new_source: New source code of the function.
      :type new_source: str
      :param func_name: Name of the function.
      :type func_name: str

      :returns: * *Optional[ChangeRecord]* -- A ChangeRecord if a breaking change is detected, None otherwise.
                * **Validates** (*Requirement 4.6*)



.. py:class:: SourceChangeDetector(snapshot_path: Optional[str] = None)

   Detects changes to docstrings and function signatures.

   Validates: Requirements 4.1, 4.6

   Initialize the change detector.

   :param snapshot_path: Path to store/load the snapshot file.
   :type snapshot_path: str, optional


   .. py:method:: detect_changes(old_snapshot: Dict[str, str], new_snapshot: Dict[str, str], module_name: str = '') -> List[ChangeRecord]

      Detect changes between two snapshots.

      :param old_snapshot: Previous snapshot.
      :type old_snapshot: Dict[str, str]
      :param new_snapshot: Current snapshot.
      :type new_snapshot: Dict[str, str]
      :param module_name: Name of the module being compared.
      :type module_name: str, optional

      :returns: * *List[ChangeRecord]* -- List of detected changes.
                * **Validates** (*Requirements 4.1, 4.3, 4.4*)



   .. py:method:: load_snapshot() -> Dict[str, str]

      Load a snapshot from disk.

      :returns: Loaded snapshot, or empty dict if not found.
      :rtype: Dict[str, str]



   .. py:method:: save_snapshot(snapshot: Dict[str, str]) -> None

      Save a snapshot to disk.

      :param snapshot: Snapshot to save.
      :type snapshot: Dict[str, str]



   .. py:method:: snapshot_module(module) -> Dict[str, str]

      Take a snapshot of all public elements in a module.

      :param module: The module to snapshot.
      :type module: module

      :returns: * *Dict[str, str]* -- Mapping of element names to their hashes.
                * **Validates** (*Requirement 4.1*)



   .. py:attribute:: snapshot_path
      :value: None



