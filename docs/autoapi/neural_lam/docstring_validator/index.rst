neural_lam.docstring_validator
==============================

.. py:module:: neural_lam.docstring_validator

.. autoapi-nested-parse::

   Docstring quality validation module.

   This module provides validators for checking docstring completeness,
   consistency, and correctness across the neural_lam package.







Module Contents
---------------

.. py:class:: ValidationIssue

   Represents a single validation issue found in a docstring.


   .. py:attribute:: code
      :type:  str

      Issue code (e.g., 'MISSING_PARAM_DOC').


   .. py:attribute:: element_name
      :type:  str
      :value: ''


      Name of the function/class/module with the issue.


   .. py:attribute:: level
      :type:  str

      'error', 'warning', or 'info'.

      :type: Severity level


   .. py:attribute:: message
      :type:  str

      Human-readable description of the issue.


   .. py:attribute:: param_name
      :type:  str
      :value: ''


      Parameter name if applicable.


   .. py:attribute:: suggestion
      :type:  str

      Actionable suggestion for fixing the issue.


.. py:class:: ValidationReport

   Aggregated validation report for a function or module.


   .. py:method:: summary() -> str

      Return a human-readable summary of the report.



   .. py:attribute:: element_name
      :type:  str

      Name of the validated element.


   .. py:attribute:: element_type
      :type:  str

      'function', 'class', or 'module'.

      :type: Type


   .. py:property:: errors
      :type: List[ValidationIssue]


      Return only error-level issues.


   .. py:property:: is_valid
      :type: bool


      Return True if no errors found.


   .. py:attribute:: issues
      :type:  List[ValidationIssue]
      :value: []


      List of validation issues found.


   .. py:property:: warnings
      :type: List[ValidationIssue]


      Return only warning-level issues.


.. py:function:: generate_validation_suggestions(report: ValidationReport) -> List[str]

   Generate actionable suggestions from a validation report.

   :param report: The validation report to generate suggestions for.
   :type report: ValidationReport

   :returns: * *List[str]* -- List of actionable suggestions.
             * **Validates** (*Requirement 6.6*)


.. py:function:: validate_exception_documentation(func: Callable) -> ValidationReport

   Validate that raised exceptions are documented.

   :param func: The function to validate.
   :type func: Callable

   :returns: * *ValidationReport* -- Validation report with any issues found.
             * **Validates** (*Requirement 6.3*)


.. py:function:: validate_formatting_consistency(func: Callable) -> ValidationReport

   Validate docstring formatting consistency.

   :param func: The function to validate.
   :type func: Callable

   :returns: * *ValidationReport* -- Validation report with any issues found.
             * **Validates** (*Requirement 6.5*)


.. py:function:: validate_function(func: Callable) -> ValidationReport

   Run all validators on a function and merge results.

   :param func: The function to validate.
   :type func: Callable

   :returns: * *ValidationReport* -- Combined validation report.
             * **Validates** (*Requirements 6.1, 6.2, 6.3, 6.4, 6.5, 6.6*)


.. py:function:: validate_parameter_documentation(func: Callable) -> ValidationReport

   Validate that all function parameters are documented.

   :param func: The function to validate.
   :type func: Callable

   :returns: * *ValidationReport* -- Validation report with any issues found.
             * **Validates** (*Requirement 6.1*)


.. py:function:: validate_return_documentation(func: Callable) -> ValidationReport

   Validate that functions with return values have documented returns.

   :param func: The function to validate.
   :type func: Callable

   :returns: * *ValidationReport* -- Validation report with any issues found.
             * **Validates** (*Requirement 6.2*)


